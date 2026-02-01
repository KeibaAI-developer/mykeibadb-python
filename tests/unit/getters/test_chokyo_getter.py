"""ChokyoGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import ChokyoGetter

from .conftest import VALID_END_DATE, VALID_KETTO_TOROKU_BANGO, VALID_START_DATE, VALID_TRACEN_KUBUN

# 正常系

# get_hanro_chokyo


def test_get_hanro_chokyo_without_filters(
    chokyo_getter: ChokyoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanro_chokyo: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = chokyo_getter.get_hanro_chokyo()

    mock_table_accessor.get_table_data.assert_called_once_with("HANRO_CHOKYO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanro_chokyo_with_ketto_toroku_bango(
    chokyo_getter: ChokyoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanro_chokyo: ketto_toroku_bangoフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = chokyo_getter.get_hanro_chokyo(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HANRO_CHOKYO",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanro_chokyo_with_tracen_kubun(
    chokyo_getter: ChokyoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanro_chokyo: tracen_kubunフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"TRACEN_KUBUN": [VALID_TRACEN_KUBUN]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = chokyo_getter.get_hanro_chokyo(tracen_kubun=VALID_TRACEN_KUBUN)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HANRO_CHOKYO",
        {"TRACEN_KUBUN": VALID_TRACEN_KUBUN},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanro_chokyo_with_date_range(
    chokyo_getter: ChokyoGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_hanro_chokyo: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = chokyo_getter.get_hanro_chokyo(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM HANRO_CHOKYO WHERE" in query
    pd.testing.assert_frame_equal(result, expected_df)


# get_woodchip_chokyo


def test_get_woodchip_chokyo_without_filters(
    chokyo_getter: ChokyoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_woodchip_chokyo: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = chokyo_getter.get_woodchip_chokyo()

    mock_table_accessor.get_table_data.assert_called_once_with("WOODCHIP_CHOKYO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_woodchip_chokyo_with_ketto_toroku_bango(
    chokyo_getter: ChokyoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_woodchip_chokyo: ketto_toroku_bangoフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = chokyo_getter.get_woodchip_chokyo(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "WOODCHIP_CHOKYO",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_woodchip_chokyo_with_tracen_kubun(
    chokyo_getter: ChokyoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_woodchip_chokyo: tracen_kubunフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"TRACEN_KUBUN": [VALID_TRACEN_KUBUN]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = chokyo_getter.get_woodchip_chokyo(tracen_kubun=VALID_TRACEN_KUBUN)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "WOODCHIP_CHOKYO",
        {"TRACEN_KUBUN": VALID_TRACEN_KUBUN},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_woodchip_chokyo_with_date_range(
    chokyo_getter: ChokyoGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_woodchip_chokyo: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = chokyo_getter.get_woodchip_chokyo(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM WOODCHIP_CHOKYO WHERE" in query
    pd.testing.assert_frame_equal(result, expected_df)
