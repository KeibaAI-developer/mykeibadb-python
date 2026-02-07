"""レース関連テーブルの結合テスト.

RACE_SHOSAI、UMAGOTO_RACE_JOHO、HARAIMODOSHI、TOKUBETSU_TOROKUBA、
TOKUBETSU_TOROKUBAGOTO_JOHOテーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import TableNotFoundError
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 正常系
def test_get_race_shosai_sample_data(connection_manager: ConnectionManager) -> None:
    """RACE_SHOSAIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "RACE_SHOSAI")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "race_code" in df.columns
    assert "keibajo_code" in df.columns
    assert "kyori" in df.columns


def test_get_race_shosai_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """RACE_SHOSAIテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    # サンプルからレースコードを取得
    sample_races = get_sample_data(connection_manager, "RACE_SHOSAI")
    if len(sample_races) == 0:
        pytest.skip("RACE_SHOSAIテーブルにデータがありません")

    sample_race_code = sample_races.iloc[0]["race_code"]

    # レースコードでフィルタして取得
    df = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) == 1
    assert df.iloc[0]["race_code"] == sample_race_code


def test_get_race_shosai_with_multiple_race_codes(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """RACE_SHOSAIテーブルから複数のレースコードでフィルタしてデータを取得できることを確認."""
    sample_races = get_sample_data(connection_manager, "RACE_SHOSAI")
    if len(sample_races) < 2:
        pytest.skip("RACE_SHOSAIテーブルに十分なデータがありません")

    race_codes = [sample_races.iloc[0]["race_code"], sample_races.iloc[1]["race_code"]]

    df = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": race_codes},
    )

    assert len(df) == 2
    assert set(df["race_code"].tolist()) == set(race_codes)


def test_get_race_shosai_with_keibajo_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """RACE_SHOSAIテーブルから競馬場コードでフィルタしてデータを取得できることを確認."""
    sample_races = get_sample_data(connection_manager, "RACE_SHOSAI")
    if len(sample_races) == 0:
        pytest.skip("RACE_SHOSAIテーブルにデータがありません")

    sample_keibajo_code = sample_races.iloc[0]["keibajo_code"]

    df = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"KEIBAJO_CODE": sample_keibajo_code},
    )

    assert len(df) > 0
    assert all(df["keibajo_code"] == sample_keibajo_code)


def test_get_umagoto_race_joho_sample_data(connection_manager: ConnectionManager) -> None:
    """UMAGOTO_RACE_JOHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "UMAGOTO_RACE_JOHO")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "race_code" in df.columns
    assert "umaban" in df.columns
    assert "ketto_toroku_bango" in df.columns


def test_get_umagoto_race_joho_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """UMAGOTO_RACE_JOHOテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_entries = get_sample_data(connection_manager, "UMAGOTO_RACE_JOHO")
    if len(sample_entries) == 0:
        pytest.skip("UMAGOTO_RACE_JOHOテーブルにデータがありません")

    sample_race_code = sample_entries.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_umagoto_race_joho_with_umaban_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """UMAGOTO_RACE_JOHOテーブルから馬番でフィルタしてデータを取得できることを確認."""
    sample_entries = get_sample_data(connection_manager, "UMAGOTO_RACE_JOHO")
    if len(sample_entries) == 0:
        pytest.skip("UMAGOTO_RACE_JOHOテーブルにデータがありません")

    # サンプルから馬番を取得
    sample_race_code = sample_entries.iloc[0]["race_code"]
    sample_umaban = sample_entries.iloc[0]["umaban"]

    # 馬番でフィルタ（文字列型）
    df = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={"RACE_CODE": sample_race_code, "UMABAN": sample_umaban},
    )

    # すべて同じ馬番であることを確認
    assert all(df["umaban"] == sample_umaban)


def test_get_umagoto_race_joho_with_compound_filters(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """UMAGOTO_RACE_JOHOテーブルから複合フィルタでデータを取得できることを確認."""
    sample_entries = get_sample_data(connection_manager, "UMAGOTO_RACE_JOHO")
    if len(sample_entries) == 0:
        pytest.skip("UMAGOTO_RACE_JOHOテーブルにデータがありません")

    sample_race_code = sample_entries.iloc[0]["race_code"]
    sample_umaban = sample_entries.iloc[0]["umaban"]

    df = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={
            "RACE_CODE": sample_race_code,
            "UMABAN": sample_umaban,
        },
    )

    assert len(df) == 1


def test_get_haraimodoshi_sample_data(connection_manager: ConnectionManager) -> None:
    """HARAIMODOSHIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HARAIMODOSHI")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "race_code" in df.columns


def test_get_haraimodoshi_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HARAIMODOSHIテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_haraimodoshi = get_sample_data(connection_manager, "HARAIMODOSHI")
    if len(sample_haraimodoshi) == 0:
        pytest.skip("HARAIMODOSHIテーブルにデータがありません")

    sample_race_code = sample_haraimodoshi.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "HARAIMODOSHI",
        filters={"RACE_CODE": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_tokubetsu_torokuba_sample_data(connection_manager: ConnectionManager) -> None:
    """TOKUBETSU_TOROKUBAテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "TOKUBETSU_TOROKUBA")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_tokubetsu_torokubagoto_joho_sample_data(
    connection_manager: ConnectionManager,
) -> None:
    """TOKUBETSU_TOROKUBAGOTO_JOHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "TOKUBETSU_TOROKUBAGOTO_JOHO")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


# 準正常系
def test_get_race_shosai_with_nonexistent_race_code(table_accessor: TableAccessor) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"RACE_CODE": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_umagoto_race_joho_with_nonexistent_ketto_bango(table_accessor: TableAccessor) -> None:
    """存在しない血統登録番号でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "UMAGOTO_RACE_JOHO",
        filters={"KETTO_TOROKU_BANGO": "ZZZZZZZZZZ"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_nonexistent_race_table_raises_error(table_accessor: TableAccessor) -> None:
    """存在しないテーブル名でTableNotFoundErrorが発生することを確認."""
    with pytest.raises(TableNotFoundError) as exc_info:
        table_accessor.get_table_data("NONEXISTENT_RACE_TABLE")

    assert "サポートされていません" in str(exc_info.value)
