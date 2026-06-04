"""analyze_chakudo の単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import ChakudoRow, analyze_chakudo
from mykeibadb.exceptions import QueryExecutionError


def _make_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DataFrameを生成する."""
    return pd.DataFrame(rows)


# 正常系
def test_analyze_chakudo_returns_success(mocker: MockerFixture) -> None:
    """正常なDBレスポンスで success=True / ChakudoRow のリストが返る."""
    mock_df = _make_df([
        {
            "grp": "1人気", "sort_key": 1, "total": 100, "wins": 30,
            "second": 20, "third": 15, "chakugai": 35,
            "win_rate": 30.0, "fukusho_rate": 65.0,
            "tansho_kaishuu": 78.0, "fukusho_kaishuu": 85.0,
        },
    ])
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = mock_df

    result = analyze_chakudo(manager, "grp_expr", "sort_expr")

    assert result.success is True
    assert result.error is None
    assert len(result.rows) == 1
    row = result.rows[0]
    assert isinstance(row, ChakudoRow)
    assert row.group == "1人気"
    assert row.total == 100
    assert row.wins == 30
    assert row.win_rate == 30.0


def test_analyze_chakudo_with_filters_passes_params(mocker: MockerFixture) -> None:
    """フィルタ引数が SQL パラメータとして渡される."""
    mock_df = _make_df([
        {
            "grp": "A", "sort_key": 0, "total": 50, "wins": 10,
            "second": 5, "third": 5, "chakugai": 30,
            "win_rate": 20.0, "fukusho_rate": 40.0,
            "tansho_kaishuu": 60.0, "fukusho_kaishuu": 70.0,
        },
    ])
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = mock_df

    analyze_chakudo(
        manager, "grp_expr", "sort_expr",
        race_name="有馬記念",
        keibajo="06",
        kyori=2500,
        year_from="2020",
        year_to="2024",
        grade="A",
    )

    call_args = manager.fetch_dataframe.call_args
    sql, params = call_args[0][0], call_args[1]["params"]
    assert "%有馬記念%" in params
    assert "06" in params
    assert 2500 in params
    assert "2020" in params
    assert "2024" in params
    assert "A" in params
    assert "race_name LIKE %s" in sql


def test_analyze_chakudo_empty_result(mocker: MockerFixture) -> None:
    """空のDataFrameで success=True / rows=[] が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = pd.DataFrame()

    result = analyze_chakudo(manager, "grp_expr", "sort_expr")

    assert result.success is True
    assert result.rows == []


def test_analyze_chakudo_nan_rates_default_to_zero(mocker: MockerFixture) -> None:
    """win_rate等がNaNの場合は0.0になる."""
    mock_df = _make_df([
        {
            "grp": "X", "sort_key": 1, "total": 0, "wins": 0,
            "second": 0, "third": 0, "chakugai": 0,
            "win_rate": float("nan"), "fukusho_rate": float("nan"),
            "tansho_kaishuu": float("nan"), "fukusho_kaishuu": float("nan"),
        },
    ])
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = mock_df

    result = analyze_chakudo(manager, "grp_expr", "sort_expr")

    row = result.rows[0]
    assert row.win_rate == 0.0
    assert row.fukusho_rate == 0.0
    assert row.tansho_kaishuu == 0.0
    assert row.fukusho_kaishuu == 0.0


def test_analyze_chakudo_with_course_week_filter(mocker: MockerFixture) -> None:
    """course_kubun + week_in_course 指定時に CTE が SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([
        {
            "grp": "A", "sort_key": 0, "total": 10, "wins": 3,
            "second": 2, "third": 1, "chakugai": 4,
            "win_rate": 30.0, "fukusho_rate": 60.0,
            "tansho_kaishuu": 75.0, "fukusho_kaishuu": 80.0,
        },
    ])

    analyze_chakudo(
        manager, "grp_expr", "sort_expr",
        keibajo="05", course_kubun="C", week_in_course=2,
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "cw_target" in sql
    assert "r.keibajo_code = %s" not in sql


def test_analyze_chakudo_keibajo_in_where_without_cw(mocker: MockerFixture) -> None:
    """course_week指定なしの場合、keibajo が WHERE 句に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([
        {
            "grp": "A", "sort_key": 0, "total": 10, "wins": 3,
            "second": 2, "third": 1, "chakugai": 4,
            "win_rate": 30.0, "fukusho_rate": 60.0,
            "tansho_kaishuu": 75.0, "fukusho_kaishuu": 80.0,
        },
    ])

    analyze_chakudo(manager, "grp_expr", "sort_expr", keibajo="05")

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "r.keibajo_code = %s" in sql
    assert "05" in params


# 準正常系
def test_analyze_chakudo_raises_on_only_course_kubun(mocker: MockerFixture) -> None:
    """course_kubun のみ指定で ValueError が発生する."""
    manager = mocker.MagicMock()
    with pytest.raises(ValueError):
        analyze_chakudo(manager, "grp_expr", "sort_expr", course_kubun="C")


def test_analyze_chakudo_raises_on_only_week_in_course(mocker: MockerFixture) -> None:
    """week_in_course のみ指定で ValueError が発生する."""
    manager = mocker.MagicMock()
    with pytest.raises(ValueError):
        analyze_chakudo(manager, "grp_expr", "sort_expr", week_in_course=1)


def test_analyze_chakudo_returns_error_on_db_failure(mocker: MockerFixture) -> None:
    """DBエラーで success=False / error が設定される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("DB接続失敗")

    result = analyze_chakudo(manager, "grp_expr", "sort_expr")

    assert result.success is False
    assert result.error is not None
    assert "DB接続失敗" in result.error
