"""Win5Getterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import Win5Getter

from .conftest import VALID_END_DATE, VALID_KAISAI_CODE, VALID_START_DATE

# 正常系

# get_win5


def test_get_win5_without_filters(
    win5_getter: Win5Getter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_win5: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = win5_getter.get_win5(convert_codes=False)

    mock_table_accessor.get_table_data.assert_called_once_with("WIN5", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_win5_with_date_range(
    win5_getter: Win5Getter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_win5: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = win5_getter.get_win5(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
        convert_codes=False,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "WIN5",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_win5_haraimodoshi


def test_get_win5_haraimodoshi_without_filters(
    win5_getter: Win5Getter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_win5_haraimodoshi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = win5_getter.get_win5_haraimodoshi()

    mock_table_accessor.get_table_data.assert_called_once_with("WIN5_HARAIMODOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_win5_haraimodoshi_with_date_range(
    win5_getter: Win5Getter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_win5_haraimodoshi: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = win5_getter.get_win5_haraimodoshi(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "WIN5_HARAIMODOSHI",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)
