"""着度数集計フェーズ1で使用するフィルタ→サブクエリSQL生成モジュール."""

from typing import Any

from mykeibadb.analytics._chokyo_helpers import build_threshold_where
from mykeibadb.analytics._cte_helpers import SUBJECT_MAP, build_race_condition_where
from mykeibadb.analytics._models import (
    AttrSource,
    ChokyoFilter,
    EntryFilter,
    HistoryFilter,
    RaceColFilter,
    SubjectFilter,
)

_ENTRY_VALID_PARTS = [
    "u.kakutei_chakujun ~ '^[0-9]{2}$'",
    "u.kakutei_chakujun != '00'",
]
_HIST_VALID_PARTS = [
    "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
    "u2.kakutei_chakujun != '00'",
]
_WOOD_VALID = "lw.time_gokei_6furlong NOT IN ('0000', '9999')"
_HANRO_VALID = "lh.time_gokei_4furlong NOT IN ('0000', '9999')"


def build_filter_subquery(f: EntryFilter, params: list[Any]) -> str:
    """EntryFilter の種別に応じた (ketto_toroku_bango, race_code) サブクエリを返す.

    Args:
        f (EntryFilter): フィルタ
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: (ketto_toroku_bango, race_code) を返すSELECT文

    Raises:
        ValueError: 未対応のフィルタ型の場合
    """
    if isinstance(f, RaceColFilter):
        return build_race_col_filter_subquery(f, params)
    if isinstance(f, SubjectFilter):
        return build_subject_filter_subquery(f, params)
    if isinstance(f, HistoryFilter):
        return build_history_filter_subquery(f, params)
    if isinstance(f, ChokyoFilter):
        return build_chokyo_filter_subquery(f, params)
    raise ValueError(f"未対応のフィルタ型です: {type(f)!r}")


def build_race_col_filter_subquery(f: RaceColFilter, params: list[Any]) -> str:
    """RaceColFilter → (ketto_toroku_bango, race_code) サブクエリを返す.

    Args:
        f (RaceColFilter): レース列フィルタ
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: (ketto_toroku_bango, race_code) を返すSELECT文
    """
    where_parts = list(_ENTRY_VALID_PARTS)
    if f.values is not None:
        placeholders = ", ".join(["%s"] * len(f.values))
        where_parts.append(f"{f.column} IN ({placeholders})")
        params.extend(f.values)
    if f.min_value is not None:
        where_parts.append(f"{f.column}::INTEGER >= %s")
        params.append(f.min_value)
    if f.max_value is not None:
        where_parts.append(f"{f.column}::INTEGER <= %s")
        params.append(f.max_value)
    where = "\n              AND ".join(where_parts)
    return f"""SELECT u.ketto_toroku_bango, u.race_code
        FROM umagoto_race_joho u
        JOIN race_shosai r ON u.race_code = r.race_code
        WHERE {where}"""


def build_subject_filter_subquery(f: SubjectFilter, params: list[Any]) -> str:
    """SubjectFilter → (ketto_toroku_bango, race_code) サブクエリを返す.

    Args:
        f (SubjectFilter): 主体フィルタ
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: (ketto_toroku_bango, race_code) を返すSELECT文

    Raises:
        ValueError: code非対応の主体にcodeを指定した場合
    """
    mapping = SUBJECT_MAP[f.subject]
    if f.code is not None and mapping.code_col is None:
        raise ValueError(
            f"{f.subject.value} はコード指定に対応していません。name を使用してください。"
        )
    extra_join = mapping.join_sql or ""
    where_parts = list(_ENTRY_VALID_PARTS)
    if f.code is not None and mapping.code_col is not None:
        where_parts.append(f"{mapping.code_col} = %s")
        params.append(f.code)
    elif f.name is not None:
        where_parts.append(f"{mapping.name_col} LIKE %s")
        params.append(f"%{f.name}%")
    where = "\n              AND ".join(where_parts)
    return f"""SELECT u.ketto_toroku_bango, u.race_code
        FROM umagoto_race_joho u
        JOIN race_shosai r ON u.race_code = r.race_code
        {extra_join}
        WHERE {where}"""


