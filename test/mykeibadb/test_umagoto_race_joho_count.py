"""umagoto_race_johoテーブルのデータ件数検証テスト.

JRA公式発表の年間延べ出走頭数と、mykeibadbのumagoto_race_johoテーブルの
中央競馬レコード数が一致しているかを検証する。
mykeibadb-pythonのコードは使用せず、直接SQLで確認する。

CIでは実行されない（test/unit/のみがCI対象）。
"""

import psycopg2.extensions
import pytest

from .conftest import JRA_OFFICIAL_HORSE_COUNT


def _get_horse_count(conn: psycopg2.extensions.connection, year: str) -> int:
    """指定年の中央競馬延べ出走頭数をumagoto_race_johoテーブルから取得.

    JRA公式の「延べ出走頭数」は出走取消・発走除外を除いた頭数のため、
    ijo_kubun_codeが1（出走取消）と3（発走除外）を除外する。
    """
    query = """
        SELECT COUNT(*) AS horse_count
        FROM umagoto_race_joho
        WHERE TRIM(kaisai_nen) = %s
          AND TRIM(keibajo_code) BETWEEN '01' AND '10'
          AND TRIM(data_kubun) = '7'
          AND TRIM(ijo_kubun_code) NOT IN ('1', '3')
    """
    with conn.cursor() as cur:
        cur.execute(query, (year,))
        row = cur.fetchone()
        return int(row[0])


@pytest.mark.parametrize(
    "year, expected_count",
    list(JRA_OFFICIAL_HORSE_COUNT.items()),
    ids=[f"{y}年" for y in JRA_OFFICIAL_HORSE_COUNT],
)
def test_umagoto_race_joho_count_matches_jra_official(
    db_connection: psycopg2.extensions.connection, year: str, expected_count: int
) -> None:
    """umagoto_race_johoの出走頭数がJRA公式発表と一致することを確認."""
    actual_count = _get_horse_count(db_connection, year)
    assert (
        actual_count == expected_count
    ), f"{year}年: umagoto_race_johoの出走頭数が{actual_count}件（期待値: {expected_count}件）"
