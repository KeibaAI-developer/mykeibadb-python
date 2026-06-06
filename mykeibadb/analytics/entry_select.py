"""着度数集計フェーズ1: エントリ選択モジュール."""

from typing import Any

from mykeibadb.analytics._cte_helpers import (
    SUBJECT_MAP,
    build_course_week_cte,
    build_race_condition_where,
)
from mykeibadb.analytics._entry_filters import _validate_sql_expr, build_filter_subquery
from mykeibadb.analytics._models import (
    AttrSource,
    Entry,
    EntryFilter,
    EntrySet,
    GroupBy,
    RaceCondition,
    RowsDef,
)
from mykeibadb.connection import ConnectionManager

_ENTRY_VALID_PARTS = [
    "u.kakutei_chakujun ~ '^[0-9]{2}$'",
    "u.kakutei_chakujun != '00'",
]
_HIST_VALID_PARTS = [
    "kakutei_chakujun ~ '^[0-9]{2}$'",
    "kakutei_chakujun != '00'",
]
_HIST_CTE_SOURCE_TYPES = frozenset(
    {
        "career_count",
        "past_finish_count",
        "debut_venue",
        "prev_race_name",
        "jockey_continuity",
        "prev_race_col",
    }
)
_PREV_RACE_COL_ALLOWED: frozenset[str] = frozenset({"kyakushitsu_hantei", "kyori"})


def select_entries(
    manager: ConnectionManager,
    filters: list[EntryFilter],
    condition: RaceCondition | None = None,
    group_by: GroupBy | None = None,
) -> EntrySet:
    """条件を満たす馬×レースエントリのリストを返す.

    Args:
        manager (ConnectionManager): DB接続マネージャ
        filters (list[EntryFilter]): エントリフィルタリスト
        condition (RaceCondition | None): レース絞り込み条件
        group_by (GroupBy | None): グループ分け軸

    Returns:
        EntrySet: エントリリスト

    Raises:
        MykeibaDBError: DBエラーが発生した場合
        ValueError: group_by.kind が未対応の場合
        ValueError: condition.course_kubun と week_in_course のどちらか一方のみ指定した場合
    """
    params: list[Any] = []
    cte_parts: list[str] = []
    extra_joins: list[str] = []
    cw_join_sql = ""
    using_cw = False

    _validate_course_week(condition)

    if (
        condition is not None
        and condition.course_kubun is not None
        and condition.week_in_course is not None
    ):
        cte_sql, cw_join_sql = build_course_week_cte(
            condition.keibajo_code,
            condition.course_kubun,
            condition.week_in_course,
            params,
        )
        cte_parts.append(cte_sql)
        using_cw = True

    use_hist_cte = (
        group_by is not None
        and group_by.kind in ("history", "fixed")
        and group_by.source is not None
        and group_by.source.type in _HIST_CTE_SOURCE_TYPES
    )

    if use_hist_cte:
        th_where_parts = list(_ENTRY_VALID_PARTS)
        if condition is not None:
            th_where_parts.extend(
                build_race_condition_where(condition, params, include_keibajo_code=not using_cw)
            )
        if filters:
            filter_subqs = [build_filter_subquery(f, params) for f in filters]
            intersect_sql = "\n            INTERSECT\n            ".join(filter_subqs)
            th_where_parts.append(
                f"(u.ketto_toroku_bango, u.race_code) IN (\n"
                f"          {intersect_sql}\n"
                f"        )"
            )
        th_where_clause = "\n          AND ".join(th_where_parts)

        assert group_by is not None and group_by.source is not None
        cte_parts.append(_build_target_horses_cte(th_where_clause, cw_join_sql))
        cte_parts.append(_build_horse_hist_cte())
        cte_parts.extend(_build_attr_agg_cte(group_by.source, params))

        group_label_expr = _build_hist_group_label_expr(group_by, params)
        extra_joins = [
            "LEFT JOIN attr_agg\n"
            "            ON attr_agg.ketto_toroku_bango = u.ketto_toroku_bango\n"
            "            AND attr_agg.target_race_code = u.race_code"
        ]
        where_clause = (
            "(u.ketto_toroku_bango, u.race_code) IN "
            "(SELECT ketto_toroku_bango, race_code FROM target_horses)"
        )
    else:
        group_label_expr, group_extra_joins = _build_group_label_expr(group_by, params)
        extra_joins.extend(group_extra_joins)

        where_parts = list(_ENTRY_VALID_PARTS)
        if condition is not None:
            where_parts.extend(
                build_race_condition_where(condition, params, include_keibajo_code=not using_cw)
            )
        if filters:
            filter_subqs = [build_filter_subquery(f, params) for f in filters]
            intersect_sql = "\n            INTERSECT\n            ".join(filter_subqs)
            where_parts.append(
                f"(u.ketto_toroku_bango, u.race_code) IN (\n"
                f"          {intersect_sql}\n"
                f"        )"
            )
        where_clause = "\n          AND ".join(where_parts)

    join_lines = ([cw_join_sql] if cw_join_sql else []) + extra_joins
    joins_sql = "\n        ".join(join_lines)

    select_body = (
        f"        SELECT\n"
        f"            u.ketto_toroku_bango,\n"
        f"            u.race_code,\n"
        f"            u.umaban,\n"
        f"            {group_label_expr} AS group_label\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        {joins_sql}\n"
        f"        WHERE {where_clause}"
    )

    if cte_parts:
        sql = f"WITH RECURSIVE {', '.join(cte_parts)}\n{select_body}"
    else:
        sql = select_body

    df = manager.fetch_dataframe(sql, params=tuple(params))
    return [
        Entry(
            ketto_toroku_bango=str(row["ketto_toroku_bango"]),
            race_code=str(row["race_code"]),
            umaban=str(row["umaban"]),
            group_label=str(row["group_label"]),
        )
        for _, row in df.iterrows()
    ]


