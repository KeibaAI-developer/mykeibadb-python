"""競走馬詳細情報テーブルの結合テスト.

KYOSOBA_TORIHIKI_KAKAKU2（取引価格）、BAMEI_IMI_YURAI（馬名意味由来）、
KEITO_JOHO2（系統情報）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 取引価格テーブルのテスト
def test_get_kyosoba_torihiki_kakaku2_sample_data(connection_manager: ConnectionManager) -> None:
    """KYOSOBA_TORIHIKI_KAKAKU2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KYOSOBA_TORIHIKI_KAKAKU2")
    if len(df) == 0:
        pytest.skip("KYOSOBA_TORIHIKI_KAKAKU2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "ketto_toroku_bango" in df.columns


def test_get_kyosoba_torihiki_kakaku2_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KYOSOBA_TORIHIKI_KAKAKU2テーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "KYOSOBA_TORIHIKI_KAKAKU2")
    if len(sample_data) == 0:
        pytest.skip("KYOSOBA_TORIHIKI_KAKAKU2テーブルにデータがありません")

    sample_ketto_bango = sample_data.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "KYOSOBA_TORIHIKI_KAKAKU2",
        filters={"KETTO_TOROKU_BANGO": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


def test_get_kyosoba_torihiki_kakaku2_with_nonexistent_ketto_bango(
    table_accessor: TableAccessor,
) -> None:
    """存在しない血統登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KYOSOBA_TORIHIKI_KAKAKU2",
        filters={"KETTO_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# 馬名意味由来テーブルのテスト
def test_get_bamei_imi_yurai_sample_data(connection_manager: ConnectionManager) -> None:
    """BAMEI_IMI_YURAIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "BAMEI_IMI_YURAI")
    if len(df) == 0:
        pytest.skip("BAMEI_IMI_YURAIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "ketto_toroku_bango" in df.columns


def test_get_bamei_imi_yurai_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """BAMEI_IMI_YURAIテーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "BAMEI_IMI_YURAI")
    if len(sample_data) == 0:
        pytest.skip("BAMEI_IMI_YURAIテーブルにデータがありません")

    sample_ketto_bango = sample_data.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "BAMEI_IMI_YURAI",
        filters={"KETTO_TOROKU_BANGO": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


def test_get_bamei_imi_yurai_with_nonexistent_ketto_bango(
    table_accessor: TableAccessor,
) -> None:
    """存在しない血統登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "BAMEI_IMI_YURAI",
        filters={"KETTO_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# 系統情報テーブルのテスト
def test_get_keito_joho2_sample_data(connection_manager: ConnectionManager) -> None:
    """KEITO_JOHO2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KEITO_JOHO2")
    if len(df) == 0:
        pytest.skip("KEITO_JOHO2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    # 系統情報テーブルは繁殖登録番号を使用
    assert "hanshoku_toroku_bango" in df.columns


def test_get_keito_joho2_with_hanshoku_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KEITO_JOHO2テーブルから繁殖登録番号でフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "KEITO_JOHO2")
    if len(sample_data) == 0:
        pytest.skip("KEITO_JOHO2テーブルにデータがありません")

    sample_hanshoku_bango = sample_data.iloc[0]["hanshoku_toroku_bango"]

    df = table_accessor.get_table_data(
        "KEITO_JOHO2",
        filters={"HANSHOKU_TOROKU_BANGO": sample_hanshoku_bango},
    )

    assert len(df) > 0
    assert all(df["hanshoku_toroku_bango"] == sample_hanshoku_bango)


def test_get_keito_joho2_with_nonexistent_hanshoku_bango(
    table_accessor: TableAccessor,
) -> None:
    """存在しない繁殖登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KEITO_JOHO2",
        filters={"HANSHOKU_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
