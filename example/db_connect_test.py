"""PostgreSQL接続テストスクリプト.

.envファイルから接続情報を取得してPostgreSQLへの接続をテストする。
既存のmykeibadbモジュールを使用して接続を確認する。
"""

from mykeibadb.config import ConfigManager
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBConnectionError, QueryExecutionError


def test_connection() -> None:
    """データベース接続をテストする.

    .envファイルから接続情報を読み込み、PostgreSQLへの接続をテストする。
    接続に成功した場合は、バージョン情報を取得して表示する。

    Raises:
        MykeibaDBConnectionError: データベース接続に失敗した場合
        QueryExecutionError: クエリ実行に失敗した場合
        Exception: その他の予期しないエラーが発生した場合
    """
    try:
        # .envから設定を読み込む
        config = ConfigManager.from_env()
        print(f"接続先: {config.host}:{config.port}/{config.database}")
        print(f"ユーザー: {config.user}")

        # 接続マネージャーをwithステートメントで使用し、自動的にクローズする
        with ConnectionManager(config) as conn_manager:
            print("✓ 接続プール作成成功")

            # 簡単なクエリを実行してバージョンを取得
            result = conn_manager.execute_query("SELECT version();")
            version = result[0][0]
            print("✓ クエリ実行成功")
            print(f"PostgreSQLバージョン: {version}")

            # テーブル数を取得
            table_count_query = """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """
            result = conn_manager.execute_query(table_count_query)
            table_count = result[0][0]
            print(f"✓ publicスキーマのテーブル数: {table_count}")

        print("\n接続テスト成功！")

    except MykeibaDBConnectionError as e:
        print(f"✗ 接続失敗: {e}")
        raise
    except QueryExecutionError as e:
        print(f"✗ クエリ実行失敗: {e}")
        raise
    except Exception as e:
        print(f"✗ 予期しないエラー: {e}")
        raise


if __name__ == "__main__":
    test_connection()
