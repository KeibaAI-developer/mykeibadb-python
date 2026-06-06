"""select_entries の単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics._models import (
    AttrSource,
    ChokyoFilter,
    ChokyoThreshold,
    GroupBy,
    HistoryFilter,
    RaceColFilter,
    RaceCondition,
    Subject,
    SubjectFilter,
)
from mykeibadb.analytics.entry_select import select_entries
from mykeibadb.exceptions import QueryExecutionError


def _make_entry_df(rows: list[dict[str, object]] | None = None) -> pd.DataFrame:
    """テスト用エントリDataFrameを生成する."""
    if rows is None:
        rows = [
            {
                "ketto_toroku_bango": "2019100001",
                "race_code": "202101010101",
                "umaban": "01",
                "group_label": "全体",
            }
        ]
    return pd.DataFrame(rows)


# RaceColFilter 単独
def test_select_entries_race_col_filter_returns_entries(mocker: MockerFixture) -> None:
    """RaceColFilter のみ指定で Entry リストが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    result = select_entries(
        manager,
        filters=[RaceColFilter(column="u.wakuban", values=["1", "2"])],
    )

    assert len(result) == 1
    assert result[0].ketto_toroku_bango == "2019100001"
    assert result[0].race_code == "202101010101"
    assert result[0].umaban == "01"


def test_select_entries_race_col_filter_sql_contains_in_clause(mocker: MockerFixture) -> None:
    """RaceColFilter 指定時にINサブクエリがSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[RaceColFilter(column="u.wakuban", values=["1", "2"])],
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "ketto_toroku_bango, u.race_code" in sql
    assert "IN (" in sql
    assert "1" in params
    assert "2" in params


# INTERSECT 合成
def test_select_entries_multiple_filters_uses_intersect(mocker: MockerFixture) -> None:
    """複数フィルタ指定時にINTERSECTが使われる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[
            RaceColFilter(column="u.wakuban", values=["1"]),
            SubjectFilter(subject=Subject.SIRE, name="キタサンブラック"),
        ],
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "INTERSECT" in sql


# group_by 指定時
def test_select_entries_group_by_race_col_sets_group_label(mocker: MockerFixture) -> None:
    """group_by=race_col 指定時にgroup_labelがSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        group_by=GroupBy(kind="race_col", column="u.wakuban"),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "u.wakuban::TEXT" in sql
    assert "group_label" in sql


def test_select_entries_group_by_none_uses_zentai_label(mocker: MockerFixture) -> None:
    """group_by=None のとき '全体' がラベルとして使われる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(manager, filters=[])

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "'全体'" in sql


def test_select_entries_group_by_subject_includes_join(mocker: MockerFixture) -> None:
    """group_by=subject で km2 JOINが追加される（種牡馬）."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        group_by=GroupBy(kind="subject", subject=Subject.SIRE),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "kyosoba_master2" in sql
    assert "ketto1_bamei" in sql


# condition 指定
def test_select_entries_condition_keibajo_code_in_sql(mocker: MockerFixture) -> None:
    """condition でkeibajo_codeフィルタがSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        condition=RaceCondition(keibajo_code="05", year_from="2020"),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "keibajo_code = %s" in sql
    assert "kaisai_nen >= %s" in sql
    assert "05" in params
    assert "2020" in params


def test_select_entries_filters_empty_returns_base_set(mocker: MockerFixture) -> None:
    """filters が空のときINTERSECTなしのベース集合を返す."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(manager, filters=[])

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "INTERSECT" not in sql


# ChokyoFilter
def test_select_entries_chokyo_filter_includes_exists_clause(mocker: MockerFixture) -> None:
    """ChokyoFilter 指定時にEXISTSサブクエリがSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[
            ChokyoFilter(
                condition=[ChokyoThreshold(course="wood", metric="lap", furlong=1, max_value=115)]
            )
        ],
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "EXISTS" in sql
    assert "woodchip_chokyo" in sql


# HistoryFilter
def test_select_entries_history_filter_career_count(mocker: MockerFixture) -> None:
    """HistoryFilter(career_count) 指定時に相関サブクエリがSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[HistoryFilter(source=AttrSource(type="career_count"), cond=(0, 5))],
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "COUNT(*)" in sql
    assert "BETWEEN" in sql


# DBエラー
def test_select_entries_raises_on_db_error(mocker: MockerFixture) -> None:
    """DBエラーで例外が送出される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("DB接続失敗")

    with pytest.raises(QueryExecutionError, match="DB接続失敗"):
        select_entries(manager, filters=[])


