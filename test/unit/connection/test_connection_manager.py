"""ConnectionManagerクラスの単体テスト.

ConnectionManagerクラスの各メソッドに対するテストを実装する。
外部依存（PostgreSQL）はモックを使用して排除する。
"""

from unittest.mock import MagicMock, patch

import pandas as pd
import psycopg2
import pytest

from mykeibadb.config import DBConfig
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBConnectionError, QueryExecutionError


@pytest.fixture
def db_config() -> DBConfig:
    """テスト用のDBConfig fixture."""
    return DBConfig(
        host="localhost",
        port=5432,
        database="test_db",
        user="test_user",
        password="test_password",
    )


@pytest.fixture
def mock_pool() -> MagicMock:
    """モックの接続プール fixture."""
    mock = MagicMock()
    return mock


# 正常系
def test_init_creates_connection_pool(db_config: DBConfig) -> None:
    """初期化時に接続プールが作成されることを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.return_value = MagicMock()

        manager = ConnectionManager(db_config)

        mock_pool_class.assert_called_once_with(
            minconn=ConnectionManager.MIN_CONNECTIONS,
            maxconn=ConnectionManager.MAX_CONNECTIONS,
            host=db_config.host,
            port=db_config.port,
            dbname=db_config.database,
            user=db_config.user,
            password=db_config.password,
        )
        assert manager.is_connected is True


def test_execute_query_returns_results(db_config: DBConfig) -> None:
    """execute_queryがクエリ結果を正しく返すことを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("value1", 1), ("value2", 2)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_conn
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)
        result = manager.execute_query("SELECT * FROM test_table")

        assert result == [("value1", 1), ("value2", 2)]
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test_table", None)
        mock_pool.putconn.assert_called_once_with(mock_conn)


def test_execute_query_with_params(db_config: DBConfig) -> None:
    """execute_queryがパラメータ付きクエリを正しく実行することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("value1",)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_conn
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)
        result = manager.execute_query(
            "SELECT * FROM test_table WHERE id = %s",
            params=("123",),
        )

        assert result == [("value1",)]
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM test_table WHERE id = %s",
            ("123",),
        )


def test_fetch_dataframe_returns_dataframe(db_config: DBConfig) -> None:
    """fetch_dataframeがDataFrameを正しく返すことを確認."""
    expected_df = pd.DataFrame({"col1": ["a", "b"], "col2": [1, 2]})

    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        with patch("mykeibadb.connection.pd.read_sql_query") as mock_read_sql:
            mock_pool = MagicMock()
            mock_conn = MagicMock()
            mock_pool.getconn.return_value = mock_conn
            mock_pool_class.return_value = mock_pool
            mock_read_sql.return_value = expected_df

            manager = ConnectionManager(db_config)
            result = manager.fetch_dataframe("SELECT * FROM test_table")

            pd.testing.assert_frame_equal(result, expected_df)
            mock_read_sql.assert_called_once_with(
                "SELECT * FROM test_table",
                mock_conn,
                params=None,
            )
            mock_pool.putconn.assert_called_once_with(mock_conn)


def test_fetch_dataframe_with_params(db_config: DBConfig) -> None:
    """fetch_dataframeがパラメータ付きクエリを正しく実行することを確認."""
    expected_df = pd.DataFrame({"col1": ["a"]})

    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        with patch("mykeibadb.connection.pd.read_sql_query") as mock_read_sql:
            mock_pool = MagicMock()
            mock_conn = MagicMock()
            mock_pool.getconn.return_value = mock_conn
            mock_pool_class.return_value = mock_pool
            mock_read_sql.return_value = expected_df

            manager = ConnectionManager(db_config)
            result = manager.fetch_dataframe(
                "SELECT * FROM test_table WHERE id = %s",
                params=("123",),
            )

            pd.testing.assert_frame_equal(result, expected_df)
            mock_read_sql.assert_called_once_with(
                "SELECT * FROM test_table WHERE id = %s",
                mock_conn,
                params=("123",),
            )


def test_close_releases_all_connections(db_config: DBConfig) -> None:
    """closeメソッドが全ての接続を解放することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)
        assert manager.is_connected is True

        manager.close()

        mock_pool.closeall.assert_called_once()
        assert manager.is_connected is False


