"""MiningGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import MiningGetter

from .conftest import VALID_END_DATE, VALID_RACE_CODE, VALID_START_DATE

# 正常系

# get_data_mining_time


def test_get_data_mining_time_without_filters(
    mining_getter: MiningGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_time: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = mining_getter.get_data_mining_time(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("DATA_MINING_TIME", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_data_mining_time_with_race_code(
    mining_getter: MiningGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_time: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = mining_getter.get_data_mining_time(race_code=VALID_RACE_CODE, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "DATA_MINING_TIME",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_data_mining_time_with_date_range(
    mining_getter: MiningGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_time: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = mining_getter.get_data_mining_time(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "DATA_MINING_TIME",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_data_mining_taisen


def test_get_data_mining_taisen_without_filters(
    mining_getter: MiningGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_taisen: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = mining_getter.get_data_mining_taisen(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("DATA_MINING_TAISEN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_data_mining_taisen_with_race_code(
    mining_getter: MiningGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_taisen: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = mining_getter.get_data_mining_taisen(race_code=VALID_RACE_CODE, convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "DATA_MINING_TAISEN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_data_mining_taisen_with_date_range(
    mining_getter: MiningGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_taisen: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = mining_getter.get_data_mining_taisen(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "DATA_MINING_TAISEN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)
