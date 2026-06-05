"""出走馬属性別着度数・回収率集計モジュール."""

from typing import Any

from mykeibadb.analytics._cte_helpers import build_payout_ctes, build_race_condition_where
from mykeibadb.analytics._models import (
    AttrSource,
    ChakudoResult,
    ChakudoRow,
    EntryAttrDef,
    RaceCondition,
    RowsDef,
)
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError

_HORSE_HIST_BODY = """        SELECT u2.ketto_toroku_bango,
               r2.kaisai_nen AS hist_nen,
               r2.kaisai_gappi AS hist_gappi,
               u2.kakutei_chakujun AS hist_chakujun,
               u2.kishu_code AS hist_kishu_code,
               r2.keibajo_code AS hist_keibajo_code,
               TRIM(r2.kyori)::INTEGER AS hist_kyori,
               r2.kyosomei_hondai AS hist_race_name,
               r2.grade_code AS hist_grade_code
        FROM umagoto_race_joho u2
        JOIN race_shosai r2 ON u2.race_code = r2.race_code"""


def _build_horse_hist_cte(source: AttrSource, params: list[Any]) -> str:
    """horse_hist CTE SQL文字列を生成する.

    past_finish_count でgrade_codes/keibajo_code/kyoriが指定されている場合は
    race_code PKインデックスを活用したフィルタを使用する。
    それ以外はketto_toroku_bango IN（全履歴スキャン）を使用する。

    Args:
        source (AttrSource): 属性算出方法の定義
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: horse_hist CTE SQL
    """
    race_filter_parts: list[str] = []
    if source.type == "past_finish_count":
        if source.grade_codes:
            race_filter_parts.append("grade_code = ANY(%s)")
            params.append(source.grade_codes)
        if source.keibajo_code:
            race_filter_parts.append("keibajo_code = %s")
            params.append(source.keibajo_code)
        if source.kyori:
            race_filter_parts.append("TRIM(kyori)::INTEGER = %s")
            params.append(int(source.kyori))

    if race_filter_parts:
        race_filter = "\n              AND ".join(race_filter_parts)
        hist_where = (
            f"WHERE u2.race_code IN (\n"
            f"            SELECT race_code FROM race_shosai WHERE {race_filter}\n"
            f"        )\n"
            f"          AND u2.ketto_toroku_bango IN "
            f"(SELECT ketto_toroku_bango FROM target_horses)"
        )
    else:
        hist_where = (
            "WHERE u2.ketto_toroku_bango IN (SELECT ketto_toroku_bango FROM target_horses)"
        )

    return f"horse_hist AS MATERIALIZED (\n{_HORSE_HIST_BODY}\n        {hist_where}\n    )"


