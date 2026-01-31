"""オッズ関連テーブルの結合テスト.

ODDS1系（単複枠オッズ）、ODDS2（馬連）、ODDS3（ワイド）、ODDS4（馬単）、
ODDS5（三連複）、ODDS6（三連単）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# ODDS1系テーブル（単複枠オッズ）のテスト
# 正常系
def test_get_odds1_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS1テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1")
    if len(df) == 0:
        pytest.skip("ODDS1テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "tansho_hyosu_gokei" in df.columns


def test_get_odds1_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS1テーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS1")
    if len(sample_odds) == 0:
        pytest.skip("ODDS1テーブルにデータがありません")

    sample_race_code = sample_odds.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "ODDS1",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_odds1_tansho_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS1_TANSHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_TANSHO")
    if len(df) == 0:
        pytest.skip("ODDS1_TANSHOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds1_fukusho_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS1_FUKUSHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_FUKUSHO")
    if len(df) == 0:
        pytest.skip("ODDS1_FUKUSHOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds1_wakuren_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS1_WAKURENテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_WAKUREN")
    if len(df) == 0:
        pytest.skip("ODDS1_WAKURENテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


# ODDS1時系列テーブルのテスト
def test_get_odds1_jikeiretsu_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS1_JIKEIRETSUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_JIKEIRETSU")
    if len(df) == 0:
        pytest.skip("ODDS1_JIKEIRETSUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds1_tansho_jikeiretsu_sample_data(
    connection_manager: ConnectionManager,
) -> None:
    """ODDS1_TANSHO_JIKEIRETSUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_TANSHO_JIKEIRETSU")
    if len(df) == 0:
        pytest.skip("ODDS1_TANSHO_JIKEIRETSUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds1_fukusho_jikeiretsu_sample_data(
    connection_manager: ConnectionManager,
) -> None:
    """ODDS1_FUKUSHO_JIKEIRETSUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_FUKUSHO_JIKEIRETSU")
    if len(df) == 0:
        pytest.skip("ODDS1_FUKUSHO_JIKEIRETSUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds1_wakuren_jikeiretsu_sample_data(
    connection_manager: ConnectionManager,
) -> None:
    """ODDS1_WAKUREN_JIKEIRETSUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS1_WAKUREN_JIKEIRETSU")
    if len(df) == 0:
        pytest.skip("ODDS1_WAKUREN_JIKEIRETSUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


# ODDS2（馬連）のテスト
def test_get_odds2_umaren_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS2_UMARENテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS2_UMAREN")
    if len(df) == 0:
        pytest.skip("ODDS2_UMARENテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds2_umaren_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS2_UMARENテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS2_UMAREN")
    if len(sample_odds) == 0:
        pytest.skip("ODDS2_UMARENテーブルにデータがありません")

    sample_race_code = sample_odds.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "ODDS2_UMAREN",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_odds2_umaren_jikeiretsu_sample_data(
    connection_manager: ConnectionManager,
) -> None:
    """ODDS2_UMAREN_JIKEIRETSUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS2_UMAREN_JIKEIRETSU")
    if len(df) == 0:
        pytest.skip("ODDS2_UMAREN_JIKEIRETSUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


# ODDS3（ワイド）のテスト
def test_get_odds3_wide_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS3_WIDEテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS3_WIDE")
    if len(df) == 0:
        pytest.skip("ODDS3_WIDEテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds3_wide_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS3_WIDEテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS3_WIDE")
    if len(sample_odds) == 0:
        pytest.skip("ODDS3_WIDEテーブルにデータがありません")

    sample_race_code = sample_odds.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "ODDS3_WIDE",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# ODDS4（馬単）のテスト
def test_get_odds4_umatan_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS4_UMATANテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS4_UMATAN")
    if len(df) == 0:
        pytest.skip("ODDS4_UMATANテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds4_umatan_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS4_UMATANテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS4_UMATAN")
    if len(sample_odds) == 0:
        pytest.skip("ODDS4_UMATANテーブルにデータがありません")

    sample_race_code = sample_odds.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "ODDS4_UMATAN",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# ODDS5（三連複）のテスト
def test_get_odds5_sanrenpuku_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS5_SANRENPUKUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS5_SANRENPUKU")
    if len(df) == 0:
        pytest.skip("ODDS5_SANRENPUKUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds5_sanrenpuku_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS5_SANRENPUKUテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS5_SANRENPUKU")
    if len(sample_odds) == 0:
        pytest.skip("ODDS5_SANRENPUKUテーブルにデータがありません")

    sample_race_code = sample_odds.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "ODDS5_SANRENPUKU",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# ODDS6（三連単）のテスト
def test_get_odds6_sanrentan_sample_data(connection_manager: ConnectionManager) -> None:
    """ODDS6_SANRENTANテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "ODDS6_SANRENTAN")
    if len(df) == 0:
        pytest.skip("ODDS6_SANRENTANテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_odds6_sanrentan_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS6_SANRENTANテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS6_SANRENTAN")
    if len(sample_odds) == 0:
        pytest.skip("ODDS6_SANRENTANテーブルにデータがありません")

    sample_race_code = sample_odds.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "ODDS6_SANRENTAN",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 複数レースでのフィルタテスト
def test_get_odds1_with_multiple_race_codes(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """ODDS1テーブルから複数のレースコードでフィルタしてデータを取得できることを確認."""
    sample_odds = get_sample_data(connection_manager, "ODDS1")
    if len(sample_odds) < 2:
        pytest.skip("ODDS1テーブルに十分なデータがありません")

    race_codes = [sample_odds.iloc[0]["race_code"], sample_odds.iloc[1]["race_code"]]

    df = table_accessor.get_table_data(
        "ODDS1",
        filters={"race_code": race_codes},
    )

    assert len(df) >= 2
    assert set(df["race_code"].tolist()).issubset(set(race_codes))


# 準正常系
def test_get_odds1_with_nonexistent_race_code(table_accessor: TableAccessor) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "ODDS1",
        filters={"race_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_odds6_sanrentan_with_nonexistent_race_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しないレースコードでODDS6_SANRENTANをフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "ODDS6_SANRENTAN",
        filters={"race_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
