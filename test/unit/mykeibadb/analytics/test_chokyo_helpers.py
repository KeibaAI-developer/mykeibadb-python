"""_chokyo_helpers モジュールの単体テスト."""

import pytest

from mykeibadb.analytics._chokyo_helpers import build_threshold_where, resolve_threshold_col
from mykeibadb.analytics._models import ChokyoThreshold


# 正常系
def test_resolve_threshold_col_wood_gokei() -> None:
    """wood+gokeiはwoodchip_chokyoのtime_gokei_Nfurlongを返す."""
    t = ChokyoThreshold(course="wood", metric="gokei", furlong=6)
    table, col = resolve_threshold_col(t)
    assert table == "woodchip_chokyo"
    assert col == "time_gokei_6furlong"


def test_resolve_threshold_col_wood_lap() -> None:
    """wood+lapはwoodchip_chokyoのlaptime_Nfurlongを返す."""
    t = ChokyoThreshold(course="wood", metric="lap", furlong=1)
    table, col = resolve_threshold_col(t)
    assert table == "woodchip_chokyo"
    assert col == "laptime_1furlong"


def test_resolve_threshold_col_hanro_gokei() -> None:
    """hanro+gokeiはhanro_chokyoのtime_gokei_Nfurlongを返す."""
    t = ChokyoThreshold(course="hanro", metric="gokei", furlong=4)
    table, col = resolve_threshold_col(t)
    assert table == "hanro_chokyo"
    assert col == "time_gokei_4furlong"


def test_resolve_threshold_col_hanro_lap() -> None:
    """hanro+lapはhanro_chokyoのlap_time_Nfurlongを返す."""
    t = ChokyoThreshold(course="hanro", metric="lap", furlong=1)
    table, col = resolve_threshold_col(t)
    assert table == "hanro_chokyo"
    assert col == "lap_time_1furlong"


def test_build_threshold_where_gokei_sentinel() -> None:
    """gokeiはセンチネル0000/9999を除外するWHERE条件を生成する."""
    t = ChokyoThreshold(course="wood", metric="gokei", furlong=6)
    params: list[object] = []
    parts = build_threshold_where(t, "w", params)
    assert any("'0000'" in p and "'9999'" in p for p in parts)
    assert params == []


def test_build_threshold_where_lap_sentinel() -> None:
    """lapはセンチネル000/999を除外するWHERE条件を生成する."""
    t = ChokyoThreshold(course="wood", metric="lap", furlong=1)
    params: list[object] = []
    parts = build_threshold_where(t, "w", params)
    assert any("'000'" in p and "'999'" in p for p in parts)


def test_build_threshold_where_max_value() -> None:
    """max_value指定でCAST(col AS INTEGER) <= %sが追加される."""
    t = ChokyoThreshold(course="wood", metric="gokei", furlong=6, max_value=815)
    params: list[object] = []
    parts = build_threshold_where(t, "w", params)
    assert any("<= %s" in p for p in parts)
    assert 815 in params


def test_build_threshold_where_min_value() -> None:
    """min_value指定でCAST(col AS INTEGER) >= %sが追加される."""
    t = ChokyoThreshold(course="wood", metric="gokei", furlong=6, min_value=700)
    params: list[object] = []
    parts = build_threshold_where(t, "w", params)
    assert any(">= %s" in p for p in parts)
    assert 700 in params


def test_build_threshold_where_tracen_kubun() -> None:
    """tracen_kubun指定でtracen_kubun = %sが追加される."""
    t = ChokyoThreshold(course="wood", metric="gokei", furlong=6, tracen_kubun="1")
    params: list[object] = []
    parts = build_threshold_where(t, "w", params)
    assert any("tracen_kubun = %s" in p for p in parts)
    assert "1" in params


def test_build_threshold_where_all_conditions() -> None:
    """全条件指定でパラメータがすべて追加される."""
    t = ChokyoThreshold(
        course="wood", metric="gokei", furlong=6,
        max_value=815, min_value=700, tracen_kubun="1",
    )
    params: list[object] = []
    parts = build_threshold_where(t, "w", params)
    assert len(parts) == 4
    assert "1" in params
    assert 815 in params
    assert 700 in params


# 準正常系
def test_resolve_threshold_col_invalid_course() -> None:
    """不正なcourseでValueErrorが発生する."""
    t = ChokyoThreshold(course="turf", metric="gokei", furlong=6)
    with pytest.raises(ValueError, match="course"):
        resolve_threshold_col(t)


def test_resolve_threshold_col_invalid_metric() -> None:
    """不正なmetricでValueErrorが発生する."""
    t = ChokyoThreshold(course="wood", metric="speed", furlong=6)
    with pytest.raises(ValueError, match="metric"):
        resolve_threshold_col(t)
