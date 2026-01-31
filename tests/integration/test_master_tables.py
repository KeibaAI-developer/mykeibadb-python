"""マスタテーブルの結合テスト.

KYOSOBA_MASTER2（競走馬）、KISHU_MASTER（騎手）、CHOKYOSHI_MASTER（調教師）、
SEISANSHA_MASTER2（生産者）、BANUSHI_MASTER（馬主）、HANSHOKUBA_MASTER2（繁殖馬）、
SANKU_MASTER2（産駒）、RECORD_MASTER（レコード）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 競走馬マスタのテスト
# 正常系
def test_get_kyosoba_master2_sample_data(connection_manager: ConnectionManager) -> None:
    """KYOSOBA_MASTER2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KYOSOBA_MASTER2")
    if len(df) == 0:
        pytest.skip("KYOSOBA_MASTER2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "ketto_toroku_bango" in df.columns
    assert "bamei" in df.columns


def test_get_kyosoba_master2_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KYOSOBA_MASTER2テーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "KYOSOBA_MASTER2")
    if len(sample_master) == 0:
        pytest.skip("KYOSOBA_MASTER2テーブルにデータがありません")

    sample_ketto_bango = sample_master.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "KYOSOBA_MASTER2",
        filters={"ketto_toroku_bango": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


def test_get_kyosoba_master2_with_multiple_ketto_bangos(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KYOSOBA_MASTER2テーブルから複数の血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "KYOSOBA_MASTER2")
    if len(sample_master) < 2:
        pytest.skip("KYOSOBA_MASTER2テーブルに十分なデータがありません")

    ketto_bangos = [
        sample_master.iloc[0]["ketto_toroku_bango"],
        sample_master.iloc[1]["ketto_toroku_bango"],
    ]

    df = table_accessor.get_table_data(
        "KYOSOBA_MASTER2",
        filters={"ketto_toroku_bango": ketto_bangos},
    )

    assert len(df) >= 2
    assert all(bango in ketto_bangos for bango in df["ketto_toroku_bango"])


# 騎手マスタのテスト
def test_get_kishu_master_sample_data(connection_manager: ConnectionManager) -> None:
    """KISHU_MASTERテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KISHU_MASTER")
    if len(df) == 0:
        pytest.skip("KISHU_MASTERテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "kishu_code" in df.columns
    assert "kishumei" in df.columns


def test_get_kishu_master_with_kishu_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KISHU_MASTERテーブルから騎手コードでフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "KISHU_MASTER")
    if len(sample_master) == 0:
        pytest.skip("KISHU_MASTERテーブルにデータがありません")

    sample_kishu_code = sample_master.iloc[0]["kishu_code"]

    df = table_accessor.get_table_data(
        "KISHU_MASTER",
        filters={"kishu_code": sample_kishu_code},
    )

    assert len(df) > 0
    assert all(df["kishu_code"] == sample_kishu_code)


# 調教師マスタのテスト
def test_get_chokyoshi_master_sample_data(connection_manager: ConnectionManager) -> None:
    """CHOKYOSHI_MASTERテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "CHOKYOSHI_MASTER")
    if len(df) == 0:
        pytest.skip("CHOKYOSHI_MASTERテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "chokyoshi_code" in df.columns


def test_get_chokyoshi_master_with_chokyoshi_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """CHOKYOSHI_MASTERテーブルから調教師コードでフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "CHOKYOSHI_MASTER")
    if len(sample_master) == 0:
        pytest.skip("CHOKYOSHI_MASTERテーブルにデータがありません")

    sample_chokyoshi_code = sample_master.iloc[0]["chokyoshi_code"]

    df = table_accessor.get_table_data(
        "CHOKYOSHI_MASTER",
        filters={"chokyoshi_code": sample_chokyoshi_code},
    )

    assert len(df) > 0
    assert all(df["chokyoshi_code"] == sample_chokyoshi_code)


# 生産者マスタのテスト
def test_get_seisansha_master2_sample_data(connection_manager: ConnectionManager) -> None:
    """SEISANSHA_MASTER2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SEISANSHA_MASTER2")
    if len(df) == 0:
        pytest.skip("SEISANSHA_MASTER2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "seisansha_code" in df.columns


def test_get_seisansha_master2_with_seisansha_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SEISANSHA_MASTER2テーブルから生産者コードでフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "SEISANSHA_MASTER2")
    if len(sample_master) == 0:
        pytest.skip("SEISANSHA_MASTER2テーブルにデータがありません")

    sample_seisansha_code = sample_master.iloc[0]["seisansha_code"]

    df = table_accessor.get_table_data(
        "SEISANSHA_MASTER2",
        filters={"seisansha_code": sample_seisansha_code},
    )

    assert len(df) > 0
    assert all(df["seisansha_code"] == sample_seisansha_code)


# 馬主マスタのテスト
def test_get_banushi_master_sample_data(connection_manager: ConnectionManager) -> None:
    """BANUSHI_MASTERテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "BANUSHI_MASTER")
    if len(df) == 0:
        pytest.skip("BANUSHI_MASTERテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "banushi_code" in df.columns


def test_get_banushi_master_with_banushi_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """BANUSHI_MASTERテーブルから馬主コードでフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "BANUSHI_MASTER")
    if len(sample_master) == 0:
        pytest.skip("BANUSHI_MASTERテーブルにデータがありません")

    sample_banushi_code = sample_master.iloc[0]["banushi_code"]

    df = table_accessor.get_table_data(
        "BANUSHI_MASTER",
        filters={"banushi_code": sample_banushi_code},
    )

    assert len(df) > 0
    assert all(df["banushi_code"] == sample_banushi_code)


