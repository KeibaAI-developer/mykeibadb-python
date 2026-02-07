"""調教データテーブルの結合テスト.

HANRO_CHOKYO（坂路調教）、WOODCHIP_CHOKYO（ウッドチップ調教）
テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 坂路調教テーブル（HANRO_CHOKYO）のテスト
# 正常系
def test_get_hanro_chokyo_sample_data(connection_manager: ConnectionManager) -> None:
    """HANRO_CHOKYOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HANRO_CHOKYO")

    assert isinstance(df, pd.DataFrame)
    assert "ketto_toroku_bango" in df.columns
    assert "chokyo_nengappi" in df.columns
    assert "tracen_kubun" in df.columns


def test_get_hanro_chokyo_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HANRO_CHOKYOテーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "HANRO_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("HANRO_CHOKYOテーブルにデータがありません")

    sample_ketto_bango = sample_chokyo.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={"KETTO_TOROKU_BANGO": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


def test_get_hanro_chokyo_with_tracen_kubun_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HANRO_CHOKYOテーブルからトレセン区分でフィルタしてデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "HANRO_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("HANRO_CHOKYOテーブルにデータがありません")

    sample_tracen_kubun = sample_chokyo.iloc[0]["tracen_kubun"]

    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={"TRACEN_KUBUN": sample_tracen_kubun},
    )

    assert len(df) > 0
    assert all(df["tracen_kubun"] == sample_tracen_kubun)


def test_get_hanro_chokyo_with_chokyo_nengappi_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HANRO_CHOKYOテーブルから調教年月日でフィルタしてデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "HANRO_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("HANRO_CHOKYOテーブルにデータがありません")

    sample_nengappi = sample_chokyo.iloc[0]["chokyo_nengappi"]

    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={"CHOKYO_NENGAPPI": sample_nengappi},
    )

    assert len(df) > 0
    assert all(df["chokyo_nengappi"] == sample_nengappi)


def test_get_hanro_chokyo_with_compound_filters(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HANRO_CHOKYOテーブルから複合フィルタでデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "HANRO_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("HANRO_CHOKYOテーブルにデータがありません")

    sample_ketto_bango = sample_chokyo.iloc[0]["ketto_toroku_bango"]
    sample_nengappi = sample_chokyo.iloc[0]["chokyo_nengappi"]

    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={
            "KETTO_TOROKU_BANGO": sample_ketto_bango,
            "CHOKYO_NENGAPPI": sample_nengappi,
        },
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


# ウッドチップ調教テーブル（WOODCHIP_CHOKYO）のテスト
def test_get_woodchip_chokyo_sample_data(connection_manager: ConnectionManager) -> None:
    """WOODCHIP_CHOKYOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "WOODCHIP_CHOKYO")

    assert isinstance(df, pd.DataFrame)
    assert "ketto_toroku_bango" in df.columns


def test_get_woodchip_chokyo_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """WOODCHIP_CHOKYOテーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "WOODCHIP_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("WOODCHIP_CHOKYOテーブルにデータがありません")

    sample_ketto_bango = sample_chokyo.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "WOODCHIP_CHOKYO",
        filters={"KETTO_TOROKU_BANGO": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


def test_get_woodchip_chokyo_with_tracen_kubun_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """WOODCHIP_CHOKYOテーブルからトレセン区分でフィルタしてデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "WOODCHIP_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("WOODCHIP_CHOKYOテーブルにデータがありません")

    sample_tracen_kubun = sample_chokyo.iloc[0]["tracen_kubun"]

    df = table_accessor.get_table_data(
        "WOODCHIP_CHOKYO",
        filters={"TRACEN_KUBUN": sample_tracen_kubun},
    )

    assert len(df) > 0
    assert all(df["tracen_kubun"] == sample_tracen_kubun)


def test_get_woodchip_chokyo_with_compound_filters(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """WOODCHIP_CHOKYOテーブルから複合フィルタでデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "WOODCHIP_CHOKYO")
    if len(sample_chokyo) == 0:
        pytest.skip("WOODCHIP_CHOKYOテーブルにデータがありません")

    sample_ketto_bango = sample_chokyo.iloc[0]["ketto_toroku_bango"]
    sample_tracen_kubun = sample_chokyo.iloc[0]["tracen_kubun"]

    df = table_accessor.get_table_data(
        "WOODCHIP_CHOKYO",
        filters={
            "KETTO_TOROKU_BANGO": sample_ketto_bango,
            "TRACEN_KUBUN": sample_tracen_kubun,
        },
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


# 複数の血統登録番号でのフィルタテスト
def test_get_hanro_chokyo_with_multiple_ketto_bangos(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HANRO_CHOKYOテーブルから複数の血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_chokyo = get_sample_data(connection_manager, "HANRO_CHOKYO")
    if len(sample_chokyo) < 2:
        pytest.skip("HANRO_CHOKYOテーブルに十分なデータがありません")

    unique_ketto_bangos = sample_chokyo["ketto_toroku_bango"].unique()
    if len(unique_ketto_bangos) < 2:
        pytest.skip("異なる血統登録番号が2つ以上必要です")

    ketto_bangos = list(unique_ketto_bangos[:2])

    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={"KETTO_TOROKU_BANGO": ketto_bangos},
    )

    assert len(df) > 0
    assert all(bango in ketto_bangos for bango in df["ketto_toroku_bango"])


# 準正常系
def test_get_hanro_chokyo_with_nonexistent_ketto_bango(table_accessor: TableAccessor) -> None:
    """存在しない血統登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={"KETTO_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_woodchip_chokyo_with_nonexistent_ketto_bango(table_accessor: TableAccessor) -> None:
    """存在しない血統登録番号でWOODCHIP_CHOKYOをフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "WOODCHIP_CHOKYO",
        filters={"KETTO_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_hanro_chokyo_with_future_date(table_accessor: TableAccessor) -> None:
    """未来の調教年月日でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "HANRO_CHOKYO",
        filters={"CHOKYO_NENGAPPI": "20991231"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
