"""コース情報テーブルの結合テスト.

COURSE_JOHOテーブルへのアクセスをテストする。
PostgreSQLのカラム名は小文字で返されるため、小文字で確認する。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

from .conftest import get_sample_data


# 正常系
def test_get_course_joho_sample_data(connection_manager: ConnectionManager) -> None:
    """COURSE_JOHOテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "COURSE_JOHO")

    assert isinstance(df, pd.DataFrame)
    assert "keibajo_code" in df.columns
    assert "kyori" in df.columns
    assert "track_code" in df.columns


def test_get_course_joho_with_keibajo_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """COURSE_JOHOテーブルから競馬場コードでフィルタしてデータを取得できることを確認."""
    sample_courses = get_sample_data(connection_manager, "COURSE_JOHO")
    if len(sample_courses) == 0:
        pytest.skip("COURSE_JOHOテーブルにデータがありません")

    sample_keibajo_code = sample_courses.iloc[0]["keibajo_code"]

    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={"KEIBAJO_CODE": sample_keibajo_code},
    )

    assert len(df) > 0
    assert all(df["keibajo_code"] == sample_keibajo_code)


def test_get_course_joho_with_kyori_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """COURSE_JOHOテーブルから距離でフィルタしてデータを取得できることを確認."""
    sample_courses = get_sample_data(connection_manager, "COURSE_JOHO")
    if len(sample_courses) == 0:
        pytest.skip("COURSE_JOHOテーブルにデータがありません")

    sample_kyori = sample_courses.iloc[0]["kyori"]

    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={"KYORI": sample_kyori},
    )

    assert len(df) > 0


def test_get_course_joho_with_track_code_filter(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """COURSE_JOHOテーブルからトラックコードでフィルタしてデータを取得できることを確認."""
    sample_courses = get_sample_data(connection_manager, "COURSE_JOHO")
    if len(sample_courses) == 0:
        pytest.skip("COURSE_JOHOテーブルにデータがありません")

    sample_track_code = sample_courses.iloc[0]["track_code"]

    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={"TRACK_CODE": sample_track_code},
    )

    assert len(df) > 0
    assert all(df["track_code"] == sample_track_code)


def test_get_course_joho_with_compound_filters(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """COURSE_JOHOテーブルから複合フィルタでデータを取得できることを確認."""
    sample_courses = get_sample_data(connection_manager, "COURSE_JOHO")
    if len(sample_courses) == 0:
        pytest.skip("COURSE_JOHOテーブルにデータがありません")

    sample_keibajo_code = sample_courses.iloc[0]["keibajo_code"]
    sample_kyori = sample_courses.iloc[0]["kyori"]

    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={
            "KEIBAJO_CODE": sample_keibajo_code,
            "KYORI": sample_kyori,
        },
    )

    assert len(df) > 0
    assert all(df["keibajo_code"] == sample_keibajo_code)


def test_get_course_joho_with_multiple_keibajo_codes(
    table_accessor: TableAccessor,
    connection_manager: ConnectionManager,
) -> None:
    """COURSE_JOHOテーブルから複数の競馬場コードでフィルタしてデータを取得できることを確認."""
    sample_courses = get_sample_data(connection_manager, "COURSE_JOHO")
    if len(sample_courses) < 2:
        pytest.skip("COURSE_JOHOテーブルに十分なデータがありません")

    unique_keibajo_codes = sample_courses["keibajo_code"].unique()
    if len(unique_keibajo_codes) < 2:
        pytest.skip("異なる競馬場コードが2つ以上必要です")

    keibajo_codes = list(unique_keibajo_codes[:2])

    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={"KEIBAJO_CODE": keibajo_codes},
    )

    assert len(df) > 0
    assert all(code in keibajo_codes for code in df["keibajo_code"])


# 準正常系
def test_get_course_joho_with_nonexistent_keibajo_code(table_accessor: TableAccessor) -> None:
    """存在しない競馬場コードでフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={"KEIBAJO_CODE": "99"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_get_course_joho_with_nonexistent_kyori(table_accessor: TableAccessor) -> None:
    """存在しない距離でフィルタすると空のDataFrameが返ることを確認."""
    df = table_accessor.get_table_data(
        "COURSE_JOHO",
        filters={"KYORI": "99999"},
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