def build_history_filter_subquery(f: HistoryFilter, params: list[Any]) -> str:
    """HistoryFilter → (ketto_toroku_bango, race_code) サブクエリを返す.

    Args:
        f (HistoryFilter): 履歴フィルタ
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: (ketto_toroku_bango, race_code) を返すSELECT文

    Raises:
        ValueError: source.type が未対応の場合
    """
    source = f.source
    if source.type == "debut_venue":
        return _build_debut_venue_filter(source, f.cond, params)
    if source.type == "past_finish_count":
        return _build_past_finish_count_filter(source, f.cond, params)
    if source.type == "career_count":
        return _build_career_count_filter(f.cond, params)
    if source.type == "prev_race_name":
        return _build_prev_race_name_filter(f.cond, params)
    if source.type == "jockey_continuity":
        return _build_jockey_continuity_filter(f.cond, params)
    if source.type == "sire_condition_finisher":
        return _build_sire_condition_finisher_filter(source, f.cond, params)
    raise ValueError(f"未対応の source.type です: {source.type!r}")


def build_chokyo_filter_subquery(f: ChokyoFilter, params: list[Any]) -> str:
    """ChokyoFilter → (ketto_toroku_bango, race_code) サブクエリを返す.

    対象レース直前の最新調教窓が全閾値を満たす馬×レースを返す。

    Args:
        f (ChokyoFilter): 調教フィルタ
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: (ketto_toroku_bango, race_code) を返すSELECT文
    """
    wood_thresholds = [t for t in f.condition if t.course == "wood"]
    hanro_thresholds = [t for t in f.condition if t.course == "hanro"]

    where_parts = list(_ENTRY_VALID_PARTS)

    if wood_thresholds:
        threshold_conds: list[str] = []
        for t in wood_thresholds:
            threshold_conds.extend(build_threshold_where(t, "lw", params))
        threshold_where = " AND ".join(threshold_conds)
        inner_where = f"lw.ketto_toroku_bango = u.ketto_toroku_bango\n                  AND lw.chokyo_nengappi < (r.kaisai_nen || r.kaisai_gappi)\n                  AND {_WOOD_VALID}"  # noqa: E501
        where_parts.append(
            f"EXISTS (\n"
            f"            SELECT 1 FROM (\n"
            f"              SELECT lw.*\n"
            f"              FROM woodchip_chokyo lw\n"
            f"              WHERE {inner_where}\n"
            f"              ORDER BY lw.chokyo_nengappi DESC, lw.chokyo_jikoku DESC\n"
            f"              LIMIT 1\n"
            f"            ) lw\n"
            f"            WHERE {threshold_where}\n"
            f"          )"
        )

    if hanro_thresholds:
        hanro_conds: list[str] = []
        for t in hanro_thresholds:
            hanro_conds.extend(build_threshold_where(t, "lh", params))
        hanro_threshold_where = " AND ".join(hanro_conds)
        inner_hanro_where = f"lh.ketto_toroku_bango = u.ketto_toroku_bango\n                  AND lh.chokyo_nengappi < (r.kaisai_nen || r.kaisai_gappi)\n                  AND {_HANRO_VALID}"  # noqa: E501
        where_parts.append(
            f"EXISTS (\n"
            f"            SELECT 1 FROM (\n"
            f"              SELECT lh.*\n"
            f"              FROM hanro_chokyo lh\n"
            f"              WHERE {inner_hanro_where}\n"
            f"              ORDER BY lh.chokyo_nengappi DESC, lh.chokyo_jikoku DESC\n"
            f"              LIMIT 1\n"
            f"            ) lh\n"
            f"            WHERE {hanro_threshold_where}\n"
            f"          )"
        )

    where = "\n              AND ".join(where_parts)
    return f"""SELECT u.ketto_toroku_bango, u.race_code
        FROM umagoto_race_joho u
        JOIN race_shosai r ON u.race_code = r.race_code
        WHERE {where}"""


