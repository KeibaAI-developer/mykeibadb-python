"""chokyo モジュールの単体テスト."""

import pandas as pd
from pytest_mock import MockerFixture

from mykeibadb.analytics import RaceCondition, analyze_chokyo_seiseki, get_uma_chokyo
from mykeibadb.exceptions import QueryExecutionError


def _make_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DataFrameを生成する."""
    return pd.DataFrame(rows)


def _make_info_row() -> dict[str, object]:
    """umagoto_race_joho + race_joho 結合行（馬情報）."""
    return {"ketto_toroku_bango": "2020100001", "race_date": "20230101"}


def _make_prev_race_row() -> dict[str, object]:
    """前走日付行."""
    return {"prev_race_date": "20221201"}


def _make_wood_row() -> dict[str, object]:
    """woodchip_chokyo テーブルの行."""
    return {
        "tracen_kubun": "1",
        "chokyo_nengappi": "20221220",
        "chokyo_jikoku": "0800",
        "time_gokei_6furlong": "0800",
        "time_gokei_5furlong": "0650",
        "time_gokei_4furlong": "0520",
        "laptime_1furlong": "115",
        "laptime_2furlong": "118",
        "laptime_3furlong": "125",
    }


def _make_hanro_row() -> dict[str, object]:
    """hanro_chokyo テーブルの行."""
    return {
        "tracen_kubun": "1",
        "chokyo_nengappi": "20221215",
        "chokyo_jikoku": "0730",
        "time_gokei_4furlong": "0560",
        "lap_time_1furlong": "120",
        "lap_time_2furlong": "125",
        "lap_time_3furlong": "130",
        "lap_time_4furlong": "145",
    }


def _make_seiseki_row(grp: str = "坂路+ウッド") -> dict[str, object]:
    """analyze_chokyo_seiseki の集計結果行."""
    return {
        "grp": grp, "total": 100, "wins": 30,
        "second": 20, "third": 15, "chakugai": 35,
        "win_rate": 30.0, "fukusho_rate": 65.0,
        "tansho_kaishuu": 78.0, "fukusho_kaishuu": 85.0,
    }


# 正常系
def test_get_uma_chokyo_returns_success(mocker: MockerFixture) -> None:
    """レースコードと馬番を指定して調教データが取得できる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_df([_make_info_row()]),
        _make_df([_make_prev_race_row()]),
        _make_df([_make_wood_row()]),
        _make_df([_make_hanro_row()]),
    ]

    result = get_uma_chokyo(manager, "2023010105010101", 5)

    assert result["success"] is True
    assert result["ketto_toroku_bango"] == "2020100001"
    assert len(result["wood_records"]) == 1
    assert len(result["hanro_records"]) == 1
    assert result["wood_records"][0]["course_type"] == "ウッドチップ"
    assert result["hanro_records"][0]["course_type"] == "坂路"


def test_get_uma_chokyo_tracen_label(mocker: MockerFixture) -> None:
    """tracen_kubun='0'を美浦、'1'を栗東と変換する."""
    manager = mocker.MagicMock()
    wood_row = _make_wood_row()
    wood_row["tracen_kubun"] = "0"
    hanro_row = _make_hanro_row()
    hanro_row["tracen_kubun"] = "1"
    manager.fetch_dataframe.side_effect = [
        _make_df([_make_info_row()]),
        _make_df([_make_prev_race_row()]),
        _make_df([wood_row]),
        _make_df([hanro_row]),
    ]

    result = get_uma_chokyo(manager, "2023010105010101", 1)

    assert result["wood_records"][0]["tracen"] == "美浦"
    assert result["hanro_records"][0]["tracen"] == "栗東"


def test_get_uma_chokyo_horse_not_found(mocker: MockerFixture) -> None:
    """馬番が見つからない場合は空のレコードを返す."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([])

    result = get_uma_chokyo(manager, "2023010105010101", 99)

    assert result["success"] is True
    assert result["wood_records"] == []
    assert result["hanro_records"] == []


def test_get_uma_chokyo_umaban_zero_padded(mocker: MockerFixture) -> None:
    """馬番が2桁ゼロパディングでSQLに渡される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([])

    get_uma_chokyo(manager, "2023010105010101", 5)

    first_call_params = manager.fetch_dataframe.call_args_list[0][1]["params"]
    assert "05" in first_call_params


