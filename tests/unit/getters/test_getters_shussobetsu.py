"""TableGettersクラスの出走別データテーブル取得メソッドのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import TableGetters

from .conftest import VALID_END_DATE, VALID_KETTO_TOROKU_BANGO, VALID_RACE_CODE, VALID_START_DATE

# 正常系 - get_shussobetsu_baba


def test_get_shussobetsu_baba_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_baba: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_baba()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_BABA", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_baba_with_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_baba: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_baba(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_baba_with_date_range(
    table_getters: TableGetters,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_baba: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_getters.get_shussobetsu_baba(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM SHUSSOBETSU_BABA WHERE" in query
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_shussobetsu_kyori


def test_get_shussobetsu_kyori_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kyori: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_kyori()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_KYORI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kyori_with_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kyori: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_kyori(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None

    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO


# 正常系 - get_shussobetsu_keibajo


def test_get_shussobetsu_keibajo_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_keibajo: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_keibajo()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_KEIBAJO", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_shussobetsu_kishu


def test_get_shussobetsu_kishu_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kishu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_kishu()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_KISHU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kishu_with_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kishu: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_kishu(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None
    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO


# 正常系 - get_shussobetsu_chokyoshi


def test_get_shussobetsu_chokyoshi_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_chokyoshi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_chokyoshi()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_CHOKYOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_shussobetsu_banushi


def test_get_shussobetsu_banushi_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_banushi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_banushi()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_BANUSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_shussobetsu_seisansha2


def test_get_shussobetsu_seisansha2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_seisansha2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_seisansha2()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_SEISANSHA2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_seisansha2_with_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_seisansha2: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussobetsu_seisansha2(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None

    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO
