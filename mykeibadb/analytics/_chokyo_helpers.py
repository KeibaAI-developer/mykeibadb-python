"""ChokyoThreshold解決ヘルパーモジュール."""

from typing import Any

from mykeibadb.analytics._models import ChokyoThreshold

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