def analyze_entry_attr_chakudo(
    manager: ConnectionManager,
    attr_def: EntryAttrDef | dict[str, Any],
    condition: RaceCondition | None = None,
) -> ChakudoResult:
    """出走馬属性別の着度数・勝率・回収率を集計する.

    相関サブクエリを避けるため、対象馬を事前に target_horses CTE で絞り込み、
    その馬の全履歴を horse_hist CTE で一括取得した後、属性値を集計する。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        attr_def (EntryAttrDef | dict[str, Any]): 属性集計条件定義。dictの場合は
            EntryAttrDef.from_dict で変換。
        condition (RaceCondition | None): レース絞り込み条件

    Returns:
        ChakudoResult: グループ別集計結果

    Raises:
        ValueError: attr_def.source.type が未対応の場合
    """
    if isinstance(attr_def, dict):
        attr_def = EntryAttrDef.from_dict(attr_def)

    try:
        params: list[Any] = []
        cte_parts: list[str] = []

        cte_parts.append(build_payout_ctes())

        target_where_parts: list[str] = [
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]
        if condition is not None:
            target_where_parts.extend(build_race_condition_where(condition, params))
        target_where = "\n          AND ".join(target_where_parts)

        cte_parts.append(
            f"""target_horses AS MATERIALIZED (
        SELECT DISTINCT u.ketto_toroku_bango, u.race_code,
               r.kaisai_nen, r.kaisai_gappi, u.kishu_code,
               u.kakutei_chakujun, u.umaban
        FROM umagoto_race_joho u
        JOIN race_shosai r ON u.race_code = r.race_code
        WHERE {target_where}
    )"""
        )

        cte_parts.append(_build_horse_hist_cte(attr_def.source, params))

        attr_cte, attr_join_sql = _build_attr_cte(attr_def.source, params)
        cte_parts.append(attr_cte)

        cte_parts.append(
            f"""base AS (
        SELECT
            attr_agg.attr_val,
            th.kakutei_chakujun,
            th.umaban,
            th.race_code
        FROM target_horses th
        {attr_join_sql}
    )"""
        )

        case_when = _build_case_when(attr_def.rows, params)
        order_by = _build_order_by(attr_def.rows, params)
        cte_parts.append(
            f"""grouped AS (
        SELECT
            {case_when} AS grp,
            kakutei_chakujun,
            umaban,
            race_code
        FROM base
    )"""
        )

        sql = f"""
            WITH RECURSIVE {", ".join(cte_parts)}
            SELECT
                grp,
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE kakutei_chakujun = '01') AS wins,
                COUNT(*) FILTER (WHERE kakutei_chakujun = '02') AS second,
                COUNT(*) FILTER (WHERE kakutei_chakujun = '03') AS third,
                COUNT(*) FILTER (
                    WHERE kakutei_chakujun NOT IN ('01', '02', '03')
                ) AS chakugai,
                ROUND(
                    COUNT(*) FILTER (WHERE kakutei_chakujun = '01')
                    * 100.0 / NULLIF(COUNT(*), 0), 1
                ) AS win_rate,
                ROUND(
                    COUNT(*) FILTER (WHERE kakutei_chakujun IN ('01', '02', '03'))
                    * 100.0 / NULLIF(COUNT(*), 0), 1
                ) AS fukusho_rate,
                ROUND(
                    COALESCE(SUM(tp.payout), 0) * 1.0 / NULLIF(COUNT(*), 0), 1
                ) AS tansho_kaishuu,
                ROUND(
                    COALESCE(SUM(fp.payout), 0) * 1.0 / NULLIF(COUNT(*), 0), 1
                ) AS fukusho_kaishuu
            FROM grouped
            LEFT JOIN tansho_payouts tp
                ON grouped.race_code = tp.race_code AND grouped.umaban = tp.umaban
            LEFT JOIN fukusho_payouts fp
                ON grouped.race_code = fp.race_code AND grouped.umaban = fp.umaban
            WHERE grp IS NOT NULL
            GROUP BY grp
            ORDER BY {order_by}
        """

        df = manager.fetch_dataframe(sql, params=tuple(params))
        result_rows = [ChakudoRow.from_series(row) for _, row in df.iterrows()]
        return ChakudoResult(success=True, rows=result_rows)
    except MykeibaDBError as e:
        return ChakudoResult(success=False, error=str(e))


def _build_attr_cte(
    source: AttrSource,
    params: list[Any],
) -> tuple[str, str]:
    """source.type に応じた attr_agg CTE と base への JOIN 句を返す.

    target_horses / horse_hist CTE が事前定義済みであることを前提とする。

    Args:
        source (AttrSource): 属性算出方法の定義
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: attr_agg CTE SQL
        str: base CTE への JOIN 句

    Raises:
        ValueError: source.type が未対応の場合
    """
    if source.type == "past_finish_count":
        return _build_past_finish_count_cte(source, params)
    if source.type == "career_count":
        return _build_career_count_cte()
    if source.type == "prev_race_name":
        return _build_prev_race_name_cte()
    if source.type == "debut_venue":
        return _build_debut_venue_cte()
    if source.type == "jockey_continuity":
        return _build_jockey_continuity_cte()
    if source.type == "sire_condition_finisher":
        return _build_sire_condition_finisher_cte(source, params)
    raise ValueError(f"未対応の source.type です: {source.type!r}")


