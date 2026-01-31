"""TableGettersクラスの票数関連テーブル取得メソッドのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import TableGetters

from .conftest import VALID_END_DATE, VALID_RACE_CODE, VALID_RACE_CODES, VALID_START_DATE

# 正常系 - get_hyosu1


def test_get_hyosu1_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_with_date_range(
    table_getters: TableGetters,
    mock_connection_manager: MagicMock,
) -> None:
    """get_hyosu1: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_getters.get_hyosu1(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM HYOSU1 WHERE" in query
    assert "KAISAI_GAPPI >= %s" in query
    assert "KAISAI_GAPPI <= %s" in query
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_tansho


def test_get_hyosu1_tansho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_tansho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_tansho()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_TANSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_tansho_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_tansho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_tansho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_TANSHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_fukusho


def test_get_hyosu1_fukusho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_fukusho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_fukusho()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_FUKUSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_wakuren


def test_get_hyosu1_wakuren_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wakuren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_wakuren()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_WAKUREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_umaren


def test_get_hyosu1_umaren_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umaren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_umaren()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_UMAREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_wide


def test_get_hyosu1_wide_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wide: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_wide()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_WIDE", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_umatan


def test_get_hyosu1_umatan_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umatan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_umatan()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_UMATAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu1_sanrenpuku


def test_get_hyosu1_sanrenpuku_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_sanrenpuku: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu1_sanrenpuku()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_SANRENPUKU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu6


def test_get_hyosu6_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu6()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU6", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu6_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu6(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU6",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hyosu6_sanrentan


def test_get_hyosu6_sanrentan_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6_sanrentan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu6_sanrentan()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU6_SANRENTAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu6_sanrentan_with_race_codes_list(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6_sanrentan: 複数race_codeでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": VALID_RACE_CODES})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hyosu6_sanrentan(race_code=VALID_RACE_CODES)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU6_SANRENTAN",
        {"RACE_CODE": VALID_RACE_CODES},
    )
    pd.testing.assert_frame_equal(result, expected_df)
