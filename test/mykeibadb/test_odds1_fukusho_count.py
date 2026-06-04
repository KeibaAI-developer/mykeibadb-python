"""odds1_fukushoテーブルのデータ件数検証テスト.

年間登録出走頭数（出走取消・発走除外含む）と、mykeibadbのodds1_fukushoテーブルの
中央競馬レコード数が一致しているかを検証する。
mykeibadb-pythonのコードは使用せず、直接SQLで確認する。

CIでは実行されない（test/unit/のみがCI対象）。
"""

import psycopg2.extensions
import pytest

from .conftest import JRA_REGISTERED_HORSE_COUNT


def _get_odds1_fukusho_count(conn: psycopg2.extensions.connection, year: str) -> int:
    """指定年の中央競馬の延べ出走頭数をodds1_fukushoテーブルから取得."""
    query = """
        SELECT COUNT(*) AS horse_count
        FROM odds1_fukusho
        WHERE TRIM(kaisai_nen) = %s
          AND TRIM(keibajo_code) BETWEEN '01' AND '10'
          AND TRIM(data_kubun) = '5'
    """
    with conn.cursor() as cur:
        cur.execute(query, (year,))
        row = cur.fetchone()
        return int(row[0])


@pytest.mark.parametrize(
    "year, expected_count",
    list(JRA_REGISTERED_HORSE_COUNT.items()),
    ids=[f"{y}年" for y in JRA_REGISTERED_HORSE_COUNT],
)
def test_odds1_fukusho_count_matches_jra_official(
    db_connection: psycopg2.extensions.connection, year: str, expected_count: int
) -> None:
    """odds1_fukushoの出走頭数がJRA公式発表と一致することを確認."""
    actual_count = _get_odds1_fukusho_count(db_connection, year)
    assert (
        actual_count == expected_count
    ), f"{year}年: odds1_fukushoの出走頭数が{actual_count}件（期待値: {expected_count}件）"
