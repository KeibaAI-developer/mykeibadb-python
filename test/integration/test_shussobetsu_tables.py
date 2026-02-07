"""出走別着度数テーブルの結合テスト.

SHUSSOBETSU_BABA（馬場別）、SHUSSOBETSU_KYORI（距離別）、SHUSSOBETSU_KEIBAJO（競馬場別）、
SHUSSOBETSU_KISHU（騎手別）、SHUSSOBETSU_CHOKYOSHI（調教師別）、SHUSSOBETSU_BANUSHI（馬主別）、
SHUSSOBETSU_SEISANSHA2（生産者別）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 馬場別着度数のテスト
# 正常系
def test_get_shussobetsu_baba_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_BABAテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_BABA")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_BABAテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_baba_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_BABAテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_BABA")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_BABAテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_BABA",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_shussobetsu_baba_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_BABAテーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_BABA")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_BABAテーブルにデータがありません")

    sample_ketto_bango = sample_data.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_BABA",
        filters={"KETTO_TOROKU_BANGO": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


# 距離別着度数のテスト
def test_get_shussobetsu_kyori_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_KYORIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_KYORI")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_KYORIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_kyori_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_KYORIテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_KYORI")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_KYORIテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_KYORI",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 競馬場別着度数のテスト
def test_get_shussobetsu_keibajo_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_KEIBAJOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_KEIBAJO")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_KEIBAJOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_keibajo_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_KEIBAJOテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_KEIBAJO")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_KEIBAJOテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_KEIBAJO",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 騎手別着度数のテスト
def test_get_shussobetsu_kishu_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_KISHUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_KISHU")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_KISHUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_kishu_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_KISHUテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_KISHU")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_KISHUテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_KISHU",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 調教師別着度数のテスト
def test_get_shussobetsu_chokyoshi_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_CHOKYOSHIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_CHOKYOSHI")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_CHOKYOSHIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_chokyoshi_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_CHOKYOSHIテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_CHOKYOSHI")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_CHOKYOSHIテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_CHOKYOSHI",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 馬主別着度数のテスト
def test_get_shussobetsu_banushi_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_BANUSHIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_BANUSHI")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_BANUSHIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_banushi_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_BANUSHIテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_BANUSHI")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_BANUSHIテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_BANUSHI",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 生産者別着度数のテスト
def test_get_shussobetsu_seisansha2_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOBETSU_SEISANSHA2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOBETSU_SEISANSHA2")
    if len(df) == 0:
        pytest.skip("SHUSSOBETSU_SEISANSHA2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_shussobetsu_seisansha2_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOBETSU_SEISANSHA2テーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOBETSU_SEISANSHA2")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOBETSU_SEISANSHA2テーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOBETSU_SEISANSHA2",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 準正常系
def test_get_shussobetsu_baba_with_nonexistent_race_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "SHUSSOBETSU_BABA",
        filters={"RACE_CODE": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_shussobetsu_kyori_with_nonexistent_ketto_bango(
    table_accessor: TableAccessor,
) -> None:
    """存在しない血統登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "SHUSSOBETSU_KYORI",
        filters={"KETTO_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
