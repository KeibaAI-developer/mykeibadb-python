"""haraimodoshiテーブルのデータ件数検証テスト.

JRA公式発表の年間レース数と、mykeibadbのharaimodoshiテーブルの
中央競馬レコード数が一致しているかを検証する。
mykeibadb-pythonのコードは使用せず、直接SQLで確認する。

CIでは実行されない（test/unit/のみがCI対象）。
"""

import psycopg2.extensions
import pytest

from .conftest import JRA_OFFICIAL_RACE_COUNT


def _get_haraimodoshi_count(conn: psycopg2.extensions.connection, year: str) -> int:
    """指定年の中央競馬レース数をharaimodoshiテーブルから取得."""
    query = """
        SELECT COUNT(*) AS race_count
        FROM haraimodoshi
        WHERE TRIM(kaisai_nen) = %s
          AND TRIM(keibajo_code) BETWEEN '01' AND '10'
          AND TRIM(data_kubun) = '2'
    """
    with conn.cursor() as cur:
        cur.execute(query, (year,))
        row = cur.fetchone()
        return int(row[0])


@pytest.mark.parametrize(
    "year, expected_count",
    list(JRA_OFFICIAL_RACE_COUNT.items()),
    ids=[f"{y}年" for y in JRA_OFFICIAL_RACE_COUNT],
)
def test_haraimodoshi_count_matches_jra_official(
    db_connection: psycopg2.extensions.connection, year: str, expected_count: int
) -> None:
    """haraimodoshiのレース数がJRA公式発表と一致することを確認."""
    actual_count = _get_haraimodoshi_count(db_connection, year)
    assert (
        actual_count == expected_count
    ), f"{year}年: haraimodoshiのレース数が{actual_count}件（期待値: {expected_count}件）"