def _validate_course_week(condition: RaceCondition | None) -> None:
    """course_kubun / week_in_course の組み合わせを検証する.

    Args:
        condition (RaceCondition | None): レース絞り込み条件

    Raises:
        ValueError: course_kubun と week_in_course のどちらか一方のみ指定した場合
    """
    cond_kubun = condition.course_kubun if condition else None
    cond_week = condition.week_in_course if condition else None
    if (cond_kubun is None) != (cond_week is None):
        raise ValueError(
            "condition.course_kubun と condition.week_in_course は"
            "両方同時に指定するか、両方 None にしてください。"
        )


def _build_group_label_expr(
    group_by: GroupBy | None,
    params: list[Any],
) -> tuple[str, list[str]]:
    """GroupBy から group_label SQL式と追加JOIN文のリストを返す.

    race_col / subject / sire_condition_finisher(history/fixed) kind に対応。
    _HIST_CTE_SOURCE_TYPES に属する source.type の history/fixed kind は
    select_entries 内の CTE 方式で処理するためここには来ない。

    Args:
        group_by (GroupBy | None): グループ分け軸
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        tuple[str, list[str]]: (group_label_expr, extra_join_list)

    Raises:
        ValueError: group_by.kind が未対応の場合
        ValueError: group_by.kind に必要なフィールドが None の場合
    """
    if group_by is None:
        return "'全体'", []

    if group_by.kind == "race_col":
        if group_by.column is None:
            raise ValueError("GroupBy.kind='race_col' には column が必要です。")
        _validate_sql_expr(group_by.column, "GroupBy.column")
        return f"{group_by.column}::TEXT", []

    if group_by.kind == "subject":
        if group_by.subject is None:
            raise ValueError("GroupBy.kind='subject' には subject が必要です。")
        mapping = SUBJECT_MAP[group_by.subject]
        extra = [mapping.join_sql] if mapping.join_sql else []
        return f"{mapping.group_col}", extra

    if group_by.kind == "history":
        if group_by.source is None:
            raise ValueError("GroupBy.kind='history' には source が必要です。")
        expr = _build_attr_value_expr(group_by.source, params)
        km2_join = _needs_km2_join(group_by.source)
        extra = (
            ["JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango"]
            if km2_join
            else []
        )
        return f"({expr})::TEXT", extra

    if group_by.kind == "fixed":
        if group_by.source is None or group_by.rows is None:
            raise ValueError("GroupBy.kind='fixed' には source と rows が必要です。")
        expr = _build_fixed_group_label_expr(group_by.source, group_by.rows, params)
        km2_join = _needs_km2_join(group_by.source)
        extra = (
            ["JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango"]
            if km2_join
            else []
        )
        return expr, extra

    raise ValueError(f"未対応の group_by.kind です: {group_by.kind!r}")


def _needs_km2_join(source: AttrSource) -> bool:
    """AttrSource が kyosoba_master2 JOIN を必要とするか判定する.

    Args:
        source (AttrSource): 属性算出方法

    Returns:
        bool: JOIN が必要な場合は True
    """
    return source.type == "sire_condition_finisher"


