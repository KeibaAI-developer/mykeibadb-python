"""tally_chakujun の単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics._models import Entry, EntrySet
from mykeibadb.analytics.chakujun_tally import tally_chakujun
from mykeibadb.exceptions import QueryExecutionError


def _make_entries(*args: tuple[str, str, str, str]) -> EntrySet:
    """テスト用EntrySetを生成する.

    Args:
        *args: (ketto_toroku_bango, race_code, umaban, group_label) のタプル列
    """
    return [
        Entry(
            ketto_toroku_bango=a[0],
            race_code=a[1],
            umaban=a[2],
            group_label=a[3],
        )
        for a in args
    ]


def _make_tally_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DBレスポンスDataFrameを生成する."""
    return pd.DataFrame(rows)


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


# 正常系
def test_tally_chakujun_returns_group_tally_list(mocker: MockerFixture) -> None:
    """正常なDBレスポンスで GroupTally リストが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_tally_df([_tally_row()])

    entries = _make_entries(("2019100001", "202101010101", "01", "全体"))
    result = tally_chakujun(manager, entries)

    assert len(result) == 1
    assert result[0].group == "全体"
    assert result[0].total == 10


def test_tally_chakujun_maps_all_fields(mocker: MockerFixture) -> None:
    """全フィールドが GroupTally に正しくマッピングされる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_tally_df(
        [_tally_row(total=20, wins=5, second=3, third=2, chakugai=10, tansho=5000, fukusho=2500)]
    )

    entries = _make_entries(("2019100001", "202101010101", "01", "全体"))
    result = tally_chakujun(manager, entries)

    gt = result[0]
    assert gt.total == 20
    assert gt.wins == 5
    assert gt.second == 3
    assert gt.third == 2
    assert gt.chakugai == 10
    assert gt.tansho_payout_sum == 5000
    assert gt.fukusho_payout_sum == 2500


def test_tally_chakujun_groups_correctly(mocker: MockerFixture) -> None:
    """複数 group_label のレコードが個別の GroupTally に集計される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_tally_df(
        [
            _tally_row(group="キタサンブラック", total=5, wins=2),
            _tally_row(group="ディープインパクト", total=8, wins=1),
        ]
    )

    entries = _make_entries(
        ("2019100001", "202101010101", "01", "キタサンブラック"),
        ("2019100002", "202101010102", "02", "ディープインパクト"),
    )
    result = tally_chakujun(manager, entries)

    assert len(result) == 2
    groups = {r.group for r in result}
    assert groups == {"キタサンブラック", "ディープインパクト"}


def test_tally_chakujun_payout_sums_accumulated(mocker: MockerFixture) -> None:
    """払戻が tansho_payout_sum / fukusho_payout_sum に合算される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_tally_df(
        [_tally_row(tansho=13500, fukusho=7800)]
    )

    entries = _make_entries(
        ("2019100001", "202101010101", "01", "全体"),
        ("2019100002", "202101010102", "02", "全体"),
    )
    result = tally_chakujun(manager, entries)

    assert result[0].tansho_payout_sum == 13500
    assert result[0].fukusho_payout_sum == 7800


def test_tally_chakujun_sql_uses_values_clause(mocker: MockerFixture) -> None:
    """entries の (race_code, umaban, group_label) が VALUES 句でSQLに展開される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_tally_df([_tally_row()])

    entries = _make_entries(
        ("2019100001", "202101010101", "03", "全体"),
        ("2019100002", "202101010102", "07", "全体"),
    )
    tally_chakujun(manager, entries)

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "VALUES" in sql
    assert "202101010101" in params
    assert "202101010102" in params
    assert "03" in params
    assert "07" in params


def test_tally_chakujun_sql_joins_payout_tables(mocker: MockerFixture) -> None:
    """生成SQLに払戻CTEへのJOINが含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_tally_df([_tally_row()])

    entries = _make_entries(("2019100001", "202101010101", "01", "全体"))
    tally_chakujun(manager, entries)

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "tansho_payouts" in sql
    assert "fukusho_payouts" in sql
    assert "LEFT JOIN" in sql


# 空EntrySet
def test_tally_chakujun_returns_empty_list_when_entries_empty(
    mocker: MockerFixture,
) -> None:
    """空 EntrySet で空リストが返る（DBアクセスなし）."""
    manager = mocker.MagicMock()

    result = tally_chakujun(manager, [])

    assert result == []
    manager.fetch_dataframe.assert_not_called()


# DBエラー
def test_tally_chakujun_raises_on_db_error(mocker: MockerFixture) -> None:
    """DBエラーで例外が送出される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("DB接続失敗")

    with pytest.raises(QueryExecutionError, match="DB接続失敗"):
        tally_chakujun(
            manager,
            _make_entries(("2019100001", "202101010101", "01", "全体")),
        )
