"""TableAccessorクラスの単体テスト."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from mykeibadb.exceptions import InvalidFilterError, TableNotFoundError
from mykeibadb.tables import SUPPORTED_TABLES, TableAccessor


@pytest.fixture
def mock_connection_manager() -> MagicMock:
    """モック化されたConnectionManagerを生成するfixture."""
    mock_cm = MagicMock()
    mock_cm.fetch_dataframe.return_value = pd.DataFrame()
    return mock_cm


@pytest.fixture
def table_accessor(mock_connection_manager: MagicMock) -> TableAccessor:
    """TableAccessorインスタンスを生成するfixture."""
    return TableAccessor(mock_connection_manager)


# 正常系


def test_get_table_data_without_filters(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """フィルタなしでテーブルデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": ["202509030411"]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data("RACE_SHOSAI")

    mock_connection_manager.fetch_dataframe.assert_called_once_with(
        "SELECT * FROM race_shosai",
        None,
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_table_data_with_single_value_filter(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """単一値フィルタでテーブルデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": ["202509030411"]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": "202509030411"},
    )

    mock_connection_manager.fetch_dataframe.assert_called_once_with(
        "SELECT * FROM race_shosai WHERE TRIM(race_code) = %s",
        ("202509030411",),
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_table_data_with_int_filter(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """整数型フィルタでテーブルデータを取得できることを確認."""
    expected_df = pd.DataFrame({"UMABAN": [1]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={"UMABAN": 1},
    )

    mock_connection_manager.fetch_dataframe.assert_called_once_with(
        "SELECT * FROM umagoto_race_joho WHERE TRIM(umaban) = %s",
        (1,),
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_table_data_with_list_filter(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """リスト値フィルタ（IN句）でテーブルデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": ["202509030411", "202509030412"]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": ["202509030411", "202509030412"]},
    )

    mock_connection_manager.fetch_dataframe.assert_called_once_with(
        "SELECT * FROM race_shosai WHERE TRIM(race_code) IN (%s, %s)",
        ("202509030411", "202509030412"),
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_table_data_with_compound_filters(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """複合フィルタでテーブルデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": ["202509030411"], "UMABAN": [1]})
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={"RACE_CODE": "202509030411", "UMABAN": 1},
    )

    # フィルタの順序は辞書の順序に依存
    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM umagoto_race_joho WHERE" in query
    assert "TRIM(race_code) = %s" in query
    assert "TRIM(umaban) = %s" in query
    assert " AND " in query
    assert "202509030411" in params
    assert 1 in params
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_table_data_with_mixed_filter_types(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """単一値とリスト値を組み合わせたフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame(
        {
            "RACE_CODE": ["202509030411", "202509030411"],
            "UMABAN": [1, 2],
        }
    )
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={"RACE_CODE": "202509030411", "UMABAN": [1, 2]},
    )

    call_args = mock_connection_manager.fetch_dataframe.call_args
    query = call_args[0][0]
    params = call_args[0][1]

    assert "SELECT * FROM umagoto_race_joho WHERE" in query
    assert "TRIM(race_code) = %s" in query
    assert "TRIM(umaban) IN (%s, %s)" in query
    assert "202509030411" in params
    assert 1 in params
    assert 2 in params
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_table_data_returns_empty_dataframe(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """条件に合致するデータがない場合、空のDataFrameが返されることを確認."""
    expected_df = pd.DataFrame()
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": "999999999999"},
    )

    assert result.empty


@pytest.mark.parametrize("table_name", list(SUPPORTED_TABLES)[:10])
def test_get_table_data_with_various_supported_tables(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
    table_name: str,
) -> None:
    """各種サポートテーブルでデータ取得が可能であることを確認."""
    expected_df = pd.DataFrame()
    mock_connection_manager.fetch_dataframe.return_value = expected_df

    result = table_accessor.get_table_data(table_name)

    mock_connection_manager.fetch_dataframe.assert_called_once()
    assert isinstance(result, pd.DataFrame)


# 準正常系


def test_get_table_data_raises_error_for_nonexistent_table(
    table_accessor: TableAccessor,
) -> None:
    """存在しないテーブル名を指定した場合、TableNotFoundErrorが発生することを確認."""
    with pytest.raises(TableNotFoundError) as exc_info:
        table_accessor.get_table_data("NONEXISTENT_TABLE")

    assert "NONEXISTENT_TABLE" in str(exc_info.value)
    assert "サポートされていません" in str(exc_info.value)


def test_get_table_data_raises_error_for_invalid_column_name(
    table_accessor: TableAccessor,
) -> None:
    """不正なカラム名を指定した場合、InvalidFilterErrorが発生することを確認."""
    with pytest.raises(InvalidFilterError) as exc_info:
        table_accessor.get_table_data(
            "RACE_SHOSAI",
            filters={"123INVALID": "value"},
        )

    assert "123INVALID" in str(exc_info.value)
    assert "無効なカラム名" in str(exc_info.value)


def test_get_table_data_raises_error_for_sql_injection_attempt(
    table_accessor: TableAccessor,
) -> None:
    """SQLインジェクション攻撃を試みた場合、InvalidFilterErrorが発生することを確認."""
    malicious_inputs = [
        "column; DROP TABLE RACE_SHOSAI;--",
        "column' OR '1'='1",
        "column/*comment*/",
        "column-name",
        "column.name",
        "",
    ]

    for malicious_input in malicious_inputs:
        with pytest.raises(InvalidFilterError):
            table_accessor.get_table_data(
                "RACE_SHOSAI",
                filters={malicious_input: "value"},
            )


def test_get_table_data_allows_underscore_in_column_name(
    table_accessor: TableAccessor,
    mock_connection_manager: MagicMock,
) -> None:
    """アンダースコアを含むカラム名が許可されることを確認."""
    table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": "202509030411", "_PRIVATE_COL": "value"},
    )

    mock_connection_manager.fetch_dataframe.assert_called_once()


