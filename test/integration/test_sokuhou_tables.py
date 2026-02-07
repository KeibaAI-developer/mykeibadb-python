"""速報テーブルの結合テスト.

KYOSOBA_JOGAI_JOHO（競走馬除外情報）、BATAIJU（馬体重）、TENKO_BABA_JOTAI（天候馬場状態）、
SHUSSOTORIKESHI_KYOSOJOGAI（出走取消競走除外）、KISHU_HENKO（騎手変更）、
HASSOJIKOKU_HENKO（発走時刻変更）、COURSE_HENKO（コース変更）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 競走馬除外情報テーブルのテスト
def test_get_kyosoba_jogai_joho_sample_data(connection_manager: ConnectionManager) -> None:
    """KYOSOBA_JOGAI_JOHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KYOSOBA_JOGAI_JOHO")
    if len(df) == 0:
        pytest.skip("KYOSOBA_JOGAI_JOHOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "ketto_toroku_bango" in df.columns


def test_get_kyosoba_jogai_joho_with_ketto_bango_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KYOSOBA_JOGAI_JOHOテーブルから血統登録番号でフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "KYOSOBA_JOGAI_JOHO")
    if len(sample_data) == 0:
        pytest.skip("KYOSOBA_JOGAI_JOHOテーブルにデータがありません")

    sample_ketto_bango = sample_data.iloc[0]["ketto_toroku_bango"]

    df = table_accessor.get_table_data(
        "KYOSOBA_JOGAI_JOHO",
        filters={"ketto_toroku_bango": sample_ketto_bango},
    )

    assert len(df) > 0
    assert all(df["ketto_toroku_bango"] == sample_ketto_bango)


# 馬体重テーブルのテスト
def test_get_bataiju_sample_data(connection_manager: ConnectionManager) -> None:
    """BATAIJUテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "BATAIJU")
    if len(df) == 0:
        pytest.skip("BATAIJUテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_bataiju_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """BATAIJUテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "BATAIJU")
    if len(sample_data) == 0:
        pytest.skip("BATAIJUテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "BATAIJU",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


def test_get_bataiju_has_weight_column(connection_manager: ConnectionManager) -> None:
    """BATAIJUテーブルに体重関連カラムがあることを確認."""
    df = get_sample_data(connection_manager, "BATAIJU")
    if len(df) == 0:
        pytest.skip("BATAIJUテーブルにデータがありません")

    # 馬番は umaban1, umaban2, ... という形式
    assert "umaban1" in df.columns


# 天候馬場状態テーブルのテスト
def test_get_tenko_baba_jotai_sample_data(connection_manager: ConnectionManager) -> None:
    """TENKO_BABA_JOTAIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "TENKO_BABA_JOTAI")
    if len(df) == 0:
        pytest.skip("TENKO_BABA_JOTAIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) > 0


# 出走取消競走除外テーブルのテスト
def test_get_shussotorikeshi_kyosojogai_sample_data(connection_manager: ConnectionManager) -> None:
    """SHUSSOTORIKESHI_KYOSOJOGAIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "SHUSSOTORIKESHI_KYOSOJOGAI")
    if len(df) == 0:
        pytest.skip("SHUSSOTORIKESHI_KYOSOJOGAIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_shussotorikeshi_kyosojogai_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """SHUSSOTORIKESHI_KYOSOJOGAIテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "SHUSSOTORIKESHI_KYOSOJOGAI")
    if len(sample_data) == 0:
        pytest.skip("SHUSSOTORIKESHI_KYOSOJOGAIテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "SHUSSOTORIKESHI_KYOSOJOGAI",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 騎手変更テーブルのテスト
def test_get_kishu_henko_sample_data(connection_manager: ConnectionManager) -> None:
    """KISHU_HENKOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "KISHU_HENKO")
    if len(df) == 0:
        pytest.skip("KISHU_HENKOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_kishu_henko_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """KISHU_HENKOテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "KISHU_HENKO")
    if len(sample_data) == 0:
        pytest.skip("KISHU_HENKOテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "KISHU_HENKO",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 発走時刻変更テーブルのテスト
def test_get_hassojikoku_henko_sample_data(connection_manager: ConnectionManager) -> None:
    """HASSOJIKOKU_HENKOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "HASSOJIKOKU_HENKO")
    if len(df) == 0:
        pytest.skip("HASSOJIKOKU_HENKOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_hassojikoku_henko_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """HASSOJIKOKU_HENKOテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "HASSOJIKOKU_HENKO")
    if len(sample_data) == 0:
        pytest.skip("HASSOJIKOKU_HENKOテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "HASSOJIKOKU_HENKO",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# コース変更テーブルのテスト
def test_get_course_henko_sample_data(connection_manager: ConnectionManager) -> None:
    """COURSE_HENKOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "COURSE_HENKO")
    if len(df) == 0:
        pytest.skip("COURSE_HENKOテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert "race_code" in df.columns


def test_get_course_henko_with_race_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """COURSE_HENKOテーブルからレースコードでフィルタしてデータを取得できることを確認."""
    sample_data = get_sample_data(connection_manager, "COURSE_HENKO")
    if len(sample_data) == 0:
        pytest.skip("COURSE_HENKOテーブルにデータがありません")

    sample_race_code = sample_data.iloc[0]["race_code"]

    df = table_accessor.get_table_data(
        "COURSE_HENKO",
        filters={"race_code": sample_race_code},
    )

    assert len(df) > 0
    assert all(df["race_code"] == sample_race_code)


# 準正常系
def test_get_bataiju_with_nonexistent_race_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "BATAIJU",
        filters={"race_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_kishu_henko_with_nonexistent_race_code(
    table_accessor: TableAccessor,
) -> None:
    """存在しないレースコードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "KISHU_HENKO",
        filters={"race_code": "999999999999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
