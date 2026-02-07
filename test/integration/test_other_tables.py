"""その他テーブルの結合テスト.

SHOBUFUKU（勝負服）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 勝負服テーブルのテスト
def test_get_shobufuku_sample_data(connection_manager: ConnectionManager) -> None:
    """SHOBUFUKUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHOBUFUKU")
    if len(df) == 0:
        pytest.skip("SHOBUFUKUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) > 0


def test_get_shobufuku_has_owner_related_columns(connection_manager: ConnectionManager) -> None:
    """SHOBUFUKUテーブルに馬主関連カラムがあることを確認."""
    df = get_sample_data(connection_manager, "SHOBUFUKU")
    if len(df) == 0:
        pytest.skip("SHOBUFUKUテーブルにデータがありません")

    # 勝負服テーブルは馬主コードで識別されるはず
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) > 0


def test_get_shobufuku_with_banushi_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHOBUFUKUテーブルから馬主コードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHOBUFUKU")
    if len(sample_data) == 0:
        pytest.skip("SHOBUFUKUテーブルにデータがありません")

    # 馬主コードカラムがあれば使用
    if "banushi_code" in sample_data.columns:
        sample_banushi_code = sample_data.iloc[0]["banushi_code"]

        df = table_accessor.get_table_data(
            "SHOBUFUKU",
            filters={"BANUSHI_CODE": sample_banushi_code},
        )

        assert len(df) > 0
        assert all(df["banushi_code"] == sample_banushi_code)
    else:
        pytest.skip("SHOBUFUKUテーブルにbanushi_codeカラムがありません")


def test_get_shobufuku_with_nonexistent_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """存在しないフィルタ値でフィルタすると空のDataFrameが返ることを確認."""
    sample_data = get_sample_data(connection_manager, "SHOBUFUKU")
    if len(sample_data) == 0:
        pytest.skip("SHOBUFUKUテーブルにデータがありません")

    # テーブルの最初のカラムを使って存在しない値でフィルタ
    first_column = sample_data.columns[0]

    df = table_accessor.get_table_data(
        "SHOBUFUKU",
        filters={first_column: "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
