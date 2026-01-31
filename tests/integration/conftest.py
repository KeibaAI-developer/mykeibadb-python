"""結合テスト用の共通fixture.

PostgreSQLへの接続設定や共通のテストデータを提供する。
"""

import os
from collections.abc import Generator

import pandas as pd
import pytest

from mykeibadb.config import DBConfig
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBConnectionError
from mykeibadb.tables import TableAccessor


def _is_postgres_available() -> bool:
    """PostgreSQLが利用可能かどうかを確認."""
    try:
        config = DBConfig(
            host=os.getenv("MYKEIBADB_HOST", "host.docker.internal"),
            port=int(os.getenv("MYKEIBADB_PORT", "5432")),
            database=os.getenv("MYKEIBADB_DATABASE", "mykeibadb"),
            user=os.getenv("MYKEIBADB_USER", "postgres"),
            password=os.getenv("MYKEIBADB_PASSWORD", "postgres"),
        )
        with ConnectionManager(config):
            return True
    except MykeibaDBConnectionError:
        return False


# PostgreSQLが利用不可の場合はスキップ
pytestmark = pytest.mark.skipif(
    not _is_postgres_available(),
    reason="PostgreSQLに接続できません。mykeibadbが起動していることを確認してください。",
)


@pytest.fixture
def db_config() -> DBConfig:
    """テスト用のDBConfig fixture."""
    return DBConfig(
        host=os.getenv("MYKEIBADB_HOST", "host.docker.internal"),
        port=int(os.getenv("MYKEIBADB_PORT", "5432")),
        database=os.getenv("MYKEIBADB_DATABASE", "mykeibadb"),
        user=os.getenv("MYKEIBADB_USER", "postgres"),
        password=os.getenv("MYKEIBADB_PASSWORD", "postgres"),
    )


@pytest.fixture
def connection_manager(db_config: DBConfig) -> Generator[ConnectionManager, None, None]:
    """ConnectionManager fixture.

    テスト終了後に自動的に接続をクローズする。

    Yields:
        ConnectionManager: 接続マネージャーインスタンス
    """
    manager = ConnectionManager(db_config)
    yield manager
    manager.close()


@pytest.fixture
def table_accessor(connection_manager: ConnectionManager) -> TableAccessor:
    """TableAccessor fixture.

    Args:
        connection_manager: ConnectionManager fixture

    Returns:
        TableAccessor: テーブルアクセサーインスタンス
    """
    return TableAccessor(connection_manager)


def get_sample_data(
    connection_manager: ConnectionManager,
    table_name: str,
    limit: int = 10,
) -> pd.DataFrame:
    """テーブルからサンプルデータを取得するヘルパー関数.

    大量データのテーブルから少数のサンプルを取得するために使用する。

    Args:
        connection_manager: データベース接続マネージャー
        table_name: テーブル名
        limit: 取得する行数（デフォルト10）

    Returns:
        pd.DataFrame: サンプルデータ
    """
    query = f"SELECT * FROM {table_name} LIMIT {limit}"  # noqa: S608
    return connection_manager.fetch_dataframe(query)
