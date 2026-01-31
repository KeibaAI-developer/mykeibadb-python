"""設定管理モジュール.

このモジュールは、mykeibadb-pythonライブラリの設定を管理する。
DB接続設定とSSH接続設定を環境変数や.envファイルから読み込む機能を提供する。
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class DBConfig:
    """データベース接続設定.

    PostgreSQLへの接続に必要な設定情報を保持する。

    Attributes:
        host: PostgreSQLホスト名（デフォルト: localhost）
        port: PostgreSQLポート番号（デフォルト: 5432）
        database: データベース名（デフォルト: mykeibadb）
        user: ユーザー名（デフォルト: postgres）
        password: パスワード（デフォルト: postgres）
    """

    host: str = "localhost"
    port: int = 5432
    database: str = "mykeibadb"
    user: str = "postgres"
    password: str = "postgres"


class ConfigManager:
    """設定マネージャー.

    設定ファイルや環境変数から設定を読み込み、DBConfigやSSHConfigを生成する。
    """

    def __init__(self, config_path: str | None = None) -> None:
        """設定マネージャーを初期化.

        Args:
            config_path: .envファイルのパス（デフォルト: None）
                Noneの場合は、カレントディレクトリから親ディレクトリに向かって.envを探索する
        """
        self.config_path = config_path
        if config_path:
            load_dotenv(config_path)
        else:
            load_dotenv()

    def load_config(self) -> DBConfig:
        """設定を読み込み.

        環境変数または.envファイルからDB接続設定を読み込む。
        環境変数が存在しない場合はデフォルト値を使用する。

        Returns:
            DBConfig: データベース接続設定

        Raises:
            ValueError: ポート番号が範囲外の場合
        """
        return self._create_db_config_from_env()

    @staticmethod
    def from_env() -> DBConfig:
        """環境変数から設定を生成.

        環境変数からDB接続設定を読み込み、DBConfigインスタンスを生成する。
        .envファイルが存在する場合は、それも読み込む。

        Returns:
            DBConfig: データベース接続設定

        Raises:
            ValueError: ポート番号が範囲外の場合
        """
        load_dotenv()
        return ConfigManager._create_db_config_from_env()

    @staticmethod
    def _create_db_config_from_env() -> DBConfig:
        """環境変数からDBConfigを生成する内部ヘルパーメソッド.

        Returns:
            DBConfig: データベース接続設定

        Raises:
            ValueError: ポート番号が範囲外の場合
        """
        port = int(os.getenv("MYKEIBADB_PORT", "5432"))
        if port < 1 or port > 65535:
            raise ValueError(f"ポート番号は1～65535の範囲で指定してください: {port}")

        return DBConfig(
            host=os.getenv("MYKEIBADB_HOST", "localhost"),
            port=port,
            database=os.getenv("MYKEIBADB_DATABASE", "mykeibadb"),
            user=os.getenv("MYKEIBADB_USER", "postgres"),
            password=os.getenv("MYKEIBADB_PASSWORD", "postgres"),
        )