# course_week 検証
def test_select_entries_raises_when_only_course_kubun_given(mocker: MockerFixture) -> None:
    """course_kubun のみ指定時にValueErrorが発生する."""
    manager = mocker.MagicMock()

    with pytest.raises(ValueError):
        select_entries(
            manager,
            filters=[],
            condition=RaceCondition(course_kubun="C"),
        )


# Entry の内容確認
def test_select_entries_entry_fields_are_mapped_correctly(mocker: MockerFixture) -> None:
    """DataFrameの各列がEntryフィールドに正しくマッピングされる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df(
        [
            {
                "ketto_toroku_bango": "2019100001",
                "race_code": "202101010101",
                "umaban": "05",
                "group_label": "キタサンブラック",
            },
            {
                "ketto_toroku_bango": "2020200002",
                "race_code": "202101010102",
                "umaban": "08",
                "group_label": "キタサンブラック",
            },
        ]
    )

    result = select_entries(
        manager,
        filters=[SubjectFilter(subject=Subject.SIRE, name="キタサンブラック")],
    )

    assert len(result) == 2
    assert result[0].umaban == "05"
    assert result[1].ketto_toroku_bango == "2020200002"
    assert result[0].group_label == "キタサンブラック"


# group_by history/fixed
def test_select_entries_group_by_history_includes_correlated_subquery(
    mocker: MockerFixture,
) -> None:
    """group_by=history で相関サブクエリが group_label 式としてSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        group_by=GroupBy(kind="history", source=AttrSource(type="career_count")),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "COUNT(*)" in sql
    assert "group_label" in sql
    assert "ketto_toroku_bango = u.ketto_toroku_bango" in sql


def test_select_entries_group_by_history_debut_venue_includes_keibajo(
    mocker: MockerFixture,
) -> None:
    """group_by=history(debut_venue) で keibajo_code 式がSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        group_by=GroupBy(kind="history", source=AttrSource(type="debut_venue")),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "keibajo_code" in sql
    assert "group_label" in sql


def test_select_entries_group_by_fixed_generates_case_when(mocker: MockerFixture) -> None:
    """group_by=fixed で CASE WHEN 式が group_label としてSQLに含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        group_by=GroupBy(
            kind="fixed",
            source=AttrSource(type="career_count"),
            rows={"初戦": (0, 0), "2〜5戦": (1, 4), "6戦以上": (5, 999)},
        ),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "CASE" in sql
    assert "WHEN" in sql
    assert "初戦" in params
    assert "2〜5戦" in params


def test_select_entries_group_by_history_sire_condition_finisher_includes_km2(
    mocker: MockerFixture,
) -> None:
    """group_by=history(sire_condition_finisher) で kyosoba_master2 JOIN が含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        group_by=GroupBy(
            kind="history",
            source=AttrSource(type="sire_condition_finisher", top_n=1),
        ),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "kyosoba_master2" in sql
    assert "ketto1_bamei" in sql


# course_week CTE
def test_select_entries_course_week_uses_cte_and_excludes_keibajo_from_where(
    mocker: MockerFixture,
) -> None:
    """course_kubun+week_in_course 指定時にCTEが生成され、keibajo_codeがWHEREから除外される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        condition=RaceCondition(keibajo_code="05", course_kubun="C", week_in_course=1),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "WITH RECURSIVE" in sql
    assert "cw_target" in sql
    assert "cw_target" in sql
    assert "05" in params
    assert "C" in params
    assert 1 in params


def test_select_entries_course_week_params_order(mocker: MockerFixture) -> None:
    """course_week + condition の params がCTE先行・WHERE条件後続の順になる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_entry_df()

    select_entries(
        manager,
        filters=[],
        condition=RaceCondition(
            keibajo_code="05",
            course_kubun="C",
            week_in_course=2,
            year_from="2022",
        ),
    )

    params = list(manager.fetch_dataframe.call_args[1]["params"])
    keibajo_idx = params.index("05")
    course_kubun_idx = params.index("C")
    year_idx = params.index("2022")
    assert keibajo_idx < course_kubun_idx < year_idx
