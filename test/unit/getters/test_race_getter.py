"""RaceGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import RaceGetter

from .conftest import (
    VALID_END_DATE,
    VALID_KAISAI_CODE,
    VALID_KEIBAJO_CODE,
    VALID_KETTO_TOROKU_BANGO,
    VALID_RACE_CODE,
    VALID_RACE_CODES,
    VALID_START_DATE,
    VALID_TRACK_CODE,
)

# 正常系

# get_tokubetsu_torokuba


def test_get_tokubetsu_torokuba_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_tokubetsu_torokuba(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("TOKUBETSU_TOROKUBA", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_tokubetsu_torokuba(race_code=VALID_RACE_CODE, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TOKUBETSU_TOROKUBA",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_race_codes_list(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: 複数race_codeでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": VALID_RACE_CODES})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_tokubetsu_torokuba(race_code=VALID_RACE_CODES, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TOKUBETSU_TOROKUBA",
        {"RACE_CODE": VALID_RACE_CODES},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_date_range(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = race_getter.get_tokubetsu_torokuba(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "TOKUBETSU_TOROKUBA",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_tokubetsu_torokubagoto_joho


def test_get_tokubetsu_torokubagoto_joho_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokubagoto_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_tokubetsu_torokubagoto_joho(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TOKUBETSU_TOROKUBAGOTO_JOHO",
        None,
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokubagoto_joho_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokubagoto_joho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_tokubetsu_torokubagoto_joho(
        race_code=VALID_RACE_CODE,
        convert_codes=False,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    table_name = call_args[0][0]
    filters = call_args[0][1]

    assert table_name == "TOKUBETSU_TOROKUBAGOTO_JOHO"
    assert filters["RACE_CODE"] == VALID_RACE_CODE
    pd.testing.assert_frame_equal(result, expected_df)


# get_race_shosai


def test_get_race_shosai_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_race_shosai(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("RACE_SHOSAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_race_shosai_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_race_shosai(race_code=VALID_RACE_CODE, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "RACE_SHOSAI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_race_shosai_with_date_range(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = race_getter.get_race_shosai(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "RACE_SHOSAI",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_umagoto_race_joho


def test_get_umagoto_race_joho_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_umagoto_race_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_umagoto_race_joho(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("UMAGOTO_RACE_JOHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_umagoto_race_joho_with_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_umagoto_race_joho: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_umagoto_race_joho(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
        convert_codes=False,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None
    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO


def test_get_umagoto_race_joho_with_date_range(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_umagoto_race_joho: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = race_getter.get_umagoto_race_joho(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "UMAGOTO_RACE_JOHO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_haraimodoshi


def test_get_haraimodoshi_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_haraimodoshi(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("HARAIMODOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_haraimodoshi_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_haraimodoshi(race_code=VALID_RACE_CODE, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HARAIMODOSHI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_haraimodoshi_with_date_range(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = race_getter.get_haraimodoshi(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HARAIMODOSHI",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_kaisai_schedule


def test_get_kaisai_schedule_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kaisai_schedule: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_kaisai_schedule(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("KAISAI_SCHEDULE", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kaisai_schedule_with_kaisai_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kaisai_schedule: kaisai_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_kaisai_schedule(kaisai_code=VALID_KAISAI_CODE, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KAISAI_SCHEDULE",
        {"KAISAI_CODE": VALID_KAISAI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kaisai_schedule_with_date_range(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kaisai_schedule: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = race_getter.get_kaisai_schedule(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "KAISAI_SCHEDULE",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_course_joho


def test_get_course_joho_without_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KEIBAJO_CODE": [VALID_KEIBAJO_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_course_joho(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("COURSE_JOHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_course_joho_with_compound_filters(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_joho: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "KEIBAJO_CODE": [VALID_KEIBAJO_CODE],
            "KYORI": [2000],
            "TRACK_CODE": [VALID_TRACK_CODE],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_course_joho(
        keibajo_code=VALID_KEIBAJO_CODE,
        kyori=2000,
        track_code=VALID_TRACK_CODE,
        convert_codes=False,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    table_name = call_args[0][0]
    filters = call_args[0][1]

    assert table_name == "COURSE_JOHO"
    assert filters["KEIBAJO_CODE"] == VALID_KEIBAJO_CODE
    assert filters["KYORI"] == "2000"
    assert filters["TRACK_CODE"] == VALID_TRACK_CODE
    pd.testing.assert_frame_equal(result, expected_df)


# convert_codes=True のテスト


def test_get_race_shosai_convert_codes_true(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: convert_codes=Trueでコード変換列が正しく追加されることを確認."""
    source_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "keibajo_code": ["06"],
            "yobi_code": ["1"],
            "grade_code": ["A"],
            "kyoso_shubetsu_code": ["11"],
            "kyoso_kigo_code": ["000"],
            "juryo_shubetsu_code": ["1"],
            "kyoso_joken_code_2sai": ["005"],
            "kyoso_joken_code_3sai": ["010"],
            "kyoso_joken_code_4sai": ["000"],
            "kyoso_joken_code_5sai_ijo": ["000"],
            "kyoso_joken_code_saijakunen": ["000"],
            "track_code": ["11"],
            "tenko_code": ["1"],
            "shiba_babajotai_code": ["1"],
            "dirt_babajotai_code": ["4"],
        }
    )
    mock_table_accessor.get_table_data.return_value = source_df.copy()

    result = race_getter.get_race_shosai(race_code=VALID_RACE_CODE, convert_codes=True)

    # 変換列が追加されていることを確認
    expected_new_columns = [
        "keibajo",
        "yobi",
        "grade",
        "kyoso_shubetsu",
        "kyoso_kigo",
        "juryo_shubetsu",
        "kyoso_joken_2sai",
        "kyoso_joken_3sai",
        "kyoso_joken_4sai",
        "kyoso_joken_5sai_ijo",
        "kyoso_joken_saijakunen",
        "track",
        "tenko",
        "shiba_babajotai",
        "dirt_babajotai",
    ]
    for col in expected_new_columns:
        assert col in result.columns, f"変換列 '{col}' が結果に含まれていない"

    # 変換後の値が正しいことを確認
    row = result.iloc[0]
    assert row["keibajo"] == "中山"
    assert row["yobi"] == "土"
    assert row["grade"] == "GI"
    assert row["kyoso_shubetsu"] == "サラ系２歳"
    assert row["kyoso_kigo"] == ""
    assert row["juryo_shubetsu"] == "ハンデ"
    assert row["kyoso_joken_2sai"] == "５００万円以下"
    assert row["kyoso_joken_3sai"] == "１０００万円以下"
    assert row["kyoso_joken_4sai"] == ""
    assert row["kyoso_joken_5sai_ijo"] == ""
    assert row["kyoso_joken_saijakunen"] == ""
    assert row["track"] == "芝・左"
    assert row["tenko"] == "晴"
    assert row["shiba_babajotai"] == "良"
    assert row["dirt_babajotai"] == "不良"

    # 元のコード列も保持されていることを確認
    assert row["keibajo_code"] == "06"
    assert row["track_code"] == "11"


