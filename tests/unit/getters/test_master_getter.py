"""MasterGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import MasterGetter

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

# 正常系

# get_kyosoba_master2


def test_get_kyosoba_master2_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_kyosoba_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("KYOSOBA_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_master2_with_ketto_toroku_bango(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_master2: ketto_toroku_bangoフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_kyosoba_master2(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KYOSOBA_MASTER2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_master2_with_date_range(
    master_getter: MasterGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_kyosoba_master2: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = master_getter.get_kyosoba_master2(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]

    assert "SELECT * FROM KYOSOBA_MASTER2 WHERE" in query
    pd.testing.assert_frame_equal(result, expected_df)


# get_kishu_master


def test_get_kishu_master_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KISHU_CODE": [VALID_KISHU_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_kishu_master()

    mock_table_accessor.get_table_data.assert_called_once_with("KISHU_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kishu_master_with_kishu_code(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_master: kishu_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KISHU_CODE": [VALID_KISHU_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_kishu_master(kishu_code=VALID_KISHU_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KISHU_MASTER",
        {"KISHU_CODE": VALID_KISHU_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kishu_master_with_date_range(
    master_getter: MasterGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_kishu_master: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KISHU_CODE": [VALID_KISHU_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = master_getter.get_kishu_master(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM KISHU_MASTER WHERE" in query
    assert "MENKYO_KOFU_NENGAPPI >= %s" in query
    assert "MENKYO_KOFU_NENGAPPI <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_chokyoshi_master


def test_get_chokyoshi_master_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_chokyoshi_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"CHOKYOSHI_CODE": [VALID_CHOKYOSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_chokyoshi_master()

    mock_table_accessor.get_table_data.assert_called_once_with("CHOKYOSHI_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_chokyoshi_master_with_chokyoshi_code(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_chokyoshi_master: chokyoshi_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"CHOKYOSHI_CODE": [VALID_CHOKYOSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_chokyoshi_master(chokyoshi_code=VALID_CHOKYOSHI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "CHOKYOSHI_MASTER",
        {"CHOKYOSHI_CODE": VALID_CHOKYOSHI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_chokyoshi_master_with_date_range(
    master_getter: MasterGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_chokyoshi_master: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"CHOKYOSHI_CODE": [VALID_CHOKYOSHI_CODE]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = master_getter.get_chokyoshi_master(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM CHOKYOSHI_MASTER WHERE" in query
    assert "MENKYO_KOFU_NENGAPPI >= %s" in query
    assert "MENKYO_KOFU_NENGAPPI <= %s" in query
    assert "20250101" in params
    assert "20250131" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_seisansha_master2


def test_get_seisansha_master2_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_seisansha_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"SEISANSHA_CODE": [VALID_SEISANSHA_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_seisansha_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("SEISANSHA_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_seisansha_master2_with_seisansha_code(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_seisansha_master2: seisansha_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"SEISANSHA_CODE": [VALID_SEISANSHA_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_seisansha_master2(seisansha_code=VALID_SEISANSHA_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SEISANSHA_MASTER2",
        {"SEISANSHA_CODE": VALID_SEISANSHA_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_banushi_master


def test_get_banushi_master_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_banushi_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_banushi_master()

    mock_table_accessor.get_table_data.assert_called_once_with("BANUSHI_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_banushi_master_with_banushi_code(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_banushi_master: banushi_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_banushi_master(banushi_code=VALID_BANUSHI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "BANUSHI_MASTER",
        {"BANUSHI_CODE": VALID_BANUSHI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hanshokuba_master2


def test_get_hanshokuba_master2_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanshokuba_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"HANSHOKU_TOROKU_BANGO": [VALID_HANSHOKU_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_hanshokuba_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("HANSHOKUBA_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanshokuba_master2_with_hanshoku_toroku_bango(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hanshokuba_master2: hanshoku_toroku_bangoでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"HANSHOKU_TOROKU_BANGO": [VALID_HANSHOKU_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_hanshokuba_master2(hanshoku_toroku_bango=VALID_HANSHOKU_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HANSHOKUBA_MASTER2",
        {"HANSHOKU_TOROKU_BANGO": VALID_HANSHOKU_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hanshokuba_master2_with_date_range(
    master_getter: MasterGetter,
    mock_connection_manager: MagicMock,
) -> None:
    """get_hanshokuba_master2: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"HANSHOKU_TOROKU_BANGO": [VALID_HANSHOKU_TOROKU_BANGO]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = master_getter.get_hanshokuba_master2(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM HANSHOKUBA_MASTER2 WHERE" in query
    assert "SEINEN >= %s" in query
    assert "SEINEN <= %s" in query
    assert "2025" in params
    assert "2025" in params
    pd.testing.assert_frame_equal(result, expected_df)


# get_sanku_master2


def test_get_sanku_master2_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_sanku_master2: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_sanku_master2()

    mock_table_accessor.get_table_data.assert_called_once_with("SANKU_MASTER2", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_sanku_master2_with_ketto_toroku_bango(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_sanku_master2: ketto_toroku_bangoフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KETTO_TOROKU_BANGO": [VALID_KETTO_TOROKU_BANGO]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_sanku_master2(ketto_toroku_bango=VALID_KETTO_TOROKU_BANGO)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SANKU_MASTER2",
        {"KETTO_TOROKU_BANGO": VALID_KETTO_TOROKU_BANGO},
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_record_master


def test_get_record_master_without_filters(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_record_master: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"KEIBAJO_CODE": [VALID_KEIBAJO_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_record_master()

    mock_table_accessor.get_table_data.assert_called_once_with("RECORD_MASTER", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_record_master_with_keibajo_code(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_record_master: keibajo_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KEIBAJO_CODE": [VALID_KEIBAJO_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_record_master(keibajo_code=VALID_KEIBAJO_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "RECORD_MASTER",
        {"KEIBAJO_CODE": VALID_KEIBAJO_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_record_master_with_kyori(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_record_master: kyoriフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"KEIBAJO_CODE": [VALID_KEIBAJO_CODE], "KYORI": [2000]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_record_master(kyori=2000)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "RECORD_MASTER",
        {"KYORI": 2000},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_record_master_with_track_code(
    master_getter: MasterGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_record_master: track_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {"KEIBAJO_CODE": [VALID_KEIBAJO_CODE], "TRACK_CODE": [VALID_TRACK_CODE]}
    )
    mock_table_accessor.get_table_data.return_value = expected_df

    result = master_getter.get_record_master(track_code=VALID_TRACK_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "RECORD_MASTER",
        {"TRACK_CODE": VALID_TRACK_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)
