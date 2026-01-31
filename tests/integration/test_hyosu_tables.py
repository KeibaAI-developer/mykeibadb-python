"""票数関連テーブルの結合テスト.

HYOSU1、HYOSU1_TANSHO、HYOSU1_FUKUSHO、HYOSU1_WAKUREN、HYOSU1_UMAREN、
HYOSU1_WIDE、HYOSU1_UMATAN、HYOSU1_SANRENPUKU、HYOSU6、HYOSU6_SANRENTAN
テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 票数1関連テーブル（HYOSU1系）のテスト
# 正常系
def test_get_hyosu1_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "tansho_hyosu_gokei" in df.columns


def test_get_hyosu1_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HYOSU1テーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_hyosu = get_sample_data(connection_manager, "HYOSU1")
    if len(sample_hyosu) == 0:
        pytest.skip("HYOSU1テーブルにデータがありません")

    sample_race_code = sample_hyosu.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "HYOSU1",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_hyosu1_tansho_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_TANSHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_TANSHO")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu1_tansho_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HYOSU1_TANSHOテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_tansho = get_sample_data(connection_manager, "HYOSU1_TANSHO")
    if len(sample_tansho) == 0:
        pytest.skip("HYOSU1_TANSHOテーブルにデータがありません")

    sample_race_code = sample_tansho.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "HYOSU1_TANSHO",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_hyosu1_fukusho_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_FUKUSHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_FUKUSHO")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu1_wakuren_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_WAKURENテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_WAKUREN")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu1_umaren_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_UMARENテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_UMAREN")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu1_wide_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_WIDEテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_WIDE")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu1_umatan_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_UMATANテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_UMATAN")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu1_sanrenpuku_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU1_SANRENPUKUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU1_SANRENPUKU")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


# 票数6関連テーブル（HYOSU6系）のテスト
def test_get_hyosu6_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU6テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU6")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu6_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HYOSU6テーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_hyosu6 = get_sample_data(connection_manager, "HYOSU6")
    if len(sample_hyosu6) == 0:
        pytest.skip("HYOSU6テーブルにデータがありません")

    sample_race_code = sample_hyosu6.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "HYOSU6",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_hyosu6_sanrentan_sample_data(connection_manager: ConnectionManager) -> None:
    """HYOSU6_SANRENTANテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HYOSU6_SANRENTAN")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hyosu6_sanrentan_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HYOSU6_SANRENTANテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_sanrentan = get_sample_data(connection_manager, "HYOSU6_SANRENTAN")
    if len(sample_sanrentan) == 0:
        pytest.skip("HYOSU6_SANRENTANテーブルにデータがありません")

    sample_race_code = sample_sanrentan.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "HYOSU6_SANRENTAN",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 複数レースでのフィルタテスト
def test_get_hyosu1_with_multiple_race_codes(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HYOSU1テーブルから複数のレースコードでフィルタしてデータを取得できることを確認."""
    sample_hyosu = get_sample_data(connection_manager, "HYOSU1")
    if len(sample_hyosu) < 2:
        pytest.skip("HYOSU1テーブルに十分なデータがありません")

    race_codes = [sample_hyosu.iloc[0]["race_code"], sample_hyosu.iloc[1]["race_code"]]

    df = table_accessor.get_table_data(
        "HYOSU1",
        filters={"race_code": race_codes},
    )

    assert len(df) >= 2
    assert set(df["race_code"].tolist()).issubset(set(race_codes))


# 準正常系
def test_get_hyosu1_with_nonexistent_race_code(table_accessor: TableAccessor) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "HYOSU1",
        filters={"race_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_hyosu6_sanrentan_with_nonexistent_race_code(table_accessor: TableAccessor) -> None:
    """存在しないレースコードでHYOSU6_SANRENTANをフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "HYOSU6_SANRENTAN",
        filters={"race_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
