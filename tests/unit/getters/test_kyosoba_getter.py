"""KyosobaGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import KyosobaGetter

from .conftest import VALID_KEITO_ID, VALID_KETTO_TOROKU_BANGO

# 正常系

# get_kyosoba_torihiki_kakaku2


def test_get_kyosoba_torihiki_kakaku2_without_filters(
    kyosoba_getter: KyosobaGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_torihiki_kakaku2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = kyosoba_getter.get_kyosoba_torihiki_kakaku2()

    mock_table_accessor.get_table_data.assert_called_once_with("KYOSOBA_TORIHIKI_KAKAKU2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_torihiki_kakaku2_with_ketto_toroku_bango(
    kyosoba_getter: KyosobaGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_torihiki_kakaku2: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = kyosoba_getter.get_kyosoba_torihiki_kakaku2(
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO
    )

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KYOSOBA_TORIHIKI_KAKAKU2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_bamei_imi_yurai


def test_get_bamei_imi_yurai_without_filters(
    kyosoba_getter: KyosobaGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bamei_imi_yurai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = kyosoba_getter.get_bamei_imi_yurai()

    mock_table_accessor.get_table_data.assert_called_once_with("BAMEI_IMI_YURAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_bamei_imi_yurai_with_ketto_toroku_bango(
    kyosoba_getter: KyosobaGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bamei_imi_yurai: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = kyosoba_getter.get_bamei_imi_yurai(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "BAMEI_IMI_YURAI",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_keito_joho2


def test_get_keito_joho2_without_filters(
    kyosoba_getter: KyosobaGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_keito_joho2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KEITO_CODE": ["00001"]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = kyosoba_getter.get_keito_joho2()

    mock_table_accessor.get_table_data.assert_called_once_with("KEITO_JOHO2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_keito_joho2_with_keito_id(
    kyosoba_getter: KyosobaGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_keito_joho2: keito_idでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KEITO_ID": [VALID_KEITO_ID]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = kyosoba_getter.get_keito_joho2(keito_id=VALID_KEITO_ID)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KEITO_JOHO2",
        {"KEITO_ID": VALID_KEITO_ID},
    )
    pd.testing.assert_frame_equal(result, expected_df)
