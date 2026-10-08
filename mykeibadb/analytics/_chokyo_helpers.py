"""ChokyoThreshold解決ヘルパーモジュール."""

from typing import Any

from mykeibadb.analytics._models import AttrSource, ChokyoThreshold

_VALID_COURSES = ("wood", "hanro")
_VALID_METRICS = ("gokei", "lap")


def resolve_threshold_col(threshold: ChokyoThreshold) -> tuple[str, str]:
    """ChokyoThresholdからテーブル名とカラム名を解決する.

    Args:
        threshold (ChokyoThreshold): 調教閾値条件

    Returns:
        tuple[str, str]: (テーブル名（"woodchip_chokyo" または "hanro_chokyo"）, カラム名)

    Raises:
        ValueError: course / metric が未対応、または furlong が正の整数でない場合
    """
    if threshold.course not in _VALID_COURSES:
        raise ValueError(f"未対応の course です: {threshold.course!r}")
    if threshold.metric not in _VALID_METRICS:
        raise ValueError(f"未対応の metric です: {threshold.metric!r}")

    n = int(threshold.furlong)
    if n <= 0:
        raise ValueError(f"furlong は正の整数でなければなりません: {threshold.furlong!r}")
    if threshold.metric == "gokei":
        col = f"time_gokei_{n}furlong"
    elif threshold.course == "wood":
        col = f"laptime_{n}furlong"
    else:
        col = f"lap_time_{n}furlong"

    table = "woodchip_chokyo" if threshold.course == "wood" else "hanro_chokyo"
    return table, col


def resolve_valid_where(course: str, alias: str) -> str:
    """調教コースに応じた有効判定WHERE句を返す.

    合計タイムのセンチネル値（0000/9999）を除外する。

    Args:
        course (str): "wood" または "hanro"
        alias (str): SQLテーブルエイリアス

    Returns:
        str: 有効判定WHERE句

    Raises:
        ValueError: course が未対応の場合
    """
    if course not in _VALID_COURSES:
        raise ValueError(f"未対応の course です: {course!r}")
    col = "time_gokei_6furlong" if course == "wood" else "time_gokei_4furlong"
    return f"{alias}.{col} NOT IN ('0000', '9999')"


def build_threshold_where(
    threshold: ChokyoThreshold,
    alias: str,
    params: list[Any],
) -> list[str]:
    """ChokyoThresholdからWHERE句のpartsリストを生成する.

    センチネル値（0000/9999 または 000/999）を除外し、max_value / min_value /
    tracen_kubun の各条件をWHERE句として追加する。

    Args:
        threshold (ChokyoThreshold): 調教閾値条件
        alias (str): SQLテーブルエイリアス
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        list[str]: WHERE句のpartsリスト
    """
    _, col = resolve_threshold_col(threshold)
    if threshold.metric == "gokei":
        sentinels = ("'0000'", "'9999'")
    else:
        sentinels = ("'000'", "'999'")

    parts: list[str] = [f"{alias}.{col} NOT IN ({', '.join(sentinels)})"]

    if threshold.tracen_kubun is not None:
        parts.append(f"{alias}.tracen_kubun = %s")
        params.append(threshold.tracen_kubun)
    if threshold.max_value is not None:
        parts.append(f"CAST({alias}.{col} AS INTEGER) <= %s")
        params.append(threshold.max_value)
    if threshold.min_value is not None:
        parts.append(f"CAST({alias}.{col} AS INTEGER) >= %s")
        params.append(threshold.min_value)

    return parts


def validate_chokyo_match_days(source: AttrSource) -> str:
    """chokyo_match_days の設定を検証しコースを返す.

    Args:
        source (AttrSource): 属性算出方法（chokyo_condition・days_from・days_to 必須）

    Returns:
        str: 統一されたコース（"wood" または "hanro"）

    Raises:
        ValueError: source.chokyo_condition が未指定・空リストの場合
        ValueError: source.chokyo_condition 内の course が統一されていない場合
        ValueError: source.days_from または source.days_to が未指定の場合
        ValueError: source.days_from が1未満の場合
        ValueError: source.days_from が source.days_to を超える場合
    """
    condition = source.chokyo_condition
    if not condition:
        raise ValueError("chokyo_match_days には chokyo_condition の指定が必要です。")
    courses = {t.course for t in condition}
    if len(courses) > 1:
        raise ValueError(f"chokyo_condition の course は統一してください: {courses!r}")
    if source.days_from is None or source.days_to is None:
        raise ValueError("chokyo_match_days には days_from と days_to の指定が必要です。")
    if source.days_from < 1:
        raise ValueError(f"days_from は1以上でなければなりません: {source.days_from!r}")
    if source.days_from > source.days_to:
        raise ValueError(
            f"days_from は days_to 以下でなければなりません: "
            f"days_from={source.days_from!r}, days_to={source.days_to!r}"
        )
    return next(iter(courses))


def build_chokyo_match_days_ctes(source: AttrSource, params: list[Any]) -> list[str]:
    """chokyo_match_days 用 CTE リストを返す.

    対象レース日の days_to 日前〜days_from 日前（両端含む）に行われた、対象コースの
    有効な調教記録すべてについて、レース何日前かと chokyo_condition の全閾値を
    満たすかを判定する。対象馬の調教を1回の走査で取得する chokyo_rows CTE と、
    それを対象レースと突き合わせて JSON 配列にまとめる attr_agg CTE の2つを返す。

    呼び出し側で target_horses CTE（ketto_toroku_bango・race_code・kaisai_nen・
    kaisai_gappi 列を持つ）を用意しておく必要がある。

    Args:
        source (AttrSource): 属性算出方法（chokyo_condition・days_from・days_to 必須）
        params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        list[str]: [chokyo_rows CTE, attr_agg CTE] の文字列リスト

    Raises:
        ValueError: source.chokyo_condition が未指定・空リストの場合
        ValueError: source.chokyo_condition 内の course が統一されていない場合
        ValueError: source.days_from または source.days_to が未指定の場合
        ValueError: source.days_from が1未満の場合
        ValueError: source.days_from が source.days_to を超える場合
    """
    course = validate_chokyo_match_days(source)
    condition = source.chokyo_condition
    assert condition is not None
    table, _ = resolve_threshold_col(condition[0])
    valid_where = resolve_valid_where(course, "c")
    match_conds: list[str] = []
    for threshold in condition:
        match_conds.extend(build_threshold_where(threshold, "c", params))
    match_expr = "\n                    AND ".join(match_conds)
    chokyo_rows_cte = (
        f"chokyo_rows AS (\n"
        f"        SELECT c.ketto_toroku_bango,\n"
        f"               TO_DATE(c.chokyo_nengappi, 'YYYYMMDD') AS chokyo_date,\n"
        f"               c.chokyo_jikoku,\n"
        f"               ({match_expr}) AS is_match\n"
        f"        FROM {table} c\n"
        f"        WHERE {valid_where}\n"
        f"          AND c.ketto_toroku_bango IN (SELECT ketto_toroku_bango FROM target_horses)\n"
        f"    )"
    )
    assert source.days_from is not None and source.days_to is not None
    params.append(source.days_from)
    params.append(source.days_to)
    attr_agg_cte = (
        "attr_agg AS (\n"
        "        SELECT\n"
        "            th.ketto_toroku_bango,\n"
        "            th.race_code AS target_race_code,\n"
        "            COALESCE(\n"
        "                jsonb_agg(\n"
        "                    jsonb_build_array(cr.days_before, cr.is_match)\n"
        "                    ORDER BY cr.days_before ASC, cr.chokyo_jikoku ASC\n"
        "                ) FILTER (WHERE cr.days_before IS NOT NULL),\n"
        "                '[]'::jsonb\n"
        "            )::TEXT AS attr_val\n"
        "        FROM target_horses th\n"
        "        LEFT JOIN (\n"
        "            SELECT th2.ketto_toroku_bango, th2.race_code, c.is_match, c.chokyo_jikoku,\n"
        "                   TO_DATE(th2.kaisai_nen || th2.kaisai_gappi, 'YYYYMMDD')\n"
        "                       - c.chokyo_date AS days_before\n"
        "            FROM target_horses th2\n"
        "            JOIN chokyo_rows c ON c.ketto_toroku_bango = th2.ketto_toroku_bango\n"
        "        ) cr\n"
        "            ON cr.ketto_toroku_bango = th.ketto_toroku_bango\n"
        "            AND cr.race_code = th.race_code\n"
        "            AND cr.days_before BETWEEN %s AND %s\n"
        "        GROUP BY th.ketto_toroku_bango, th.race_code\n"
        "    )"
    )
    return [chokyo_rows_cte, attr_agg_cte]
