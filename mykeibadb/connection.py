"""DB接続管理モジュール.

このモジュールは、PostgreSQLへの接続管理機能を提供する。
接続プールの管理、クエリ実行、DataFrameへの変換機能を含む。
"""

import warnings
from typing import Any

import pandas as pd
import psycopg2
from pandas.errors import DatabaseError
from psycopg2 import pool

from mykeibadb.config import DBConfig
from mykeibadb.exceptions import MykeibaDBConnectionError, QueryExecutionError


class ConnectionManager:
    """PostgreSQL接続マネージャー.

    PostgreSQLへの接続プールを管理し、クエリ実行機能を提供する。

    Attributes:
        config (DBConfig): データベース接続設定
        _pool (pool.SimpleConnectionPool | None): 接続プールオブジェクト
    """

    # 接続プールのデフォルト設定
    MIN_CONNECTIONS = 1
    MAX_CONNECTIONS = 10

    def __init__(self, config: DBConfig) -> None:
        """接続マネージャーを初期化.

        Args:
            config (DBConfig): データベース接続設定

        Raises:
            MykeibaDBConnectionError: DB接続に失敗した場合
        """
        self.config = config
        self._pool: pool.SimpleConnectionPool | None = None
        self._initialize_pool()

    def execute_query(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        """SQLクエリを実行.

        SELECT文などの結果を返すクエリを実行し、結果をタプルのリストとして返す。

        Args:
            query (str): 実行するSQLクエリ
            params (tuple[Any, ...] | None): クエリパラメータ（プリペアドステートメント用）

        Returns:
            list[tuple[Any, ...]]: クエリ結果のタプルのリスト

        Raises:
            QueryExecutionError: クエリ実行に失敗した場合
            MykeibaDBConnectionError: 接続に失敗した場合
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result: list[tuple[Any, ...]] = cursor.fetchall()
                return result
        except psycopg2.ProgrammingError as e:
            raise QueryExecutionError(f"SQLクエリの実行に失敗しました: {e}. クエリ: {query}") from e
        except psycopg2.Error as e:
            raise QueryExecutionError(f"クエリ実行中にエラーが発生しました: {e}") from e
        finally:
            if conn is not None:
                self._put_connection(conn)

    def fetch_dataframe(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> pd.DataFrame:
        """クエリ結果をDataFrameとして取得.

        SELECT文などの結果を返すクエリを実行し、pandasのDataFrameとして返す。

        Args:
            query (str): 実行するSQLクエリ
            params (QueryParams | None): クエリパラメータ（プリペアドステートメント用）

        Returns:
            pd.DataFrame: クエリ結果のDataFrame

        Raises:
            QueryExecutionError: クエリ実行に失敗した場合
            MykeibaDBConnectionError: 接続に失敗した場合
        """
        conn = None
        try:
            conn = self._get_connection()
            # pandasはpsycopg2接続でも動作するが、UserWarningを抑制
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
                df = pd.read_sql_query(query, conn, params=params)
            return df
        except (psycopg2.ProgrammingError, DatabaseError) as e:
            raise QueryExecutionError(f"SQLクエリの実行に失敗しました: {e}. クエリ: {query}") from e
        except psycopg2.Error as e:
            raise QueryExecutionError(f"クエリ実行中にエラーが発生しました: {e}") from e
        finally:
            if conn is not None:
                self._put_connection(conn)

    def close(self) -> None:
        """接続プールをクローズ.

        全ての接続を解放し、接続プールを閉じる。
        """
        if self._pool is not None:
            self._pool.closeall()
            self._pool = None

    @property
    def is_connected(self) -> bool:
        """接続プールが有効かどうかを確認.

        Returns:
            bool: 接続プールが有効な場合True
        """
        return self._pool is not None

    def _initialize_pool(self) -> None:
        """接続プールを初期化.

        Raises:
            MykeibaDBConnectionError: 接続プールの初期化に失敗した場合
        """
        try:
            self._pool = pool.SimpleConnectionPool(
                minconn=self.MIN_CONNECTIONS,
                maxconn=self.MAX_CONNECTIONS,
                host=self.config.host,
                port=self.config.port,
                dbname=self.config.database,
                user=self.config.user,
                password=self.config.password,
            )
        except psycopg2.OperationalError as e:
            raise MykeibaDBConnectionError(
                f"PostgreSQLへの接続に失敗しました: "
                f"host={self.config.host}, port={self.config.port}, "
                f"database={self.config.database}. 詳細: {e}"
            ) from e
        except psycopg2.Error as e:
            raise MykeibaDBConnectionError(f"接続プールの初期化に失敗しました: {e}") from e

    def _get_connection(self) -> psycopg2.extensions.connection:
        """接続プールから接続を取得.

        Returns:
            psycopg2.extensions.connection: PostgreSQL接続オブジェクト

        Raises:
            MykeibaDBConnectionError: 接続の取得に失敗した場合
        """
        if self._pool is None:
            raise MykeibaDBConnectionError("接続プールが初期化されていません")

        try:
            return self._pool.getconn()
        except psycopg2.Error as e:
            raise MykeibaDBConnectionError(f"接続プールからの接続取得に失敗しました: {e}") from e

    def _put_connection(self, conn: psycopg2.extensions.connection) -> None:
        """接続をプールに返却.

        Args:
            conn (psycopg2.extensions.connection): 返却する接続オブジェクト
        """
        if self._pool is not None:
            self._pool.putconn(conn)

    def __enter__(self) -> "ConnectionManager":
        """コンテキストマネージャーのエントリーポイント.

        Returns:
            ConnectionManager: 自身のインスタンス
        """
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: object | None,
    ) -> None:
        """コンテキストマネージャーの終了処理.

        例外の有無に関わらず、接続プールを確実にクローズする。

        Args:
            _exc_type (type[BaseException] | None): 例外の型（未使用）
            _exc_val (BaseException | None): 例外のインスタンス（未使用）
            _exc_tb (object | None): トレースバック（未使用）
        """
        self.close()