def test_context_manager_closes_connection(db_config: DBConfig) -> None:
    """コンテキストマネージャーが終了時に接続をクローズすることを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        with ConnectionManager(db_config) as manager:
            assert manager.is_connected is True

        mock_pool.closeall.assert_called_once()


def test_is_connected_returns_true_when_pool_exists(db_config: DBConfig) -> None:
    """is_connectedが接続プール存在時にTrueを返すことを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.return_value = MagicMock()

        manager = ConnectionManager(db_config)

        assert manager.is_connected is True


def test_is_connected_returns_false_after_close(db_config: DBConfig) -> None:
    """is_connectedがクローズ後にFalseを返すことを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.return_value = MagicMock()

        manager = ConnectionManager(db_config)
        manager.close()

        assert manager.is_connected is False


def test_close_is_safe_to_call_multiple_times(db_config: DBConfig) -> None:
    """closeを複数回呼び出しても安全であることを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)
        manager.close()
        manager.close()  # 2回目の呼び出し

        # closeallは1回だけ呼ばれる（2回目はpoolがNoneなので呼ばれない）
        mock_pool.closeall.assert_called_once()


# 準正常系
def test_execute_query_raises_error_for_invalid_sql(db_config: DBConfig) -> None:
    """不正なSQLクエリでQueryExecutionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg2.ProgrammingError("構文エラー")
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_conn
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)

        with pytest.raises(QueryExecutionError) as exc_info:
            manager.execute_query("INVALID SQL QUERY")

        assert "SQLクエリの実行に失敗しました" in str(exc_info.value)
        mock_pool.putconn.assert_called_once_with(mock_conn)


def test_execute_query_raises_error_for_nonexistent_table(db_config: DBConfig) -> None:
    """存在しないテーブルへのクエリでQueryExecutionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg2.ProgrammingError(
            'relation "nonexistent_table" does not exist'
        )
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_conn
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)

        with pytest.raises(QueryExecutionError) as exc_info:
            manager.execute_query("SELECT * FROM nonexistent_table")

        assert "SQLクエリの実行に失敗しました" in str(exc_info.value)


def test_fetch_dataframe_raises_error_for_invalid_sql(db_config: DBConfig) -> None:
    """不正なSQLでfetch_dataframeがQueryExecutionErrorを発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        with patch("mykeibadb.connection.pd.read_sql_query") as mock_read_sql:
            mock_pool = MagicMock()
            mock_conn = MagicMock()
            mock_pool.getconn.return_value = mock_conn
            mock_pool_class.return_value = mock_pool
            mock_read_sql.side_effect = psycopg2.ProgrammingError("構文エラー")

            manager = ConnectionManager(db_config)

            with pytest.raises(QueryExecutionError) as exc_info:
                manager.fetch_dataframe("INVALID SQL QUERY")

            assert "SQLクエリの実行に失敗しました" in str(exc_info.value)
            mock_pool.putconn.assert_called_once_with(mock_conn)


def test_init_raises_error_for_invalid_host(db_config: DBConfig) -> None:
    """無効なホスト名でMykeibaDBConnectionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.side_effect = psycopg2.OperationalError("could not connect to server")

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            ConnectionManager(db_config)

        assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)
        assert db_config.host in str(exc_info.value)


def test_init_raises_error_for_invalid_port(db_config: DBConfig) -> None:
    """無効なポート番号でMykeibaDBConnectionErrorが発生することを確認."""
    config = DBConfig(
        host="localhost",
        port=9999,
        database="test_db",
        user="test_user",
        password="test_password",
    )

    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.side_effect = psycopg2.OperationalError("connection refused")

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            ConnectionManager(config)

        assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)


