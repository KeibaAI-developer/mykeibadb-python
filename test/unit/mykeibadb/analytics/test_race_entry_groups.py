"""get_race_entry_groups の単体テスト."""

from unittest.mock import MagicMock

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import (
    AttrSource,
    ChokyoThreshold,
    GroupBy,
    Subject,
    get_race_entry_groups,
)
from mykeibadb.exceptions import MykeibaDBError, QueryExecutionError

_RACE_CODE = "2025092806040911"
_EXCLUDED_CODES = ["1", "2", "3"]


def _make_df(rows: list[tuple[str, str | None]]) -> pd.DataFrame:
    """(馬番, group_label) のリストからテスト用DataFrameを生成する."""
    return pd.DataFrame(
        [
            {
                "ketto_toroku_bango": f"20200000{i:02d}",
                "race_code": _RACE_CODE,
                "umaban": umaban,
                "group_label": label,
            }
            for i, (umaban, label) in enumerate(rows)
        ]
    )


def _fetched(manager: MagicMock) -> tuple[str, tuple[object, ...]]:
    """fetch_dataframe に渡された SQL とパラメータを返す."""
    call = manager.fetch_dataframe.call_args
    return call[0][0], call[1]["params"]


# 正常系
def test_get_race_entry_groups_race_col_returns_label_by_umaban(mocker: MockerFixture) -> None:
    """race_col で馬番 -> group_label の辞書が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([("01", "1"), ("02", "1"), ("10", "5")])

    result = get_race_entry_groups(
        manager, _RACE_CODE, GroupBy(kind="race_col", column="u.wakuban")
    )

    assert result == {1: "1", 2: "1", 10: "5"}


def test_get_race_entry_groups_filters_by_race_code_without_chakujun_condition(
    mocker: MockerFixture,
) -> None:
    """対象は race_code と異常区分コードで決まり、確定着順の条件を含まない."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([("01", "1")])

    get_race_entry_groups(manager, _RACE_CODE, GroupBy(kind="race_col", column="u.wakuban"))

    sql, params = _fetched(manager)
    assert "u.race_code = %s" in sql
    assert "u.ijo_kubun_code = ANY(%s)" in sql
    assert "kakutei_chakujun" not in sql
    assert params == (_RACE_CODE, _EXCLUDED_CODES)


def test_get_race_entry_groups_subject_includes_subject_column(mocker: MockerFixture) -> None:
    """subject で主体の列が group_label として SELECT される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([("01", "騎手A"), ("02", "騎手B")])

    result = get_race_entry_groups(
        manager, _RACE_CODE, GroupBy(kind="subject", subject=Subject.KISHU)
    )

    sql, _ = _fetched(manager)
    assert "u.kishumei_ryakusho AS group_label" in sql
    assert result == {1: "騎手A", 2: "騎手B"}


@pytest.mark.parametrize(
    "source",
    [
        AttrSource(type="prev_race_col", column="kyakushitsu_hantei"),
        AttrSource(type="past_race_top_n_count", top_n=3),
        AttrSource(type="tokubetsu_race_finish", tokubetsu_kyoso_bango="0016", year_offset=1),
    ],
)
def test_get_race_entry_groups_history_uses_horse_hist_with_race_code_in_target_horses(
    mocker: MockerFixture, source: AttrSource
) -> None:
    """過去走を使う history は target_horses を指定レースの出走馬に絞り horse_hist から求める."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([("01", "3")])

    result = get_race_entry_groups(manager, _RACE_CODE, GroupBy(kind="history", source=source))

    sql, params = _fetched(manager)
    assert "target_horses AS MATERIALIZED" in sql
    assert "horse_hist AS (" in sql
    assert "(r2.kaisai_nen || r2.kaisai_gappi) < (th.kaisai_nen || th.kaisai_gappi)" in sql
    assert params[:2] == (_RACE_CODE, _EXCLUDED_CODES)
    assert result == {1: "3"}


def test_get_race_entry_groups_chokyo_match_days_skips_horse_hist(mocker: MockerFixture) -> None:
    """chokyo_match_days は horse_hist を使わず target_horses から求める."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([("01", "[[3, true]]")])

    result = get_race_entry_groups(
        manager,
        _RACE_CODE,
        GroupBy(
            kind="history",
            source=AttrSource(
                type="chokyo_match_days",
                chokyo_condition=[
                    ChokyoThreshold(course="hanro", metric="gokei", furlong=4, max_value=540)
                ],
                days_from=1,
                days_to=13,
            ),
        ),
    )

    sql, params = _fetched(manager)
    assert "target_horses AS MATERIALIZED" in sql
    assert "horse_hist AS (" not in sql
    assert params[:2] == (_RACE_CODE, _EXCLUDED_CODES)
    assert result == {1: "[[3, true]]"}


def test_get_race_entry_groups_fixed_returns_row_labels(mocker: MockerFixture) -> None:
    """fixed で rows のラベルが返り、どの行にも当たらない馬は None になる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df(
        [("01", "0回"), ("02", "2回以上"), ("03", None)]
    )

    result = get_race_entry_groups(
        manager,
        _RACE_CODE,
        GroupBy(
            kind="fixed",
            source=AttrSource(type="past_race_top_n_count", top_n=3),
            rows={"0回": 0, "2回以上": (2, 99)},
        ),
    )

    sql, params = _fetched(manager)
    assert "CASE" in sql
    assert params[:2] == (_RACE_CODE, _EXCLUDED_CODES)
    assert result == {1: "0回", 2: "2回以上", 3: None}


def test_get_race_entry_groups_null_group_label_is_none(mocker: MockerFixture) -> None:
    """group_label が NULL の馬は文字列 'None' ではなく None になる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([("01", None), ("02", "2")])

    result = get_race_entry_groups(
        manager,
        _RACE_CODE,
        GroupBy(kind="history", source=AttrSource(type="prev_race_col", column="grade_code")),
    )

    assert result == {1: None, 2: "2"}


# 準正常系
@pytest.mark.parametrize(
    "race_code", ["", "202509280604091", "20250928060409111", "202509280604091A"]
)
def test_get_race_entry_groups_invalid_race_code_raises_value_error(
    mocker: MockerFixture, race_code: str
) -> None:
    """race_code が16桁の数字でない場合は ValueError."""
    manager = mocker.MagicMock()

    with pytest.raises(ValueError):
        get_race_entry_groups(manager, race_code, GroupBy(kind="race_col", column="u.wakuban"))

    manager.fetch_dataframe.assert_not_called()


def test_get_race_entry_groups_unsupported_kind_raises_value_error(mocker: MockerFixture) -> None:
    """未対応の group_by.kind は ValueError."""
    manager = mocker.MagicMock()

    with pytest.raises(ValueError):
        get_race_entry_groups(manager, _RACE_CODE, GroupBy(kind="unknown"))


def test_get_race_entry_groups_no_entries_raises_error(mocker: MockerFixture) -> None:
    """指定レースの出走馬が無い場合は MykeibaDBError."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([])

    with pytest.raises(MykeibaDBError):
        get_race_entry_groups(manager, _RACE_CODE, GroupBy(kind="race_col", column="u.wakuban"))


def test_get_race_entry_groups_db_error_propagates(mocker: MockerFixture) -> None:
    """DB エラーは MykeibaDBError として送出される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("failed")

    with pytest.raises(MykeibaDBError):
        get_race_entry_groups(manager, _RACE_CODE, GroupBy(kind="race_col", column="u.wakuban"))