def test_get_table_data_raises_error_for_invalid_filter_value_type(
    table_accessor: TableAccessor,
) -> None:
    """不正な型のフィルタ値を指定した場合、InvalidFilterErrorが発生することを確認."""
    with pytest.raises(InvalidFilterError) as exc_info:
        table_accessor.get_table_data(
            "RACE_SHOSAI",
            filters={"RACE_CODE": 3.14},
        )

    assert "無効なフィルタ値の型" in str(exc_info.value)
    assert "float" in str(exc_info.value)


def test_get_table_data_raises_error_for_invalid_type_in_list(
    table_accessor: TableAccessor,
) -> None:
    """リスト内に不正な型の値が含まれる場合、InvalidFilterErrorが発生することを確認."""
    with pytest.raises(InvalidFilterError) as exc_info:
        table_accessor.get_table_data(
            "RACE_SHOSAI",
            filters={"RACE_CODE": ["valid", 3.14]},
        )

    assert "無効なフィルタ値の型" in str(exc_info.value)


def test_get_table_data_raises_error_for_empty_list_filter(
    table_accessor: TableAccessor,
) -> None:
    """空のリストをフィルタ値として指定した場合、InvalidFilterErrorが発生することを確認."""
    with pytest.raises(InvalidFilterError) as exc_info:
        table_accessor.get_table_data(
            "RACE_SHOSAI",
            filters={"RACE_CODE": []},
        )

    assert "リストが空" in str(exc_info.value)


def test_get_table_data_raises_error_for_none_filter_value(
    table_accessor: TableAccessor,
) -> None:
    """Noneをフィルタ値として指定した場合、InvalidFilterErrorが発生することを確認."""
    with pytest.raises(InvalidFilterError) as exc_info:
        table_accessor.get_table_data(
            "RACE_SHOSAI",
            filters={"RACE_CODE": None},
        )

    assert "無効なフィルタ値の型" in str(exc_info.value)


def test_get_table_data_raises_error_for_dict_filter_value(
    table_accessor: TableAccessor,
) -> None:
    """辞書をフィルタ値として指定した場合、InvalidFilterErrorが発生することを確認."""
    with pytest.raises(InvalidFilterError) as exc_info:
        table_accessor.get_table_data(
            "RACE_SHOSAI",
            filters={"RACE_CODE": {"nested": "value"}},
        )

    assert "無効なフィルタ値の型" in str(exc_info.value)


# サポートテーブル一覧のテスト


def test_supported_tables_count() -> None:
    """サポートテーブルの数が63であることを確認."""
    assert len(SUPPORTED_TABLES) == 63


def test_supported_tables_contains_expected_tables() -> None:
    """主要なテーブルがサポートテーブルに含まれていることを確認."""
    expected_tables = [
        "RACE_SHOSAI",
        "UMAGOTO_RACE_JOHO",
        "HARAIMODOSHI",
        "KISHU_MASTER",
        "KYOSOBA_MASTER2",
        "ODDS1_TANSHO",
        "WIN5",
    ]

    for table in expected_tables:
        assert table in SUPPORTED_TABLES, f"'{table}'がサポートテーブルに含まれていません"
