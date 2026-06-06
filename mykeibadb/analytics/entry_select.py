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
_HIST_CORR_PARTS = [
    "u2.ketto_toroku_bango = u.ketto_toroku_bango",
    "(r2.kaisai_nen || r2.kaisai_gappi) < (r.kaisai_nen || r.kaisai_gappi)",
    "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
    "u2.kakutei_chakujun != '00'",
]


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
        extra = [
            "JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango"
        ] if km2_join else []
        return f"({expr})::TEXT", extra

    if group_by.kind == "fixed":
        if group_by.source is None or group_by.rows is None:
            raise ValueError("GroupBy.kind='fixed' には source と rows が必要です。")
        expr = _build_fixed_group_label_expr(group_by.source, group_by.rows, params)
        km2_join = _needs_km2_join(group_by.source)
        extra = [
            "JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango"
        ] if km2_join else []
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
    if source.type == "debut_venue":
        return _debut_venue_expr(params)
    if source.type == "past_finish_count":
        return _past_finish_count_expr(source, params)
    if source.type == "career_count":
        return _career_count_expr()
    if source.type == "prev_race_name":
        return _prev_race_name_expr()
    if source.type == "jockey_continuity":
        return _jockey_continuity_expr()
    if source.type == "sire_condition_finisher":
        return _sire_condition_finisher_expr(source, params)
    raise ValueError(f"未対応の source.type です: {source.type!r}")


def _debut_venue_expr(params: list[Any]) -> str:
    """debut_venue 属性値式を生成する.

    Args:
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: デビュー競馬場コードを返すSELECT式
    """
    hist_valid_parts = [
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
    ]
    hist_valid = "\n              AND ".join(hist_valid_parts)
    return (
        f"SELECT r2.keibajo_code\n"
        f"          FROM umagoto_race_joho u2\n"
        f"          JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"          WHERE u2.ketto_toroku_bango = u.ketto_toroku_bango\n"
        f"            AND {hist_valid}\n"
        f"          ORDER BY r2.kaisai_nen, r2.kaisai_gappi\n"
        f"          LIMIT 1"
    )


def _past_finish_count_expr(source: AttrSource, params: list[Any]) -> str:
    """past_finish_count 属性値式を生成する.

    Args:
        source (AttrSource): 属性算出方法
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: 過去N着以内の回数を返すCOUNT式
    """
    hist_parts = list(_HIST_CORR_PARTS) + [
        "CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.grade_codes:
        hist_parts.append("r2.grade_code = ANY(%s)")
        params.append(source.grade_codes)
    if source.keibajo_code:
        hist_parts.append("r2.keibajo_code = %s")
        params.append(source.keibajo_code)
    if source.kyori:
        hist_parts.append("TRIM(r2.kyori)::INTEGER = %s")
        params.append(int(source.kyori))
    hist_where = "\n            AND ".join(hist_parts)
    return (
        f"SELECT COUNT(*)\n"
        f"          FROM umagoto_race_joho u2\n"
        f"          JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"          WHERE {hist_where}"
    )


def _career_count_expr() -> str:
    """career_count 属性値式を生成する.

    Returns:
        str: キャリア戦数を返すCOUNT式
    """
    hist_where = "\n            AND ".join(_HIST_CORR_PARTS)
    return (
        f"SELECT COUNT(*)\n"
        f"          FROM umagoto_race_joho u2\n"
        f"          JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"          WHERE {hist_where}"
    )


def _prev_race_name_expr() -> str:
    """prev_race_name 属性値式を生成する.

    Returns:
        str: 前走レース名を返すSELECT式
    """
    hist_parts = list(_HIST_CORR_PARTS) + ["TRIM(r2.kyosomei_hondai) != ''"]
    hist_where = "\n            AND ".join(hist_parts)
    return (
        f"SELECT TRIM(r2.kyosomei_hondai)\n"
        f"          FROM umagoto_race_joho u2\n"
        f"          JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"          WHERE {hist_where}\n"
        f"          ORDER BY r2.kaisai_nen DESC, r2.kaisai_gappi DESC\n"
        f"          LIMIT 1"
    )


def _jockey_continuity_expr() -> str:
    """jockey_continuity 属性値式を生成する.

    Returns:
        str: 騎手継続性ラベルを返すCASE WHEN式
    """
    prev_hist_where = "\n              AND ".join(_HIST_CORR_PARTS)
    return (
        f"CASE\n"
        f"          WHEN u.kishu_code = (\n"
        f"            SELECT u2.kishu_code\n"
        f"            FROM umagoto_race_joho u2\n"
        f"            JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"            WHERE {prev_hist_where}\n"
        f"            ORDER BY r2.kaisai_nen DESC, r2.kaisai_gappi DESC\n"
        f"            LIMIT 1\n"
        f"          ) THEN '継続'\n"
        f"          WHEN u.kishu_code IN (\n"
        f"            SELECT u2.kishu_code\n"
        f"            FROM umagoto_race_joho u2\n"
        f"            JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"            WHERE {prev_hist_where}\n"
        f"          ) THEN '乗り戻り'\n"
        f"          ELSE 'テン乗り'\n"
        f"        END"
    )


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
    """fixed GroupBy のCASE WHEN式を生成する.

    Args:
        source (AttrSource): 属性算出方法
        rows (RowsDef): グループ名→フィルタ条件の辞書
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: CASE WHEN式
    """
    attr_expr = _build_attr_value_expr(source, params)
    when_clauses: list[str] = []
    for label, cond in rows.items():
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
