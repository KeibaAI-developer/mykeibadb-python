"""mykeibadbデータ検証テスト用の共通fixture・定数.

DB接続やJRA公式発表データなど、複数テストファイルで
共有するリソースを定義する。

JRA公式発表データは事業報告書から取得
例）2024年度：https://www.jra.go.jp/company/about/financial/pdf/houkoku06.pdf
"""

import os
from collections.abc import Generator
from pathlib import Path

import psycopg2
import psycopg2.extensions
import pytest
from dotenv import load_dotenv

_env_path = Path(__file__).parent.parent.parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

_DB_HOST = os.getenv("MYKEIBADB_HOST", "localhost")
_DB_PORT = int(os.getenv("MYKEIBADB_PORT", "5432"))
_DB_NAME = os.getenv("MYKEIBADB_DATABASE", "mykeibadb")
_DB_USER = os.getenv("MYKEIBADB_USER", "postgres")
_DB_PASSWORD = os.getenv("MYKEIBADB_PASSWORD", "postgres")


def _is_postgres_available() -> bool:
    """PostgreSQLが利用可能かどうかを確認."""
    try:
        conn = psycopg2.connect(
            host=_DB_HOST,
            port=_DB_PORT,
            database=_DB_NAME,
            user=_DB_USER,
            password=_DB_PASSWORD,
            connect_timeout=5,
        )
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False


pytestmark = pytest.mark.skipif(
    not _is_postgres_available(),
    reason="PostgreSQLに接続できません。mykeibadbが起動していることを確認してください。",
)

# JRA公式発表の年間レース数
JRA_OFFICIAL_RACE_COUNT: dict[str, int] = {
    "2015": 3454,
    "2016": 3454,
    "2017": 3455,
    "2018": 3454,
    "2019": 3452,
    "2020": 3456,
    "2021": 3456,
    "2022": 3456,
    "2023": 3456,
    "2024": 3454,
    "2025": 3455,
}

# JRA公式発表の年間延べ出走頭数
JRA_OFFICIAL_HORSE_COUNT: dict[str, int] = {
    "2015": 49822,
    "2016": 49910,
    "2017": 49148,
    "2018": 48433,
    "2019": 47345,
    "2020": 48127,
    "2021": 47660,
    "2022": 47054,
    "2023": 47493,
    "2024": 46994,
}

# 年間登録出走頭数（出走取消・発走除外を含む全登録頭数）
# オッズデータなど、取消馬を含むテーブルの検証に使用する
# 公式発表はなく、UMAGOTO_RACE_JOHOから算出
JRA_REGISTERED_HORSE_COUNT: dict[str, int] = {
    "2015": 49992,
    "2016": 50076,
    "2017": 49299,
    "2018": 48618,
    "2019": 47574,
    "2020": 48282,
    "2021": 47821,
    "2022": 47220,
    "2023": 47672,
    "2024": 47181,
}

# JRA公式発表の年間開催日数
# 2020年は中山3回2日目が降雪により3R以降が翌々日に継続開催されたため公式発表日数よりも1日多い
JRA_OFFICIAL_KAISAI_COUNT: dict[str, int] = {
    "2015": 288,
    "2016": 288,
    "2017": 288,
    "2018": 288,
    "2019": 288,
    "2020": 289,
    "2021": 288,
    "2022": 288,
    "2023": 288,
    "2024": 288,
    "2025": 288,
}


@pytest.fixture(scope="module")
def db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """PostgreSQL接続fixture.

    Yields:
        psycopg2.extensions.connection: データベース接続オブジェクト
    """
    conn = psycopg2.connect(
        host=_DB_HOST,
        port=_DB_PORT,
        database=_DB_NAME,
        user=_DB_USER,
        password=_DB_PASSWORD,
    )
    yield conn
    conn.close()
