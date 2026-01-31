"""TableGettersクラスのオッズ関連テーブル取得メソッドのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import TableGetters

from .conftest import VALID_END_DATE, VALID_RACE_CODE, VALID_RACE_CODES, VALID_START_DATE

# 正常系 - get_odds1


def test_get_odds1_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_with_date_range(
    table_getters: TableGetters,
    mock_connection_manager: MagicMock,
) -> None:
    """get_odds1: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_getters.get_odds1(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM ODDS1 WHERE" in query
    assert "KAISAI_GAPPI >= %s" in query
    assert "KAISAI_GAPPI <= %s" in query
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_tansho


def test_get_odds1_tansho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_tansho()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_TANSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_tansho_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_tansho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_TANSHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_fukusho


def test_get_odds1_fukusho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_fukusho()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_FUKUSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_wakuren


def test_get_odds1_wakuren_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_wakuren()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_WAKUREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_jikeiretsu


def test_get_odds1_jikeiretsu_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_tansho_jikeiretsu


def test_get_odds1_tansho_jikeiretsu_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_tansho_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_TANSHO_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_fukusho_jikeiretsu


def test_get_odds1_fukusho_jikeiretsu_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_fukusho_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_FUKUSHO_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds1_wakuren_jikeiretsu


def test_get_odds1_wakuren_jikeiretsu_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds1_wakuren_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_WAKUREN_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds2_umaren


def test_get_odds2_umaren_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds2_umaren()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS2_UMAREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds2_umaren_jikeiretsu


def test_get_odds2_umaren_jikeiretsu_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds2_umaren_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS2_UMAREN_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds3_wide


def test_get_odds3_wide_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds3_wide: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds3_wide()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS3_WIDE", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds4_umatan


def test_get_odds4_umatan_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds4_umatan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds4_umatan()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS4_UMATAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds5_sanrenpuku


def test_get_odds5_sanrenpuku_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds5_sanrenpuku: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds5_sanrenpuku()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS5_SANRENPUKU", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_odds6_sanrentan


def test_get_odds6_sanrentan_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds6_sanrentan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds6_sanrentan()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS6_SANRENTAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds6_sanrentan_with_race_codes_list(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds6_sanrentan: 複数race_codeでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": VALID_RACE_CODES})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_odds6_sanrentan(race_code=VALID_RACE_CODES)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS6_SANRENTAN",
        {"RACE_CODE": VALID_RACE_CODES},
    )
    pd.testing.assert_frame_equal(result, expected_df)
