"""データマイニング予想テーブルの結合テスト.

DATA_MINING_TIME（タイム型）、DATA_MINING_TAISEN（対戦型）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# タイム型予想テーブルのテスト
def test_get_data_mining_time_sample_data(connection_manager: ConnectionManager) -> None:
    """DATA_MINING_TIMEテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "DATA_MINING_TIME")
    if len(df) == 0:
        pytest.skip("DATA_MINING_TIMEテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_data_mining_time_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """DATA_MINING_TIMEテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "DATA_MINING_TIME")
    if len(sample_data) == 0:
        pytest.skip("DATA_MINING_TIMEテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "DATA_MINING_TIME",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_data_mining_time_has_umaban_column(
    connection_manager: ConnectionManager,
) -> None:
    """DATA_MINING_TIMEテーブルに馬番カラムがあることを確認."""
    df = get_sample_data(connection_manager, "DATA_MINING_TIME")
    if len(df) == 0:
        pytest.skip("DATA_MINING_TIMEテーブルにデータがありません")

    # 馬番は umaban1, umaban2, ... という形式
    assert "umaban1" in df.columns


def test_get_data_mining_time_with_nonexistent_race_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "DATA_MINING_TIME",
        filters={"RACE_CODE": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# 対戦型予想テーブルのテスト
def test_get_data_mining_taisen_sample_data(connection_manager: ConnectionManager) -> None:
    """DATA_MINING_TAISENテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "DATA_MINING_TAISEN")
    if len(df) == 0:
        pytest.skip("DATA_MINING_TAISENテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_data_mining_taisen_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """DATA_MINING_TAISENテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "DATA_MINING_TAISEN")
    if len(sample_data) == 0:
        pytest.skip("DATA_MINING_TAISENテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "DATA_MINING_TAISEN",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_data_mining_taisen_has_umaban_column(
    connection_manager: ConnectionManager,
) -> None:
    """DATA_MINING_TAISENテーブルに馬番カラムがあることを確認."""
    df = get_sample_data(connection_manager, "DATA_MINING_TAISEN")
    if len(df) == 0:
        pytest.skip("DATA_MINING_TAISENテーブルにデータがありません")

    # 馬番は umaban1, umaban2, ... という形式
    assert "umaban1" in df.columns


def test_get_data_mining_taisen_with_nonexistent_race_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "DATA_MINING_TAISEN",
        filters={"RACE_CODE": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
