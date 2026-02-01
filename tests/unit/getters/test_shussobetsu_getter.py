"""ShussobetsuGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import ShussobetsuGetter

from .conftest import VALID_END_DATE, VALID_KETTO_TOROKU_BANGO, VALID_RACE_CODE, VALID_START_DATE

# 正常系

# get_shussobetsu_baba


def test_get_shussobetsu_baba_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_baba: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_baba()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_BABA", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_baba_with_filters(
    shussobetsu_getter: ShussobetsuGetter,
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

    result = shussobetsu_getter.get_shussobetsu_baba(
        race_code=VALID_RACE_CODE,
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO,
    )

    call_args = mock_table_accessor.get_table_data.call_args
    filters = call_args[0][1]

    assert filters["RACE_CODE"] == VALID_RACE_CODE
    assert filters["KETTO_TOROKU_BANGO"] == VALID_KETTO_TOROKU_BANGO
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_baba_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_baba: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_baba(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_BABA WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussobetsu_kyori


def test_get_shussobetsu_kyori_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kyori: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kyori()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_KYORI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kyori_with_race_code(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kyori: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kyori(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_KYORI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kyori_with_ketto_toroku_bango(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kyori: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kyori(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_KYORI",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kyori_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_kyori: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kyori(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_KYORI WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussobetsu_keibajo


def test_get_shussobetsu_keibajo_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_keibajo: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_keibajo()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_KEIBAJO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_keibajo_with_race_code(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_keibajo: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_keibajo(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_KEIBAJO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_keibajo_with_ketto_toroku_bango(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_keibajo: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_keibajo(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_KEIBAJO",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_keibajo_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_keibajo: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_keibajo(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_KEIBAJO WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussobetsu_kishu


def test_get_shussobetsu_kishu_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kishu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kishu()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_KISHU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kishu_with_race_code(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kishu: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kishu(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_KISHU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kishu_with_ketto_toroku_bango(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_kishu: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kishu(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_KISHU",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_kishu_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_kishu: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_kishu(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_KISHU WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussobetsu_chokyoshi


def test_get_shussobetsu_chokyoshi_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_chokyoshi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_chokyoshi()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_CHOKYOSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_chokyoshi_with_race_code(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_chokyoshi: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_chokyoshi(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_CHOKYOSHI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_chokyoshi_with_ketto_toroku_bango(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_chokyoshi: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_chokyoshi(
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO
    )

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_CHOKYOSHI",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_chokyoshi_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_chokyoshi: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_chokyoshi(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_CHOKYOSHI WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussobetsu_banushi


def test_get_shussobetsu_banushi_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_banushi: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_banushi()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_BANUSHI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_banushi_with_race_code(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_banushi: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_banushi(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_BANUSHI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_banushi_with_ketto_toroku_bango(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_banushi: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_banushi(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_BANUSHI",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_banushi_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_banushi: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_banushi(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_BANUSHI WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussobetsu_seisansha2


def test_get_shussobetsu_seisansha2_without_filters(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_seisansha2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_seisansha2()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOBETSU_SEISANSHA2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_seisansha2_with_race_code(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_seisansha2: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_seisansha2(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_SEISANSHA2",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_seisansha2_with_ketto_toroku_bango(
    shussobetsu_getter: ShussobetsuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussobetsu_seisansha2: ketto_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_seisansha2(
        ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO
    )

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOBETSU_SEISANSHA2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussobetsu_seisansha2_with_date_range(
    shussobetsu_getter: ShussobetsuGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_shussobetsu_seisansha2: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = shussobetsu_getter.get_shussobetsu_seisansha2(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM SHUSSOBETSU_SEISANSHA2 WHERE" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) >= %s" in query
    assert "CONCAT(KAISAI_NEN, KAISAI_GAPPI) <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)
