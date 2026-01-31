"""TableGettersクラスのマスタデータテーブル取得メソッドのテスト."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.getters import TableGetters

from .conftest import (
    VALID_BANUSHI_CODE,
    VALID_CHOKYOSHI_CODE,
    VALID_END_DATE,
    VALID_HANSHOKU_TOROKU_BANGO,
    VALID_KEIBAJO_CODE,
    VALID_KETTO_TOROKU_BANGO,
    VALID_KISHU_CODE,
    VALID_SEISANSHA_CODE,
    VALID_START_DATE,
    VALID_TRACK_CODE,
)

# 正常系 - get_kyosoba_master2


def test_get_kyosoba_master2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kyosoba_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("KYOSOBA_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_master2_with_ketto_toroku_bango(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_master2: ketto_toroku_bangoフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kyosoba_master2(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KYOSOBA_MASTER2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_master2_with_date_range(
    table_getters: TableGetters,
    mock_connection_manager: MagicMock,
) -> None:
    """get_kyosoba_master2: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_getters.get_kyosoba_master2(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM KYOSOBA_MASTER2 WHERE" in query
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_kishu_master


def test_get_kishu_master_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KISHU_CODE": [VALID_KISHU_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kishu_master()

    mock_table_accessor.get_table_data.assert_called_once_with("KISHU_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kishu_master_with_kishu_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_master: kishu_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KISHU_CODE": [VALID_KISHU_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kishu_master(kishu_code=VALID_KISHU_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KISHU_MASTER",
        {"KISHU_CODE": VALID_KISHU_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_chokyoshi_master


def test_get_chokyoshi_master_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_chokyoshi_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"CHOKYOSHI_CODE": [VALID_CHOKYOSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_chokyoshi_master()

    mock_table_accessor.get_table_data.assert_called_once_with("CHOKYOSHI_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_chokyoshi_master_with_chokyoshi_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_chokyoshi_master: chokyoshi_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"CHOKYOSHI_CODE": [VALID_CHOKYOSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_chokyoshi_master(chokyoshi_code=VALID_CHOKYOSHI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "CHOKYOSHI_MASTER",
        {"CHOKYOSHI_CODE": VALID_CHOKYOSHI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_seisansha_master2


def test_get_seisansha_master2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_seisansha_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"SEISANSHA_CODE": [VALID_SEISANSHA_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_seisansha_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("SEISANSHA_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_seisansha_master2_with_seisansha_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_seisansha_master2: seisansha_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"SEISANSHA_CODE": [VALID_SEISANSHA_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_seisansha_master2(seisansha_code=VALID_SEISANSHA_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SEISANSHA_MASTER2",
        {"SEISANSHA_CODE": VALID_SEISANSHA_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_banushi_master


def test_get_banushi_master_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_banushi_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_banushi_master()

    mock_table_accessor.get_table_data.assert_called_once_with("BANUSHI_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_banushi_master_with_banushi_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_banushi_master: banushi_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_banushi_master(banushi_code=VALID_BANUSHI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "BANUSHI_MASTER",
        {"BANUSHI_CODE": VALID_BANUSHI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_hanshokuba_master2


def test_get_hanshokuba_master2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanshokuba_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"HANSHOKU_TOROKU_BANGO": [VALID_HANSHOKU_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hanshokuba_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("HANSHOKUBA_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanshokuba_master2_with_hanshoku_toroku_bango(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanshokuba_master2: hanshoku_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"HANSHOKU_TOROKU_BANGO": [VALID_HANSHOKU_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hanshokuba_master2(hanshoku_toroku_bango=VALID_HANSHOKU_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HANSHOKUBA_MASTER2",
        {"HANSHOKU_TOROKU_BANGO": VALID_HANSHOKU_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_sanku_master2


def test_get_sanku_master2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_sanku_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_sanku_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("SANKU_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_sanku_master2_with_ketto_toroku_bango(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_sanku_master2: ketto_toroku_bangoフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_sanku_master2(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SANKU_MASTER2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_record_master


def test_get_record_master_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_record_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KEIBAJO_CODE": [VALID_KEIBAJO_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_record_master()

    mock_table_accessor.get_table_data.assert_called_once_with("RECORD_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_record_master_with_compound_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_record_master: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "KEIBAJO_CODE": [VALID_KEIBAJO_CODE],
            "KYORI": [2000],
            "TRACK_CODE": [VALID_TRACK_CODE],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_record_master(
        keibajo_code=VALID_KEIBAJO_CODE,
        kyori=2000,
        track_code=VALID_TRACK_CODE,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert filters["KEIBAJO_CODE"] == VALID_KEIBAJO_CODE
    assert filters["KYORI"] == 2000
    assert filters["TRACK_CODE"] == VALID_TRACK_CODE
    pd.testing.assert_frame_equal(result, expected_df)


# 準正常系 - 不正なコードによるバリデーションエラー


@pytest.mark.parametrize(
    "invalid_kishu_code",
    [
        "1234",  # 桁数不足
        "123456",  # 桁数超過
        "ABCDE",  # 数字でない
    ],
)
def test_get_kishu_master_with_invalid_kishu_code(
    table_getters: TableGetters,
    invalid_kishu_code: str,
) -> None:
    """get_kishu_master: 不正なkishu_codeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_kishu_master(kishu_code=invalid_kishu_code)


@pytest.mark.parametrize(
    "invalid_chokyoshi_code",
    [
        "1234",  # 桁数不足
        "123456",  # 桁数超過
        "ABCDE",  # 数字でない
    ],
)
def test_get_chokyoshi_master_with_invalid_chokyoshi_code(
    table_getters: TableGetters,
    invalid_chokyoshi_code: str,
) -> None:
    """get_chokyoshi_master: 不正なcodeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_chokyoshi_master(chokyoshi_code=invalid_chokyoshi_code)


@pytest.mark.parametrize(
    "invalid_seisansha_code",
    [
        "1234567",  # 桁数不足
        "123456789",  # 桁数超過
        "ABCDEFGH",  # 数字でない
    ],
)
def test_get_seisansha_master2_with_invalid_seisansha_code(
    table_getters: TableGetters,
    invalid_seisansha_code: str,
) -> None:
    """get_seisansha_master2: 不正なcodeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_seisansha_master2(seisansha_code=invalid_seisansha_code)


@pytest.mark.parametrize(
    "invalid_banushi_code",
    [
        "12345",  # 桁数不足
        "1234567",  # 桁数超過
    ],
)
def test_get_banushi_master_with_invalid_banushi_code(
    table_getters: TableGetters,
    invalid_banushi_code: str,
) -> None:
    """get_banushi_master: 不正なbanushi_codeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_banushi_master(banushi_code=invalid_banushi_code)
