"""analyze_entry_attr_chakudo の単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import AttrSource, EntryAttrDef, RaceCondition, analyze_entry_attr_chakudo
from mykeibadb.exceptions import QueryExecutionError


def _make_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DataFrameを生成する."""
    return pd.DataFrame(rows)


def _make_result_row(grp: str = "0勝") -> dict[str, object]:
    """標準の集計結果行を返す."""
    return {
        "grp": grp, "total": 100, "wins": 30,
        "second": 20, "third": 15, "chakugai": 35,
        "win_rate": 30.0, "fukusho_rate": 65.0,
        "tansho_kaishuu": 78.0, "fukusho_kaishuu": 85.0,
    }


# 正常系
def test_analyze_entry_attr_past_finish_count_returns_success(mocker: MockerFixture) -> None:
    """past_finish_count で success=True / ChakudoRow のリストが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    attr_def = EntryAttrDef(
        source=AttrSource(type="past_finish_count", top_n=1),
        rows={"0勝": (0, 0), "1勝以上": (1, 999)},
    )
    result = analyze_entry_attr_chakudo(manager, attr_def)

    assert result.success is True
    assert result.error is None
    assert len(result.rows) == 1
    assert result.rows[0].group == "0勝"
    assert result.rows[0].total == 100


def test_analyze_entry_attr_past_finish_count_sql_contains_subquery(mocker: MockerFixture) -> None:
    """past_finish_count 指定時に相関サブクエリが SQL に含まれ、過去レース限定条件がある."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    attr_def = EntryAttrDef(
        source=AttrSource(type="past_finish_count", top_n=3, grade_codes=["A"], kyori=2400),
        rows={"0勝": (0, 0), "1勝以上": (1, 999)},
    )
    analyze_entry_attr_chakudo(manager, attr_def)

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "SELECT COUNT(*)" in sql
    assert "kaisai_tsuki_nichi" in sql
    assert 3 in params  # top_n がパラメータでバインドされている


def test_analyze_entry_attr_career_count_sql_contains_subquery(mocker: MockerFixture) -> None:
    """career_count 指定時に相関サブクエリが SQL に含まれ、過去レース限定条件がある."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    attr_def = EntryAttrDef(
        source=AttrSource(type="career_count"),
        rows={"0戦": (0, 0), "1戦以上": (1, 999)},
    )
    analyze_entry_attr_chakudo(manager, attr_def)

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "SELECT COUNT(*)" in sql
    assert "kaisai_tsuki_nichi" in sql


def test_analyze_entry_attr_prev_race_name_sql_contains_subquery(mocker: MockerFixture) -> None:
    """prev_race_name 指定時にサブクエリが SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    attr_def = EntryAttrDef(
        source=AttrSource(type="prev_race_name"),
        rows={"有馬記念": "有馬記念"},
    )
    analyze_entry_attr_chakudo(manager, attr_def)

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "r2.race_name" in sql
    assert "kaisai_tsuki_nichi" in sql


def test_analyze_entry_attr_debut_venue_sql_contains_subquery(mocker: MockerFixture) -> None:
    """debut_venue 指定時にサブクエリが SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    attr_def = EntryAttrDef(
        source=AttrSource(type="debut_venue"),
        rows={"東京": "05"},
    )
    analyze_entry_attr_chakudo(manager, attr_def)

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "r2.keibajo_code" in sql


def test_analyze_entry_attr_jockey_continuity_sql(mocker: MockerFixture) -> None:
    """jockey_continuity 指定時に kishu_code サブクエリと継続ラベルが SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row("継続")])

    attr_def = EntryAttrDef(
        source=AttrSource(type="jockey_continuity"),
        rows={"継続": "継続", "乗り戻り": "乗り戻り", "テン乗り": "テン乗り"},
    )
    result = analyze_entry_attr_chakudo(manager, attr_def)

    assert result.success is True
    sql = manager.fetch_dataframe.call_args[0][0]
    assert "kishu_code" in sql
    assert "SELECT u2.kishu_code" in sql
    assert "LIMIT 1" in sql
    assert "継続" in sql
    assert "乗り戻り" in sql
    assert "テン乗り" in sql


def test_analyze_entry_attr_sire_condition_finisher_sql(mocker: MockerFixture) -> None:
    """sire_condition_finisher 指定時に kyosoba_master2 JOIN と condition が SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row("1")])

    attr_def = EntryAttrDef(
        source=AttrSource(
            type="sire_condition_finisher",
            top_n=1,
            condition=RaceCondition(kyori=2400),
        ),
        rows={"1": 1, "0": 0},
    )
    result = analyze_entry_attr_chakudo(manager, attr_def)

    assert result.success is True
    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "kyosoba_master2" in sql
    assert "ketto1_bamei" in sql
    assert "r2.kyori = %s" in sql
    assert 2400 in params


def test_analyze_entry_attr_sire_condition_finisher_no_condition(mocker: MockerFixture) -> None:
    """sire_condition_finisher で condition=None のとき集計が成功する."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row("0")])

    attr_def = EntryAttrDef(
        source=AttrSource(type="sire_condition_finisher", top_n=1),
        rows={"1": 1, "0": 0},
    )
    result = analyze_entry_attr_chakudo(manager, attr_def)

    assert result.success is True
    sql = manager.fetch_dataframe.call_args[0][0]
    assert "kyosoba_master2" in sql
    assert "kyori = %s" not in sql


def test_analyze_entry_attr_accepts_dict(mocker: MockerFixture) -> None:
    """dict形式で attr_def を渡せる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    result = analyze_entry_attr_chakudo(
        manager,
        {
            "source": {"type": "career_count"},
            "rows": {"0戦": [0, 0], "1戦以上": [1, 999]},
        },
    )
    assert result.success is True


def test_analyze_entry_attr_condition_params(mocker: MockerFixture) -> None:
    """RaceCondition のフィルタ引数が SQL パラメータとして渡される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_result_row()])

    attr_def = EntryAttrDef(
        source=AttrSource(
            type="past_finish_count", top_n=1,
            grade_codes=["A"], keibajo_code="05", kyori=2400,
        ),
        rows={"0勝": (0, 0)},
    )
    analyze_entry_attr_chakudo(
        manager, attr_def,
        condition=RaceCondition(keibajo_code="05", year_from="2020"),
    )

    params = manager.fetch_dataframe.call_args[1]["params"]
    assert ["A"] in params
    assert "05" in params
    assert 2400 in params
    assert "2020" in params


# 準正常系
def test_analyze_entry_attr_raises_on_unknown_type(mocker: MockerFixture) -> None:
    """未対応の source.type で ValueError が発生する."""
    manager = mocker.MagicMock()
    with pytest.raises(ValueError):
        analyze_entry_attr_chakudo(
            manager,
            EntryAttrDef(
                source=AttrSource(type="unknown_type"),
                rows={"x": (0, 1)},
            ),
        )


def test_analyze_entry_attr_returns_error_on_db_failure(mocker: MockerFixture) -> None:
    """DBエラーで success=False / error が設定される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("DB接続失敗")

    result = analyze_entry_attr_chakudo(
        manager,
        EntryAttrDef(
            source=AttrSource(type="past_finish_count"),
            rows={"0勝": (0, 0)},
        ),
    )
    assert result.success is False
    assert result.error is not None
    assert "DB接続失敗" in result.error
