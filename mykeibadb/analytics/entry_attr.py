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


def analyze_entry_attr_chakudo(
    manager: ConnectionManager,
    attr_def: EntryAttrDef | dict[str, Any],
    condition: RaceCondition | None = None,
) -> ChakudoResult:
    """出走馬属性別の着度数・勝率・回収率を集計する.

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

        attr_cte, attr_join_sql, attr_val_expr = _build_attr_sql(attr_def.source, params)
        if attr_cte:
            cte_parts.append(attr_cte)

        cte_parts.append(build_payout_ctes())

        where_parts: list[str] = [
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]
        if condition is not None:
            where_parts.extend(build_race_condition_where(condition, params))

        where_clause = "\n              AND ".join(where_parts)
        cte_parts.append(
            f"""base AS (
            SELECT
                {attr_val_expr} AS attr_val,
                u.kakutei_chakujun,
                u.umaban,
                u.race_code
            FROM umagoto_race_joho u
            JOIN race_joho r ON u.race_code = r.race_code
            {attr_join_sql}
            WHERE {where_clause}
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


def _build_attr_sql(
    source: AttrSource,
    params: list[Any],
) -> tuple[str, str, str]:
    """source.type に応じた属性値CTE・JOIN句・attr_val式を生成する.

    Args:
        source (AttrSource): 属性算出方法の定義
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: CTE SQL文字列（不要な場合は空文字）
        str: JOIN句（不要な場合は空文字）
        str: attr_val を表すSQL式

    Raises:
        ValueError: source.type が未対応の場合
    """
    if source.type == "past_finish_count":
        return _build_past_finish_count_sql(source, params)
    if source.type == "career_count":
        return _build_career_count_sql()
    if source.type == "prev_race_name":
        return _build_prev_race_name_sql()
    if source.type == "debut_venue":
        return _build_debut_venue_sql()
    raise ValueError(f"未対応の source.type です: {source.type!r}")


def _build_past_finish_count_sql(
    source: AttrSource,
    params: list[Any],
) -> tuple[str, str, str]:
    """past_finish_count 用のattr_val式を生成する（対象レース以前に限定）."""
    where_parts = [
        "u2.ketto_toroku_bango = u.ketto_toroku_bango",
        "(r2.kaisai_nen || r2.kaisai_tsuki_nichi) < (r.kaisai_nen || r.kaisai_tsuki_nichi)",
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
        "CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.grade_codes:
        where_parts.append("r2.grade_code = ANY(%s)")
        params.append(source.grade_codes)
    if source.keibajo_code:
        where_parts.append("r2.keibajo_code = %s")
        params.append(source.keibajo_code)
    if source.kyori:
        where_parts.append("r2.kyori = %s")
        params.append(source.kyori)
    where_sql = "\n              AND ".join(where_parts)
    attr_val_expr = f"""(
            SELECT COUNT(*)
            FROM umagoto_race_joho u2
            JOIN race_joho r2 ON u2.race_code = r2.race_code
            WHERE {where_sql}
        )"""
    return "", "", attr_val_expr


def _build_career_count_sql() -> tuple[str, str, str]:
    """career_count 用のattr_val式を生成する（対象レース以前に限定）."""
    attr_val_expr = """(
            SELECT COUNT(*)
            FROM umagoto_race_joho u2
            JOIN race_joho r2 ON u2.race_code = r2.race_code
            WHERE u2.ketto_toroku_bango = u.ketto_toroku_bango
              AND (r2.kaisai_nen || r2.kaisai_tsuki_nichi) < (r.kaisai_nen || r.kaisai_tsuki_nichi)
              AND u2.kakutei_chakujun ~ '^[0-9]{2}$'
              AND u2.kakutei_chakujun != '00'
        )"""
    return "", "", attr_val_expr


def _build_prev_race_name_sql() -> tuple[str, str, str]:
    """prev_race_name 用のattr_val式を生成する."""
    attr_val_expr = """(
            SELECT r2.race_name
            FROM umagoto_race_joho u2
            JOIN race_joho r2 ON u2.race_code = r2.race_code
            WHERE u2.ketto_toroku_bango = u.ketto_toroku_bango
              AND (r2.kaisai_nen || r2.kaisai_tsuki_nichi)
                  < (r.kaisai_nen || r.kaisai_tsuki_nichi)
            ORDER BY r2.kaisai_nen DESC, r2.kaisai_tsuki_nichi DESC
            LIMIT 1
        )"""
    return "", "", attr_val_expr


def _build_debut_venue_sql() -> tuple[str, str, str]:
    """debut_venue 用のattr_val式を生成する."""
    attr_val_expr = """(
            SELECT r2.keibajo_code
            FROM umagoto_race_joho u2
            JOIN race_joho r2 ON u2.race_code = r2.race_code
            WHERE u2.ketto_toroku_bango = u.ketto_toroku_bango
            ORDER BY r2.kaisai_nen, r2.kaisai_tsuki_nichi
            LIMIT 1
        )"""
    return "", "", attr_val_expr


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