def _build_past_finish_count_cte(
    source: AttrSource,
    params: list[Any],
) -> tuple[str, str]:
    """past_finish_count 用の attr_agg CTE を生成する.

    horse_hist から対象レース以前の入着回数を集計する。
    """
    hist_filter_parts = [
        "h.hist_chakujun ~ '^[0-9]{2}$'",
        "h.hist_chakujun != '00'",
        "CAST(h.hist_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.grade_codes:
        hist_filter_parts.append("h.hist_grade_code = ANY(%s)")
        params.append(source.grade_codes)
    if source.keibajo_code:
        hist_filter_parts.append("h.hist_keibajo_code = %s")
        params.append(source.keibajo_code)
    if source.kyori:
        hist_filter_parts.append("h.hist_kyori = %s")
        params.append(int(source.kyori))
    hist_filter = "\n            AND ".join(hist_filter_parts)
    cte = f"""attr_agg AS (
        SELECT t.ketto_toroku_bango, t.race_code,
               COUNT(h.hist_nen) AS attr_val
        FROM target_horses t
        LEFT JOIN horse_hist h
            ON h.ketto_toroku_bango = t.ketto_toroku_bango
           AND (h.hist_nen || h.hist_gappi) < (t.kaisai_nen || t.kaisai_gappi)
           AND {hist_filter}
        GROUP BY t.ketto_toroku_bango, t.race_code
    )"""
    join = (
        "JOIN attr_agg ON attr_agg.ketto_toroku_bango = th.ketto_toroku_bango"
        " AND attr_agg.race_code = th.race_code"
    )
    return cte, join


def _build_career_count_cte() -> tuple[str, str]:
    """career_count 用の attr_agg CTE を生成する.

    horse_hist から対象レース以前の出走回数を集計する。
    """
    cte = """attr_agg AS (
        SELECT t.ketto_toroku_bango, t.race_code,
               COUNT(h.hist_nen) AS attr_val
        FROM target_horses t
        LEFT JOIN horse_hist h
            ON h.ketto_toroku_bango = t.ketto_toroku_bango
           AND (h.hist_nen || h.hist_gappi) < (t.kaisai_nen || t.kaisai_gappi)
           AND h.hist_chakujun ~ '^[0-9]{2}$'
           AND h.hist_chakujun != '00'
        GROUP BY t.ketto_toroku_bango, t.race_code
    )"""
    join = (
        "JOIN attr_agg ON attr_agg.ketto_toroku_bango = th.ketto_toroku_bango"
        " AND attr_agg.race_code = th.race_code"
    )
    return cte, join


def _build_prev_race_name_cte() -> tuple[str, str]:
    """prev_race_name 用の attr_agg CTE を生成する.

    horse_hist から対象レース直前のレース名を取得する。
    """
    cte = """attr_agg AS (
        SELECT DISTINCT ON (t.ketto_toroku_bango, t.race_code)
            t.ketto_toroku_bango, t.race_code,
            h.hist_race_name AS attr_val
        FROM target_horses t
        JOIN horse_hist h
            ON h.ketto_toroku_bango = t.ketto_toroku_bango
           AND (h.hist_nen || h.hist_gappi) < (t.kaisai_nen || t.kaisai_gappi)
        ORDER BY t.ketto_toroku_bango, t.race_code, h.hist_nen DESC, h.hist_gappi DESC
    )"""
    join = (
        "LEFT JOIN attr_agg ON attr_agg.ketto_toroku_bango = th.ketto_toroku_bango"
        " AND attr_agg.race_code = th.race_code"
    )
    return cte, join


def _build_debut_venue_cte() -> tuple[str, str]:
    """debut_venue 用の attr_agg CTE を生成する.

    horse_hist からデビュー戦の競馬場コードを取得する。
    """
    cte = """attr_agg AS (
        SELECT DISTINCT ON (ketto_toroku_bango)
            ketto_toroku_bango,
            hist_keibajo_code AS attr_val
        FROM horse_hist
        WHERE hist_chakujun ~ '^[0-9]{2}$'
          AND hist_chakujun != '00'
        ORDER BY ketto_toroku_bango, hist_nen, hist_gappi
    )"""
    join = (
        "LEFT JOIN attr_agg ON attr_agg.ketto_toroku_bango = th.ketto_toroku_bango"
    )
    return cte, join


def _build_jockey_continuity_cte() -> tuple[str, str]:
    """jockey_continuity 用の attr_agg CTE を生成する.

    直前の騎手と過去騎手一覧を horse_hist から取得し、継続/乗り戻り/テン乗りを判定する。
    """
    cte = """prev_jockey AS (
        SELECT DISTINCT ON (t.ketto_toroku_bango, t.race_code)
            t.ketto_toroku_bango, t.race_code,
            h.hist_kishu_code AS prev_kishu_code
        FROM target_horses t
        JOIN horse_hist h
            ON h.ketto_toroku_bango = t.ketto_toroku_bango
           AND (h.hist_nen || h.hist_gappi) < (t.kaisai_nen || t.kaisai_gappi)
        ORDER BY t.ketto_toroku_bango, t.race_code, h.hist_nen DESC, h.hist_gappi DESC
    ), past_jockeys AS (
        SELECT t.ketto_toroku_bango, t.race_code,
               array_agg(h.hist_kishu_code) AS kishu_codes
        FROM target_horses t
        JOIN horse_hist h
            ON h.ketto_toroku_bango = t.ketto_toroku_bango
           AND (h.hist_nen || h.hist_gappi) < (t.kaisai_nen || t.kaisai_gappi)
        GROUP BY t.ketto_toroku_bango, t.race_code
    ), attr_agg AS (
        SELECT t.ketto_toroku_bango, t.race_code,
               CASE
                   WHEN t.kishu_code = pj.prev_kishu_code THEN '継続'
                   WHEN t.kishu_code = ANY(paj.kishu_codes) THEN '乗り戻り'
                   ELSE 'テン乗り'
               END AS attr_val
        FROM target_horses t
        LEFT JOIN prev_jockey pj
            ON pj.ketto_toroku_bango = t.ketto_toroku_bango
           AND pj.race_code = t.race_code
        LEFT JOIN past_jockeys paj
            ON paj.ketto_toroku_bango = t.ketto_toroku_bango
           AND paj.race_code = t.race_code
    )"""
    join = (
        "JOIN attr_agg ON attr_agg.ketto_toroku_bango = th.ketto_toroku_bango"
        " AND attr_agg.race_code = th.race_code"
    )
    return cte, join


def _build_sire_condition_finisher_cte(
    source: AttrSource,
    params: list[Any],
) -> tuple[str, str]:
    """sire_condition_finisher 用の attr_agg CTE を生成する."""
    cond_parts: list[str] = [
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
        "CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.condition is not None:
        cond_parts.extend(build_race_condition_where(source.condition, params, race_alias="r2"))
    cond_where = "\n                  AND ".join(cond_parts)
    cte = f"""finisher_sires AS (
        SELECT DISTINCT km2.ketto1_bamei AS sire_name
        FROM umagoto_race_joho u2
        JOIN race_shosai r2 ON u2.race_code = r2.race_code
        JOIN kyosoba_master2 km2 ON u2.ketto_toroku_bango = km2.ketto_toroku_bango
        WHERE {cond_where}
    ), attr_agg AS (
        SELECT u.ketto_toroku_bango, u.race_code,
               CASE WHEN km2.ketto1_bamei IN (SELECT sire_name FROM finisher_sires)
                    THEN 1 ELSE 0 END AS attr_val
        FROM target_horses u
        JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango
    )"""
    join = (
        "JOIN attr_agg ON attr_agg.ketto_toroku_bango = th.ketto_toroku_bango"
        " AND attr_agg.race_code = th.race_code"
    )
    return cte, join


def _build_case_when(rows: RowsDef, params: list[Any]) -> str:
    """rowsからCASE WHEN式を生成する.

    Args:
        rows (RowsDef): グループ定義辞書
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: CASE WHEN式
    """
    cases = []
    for label, cond in rows.items():
        if isinstance(cond, tuple):
            min_val, max_val = cond
            cases.append("WHEN attr_val::INTEGER BETWEEN %s AND %s THEN %s")
            params.extend([int(min_val), int(max_val), label])
        elif isinstance(cond, int):
            cases.append("WHEN attr_val::INTEGER = %s THEN %s")
            params.extend([int(cond), label])
        else:
            cases.append("WHEN attr_val = %s THEN %s")
            params.extend([cond, label])
    return "CASE\n                " + "\n                ".join(cases) + "\n              END"


def _build_order_by(rows: RowsDef, params: list[Any]) -> str:
    """rows定義順でソートするORDER BY式を生成する.

    Args:
        rows (RowsDef): グループ定義辞書
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: ORDER BY式
    """
    cases = []
    for idx, label in enumerate(rows.keys()):
        cases.append(f"WHEN %s THEN {idx}")
        params.append(label)
    sep = "\n                "
    return "MIN(CASE grp\n                " + sep.join(cases) + "\n            END)"