def test_init_raises_error_for_invalid_credentials(db_config: DBConfig) -> None:
    """無効な認証情報でMykeibaDBConnectionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.side_effect = psycopg2.OperationalError("password authentication failed")

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            ConnectionManager(db_config)

        assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)


def test_init_raises_error_for_nonexistent_database(db_config: DBConfig) -> None:
    """存在しないデータベースでMykeibaDBConnectionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.side_effect = psycopg2.OperationalError(
            'database "nonexistent" does not exist'
        )

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            ConnectionManager(db_config)

        assert "PostgreSQLへの接続に失敗しました" in str(exc_info.value)


def test_get_connection_raises_error_when_pool_is_none(db_config: DBConfig) -> None:
    """接続プールがNoneの時に_get_connectionがエラーを発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool_class.return_value = MagicMock()

        manager = ConnectionManager(db_config)
        manager._pool = None

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            manager._get_connection()

        assert "接続プールが初期化されていません" in str(exc_info.value)


# 異常系


def test_execute_query_handles_general_db_error(db_config: DBConfig) -> None:
    """一般的なDBエラーでQueryExecutionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg2.Error("一般的なエラー")
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_conn
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)

        with pytest.raises(QueryExecutionError) as exc_info:
            manager.execute_query("SELECT * FROM test_table")

        assert "クエリ実行中にエラーが発生しました" in str(exc_info.value)


def test_fetch_dataframe_handles_general_db_error(db_config: DBConfig) -> None:
    """一般的なDBエラーでfetch_dataframeがQueryExecutionErrorを発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        with patch("mykeibadb.connection.pd.read_sql_query") as mock_read_sql:
            mock_pool = MagicMock()
            mock_conn = MagicMock()
            mock_pool.getconn.return_value = mock_conn
            mock_pool_class.return_value = mock_pool
            mock_read_sql.side_effect = psycopg2.Error("一般的なエラー")

            manager = ConnectionManager(db_config)

            with pytest.raises(QueryExecutionError) as exc_info:
                manager.fetch_dataframe("SELECT * FROM test_table")

            assert "クエリ実行中にエラーが発生しました" in str(exc_info.value)


def test_context_manager_closes_on_exception(db_config: DBConfig) -> None:
    """例外発生時もコンテキストマネージャーが接続をクローズすることを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        try:
            with ConnectionManager(db_config) as _:
                raise ValueError("テスト用例外")
        except ValueError:
            pass

        mock_pool.closeall.assert_called_once()


def test_get_connection_raises_error_on_pool_error(db_config: DBConfig) -> None:
    """接続プールのgetconnエラーでMykeibaDBConnectionErrorが発生することを確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool.getconn.side_effect = psycopg2.Error("プールエラー")
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            manager._get_connection()

        assert "接続プールからの接続取得に失敗しました" in str(exc_info.value)


def test_execute_query_handles_connection_failure(db_config: DBConfig) -> None:
    """execute_queryで_get_connection()が失敗した場合の動作を確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool.getconn.side_effect = psycopg2.Error("接続取得エラー")
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            manager.execute_query("SELECT * FROM test_table")

        assert "接続プールからの接続取得に失敗しました" in str(exc_info.value)
        # connがNoneのため、putconnは呼ばれない
        mock_pool.putconn.assert_not_called()


def test_fetch_dataframe_handles_connection_failure(db_config: DBConfig) -> None:
    """fetch_dataframeで_get_connection()が失敗した場合の動作を確認."""
    with patch("mykeibadb.connection.pool.SimpleConnectionPool") as mock_pool_class:
        mock_pool = MagicMock()
        mock_pool.getconn.side_effect = psycopg2.Error("接続取得エラー")
        mock_pool_class.return_value = mock_pool

        manager = ConnectionManager(db_config)

        with pytest.raises(MykeibaDBConnectionError) as exc_info:
            manager.fetch_dataframe("SELECT * FROM test_table")

        assert "接続プールからの接続取得に失敗しました" in str(exc_info.value)
        # connがNoneのため、putconnは呼ばれない
        mock_pool.putconn.assert_not_called()