def test_get_uma_chokyo_prev_race_date_filters_chokyo(mocker: MockerFixture) -> None:
    """前走が存在する場合、前走日付より後の調教データに絞り込まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_df([_make_info_row()]),
        _make_df([_make_prev_race_row()]),
        _make_df([_make_wood_row()]),
        _make_df([_make_hanro_row()]),
    ]

    get_uma_chokyo(manager, "2023010105010101", 1)

    wood_sql = manager.fetch_dataframe.call_args_list[2][0][0]
    assert "chokyo_nengappi > %s" in wood_sql


def test_get_uma_chokyo_no_prev_race_returns_all_chokyo(mocker: MockerFixture) -> None:
    """前走が存在しない場合、レース当日より前の全調教データを返す."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = [
        _make_df([_make_info_row()]),
        _make_df([]),  # 前走なし
        _make_df([_make_wood_row()]),
        _make_df([_make_hanro_row()]),
    ]

    result = get_uma_chokyo(manager, "2023010105010101", 1)

    wood_sql = manager.fetch_dataframe.call_args_list[2][0][0]
    assert result["success"] is True
    assert "chokyo_nengappi > %s" not in wood_sql


def test_analyze_chokyo_seiseki_returns_success(mocker: MockerFixture) -> None:
    """正常系: success=True と rows リストが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([
        _make_seiseki_row("坂路+ウッド"),
        _make_seiseki_row("ウッドのみ"),
        _make_seiseki_row("坂路のみ"),
        _make_seiseki_row("なし"),
    ])

    result = analyze_chokyo_seiseki(manager)

    assert result["success"] is True
    assert len(result["rows"]) == 4
    assert result["rows"][0]["group"] == "坂路+ウッド"


def test_analyze_chokyo_seiseki_sql_contains_chokyo_subquery(mocker: MockerFixture) -> None:
    """調教タイプ判定のサブクエリが SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_seiseki_row()])

    analyze_chokyo_seiseki(manager)

    sql = manager.fetch_dataframe.call_args[0][0]
    assert "woodchip_chokyo" in sql
    assert "hanro_chokyo" in sql
    assert "has_wood" in sql
    assert "has_hanro" in sql


def test_analyze_chokyo_seiseki_kyoso_joken_filter(mocker: MockerFixture) -> None:
    """kyoso_joken_codes 指定時に競走条件コードフィルタが SQL に含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_seiseki_row()])

    analyze_chokyo_seiseki(
        manager,
        condition=RaceCondition(kyoso_joken_codes=["701", "703"]),
    )

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "GREATEST" in sql
    assert "kyoso_joken_code" in sql
    assert [701, 703] in params


def test_analyze_chokyo_seiseki_condition_params(mocker: MockerFixture) -> None:
    """RaceCondition のフィルタ引数が SQL パラメータとして渡される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([_make_seiseki_row()])

    analyze_chokyo_seiseki(
        manager,
        condition=RaceCondition(
            keibajo_code="05",
            kyori=1600,
            year_from="2020",
            year_to="2023",
            kyoso_joken_codes=["701"],
        ),
    )

    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "05" in params
    assert 1600 in params
    assert "2020" in params
    assert "2023" in params
    assert [701] in params


# 準正常系
def test_get_uma_chokyo_returns_error_on_db_failure(mocker: MockerFixture) -> None:
    """DBエラーで success=False / error が設定される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("接続失敗")

    result = get_uma_chokyo(manager, "2023010105010101", 1)

    assert result["success"] is False
    assert result.get("error") is not None
    assert "接続失敗" in result["error"]


def test_analyze_chokyo_seiseki_returns_error_on_db_failure(mocker: MockerFixture) -> None:
    """DBエラーで success=False / error が設定される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("タイムアウト")

    result = analyze_chokyo_seiseki(manager)

    assert result["success"] is False
    assert result.get("error") is not None
    assert "タイムアウト" in result["error"]
