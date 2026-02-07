"""ConnectionManagerの結合テスト.

実際のPostgreSQLに接続してConnectionManagerの動作を確認する。
このテストはローカル環境でPostgreSQLが起動している場合のみ実行可能。
"""

import os

import pandas as pd
import pytest

from mykeibadb.config import DBConfig
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBConnectionError, QueryExecutionError


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


# 正常系
def test_connection_manager_connects_successfully(db_config: DBConfig) -> None:
    """ConnectionManagerが正常に接続できることを確認."""
    with ConnectionManager(db_config) as manager:
        assert manager.is_connected is True


def test_execute_query_returns_results(db_config: DBConfig) -> None:
    """execute_queryがクエリ結果を返すことを確認."""
    with ConnectionManager(db_config) as manager:
        result = manager.execute_query("SELECT 1 AS test_value")

        assert len(result) == 1
        assert result[0][0] == 1


def test_execute_query_with_params(db_config: DBConfig) -> None:
    """execute_queryがパラメータ付きクエリを実行できることを確認."""
    with ConnectionManager(db_config) as manager:
        result = manager.execute_query(
            "SELECT %s AS test_value",
            params=("hello",),
        )

        assert len(result) == 1
        assert result[0][0] == "hello"


def test_fetch_dataframe_returns_dataframe(db_config: DBConfig) -> None:
    """fetch_dataframeがDataFrameを返すことを確認."""
    with ConnectionManager(db_config) as manager:
        df = manager.fetch_dataframe("SELECT 1 AS col1, 2 AS col2")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "col1" in df.columns
        assert "col2" in df.columns
        assert df.iloc[0]["col1"] == 1
        assert df.iloc[0]["col2"] == 2


def test_fetch_dataframe_with_params(db_config: DBConfig) -> None:
    """fetch_dataframeがパラメータ付きクエリを実行できることを確認."""
    with ConnectionManager(db_config) as manager:
        df = manager.fetch_dataframe(
            "SELECT %s AS test_value",
            params=("world",),
        )

        assert len(df) == 1
        assert df.iloc[0]["test_value"] == "world"


def test_connection_close_releases_resources(db_config: DBConfig) -> None:
    """closeメソッドがリソースを解放することを確認."""
    manager = ConnectionManager(db_config)
    assert manager.is_connected is True

    manager.close()

    assert manager.is_connected is False


def test_context_manager_auto_closes(db_config: DBConfig) -> None:
    """コンテキストマネージャーが自動的に接続をクローズすることを確認."""
    with ConnectionManager(db_config) as manager:
        connected_inside = manager.is_connected

    assert connected_inside is True
    assert manager.is_connected is False


def test_multiple_queries_in_same_connection(db_config: DBConfig) -> None:
    """同一接続で複数のクエリを実行できることを確認."""
    with ConnectionManager(db_config) as manager:
        result1 = manager.execute_query("SELECT 1 AS num")
        result2 = manager.execute_query("SELECT 2 AS num")
        result3 = manager.execute_query("SELECT 3 AS num")

        assert result1[0][0] == 1
        assert result2[0][0] == 2
        assert result3[0][0] == 3


# 準正常系
def test_execute_query_with_invalid_sql(db_config: DBConfig) -> None:
    """不正なSQLでQueryExecutionErrorが発生することを確認."""
    with ConnectionManager(db_config) as manager:
        with pytest.raises(QueryExecutionError) as exc_info:
            manager.execute_query("INVALID SQL QUERY")

        assert "SQLクエリの実行に失敗しました" in str(exc_info.value)


def test_execute_query_with_nonexistent_table(db_config: DBConfig) -> None:
    """存在しないテーブルへのクエリでQueryExecutionErrorが発生することを確認."""
    with ConnectionManager(db_config) as manager:
        with pytest.raises(QueryExecutionError) as exc_info:
            manager.execute_query("SELECT * FROM nonexistent_table_12345")

        assert "SQLクエリの実行に失敗しました" in str(exc_info.value)


def test_fetch_dataframe_with_invalid_sql(db_config: DBConfig) -> None:
    """不正なSQLでfetch_dataframeがQueryExecutionErrorを発生することを確認."""
    with ConnectionManager(db_config) as manager:
        with pytest.raises(QueryExecutionError) as exc_info:
            manager.fetch_dataframe("INVALID SQL QUERY")

        assert "SQLクエリの実行に失敗しました" in str(exc_info.value)


# 異常系
def test_connection_fails_with_invalid_host() -> None:
    """無効なホスト名で接続エラーが発生することを確認."""
    config = DBConfig(
        host="invalid-host-12345.example.com",
        port=5432,
        database="mykeibadb",
        user="postgres",
        password="postgres",
    )

    with pytest.raises(MykeibaDBConnectionError) as exc_info:
        ConnectionManager(config)

    assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)


def test_connection_fails_with_invalid_port() -> None:
    """無効なポート番号で接続エラーが発生することを確認."""
    config = DBConfig(
        host=os.getenv("MYKEIBADB_HOST", "host.docker.internal"),
        port=59999,
        database="mykeibadb",
        user="postgres",
        password="postgres",
    )

    with pytest.raises(MykeibaDBConnectionError) as exc_info:
        ConnectionManager(config)

    assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)


def test_connection_fails_with_invalid_credentials() -> None:
    """無効な認証情報で接続エラーが発生することを確認."""
    config = DBConfig(
        host=os.getenv("MYKEIBADB_HOST", "host.docker.internal"),
        port=int(os.getenv("MYKEIBADB_PORT", "5432")),
        database=os.getenv("MYKEIBADB_DATABASE", "mykeibadb"),
        user="invalid_user",
        password="invalid_password",
    )

    with pytest.raises(MykeibaDBConnectionError) as exc_info:
        ConnectionManager(config)

    assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)


def test_connection_fails_with_nonexistent_database() -> None:
    """存在しないデータベースで接続エラーが発生することを確認."""
    config = DBConfig(
        host=os.getenv("MYKEIBADB_HOST", "host.docker.internal"),
        port=int(os.getenv("MYKEIBADB_PORT", "5432")),
        database="nonexistent_database_12345",
        user=os.getenv("MYKEIBADB_USER", "postgres"),
        password=os.getenv("MYKEIBADB_PASSWORD", "postgres"),
    )

    with pytest.raises(MykeibaDBConnectionError) as exc_info:
        ConnectionManager(config)

    assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)
