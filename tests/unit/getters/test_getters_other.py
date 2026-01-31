"""TableGettersクラスのその他テーブル取得メソッドのテスト."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.getters import TableGetters

from .conftest import (
    VALID_BANUSHI_CODE,
    VALID_END_DATE,
    VALID_KAISAI_CODE,
    VALID_KEIBAJO_CODE,
    VALID_KETTO_TOROKU_BANGO,
    VALID_RACE_CODE,
    VALID_START_DATE,
    VALID_TRACEN_KUBUN,
    VALID_TRACK_CODE,
)

# 正常系 - 調教データテーブル


def test_get_hanro_chokyo_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanro_chokyo: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hanro_chokyo()

    mock_table_accessor.get_table_data.assert_called_once_with("HANRO_CHOKYO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanro_chokyo_with_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanro_chokyo: 複合フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO],
            "TRACEN_KUBUN": [VALID_TRACEN_KUBUN],
        }
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hanro_chokyo(
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
        tracen_kubun=VALID_TRACEN_KUBUN,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO
    assert filters["TRACEN_KUBUN"] == VALID_TRACEN_KUBUN


def test_get_woodchip_chokyo_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_woodchip_chokyo: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_woodchip_chokyo()

    mock_table_accessor.get_table_data.assert_called_once_with("WOODCHIP_CHOKYO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_woodchip_chokyo_with_date_range(
    table_getters: TableGetters,
    mock_connection_manager: MagicMock,
) -> None:
    """get_woodchip_chokyo: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_getters.get_woodchip_chokyo(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM WOODCHIP_CHOKYO WHERE" in query
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - 開催・コース情報テーブル


def test_get_kaisai_schedule_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kaisai_schedule: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kaisai_schedule()

    mock_table_accessor.get_table_data.assert_called_once_with("KAISAI_SCHEDULE", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kaisai_schedule_with_kaisai_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kaisai_schedule: kaisai_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kaisai_schedule(kaisai_code=VALID_KAISAI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KAISAI_SCHEDULE",
        {"KAISAI_CODE": VALID_KAISAI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_course_joho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KEIBAJO_CODE": [VALID_KEIBAJO_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_course_joho()

    mock_table_accessor.get_table_data.assert_called_once_with("COURSE_JOHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_course_joho_with_compound_filters(
    table_getters: TableGetters,
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

    result = table_getters.get_course_joho(
        keibajo_code=VALID_KEIBAJO_CODE,
        kyori=2000,
        track_code=VALID_TRACK_CODE,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert result is not None
    assert filters["KEIBAJO_CODE"] == VALID_KEIBAJO_CODE
    assert filters["KYORI"] == 2000
    assert filters["TRACK_CODE"] == VALID_TRACK_CODE


# 正常系 - 競走馬詳細情報テーブル


def test_get_kyosoba_torihiki_kakaku2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_torihiki_kakaku2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kyosoba_torihiki_kakaku2()

    mock_table_accessor.get_table_data.assert_called_once_with("KYOSOBA_TORIHIKI_KAKAKU2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_torihiki_kakaku2_with_ketto_toroku_bango(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_torihiki_kakaku2: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kyosoba_torihiki_kakaku2(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KYOSOBA_TORIHIKI_KAKAKU2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_bamei_imi_yurai_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bamei_imi_yurai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_bamei_imi_yurai()

    mock_table_accessor.get_table_data.assert_called_once_with("BAMEI_IMI_YURAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_keito_joho2_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_keito_joho2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KEITO_CODE": ["00001"]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_keito_joho2()

    mock_table_accessor.get_table_data.assert_called_once_with("KEITO_JOHO2", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - データマイニング予想テーブル


def test_get_data_mining_time_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_time: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_data_mining_time()

    mock_table_accessor.get_table_data.assert_called_once_with("DATA_MINING_TIME", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_data_mining_taisen_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_data_mining_taisen: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_data_mining_taisen()

    mock_table_accessor.get_table_data.assert_called_once_with("DATA_MINING_TAISEN", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - WIN5テーブル


def test_get_win5_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_win5: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_win5()

    mock_table_accessor.get_table_data.assert_called_once_with("WIN5", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_win5_haraimodoshi_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_win5_haraimodoshi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_win5_haraimodoshi()

    mock_table_accessor.get_table_data.assert_called_once_with("WIN5_HARAIMODOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - 速報テーブル


def test_get_kyosoba_jogai_joho_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_jogai_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kyosoba_jogai_joho()

    mock_table_accessor.get_table_data.assert_called_once_with("KYOSOBA_JOGAI_JOHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_bataiju_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bataiju: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_bataiju()

    mock_table_accessor.get_table_data.assert_called_once_with("BATAIJU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tenko_baba_jotai_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tenko_baba_jotai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KAISAI_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_tenko_baba_jotai()

    mock_table_accessor.get_table_data.assert_called_once_with("TENKO_BABA_JOTAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussotorikeshi_kyosojogai_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussotorikeshi_kyosojogai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shussotorikeshi_kyosojogai()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOTORIKESHI_KYOSOJOGAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kishu_henko_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_henko: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_kishu_henko()

    mock_table_accessor.get_table_data.assert_called_once_with("KISHU_HENKO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hassojikoku_henko_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hassojikoku_henko: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_hassojikoku_henko()

    mock_table_accessor.get_table_data.assert_called_once_with("HASSOJIKOKU_HENKO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_course_henko_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_henko: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_course_henko()

    mock_table_accessor.get_table_data.assert_called_once_with("COURSE_HENKO", None)
    pd.testing.assert_frame_equal(result, expected_df)


# 正常系 - その他


def test_get_shobufuku_without_filters(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shobufuku: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shobufuku()

    mock_table_accessor.get_table_data.assert_called_once_with("SHOBUFUKU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shobufuku_with_banushi_code(
    table_getters: TableGetters,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shobufuku: banushi_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = table_getters.get_shobufuku(banushi_code=VALID_BANUSHI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHOBUFUKU",
        {"BANUSHI_CODE": VALID_BANUSHI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# 準正常系 - 不正なコードによるバリデーションエラー


@pytest.mark.parametrize(
    "invalid_kaisai_code",
    [
        "12345678901234",  # 桁数不足
        "123456789012345678",  # 桁数超過
        "ABCDEFGHIJKLMNOP",  # 数字でない
    ],
)
def test_get_kaisai_schedule_with_invalid_kaisai_code(
    table_getters: TableGetters,
    invalid_kaisai_code: str,
) -> None:
    """get_kaisai_schedule: 不正なkaisai_codeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_kaisai_schedule(kaisai_code=invalid_kaisai_code)


@pytest.mark.parametrize(
    "invalid_keibajo_code",
    [
        "1",  # 桁数不足
        "123",  # 桁数超過
    ],
)
def test_get_course_joho_with_invalid_keibajo_code(
    table_getters: TableGetters,
    invalid_keibajo_code: str,
) -> None:
    """get_course_joho: 不正なkeibajo_codeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_course_joho(keibajo_code=invalid_keibajo_code)


@pytest.mark.parametrize(
    "invalid_track_code",
    [
        "1",  # 桁数不足
        "123",  # 桁数超過
        "AB",  # 数字でない
    ],
)
def test_get_course_joho_with_invalid_track_code(
    table_getters: TableGetters,
    invalid_track_code: str,
) -> None:
    """get_course_joho: 不正なtrack_codeでValidationErrorが発生することを確認."""
    with pytest.raises(ValidationError):
        table_getters.get_course_joho(track_code=invalid_track_code)
