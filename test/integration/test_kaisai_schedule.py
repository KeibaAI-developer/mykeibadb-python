"""開催スケジュールテーブルの結合テスト.

KAISAI_SCHEDULEテーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 正常系
def test_get_kaisai_schedule_sample_data(connection_manager: ConnectionManager) -> None:
    """KAISAI_SCHEDULEテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KAISAI_SCHEDULE")

    assert isinstance(df, pd.DataFrame)
    assert "kaisai_code" in df.columns
    assert "kaisai_nen" in df.columns
    assert "keibajo_code" in df.columns


def test_get_kaisai_schedule_with_kaisai_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KAISAI_SCHEDULEテーブルから開催コードでフィルタしてデータを取得できることを確認."""
    sample_schedule = get_sample_data(connection_manager, "KAISAI_SCHEDULE")
    if len(sample_schedule) == 0:
        pytest.skip("KAISAI_SCHEDULEテーブルにデータがありません")

    sample_kaisai_code = sample_schedule.iloc[0]["kaisai_code"]

    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={"kaisai_code": sample_kaisai_code},
    )

    assert len(df) > 0
    assert all(df["kaisai_code"] == sample_kaisai_code)


def test_get_kaisai_schedule_with_keibajo_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KAISAI_SCHEDULEテーブルから競馬場コードでフィルタしてデータを取得できることを確認."""
    sample_schedule = get_sample_data(connection_manager, "KAISAI_SCHEDULE")
    if len(sample_schedule) == 0:
        pytest.skip("KAISAI_SCHEDULEテーブルにデータがありません")

    sample_keibajo_code = sample_schedule.iloc[0]["keibajo_code"]

    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={"keibajo_code": sample_keibajo_code},
    )

    assert len(df) > 0
    assert all(df["keibajo_code"] == sample_keibajo_code)


def test_get_kaisai_schedule_with_kaisai_nen_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KAISAI_SCHEDULEテーブルから開催年でフィルタしてデータを取得できることを確認."""
    sample_schedule = get_sample_data(connection_manager, "KAISAI_SCHEDULE")
    if len(sample_schedule) == 0:
        pytest.skip("KAISAI_SCHEDULEテーブルにデータがありません")

    sample_kaisai_nen = sample_schedule.iloc[0]["kaisai_nen"]

    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={"kaisai_nen": sample_kaisai_nen},
    )

    assert len(df) > 0
    assert all(df["kaisai_nen"] == sample_kaisai_nen)


def test_get_kaisai_schedule_with_multiple_keibajo_codes(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KAISAI_SCHEDULEテーブルから複数の競馬場コードでフィルタしてデータを取得できることを確認."""
    sample_schedule = get_sample_data(connection_manager, "KAISAI_SCHEDULE")
    if len(sample_schedule) < 2:
        pytest.skip("KAISAI_SCHEDULEテーブルに十分なデータがありません")

    # 異なる競馬場コードを取得
    unique_keibajo_codes = sample_schedule["keibajo_code"].unique()
    if len(unique_keibajo_codes) < 2:
        pytest.skip("異なる競馬場コードが2つ以上必要です")

    keibajo_codes = list(unique_keibajo_codes[:2])

    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={"keibajo_code": keibajo_codes},
    )

    assert len(df) > 0
    assert all(code in keibajo_codes for code in df["keibajo_code"])


def test_get_kaisai_schedule_with_compound_filters(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KAISAI_SCHEDULEテーブルから複合フィルタでデータを取得できることを確認."""
    sample_schedule = get_sample_data(connection_manager, "KAISAI_SCHEDULE")
    if len(sample_schedule) == 0:
        pytest.skip("KAISAI_SCHEDULEテーブルにデータがありません")

    sample_kaisai_nen = sample_schedule.iloc[0]["kaisai_nen"]
    sample_keibajo_code = sample_schedule.iloc[0]["keibajo_code"]

    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={
            "kaisai_nen": sample_kaisai_nen,
            "keibajo_code": sample_keibajo_code,
        },
    )

    assert len(df) > 0
    assert all(df["kaisai_nen"] == sample_kaisai_nen)
    assert all(df["keibajo_code"] == sample_keibajo_code)


# 準正常系
def test_get_kaisai_schedule_with_nonexistent_kaisai_code(table_accessor: TableAccessor) -> None:
    """存在しない開催コードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={"kaisai_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_kaisai_schedule_with_future_year(table_accessor: TableAccessor) -> None:
    """未来の開催年でフィルタすると空または少数のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KAISAI_SCHEDULE",
        filters={"kaisai_nen": "2099"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
