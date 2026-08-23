"""TRIM除去前後で取得結果が一致することを検証する結合テスト.

固定長文字列（bpchar）の列は`TRIM()`で包まなくても一致するため、インデックスを
効かせるために`TRIM()`を外している。この変更で取得結果が変わっていないことを
実データで確認する。

行の並びは`TRIM()`の有無で変わる（全表スキャンの物理順からインデックス順になる）。
いずれのクエリにも`ORDER BY`はなく行順は保証していないため、ソートしてから比較する。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor, _build_query

from .conftest import get_sample_data

# テーブル名とフィルタ対象の固定長文字列カラム
_TARGETS = [
    ("RACE_SHOSAI", "race_code"),
    ("UMAGOTO_RACE_JOHO", "race_code"),
    ("UMAGOTO_RACE_JOHO", "ketto_toroku_bango"),
    ("HARAIMODOSHI", "race_code"),
    ("KYOSOBA_MASTER2", "ketto_toroku_bango"),
]


def _fetch_with_trim(
    connection_manager: ConnectionManager, table_name: str, filters: dict[str, object]
) -> pd.DataFrame:
    """TRIMで包んだWHERE句で取得する（TRIM除去前の振る舞い）.

    Args:
        connection_manager (ConnectionManager): 接続マネージャー
        table_name (str): テーブル名
        filters (dict[str, object]): フィルタ条件

    Returns:
        pd.DataFrame: 取得したデータ
    """
    query, params = _build_query(table_name, filters, None)
    assert "TRIM(" in query
    return connection_manager.fetch_dataframe(query, params)


def _sample_values(
    connection_manager: ConnectionManager, table_name: str, column: str, count: int
) -> list[str]:
    """テーブルからフィルタ値のサンプルを取得する.

    Args:
        connection_manager (ConnectionManager): 接続マネージャー
        table_name (str): テーブル名
        column (str): カラム名
        count (int): 取得する件数

    Returns:
        list[str]: フィルタ値のリスト（重複なし）
    """
    df = get_sample_data(connection_manager, table_name, limit=count * 5)
    values = df[column].dropna().astype(str).unique().tolist()
    return values[:count]


# 正常系
@pytest.mark.parametrize("table_name, column", _TARGETS)
def test_single_value_filter_returns_same_rows(
    connection_manager: ConnectionManager,
    table_accessor: TableAccessor,
    table_name: str,
    column: str,
) -> None:
    """単一値フィルタで、TRIMの有無によらず同じ行が返ることを確認."""
    values = _sample_values(connection_manager, table_name, column, count=3)
    assert values, f"{table_name}.{column} のサンプル値を取得できませんでした"

    for value in values:
        actual = table_accessor.get_table_data(table_name, filters={column: value})
        expected = _fetch_with_trim(connection_manager, table_name, {column: value})

        pd.testing.assert_frame_equal(
            actual.sort_values(list(actual.columns)).reset_index(drop=True),
            expected.sort_values(list(expected.columns)).reset_index(drop=True),
        )


@pytest.mark.parametrize("table_name, column", _TARGETS)
def test_list_filter_returns_same_rows(
    connection_manager: ConnectionManager,
    table_accessor: TableAccessor,
    table_name: str,
    column: str,
) -> None:
    """リスト値フィルタで、TRIMの有無によらず同じ行が返ることを確認."""
    values = _sample_values(connection_manager, table_name, column, count=5)
    assert values, f"{table_name}.{column} のサンプル値を取得できませんでした"

    actual = table_accessor.get_table_data(table_name, filters={column: values})
    expected = _fetch_with_trim(connection_manager, table_name, {column: values})

    assert len(actual) == len(expected)
    pd.testing.assert_frame_equal(
        actual.sort_values(list(actual.columns)).reset_index(drop=True),
        expected.sort_values(list(expected.columns)).reset_index(drop=True),
    )


@pytest.mark.parametrize("table_name, column", _TARGETS)
def test_blank_padded_char_column_is_not_wrapped_with_trim(
    table_accessor: TableAccessor, table_name: str, column: str
) -> None:
    """固定長文字列の列がTRIMで包まれないことを確認.

    列を関数で包むとインデックスが使われず全表スキャンになる。
    """
    query, _ = _build_query(table_name, {column: "X"}, table_accessor._column_type_resolver)

    assert f"{column} = %s" in query
    assert "TRIM(" not in query


@pytest.mark.parametrize("table_name, column", _TARGETS)
def test_filter_column_has_no_leading_space(
    connection_manager: ConnectionManager, table_name: str, column: str
) -> None:
    """フィルタ対象の列に先頭空白を持つ行が存在しないことを確認.

    TRIMは先頭空白も除去するが、固定長文字列の比較が無視するのは末尾空白だけである。
    先頭空白を持つ行があるとTRIMの除去で一致しなくなるため、存在しないことを固定する。
    """
    query = f"SELECT 1 FROM {table_name.lower()} WHERE {column} LIKE ' %' LIMIT 1"  # noqa: S608
    df = connection_manager.fetch_dataframe(query)

    assert df.empty


# 準正常系
@pytest.mark.parametrize("table_name, column", _TARGETS)
def test_unknown_value_returns_no_rows_for_both(
    connection_manager: ConnectionManager,
    table_accessor: TableAccessor,
    table_name: str,
    column: str,
) -> None:
    """存在しない値を指定した場合、TRIMの有無によらず0行が返ることを確認."""
    value = "ZZZZZZZZZZZZZZZZ"

    actual = table_accessor.get_table_data(table_name, filters={column: value})
    expected = _fetch_with_trim(connection_manager, table_name, {column: value})

    assert actual.empty
    assert expected.empty