# 繁殖馬マスタのテスト
def test_get_hanshokuba_master2_sample_data(connection_manager: ConnectionManager) -> None:
    """HANSHOKUBA_MASTER2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HANSHOKUBA_MASTER2")
    if len(df) == 0:
        pytest.skip("HANSHOKUBA_MASTER2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "hanshoku_toroku_bango" in df.columns


def test_get_hanshokuba_master2_with_hanshoku_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HANSHOKUBA_MASTER2テーブルから繁殖登録番号でフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "HANSHOKUBA_MASTER2")
    if len(sample_master) == 0:
        pytest.skip("HANSHOKUBA_MASTER2テーブルにデータがありません")

    sample_hanshoku_bango = sample_master.iloc[0]["hanshoku_toroku_bango"]

    df = table_accessor.get_table_data(
        "HANSHOKUBA_MASTER2",
        filters={"hanshoku_toroku_bango": sample_hanshoku_bango},
    )

    assert len(df) > 0
    assert all(df["hanshoku_toroku_bango"] == sample_hanshoku_bango)


# 産駒マスタのテスト
def test_get_sanku_master2_sample_data(connection_manager: ConnectionManager) -> None:
    """SANKU_MASTER2テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SANKU_MASTER2")
    if len(df) == 0:
        pytest.skip("SANKU_MASTER2テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    # 産駒マスタは血統登録番号を使用
    assert "ketto_toroku_bango" in df.columns


def test_get_sanku_master2_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SANKU_MASTER2テーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SANKU_MASTER2")
    if len(sample_data) == 0:
        pytest.skip("SANKU_MASTER2テーブルにデータがありません")

    sample_ketto_bango = sample_data.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "SANKU_MASTER2",
        filters={"ketto_toroku_bango": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


# レコードマスタのテスト
def test_get_record_master_sample_data(connection_manager: ConnectionManager) -> None:
    """RECORD_MASTERテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "RECORD_MASTER")
    if len(df) == 0:
        pytest.skip("RECORD_MASTERテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "keibajo_code" in df.columns


def test_get_record_master_with_keibajo_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """RECORD_MASTERテーブルから競馬場コードでフィルタしてデータを取得できることを確認."""
    sample_master = get_sample_data(connection_manager, "RECORD_MASTER")
    if len(sample_master) == 0:
        pytest.skip("RECORD_MASTERテーブルにデータがありません")

    sample_keibajo_code = sample_master.iloc[0]["keibajo_code"]

    df = table_accessor.get_table_data(
        "RECORD_MASTER",
        filters={"keibajo_code": sample_keibajo_code},
    )

    assert len(df) > 0
    assert all(df["keibajo_code"] == sample_keibajo_code)


# 準正常系
def test_get_kyosoba_master2_with_nonexistent_ketto_bango(
    table_accessor: TableAccessor,
) -> None:
    """存在しない血統登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KYOSOBA_MASTER2",
        filters={"ketto_toroku_bango": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_kishu_master_with_nonexistent_kishu_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しない騎手コードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KISHU_MASTER",
        filters={"kishu_code": "99999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