def _build_attr_value_expr(source: AttrSource, params: list[Any]) -> str:
    """AttrSource に応じた属性値を返す相関サブクエリ式を生成する.

    Args:
        source (AttrSource): 属性算出方法
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: 属性値を返すSQL式

    Raises:
        ValueError: source.type が未対応の場合
    """
    if source.type == "sire_condition_finisher":
        return _sire_condition_finisher_expr(source, params)
    raise ValueError(f"未対応の source.type です: {source.type!r}")


def _sire_condition_finisher_expr(source: AttrSource, params: list[Any]) -> str:
    """sire_condition_finisher 属性値式を生成する.

    Args:
        source (AttrSource): 属性算出方法
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: 父馬の条件戦好走有無（0/1）を返すCASE WHEN式
    """
    sire_parts = [
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
        "CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.condition is not None:
        tmp: list[Any] = []
        sire_parts.extend(build_race_condition_where(source.condition, tmp, race_alias="r2"))
        params.extend(tmp)
    sire_where = "\n              AND ".join(sire_parts)
    finisher_subq = (
        f"SELECT DISTINCT km2b.ketto1_bamei\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              JOIN kyosoba_master2 km2b\n"
        f"                ON u2.ketto_toroku_bango = km2b.ketto_toroku_bango\n"
        f"              WHERE {sire_where}"
    )
    return (
        f"CASE WHEN km2.ketto1_bamei IN (\n"
        f"          {finisher_subq}\n"
        f"        ) THEN 1 ELSE 0 END"
    )


def _build_fixed_group_label_expr(
    source: AttrSource,
    rows: RowsDef,
    params: list[Any],
) -> str:
    """fixed GroupBy のCASE WHEN式を生成する（相関サブクエリ方式）.

    Args:
        source (AttrSource): 属性算出方法
        rows (RowsDef): グループ名→フィルタ条件の辞書
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: CASE WHEN式
    """
    attr_params: list[Any] = []
    attr_expr = _build_attr_value_expr(source, attr_params)
    when_clauses: list[str] = []
    for label, cond in rows.items():
        params.extend(attr_params)
        if isinstance(cond, tuple):
            min_val, max_val = cond
            params.extend([int(min_val), int(max_val)])
            when_clauses.append(f"WHEN ({attr_expr}) BETWEEN %s AND %s THEN %s")
            params.append(label)
        elif isinstance(cond, int):
            params.extend([cond, label])
            when_clauses.append(f"WHEN ({attr_expr}) = %s THEN %s")
        else:
            params.extend([str(cond), label])
            when_clauses.append(f"WHEN ({attr_expr}) = %s THEN %s")
    whens = "\n          ".join(when_clauses)
    return f"CASE\n          {whens}\n          ELSE NULL\n        END"


def _build_target_horses_cte(where_clause: str, cw_join_sql: str) -> str:
    """target_horses MATERIALIZED CTE の SQL 文字列を返す.

    Args:
        where_clause (str): target_horses の WHERE 句
        cw_join_sql (str): course_week CTE の JOIN 句（不要なら空文字）

    Returns:
        str: target_horses CTE 文字列
    """
    join_part = f"\n        {cw_join_sql}" if cw_join_sql else ""
    return (
        f"target_horses AS MATERIALIZED (\n"
        f"        SELECT DISTINCT\n"
        f"            u.ketto_toroku_bango,\n"
        f"            u.race_code,\n"
        f"            r.kaisai_nen,\n"
        f"            r.kaisai_gappi,\n"
        f"            u.kishu_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code"
        f"{join_part}\n"
        f"        WHERE {where_clause}\n"
        f"    )"
    )


def _build_horse_hist_cte() -> str:
    """horse_hist CTE の SQL 文字列を返す.

    target_horses の各馬の全履歴（対象レース日より前）を一括取得する。

    Returns:
        str: horse_hist CTE 文字列
    """
    return (
        "horse_hist AS (\n"
        "        SELECT\n"
        "            th.ketto_toroku_bango,\n"
        "            th.race_code              AS target_race_code,\n"
        "            th.kishu_code             AS target_kishu_code,\n"
        "            th.kaisai_nen             AS target_kaisai_nen,\n"
        "            u2.kishu_code,\n"
        "            r2.keibajo_code,\n"
        "            r2.kaisai_nen,\n"
        "            r2.kaisai_gappi,\n"
        "            u2.kakutei_chakujun,\n"
        "            u2.kyakushitsu_hantei,\n"
        "            TRIM(r2.kyosomei_hondai)  AS kyosomei_hondai,\n"
        "            r2.grade_code,\n"
        "            TRIM(r2.kyori)::INTEGER   AS kyori_int,\n"
        "            TRIM(r2.tokubetsu_kyoso_bango) AS tokubetsu_kyoso_bango\n"
        "        FROM target_horses th\n"
        "        JOIN umagoto_race_joho u2\n"
        "            ON u2.ketto_toroku_bango = th.ketto_toroku_bango\n"
        "        JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        "        WHERE (r2.kaisai_nen || r2.kaisai_gappi) < (th.kaisai_nen || th.kaisai_gappi)\n"
        "    )"
    )


def _build_attr_agg_cte(source: AttrSource, params: list[Any]) -> list[str]:
    """source.type に応じた attr_agg CTE SQL リストを返す.

    Args:
        source (AttrSource): 属性算出方法
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        list[str]: attr_agg CTE 文字列のリスト（jockey_continuity は1要素）

    Raises:
        ValueError: source.type が未対応の場合
    """
    if source.type == "career_count":
        return [_attr_agg_career_count()]
    if source.type == "past_finish_count":
        return [_attr_agg_past_finish_count(source, params)]
    if source.type == "debut_venue":
        return [_attr_agg_debut_venue()]
    if source.type == "prev_race_name":
        return [_attr_agg_prev_race_name()]
    if source.type == "jockey_continuity":
        return [_attr_agg_jockey_continuity()]
    if source.type == "prev_race_col":
        return [_attr_agg_prev_race_col(source)]
    raise ValueError(f"未対応の source.type です: {source.type!r}")


def _attr_agg_career_count() -> str:
    """career_count 用 attr_agg CTE を返す.

    Returns:
        str: attr_agg CTE 文字列
    """
    hist_valid = " AND ".join(_HIST_VALID_PARTS)
    return (
        f"attr_agg AS (\n"
        f"        SELECT ketto_toroku_bango, target_race_code, COUNT(*) AS attr_val\n"
        f"        FROM horse_hist\n"
        f"        WHERE {hist_valid}\n"
        f"        GROUP BY ketto_toroku_bango, target_race_code\n"
        f"    )"
    )


def _attr_agg_past_finish_count(source: AttrSource, params: list[Any]) -> str:
    """past_finish_count 用 attr_agg CTE を返す.

    Args:
        source (AttrSource): 属性算出方法
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: attr_agg CTE 文字列
    """
    hist_valid = " AND ".join(_HIST_VALID_PARTS)
    filter_parts = [
        hist_valid,
        "CAST(kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.grade_codes:
        filter_parts.append("grade_code = ANY(%s)")
        params.append(source.grade_codes)
    if source.keibajo_code:
        filter_parts.append("keibajo_code = %s")
        params.append(source.keibajo_code)
    if source.kyori:
        filter_parts.append("kyori_int = %s")
        params.append(int(source.kyori))
    filter_clause = "\n                AND ".join(filter_parts)
    return (
        f"attr_agg AS (\n"
        f"        SELECT ketto_toroku_bango, target_race_code,\n"
        f"               COUNT(*) FILTER (\n"
        f"                   WHERE {filter_clause}\n"
        f"               ) AS attr_val\n"
        f"        FROM horse_hist\n"
        f"        GROUP BY ketto_toroku_bango, target_race_code\n"
        f"    )"
    )


def _attr_agg_debut_venue() -> str:
    """debut_venue 用 attr_agg CTE を返す.

    Returns:
        str: attr_agg CTE 文字列
    """
    hist_valid = " AND ".join(_HIST_VALID_PARTS)
    return (
        f"attr_agg AS (\n"
        f"        SELECT DISTINCT ON (ketto_toroku_bango, target_race_code)\n"
        f"               ketto_toroku_bango, target_race_code, keibajo_code AS attr_val\n"
        f"        FROM horse_hist\n"
        f"        WHERE {hist_valid}\n"
        f"        ORDER BY ketto_toroku_bango, target_race_code,\n"
        f"                 kaisai_nen ASC, kaisai_gappi ASC\n"
        f"    )"
    )


def _attr_agg_prev_race_name() -> str:
    """prev_race_name 用 attr_agg CTE を返す.

    Returns:
        str: attr_agg CTE 文字列
    """
    return (
        "attr_agg AS (\n"
        "        SELECT DISTINCT ON (ketto_toroku_bango, target_race_code)\n"
        "               ketto_toroku_bango, target_race_code, kyosomei_hondai AS attr_val\n"
        "        FROM horse_hist\n"
        "        WHERE kyosomei_hondai != ''\n"
        "        ORDER BY ketto_toroku_bango, target_race_code,\n"
        "                 kaisai_nen DESC, kaisai_gappi DESC\n"
        "    )"
    )


def _attr_agg_jockey_continuity() -> str:
    """jockey_continuity 用 attr_agg CTE を返す.

    Returns:
        str: attr_agg CTE 文字列
    """
    hist_valid = " AND ".join(_HIST_VALID_PARTS)
    return (
        f"attr_agg AS (\n"
        f"        SELECT\n"
        f"            ketto_toroku_bango,\n"
        f"            target_race_code,\n"
        f"            CASE\n"
        f"                WHEN target_kishu_code = (\n"
        f"                    ARRAY_AGG(kishu_code ORDER BY kaisai_nen DESC, kaisai_gappi DESC)\n"
        f"                )[1]\n"
        f"                THEN '継続'\n"
        f"                WHEN target_kishu_code = ANY(ARRAY_AGG(kishu_code))\n"
        f"                THEN '乗り戻り'\n"
        f"                ELSE 'テン乗り'\n"
        f"            END AS attr_val\n"
        f"        FROM horse_hist\n"
        f"        WHERE {hist_valid}\n"
        f"        GROUP BY ketto_toroku_bango, target_race_code, target_kishu_code\n"
        f"    )"
    )


def _attr_agg_prev_race_col(source: AttrSource) -> str:
    """prev_race_col 用 attr_agg CTE を返す.

    Args:
        source (AttrSource): 属性算出方法（column 必須）

    Returns:
        str: attr_agg CTE 文字列

    Raises:
        ValueError: source.column が None または許可リスト外の場合
    """
    if source.column not in _PREV_RACE_COL_ALLOWED:
        raise ValueError(
            f"prev_race_col の column は {set(_PREV_RACE_COL_ALLOWED)} のいずれかで指定してください。"
            f" 指定値: {source.column!r}"
        )
    hist_valid = " AND ".join(_HIST_VALID_PARTS)
    attr_col = "kyori_int" if source.column == "kyori" else source.column
    return (
        f"attr_agg AS (\n"
        f"        SELECT DISTINCT ON (ketto_toroku_bango, target_race_code)\n"
        f"               ketto_toroku_bango, target_race_code, {attr_col} AS attr_val\n"
        f"        FROM horse_hist\n"
        f"        WHERE {hist_valid}\n"
        f"        ORDER BY ketto_toroku_bango, target_race_code,\n"
        f"                 kaisai_nen DESC, kaisai_gappi DESC\n"
        f"    )"
    )


def _build_hist_group_label_expr(group_by: GroupBy, params: list[Any]) -> str:
    """history/fixed kind の group_label SQL 式を返す（attr_agg.attr_val を参照）.

    Args:
        group_by (GroupBy): グループ分け軸（history または fixed kind）
        params (list[Any]): SQLパラメータリスト（fixed kind 時に末尾に追加される）

    Returns:
        str: group_label SQL 式

    Raises:
        ValueError: group_by.kind が history/fixed 以外の場合
        ValueError: group_by.kind='fixed' で rows が None の場合
    """
    if group_by.kind == "history":
        return "attr_agg.attr_val::TEXT"

    if group_by.kind == "fixed":
        if group_by.rows is None:
            raise ValueError("GroupBy.kind='fixed' には rows が必要です。")
        when_clauses: list[str] = []
        for label, cond in group_by.rows.items():
            if isinstance(cond, tuple):
                min_val, max_val = cond
                params.extend([int(min_val), int(max_val), label])
                when_clauses.append("WHEN attr_agg.attr_val::INTEGER BETWEEN %s AND %s THEN %s")
            elif isinstance(cond, int):
                params.extend([cond, label])
                when_clauses.append("WHEN attr_agg.attr_val::INTEGER = %s THEN %s")
            else:
                params.extend([str(cond), label])
                when_clauses.append("WHEN attr_agg.attr_val::TEXT = %s THEN %s")
        whens = "\n          ".join(when_clauses)
        return f"CASE\n          {whens}\n          ELSE NULL\n        END"

    raise ValueError(f"未対応の group_by.kind: {group_by.kind!r}")
