"""analyze_chakudo の統合テスト."""

import pandas as pd
from pytest_mock import MockerFixture

from mykeibadb.analytics import RaceColFilter, RaceCondition, analyze_chakudo
from mykeibadb.exceptions import QueryExecutionError


def _make_entry_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _make_tally_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _entry_row(
    ketto: str = "2019100001",
    race_code: str = "202101010101",
    umaban: str = "01",
    group_label: str = "全体",
) -> dict[str, object]:
    return {
        "ketto_toroku_bango": ketto,
        "race_code": race_code,
        "umaban": umaban,
        "group_label": group_label,
    }


def _tally_row(
    group: str = "全体",
    total: int = 10,
    wins: int = 2,
    second: int = 1,
    third: int = 1,
    chakugai: int = 6,
    tansho: int = 2000,
    fukusho: int = 1200,
) -> dict[str, object]:
    return {
        "group_label": group,
        "total": total,
        "wins": wins,
        "second": second,
        "third": third,
        "chakugai": chakugai,
        "tansho_payout_sum": tansho,
        "fukusho_payout_sum": fukusho,
    }


# 正常系: filters=[] で全体集計
def test_analyze_chakudo_no_filters_returns_success(mocker: MockerFixture) -> None:
    """filters=[] で全体集計が行われ success=True が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_entry_df([_entry_row()]),
        _make_tally_df([_tally_row()]),
    ]

    result = analyze_chakudo(manager, filters=[])

    assert result.success is True
    assert len(result.rows) == 1
    assert result.rows[0].group == "全体"
    assert result.rows[0].total == 10


def test_analyze_chakudo_computes_rates(mocker: MockerFixture) -> None:
    """フェーズ3の計算が正しく行われる（勝率・複勝率・単複回収率）."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_entry_df([_entry_row()]),
        _make_tally_df([_tally_row(total=10, wins=3, second=2, third=1, tansho=1500, fukusho=900)]),
    ]

    result = analyze_chakudo(manager, filters=[])

    row = result.rows[0]
    assert row.win_rate == 30.0
    assert row.fukusho_rate == 60.0
    assert row.tansho_kaishuu == 150.0
    assert row.fukusho_kaishuu == 90.0


def test_analyze_chakudo_with_race_col_filter(mocker: MockerFixture) -> None:
    """RaceColFilter 指定時に SQL パラメータにフィルタ値が含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_entry_df([_entry_row()]),
        _make_tally_df([_tally_row()]),
    ]

    analyze_chakudo(
        manager,
        filters=[RaceColFilter(column="u.waku_ban", values=["1", "2", "3"])],
    )

    sql = manager.fetch_dataframe.call_args_list[0][0][0]
    params = manager.fetch_dataframe.call_args_list[0][1]["params"]
    assert "u.waku_ban" in sql
    assert "1" in params
    assert "2" in params
    assert "3" in params


def test_analyze_chakudo_with_condition(mocker: MockerFixture) -> None:
    """condition 指定時に SQL に keibajo_code が含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_entry_df([_entry_row()]),
        _make_tally_df([_tally_row()]),
    ]

    analyze_chakudo(
        manager,
        filters=[],
        condition=RaceCondition(keibajo_codes=["05"]),
    )

    sql = manager.fetch_dataframe.call_args_list[0][0][0]
    params = manager.fetch_dataframe.call_args_list[0][1]["params"]
    assert ["05"] in params
    assert "keibajo_code" in sql


def test_analyze_chakudo_empty_entries_returns_empty_rows(mocker: MockerFixture) -> None:
    """フェーズ1で空 EntrySet が返った場合、rows が空の ChakudoResult が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df([])

    result = analyze_chakudo(manager, filters=[])

    assert result.success is True
    assert result.rows == []


def test_analyze_chakudo_returns_error_on_db_failure(mocker: MockerFixture) -> None:
    """DBエラーで success=False / error が設定される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("DB接続失敗")

    result = analyze_chakudo(manager, filters=[])

    assert result.success is False
    assert result.error is not None
    assert "DB接続失敗" in result.error


def test_analyze_chakudo_returns_error_on_tally_db_failure(mocker: MockerFixture) -> None:
    """フェーズ2のDBエラーで success=False が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_entry_df([_entry_row()]),
        QueryExecutionError("tally失敗"),
    ]

    result = analyze_chakudo(manager, filters=[])

    assert result.success is False
    assert result.error is not None
    assert "tally失敗" in result.error
