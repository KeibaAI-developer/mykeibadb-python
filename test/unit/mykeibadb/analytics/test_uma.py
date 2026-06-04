"""get_uma_rekisen の単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import RaceCondition, get_uma_rekisen
from mykeibadb.exceptions import QueryExecutionError


def _make_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DataFrameを生成する."""
    return pd.DataFrame(rows)


def _make_rekisen_row() -> dict[str, object]:
    """競走成績行."""
    return {
        "ketto_toroku_bango": "2020100001",
        "bamei": "ディープインパクト",
        "race_date": "20230101",
        "keibajo_code": "05",
        "race_code": "2023010105010101",
        "umaban": "01",
        "kakutei_chakujun": "01",
        "kyori": 2000,
        "track_code": "10",
        "grade_code": "A",
    }


# 正常系
def test_get_uma_rekisen_by_name(mocker: MockerFixture) -> None:
    """uma_nameで競走成績が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_rekisen_row()])

    result = get_uma_rekisen(manager, uma_name="ディープ")

    assert result["success"] is True
    assert result["count"] == 1
    assert len(result["results"]) == 1
    assert result["results"][0]["bamei"] == "ディープインパクト"


def test_get_uma_rekisen_by_ketto_toroku_bango(mocker: MockerFixture) -> None:
    """ketto_toroku_bangoで完全一致検索する."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_rekisen_row()])

    result = get_uma_rekisen(manager, ketto_toroku_bango="2020100001")

    assert result["success"] is True
    sql = manager.fetch_dataframe.call_args[0][0]
    assert "u.ketto_toroku_bango = %s" in sql
    assert "LIKE" not in sql


def test_get_uma_rekisen_ketto_takes_priority_over_name(mocker: MockerFixture) -> None:
    """ketto_toroku_bangoとuma_nameを両方指定するとketto_toroku_bangoが優先される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_rekisen_row()])

    get_uma_rekisen(manager, uma_name="ディープ", ketto_toroku_bango="2020100001")

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "u.ketto_toroku_bango = %s" in sql
    assert "LIKE" not in sql


def test_get_uma_rekisen_name_uses_like(mocker: MockerFixture) -> None:
    """uma_name指定時はLIKE検索が使われる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_rekisen_row()])

    get_uma_rekisen(manager, uma_name="ディープ")

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "u.bamei LIKE %s" in sql
    assert "%ディープ%" in params


def test_get_uma_rekisen_with_condition(mocker: MockerFixture) -> None:
    """RaceConditionを渡すと絞り込みWHERE句が生成される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_rekisen_row()])

    condition = RaceCondition(keibajo_code="05")
    get_uma_rekisen(manager, uma_name="ディープ", condition=condition)

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "r.keibajo_code" in sql


def test_get_uma_rekisen_empty_result(mocker: MockerFixture) -> None:
    """結果が0件の場合はcount=0でresults=[]が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([])

    result = get_uma_rekisen(manager, uma_name="存在しない馬")

    assert result["success"] is True
    assert result["count"] == 0
    assert result["results"] == []


def test_get_uma_rekisen_db_error_returns_failure(mocker: MockerFixture) -> None:
    """DBエラーでsuccess=Falseが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("接続失敗")

    result = get_uma_rekisen(manager, uma_name="ディープ")

    assert result["success"] is False
    assert result.get("error") is not None


# 準正常系
def test_get_uma_rekisen_no_args_raises() -> None:
    """引数なしでValueErrorが発生する."""
    manager = object()
    with pytest.raises(ValueError, match="uma_name"):
        get_uma_rekisen(manager)  # type: ignore[arg-type]