def test_get_umagoto_race_joho_convert_codes_true(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_umagoto_race_joho: convert_codes=Trueでコード変換列が正しく追加されることを確認."""
    source_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "keibajo_code": ["05"],
            "umakigo_code": ["04"],
            "seibetsu_code": ["1"],
            "hinshu_code": ["1"],
            "moshoku_code": ["03"],
            "tozai_shozoku_code": ["1"],
            "kishu_minarai_code": ["1"],
            "ijo_kubun_code": ["0"],
            "chakusa_code1": ["1__"],
            "chakusa_code2": ["_12"],
            "chakusa_code3": ["___"],
        }
    )
    mock_table_accessor.get_table_data.return_value = source_df.copy()

    result = race_getter.get_umagoto_race_joho(
        race_code=VALID_RACE_CODE,
        convert_codes=True,
    )

    # 変換列が追加されていることを確認
    expected_new_columns = [
        "keibajo",
        "umakigo",
        "seibetsu",
        "hinshu",
        "moshoku",
        "tozai_shozoku",
        "kishu_minarai",
        "ijo_kubun",
        "chakusa1",
        "chakusa2",
        "chakusa3",
    ]
    for col in expected_new_columns:
        assert col in result.columns, f"変換列 '{col}' が結果に含まれていない"

    # 変換後の値が正しいことを確認
    row = result.iloc[0]
    assert row["keibajo"] == "東京"
    assert row["umakigo"] == "(市)"
    assert row["seibetsu"] == "牡"
    assert row["hinshu"] == "サラブレッド"
    assert row["moshoku"] == "鹿毛"
    assert row["tozai_shozoku"] == "関東"
    assert row["kishu_minarai"] == "☆"
    assert row["ijo_kubun"] == ""
    assert row["chakusa1"] == "１馬身"
    assert row["chakusa2"] == "1/2馬身"
    assert row["chakusa3"] == ""

    # 元のコード列も保持されていることを確認
    assert row["keibajo_code"] == "05"
    assert row["seibetsu_code"] == "1"


def test_get_haraimodoshi_convert_codes_true(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: convert_codes=Trueでkeibajo列が正しく追加されることを確認."""
    source_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "keibajo_code": ["09"],
        }
    )
    mock_table_accessor.get_table_data.return_value = source_df.copy()

    result = race_getter.get_haraimodoshi(race_code=VALID_RACE_CODE, convert_codes=True)

    assert "keibajo" in result.columns
    assert result["keibajo"].iloc[0] == "阪神"
    # 元のコード列も保持されていることを確認
    assert result["keibajo_code"].iloc[0] == "09"


def test_get_race_shosai_convert_codes_true_empty_df(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: 空DataFrameの場合はconvert_codes=Trueでも変換列が追加されないことを確認."""
    empty_df = pd.DataFrame()
    mock_table_accessor.get_table_data.return_value = empty_df

    result = race_getter.get_race_shosai(race_code=VALID_RACE_CODE, convert_codes=True)

    assert result.empty
    assert "keibajo" not in result.columns
