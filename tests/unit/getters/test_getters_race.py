"""TableGettersクラスのレース関連テーブル取得メソッドのテスト."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.getters import TableGetters

from .conftest import (
    VALID_END_DATE,
    VALID_KETTO_TOROKU_BANGO,
    VALID_RACE_CODE,
    VALID_RACE_CODES,
    VALID_START_DATE,
)

# 正常系 - get_tokubetsu_torokuba


def test_get_tokubetsu_torokuba_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_tokubetsu_torokuba()

    mock_table_accessor.get_table_data.assert_called_once_with("TOKUBETSU_TOROKUBA", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_tokubetsu_torokuba(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TOKUBETSU_TOROKUBA",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_race_codes_list(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: 複数race_codeでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": VALID_RACE_CODES})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_tokubetsu_torokuba(race_code=VALID_RACE_CODES)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TOKUBETSU_TOROKUBA",
        {"RACE_CODE": VALID_RACE_CODES},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokuba_with_date_range(
    table_getters: TableGetters,
    mock_connection_manager: MagicMock,
) -> None:
    """get_tokubetsu_torokuba: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_getters.get_tokubetsu_torokuba(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM TOKUBETSU_TOROKUBA WHERE" in query
    assert "KAISAI_GAPPI >= %s" in query
    assert "KAISAI_GAPPI <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_tokubetsu_torokubagoto_joho


def test_get_tokubetsu_torokubagoto_joho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokubagoto_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_tokubetsu_torokubagoto_joho()

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TOKUBETSU_TOROKUBAGOTO_JOHO",
        None,
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tokubetsu_torokubagoto_joho_with_race_code_and_ketto(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tokubetsu_torokubagoto_joho: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": [VALID_RACE_CODE],
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_tokubetsu_torokubagoto_joho(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    table_name = call_args[0][0]
    filters = call_args[0][1]

    assert table_name == "TOKUBETSU_TOROKUBAGOTO_JOHO"
    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_race_shosai


def test_get_race_shosai_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_race_shosai()

    mock_table_accessor.get_table_data.assert_called_once_with("RACE_SHOSAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_race_shosai_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_race_shosai: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_race_shosai(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "RACE_SHOSAI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - get_umagoto_race_joho


def test_get_umagoto_race_joho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_umagoto_race_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_umagoto_race_joho()

    mock_table_accessor.get_table_data.assert_called_once_with("UMAGOTO_RACE_JOHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_umagoto_race_joho_with_filters(
    table_getters: TableGetters,
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

    result = table_getters.get_umagoto_race_joho(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None
    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO


# 正常系 - get_haraimodoshi


def test_get_haraimodoshi_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_haraimodoshi()

    mock_table_accessor.get_table_data.assert_called_once_with("HARAIMODOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_haraimodoshi_with_race_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_haraimodoshi: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_haraimodoshi(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HARAIMODOSHI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 準正常系 - 不正なレースコードによるバリデーションエラー


@pytest.mark.parametrize(
    "invalid_race_code",
    [
        "12345",  # 桁数不足
        "12345678901234567",  # 桁数超過
        "ABCD010306010101",  # 年部分が数字でない
        "202513030601010",  # 月が範囲外
        "2025013206010101",  # 日が範囲外
        "202501030601010A",  # レース番号に文字が含まれる
    ],
)
def test_get_tokubetsu_torokuba_with_invalid_race_code(
    table_getters: TableGetters,
    invalid_race_code: str,
) -> None:
    """get_tokubetsu_torokuba: 不正なrace_codeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_tokubetsu_torokuba(race_code=invalid_race_code)


@pytest.mark.parametrize(
    "invalid_ketto_toroku_bango",
    [
        "12345",  # 桁数不足
        "12345678901",  # 桁数超過
        "ABCDEFGHIJ",  # 数字でない
    ],
)
def test_get_tokubetsu_torokubagoto_joho_with_invalid_ketto(
    table_getters: TableGetters,
    invalid_ketto_toroku_bango: str,
) -> None:
    """get_tokubetsu_torokubagoto_joho: 不正なketto_toroku_bangoでエラー発生を確認."""
    with pytest.raises(ValidationError):
        table_getters.get_tokubetsu_torokubagoto_joho(ketto_toroku_bango=invalid_ketto_toroku_bango)
