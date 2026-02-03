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

    result = race_getter.get_tokubetsu_torokuba()

    mock_table_accessor.get_table_data.assert_called_once_with("TOKUBETSU_TOROKUBA", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_tokubetsu_torokuba(race_code=VALID_RACE_CODE)

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

    result = race_getter.get_tokubetsu_torokuba(race_code=VALID_RACE_CODES)

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

    result = race_getter.get_tokubetsu_torokubagoto_joho()

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

    result = race_getter.get_race_shosai()

    mock_table_accessor.get_table_data.assert_called_once_with("RACE_SHOSAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_race_shosai_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_race_shosai(race_code=VALID_RACE_CODE)

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

    result = race_getter.get_umagoto_race_joho()

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

    result = race_getter.get_haraimodoshi()

    mock_table_accessor.get_table_data.assert_called_once_with("HARAIMODOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_haraimodoshi_with_race_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_haraimodoshi(race_code=VALID_RACE_CODE)

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

    result = race_getter.get_kaisai_schedule()

    mock_table_accessor.get_table_data.assert_called_once_with("KAISAI_SCHEDULE", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kaisai_schedule_with_kaisai_code(
    race_getter: RaceGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kaisai_schedule: kaisai_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = race_getter.get_kaisai_schedule(kaisai_code=VALID_KAISAI_CODE)

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

    result = race_getter.get_course_joho()

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
    )

    call_args = mock_table_accessor.get_table_data.call_args
    table_name = call_args[0][0]
    filters = call_args[0][1]

    assert table_name == "COURSE_JOHO"
    assert filters["KEIBAJO_CODE"] == VALID_KEIBAJO_CODE
    assert filters["KYORI"] == "2000"
    assert filters["TRACK_CODE"] == VALID_TRACK_CODE
    pd.testing.assert_frame_equal(result, expected_df)