def _apply_cond(
    expr: str,
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """属性値式に対する条件述語を返す.

    Args:
        expr (str): 属性値を返すSQL式
        cond (tuple[int, int] | int | str): 比較条件
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: WHERE句に使える比較述語
    """
    if isinstance(cond, tuple):
        min_val, max_val = cond
        params.extend([int(min_val), int(max_val)])
        return f"({expr}) BETWEEN %s AND %s"
    if isinstance(cond, int):
        params.append(cond)
        return f"({expr}) = %s"
    params.append(str(cond))
    return f"({expr}) = %s"


def _build_debut_venue_filter(
    source: AttrSource,
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """debut_venue HistoryFilter のサブクエリを生成する."""
    hist_valid = "\n                  AND ".join(_HIST_VALID_PARTS)
    debut_info_sq = (
        f"SELECT DISTINCT ON (u2.ketto_toroku_bango)\n"
        f"                u2.ketto_toroku_bango,\n"
        f"                r2.keibajo_code AS attr_val\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              WHERE {hist_valid}\n"
        f"              ORDER BY u2.ketto_toroku_bango, r2.kaisai_nen, r2.kaisai_gappi"
    )
    cond_pred = _apply_cond("attr_val", cond, params)
    base_valid = "\n              AND ".join(_ENTRY_VALID_PARTS)
    return (
        f"SELECT u.ketto_toroku_bango, u.race_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        WHERE {base_valid}\n"
        f"          AND u.ketto_toroku_bango IN (\n"
        f"            SELECT ketto_toroku_bango FROM (\n"
        f"              {debut_info_sq}\n"
        f"            ) debut_info\n"
        f"            WHERE {cond_pred}\n"
        f"          )"
    )


def _build_past_finish_count_filter(
    source: AttrSource,
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """past_finish_count HistoryFilter のサブクエリを生成する."""
    hist_valid_parts = [
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
        "CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    all_hist_parts = [
        "u2.ketto_toroku_bango = u.ketto_toroku_bango",
        "(r2.kaisai_nen || r2.kaisai_gappi) < (r.kaisai_nen || r.kaisai_gappi)",
    ] + hist_valid_parts
    if source.grade_codes:
        all_hist_parts.append("r2.grade_code = ANY(%s)")
        params.append(source.grade_codes)
    if source.keibajo_code:
        all_hist_parts.append("r2.keibajo_code = %s")
        params.append(source.keibajo_code)
    if source.kyori:
        all_hist_parts.append("TRIM(r2.kyori)::INTEGER = %s")
        params.append(int(source.kyori))
    hist_where = "\n                  AND ".join(all_hist_parts)
    count_expr = (
        f"SELECT COUNT(*)\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              WHERE {hist_where}"
    )
    cond_pred = _apply_cond(count_expr, cond, params)
    base_valid = "\n              AND ".join(_ENTRY_VALID_PARTS)
    return (
        f"SELECT u.ketto_toroku_bango, u.race_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        WHERE {base_valid}\n"
        f"          AND {cond_pred}"
    )


def _build_career_count_filter(
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """career_count HistoryFilter のサブクエリを生成する."""
    hist_parts = [
        "u2.ketto_toroku_bango = u.ketto_toroku_bango",
        "(r2.kaisai_nen || r2.kaisai_gappi) < (r.kaisai_nen || r.kaisai_gappi)",
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
    ]
    hist_where = "\n                  AND ".join(hist_parts)
    count_expr = (
        f"SELECT COUNT(*)\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              WHERE {hist_where}"
    )
    cond_pred = _apply_cond(count_expr, cond, params)
    base_valid = "\n              AND ".join(_ENTRY_VALID_PARTS)
    return (
        f"SELECT u.ketto_toroku_bango, u.race_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        WHERE {base_valid}\n"
        f"          AND {cond_pred}"
    )


def _build_prev_race_name_filter(
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """prev_race_name HistoryFilter のサブクエリを生成する."""
    hist_parts = [
        "u2.ketto_toroku_bango = u.ketto_toroku_bango",
        "(r2.kaisai_nen || r2.kaisai_gappi) < (r.kaisai_nen || r.kaisai_gappi)",
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
        "TRIM(r2.kyosomei_hondai) != ''",
    ]
    hist_where = "\n                  AND ".join(hist_parts)
    prev_name_expr = (
        f"SELECT TRIM(r2.kyosomei_hondai)\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              WHERE {hist_where}\n"
        f"              ORDER BY r2.kaisai_nen DESC, r2.kaisai_gappi DESC\n"
        f"              LIMIT 1"
    )
    cond_pred = _apply_cond(prev_name_expr, cond, params)
    base_valid = "\n              AND ".join(_ENTRY_VALID_PARTS)
    return (
        f"SELECT u.ketto_toroku_bango, u.race_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        WHERE {base_valid}\n"
        f"          AND {cond_pred}"
    )


def _build_jockey_continuity_filter(
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """jockey_continuity HistoryFilter のサブクエリを生成する."""
    prev_hist_parts = [
        "u2.ketto_toroku_bango = u.ketto_toroku_bango",
        "(r2.kaisai_nen || r2.kaisai_gappi) < (r.kaisai_nen || r.kaisai_gappi)",
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
    ]
    prev_hist_where = "\n                  AND ".join(prev_hist_parts)
    continuity_expr = (
        f"CASE\n"
        f"            WHEN u.kishu_code = (\n"
        f"              SELECT u2.kishu_code\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              WHERE {prev_hist_where}\n"
        f"              ORDER BY r2.kaisai_nen DESC, r2.kaisai_gappi DESC\n"
        f"              LIMIT 1\n"
        f"            ) THEN '継続'\n"
        f"            WHEN u.kishu_code IN (\n"
        f"              SELECT u2.kishu_code\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              WHERE {prev_hist_where}\n"
        f"            ) THEN '乗り戻り'\n"
        f"            ELSE 'テン乗り'\n"
        f"          END"
    )
    cond_pred = _apply_cond(continuity_expr, cond, params)
    base_valid = "\n              AND ".join(_ENTRY_VALID_PARTS)
    return (
        f"SELECT u.ketto_toroku_bango, u.race_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        WHERE {base_valid}\n"
        f"          AND {cond_pred}"
    )


def _build_sire_condition_finisher_filter(
    source: AttrSource,
    cond: tuple[int, int] | int | str,
    params: list[Any],
) -> str:
    """sire_condition_finisher HistoryFilter のサブクエリを生成する."""
    sire_cond_parts = [
        "u2.kakutei_chakujun ~ '^[0-9]{2}$'",
        "u2.kakutei_chakujun != '00'",
        "CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND %s",
    ]
    params.append(int(source.top_n))
    if source.condition is not None:
        tmp: list[Any] = []
        sire_cond_parts.extend(build_race_condition_where(source.condition, tmp, race_alias="r2"))
        params.extend(tmp)
    sire_where = "\n                  AND ".join(sire_cond_parts)
    finisher_subq = (
        f"SELECT DISTINCT km2b.ketto1_bamei\n"
        f"              FROM umagoto_race_joho u2\n"
        f"              JOIN race_shosai r2 ON u2.race_code = r2.race_code\n"
        f"              JOIN kyosoba_master2 km2b\n"
        f"                ON u2.ketto_toroku_bango = km2b.ketto_toroku_bango\n"
        f"              WHERE {sire_where}"
    )
    sire_expr = (
        f"CASE WHEN km2.ketto1_bamei IN (\n"
        f"            {finisher_subq}\n"
        f"          ) THEN 1 ELSE 0 END"
    )
    cond_pred = _apply_cond(sire_expr, cond, params)
    base_valid = "\n              AND ".join(_ENTRY_VALID_PARTS)
    return (
        f"SELECT u.ketto_toroku_bango, u.race_code\n"
        f"        FROM umagoto_race_joho u\n"
        f"        JOIN race_shosai r ON u.race_code = r.race_code\n"
        f"        JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango\n"
        f"        WHERE {base_valid}\n"
        f"          AND {cond_pred}"
    )
