"""基底Getterクラス.

すべてのGetterクラスが継承する基底クラスを提供する。
共通の初期化処理とヘルパーメソッドを含む。
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.config import ConfigManager, DBConfig
from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor


class BaseGetter:
    """すべてのGetterクラスの基底クラス.

    各テーブルに対してキーや期間を指定してデータを取得するメソッドを提供する。

    Attributes:
        connection_manager (ConnectionManager): データベース接続マネージャー
        table_accessor (TableAccessor): テーブルアクセサー
    """

    def __init__(self, config: DBConfig | None = None) -> None:
        """Getterクラスを初期化.

        Args:
            config (DBConfig | None): データベース設定。
                Noneの場合は環境変数から設定を読み込む。
        """
        config = ConfigManager.from_env() if config is None else config
        self.connection_manager = ConnectionManager(config)
        self.table_accessor = TableAccessor(self.connection_manager)

    def _get_table_with_period(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        date_column: str = "KAISAI_NENGAPPI",
    ) -> pd.DataFrame:
        """期間フィルタ付きでテーブルデータを取得.

        単一の日付カラム（yyyymmdd形式）に対して期間フィルタを適用する。
        フィルタのバリデーションとTRIM処理はTableAccessorと同様に行われる。

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any] | None): フィルタ条件
            start_date (date | None): 開始日
            end_date (date | None): 終了日
            date_column (str): 日付カラム名（yyyymmdd形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            TableNotFoundError: テーブルが存在しない場合
            InvalidFilterError: 無効なフィルタ条件や日付カラム名の場合
        """
        # 期間フィルタがない場合は通常の取得
        if not start_date and not end_date:
            return self.table_accessor.get_table_data(table_name, filters)

        return self.table_accessor.get_table_data_with_period(
            table_name, filters, start_date, end_date, date_column
        )

    def _get_table_with_year_only_period(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        year_column: str = "SEINEN",
    ) -> pd.DataFrame:
        """年のみのカラムを持つテーブルから期間フィルタ付きでデータを取得.

        年カラム（yyyy形式）に対して期間フィルタを適用する。
        フィルタのバリデーションとTRIM処理はTableAccessorと同様に行われる。

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any] | None): フィルタ条件
            start_date (date | None): 開始日（年のみ使用）
            end_date (date | None): 終了日（年のみ使用）
            year_column (str): 年カラム名（yyyy形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            TableNotFoundError: テーブルが存在しない場合
            InvalidFilterError: 無効なフィルタ条件や年カラム名の場合
        """
        # 期間フィルタがない場合は通常の取得
        if not start_date and not end_date:
            return self.table_accessor.get_table_data(table_name, filters)

        return self.table_accessor.get_table_data_with_year_only_period(
            table_name, filters, start_date, end_date, year_column
        )

    def _get_table_with_period_composite_date(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        year_column: str = "KAISAI_NEN",
        date_column: str = "KAISAI_GAPPI",
    ) -> pd.DataFrame:
        """年月日が分離されたカラムを持つテーブルから期間フィルタ付きでデータを取得.

        年カラム（yyyy形式）と月日カラム（mmdd形式）を結合して期間フィルタを適用する。
        フィルタのバリデーションとTRIM処理はTableAccessorと同様に行われる。

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any] | None): フィルタ条件
            start_date (date | None): 開始日
            end_date (date | None): 終了日
            year_column (str): 年カラム名（yyyy形式）
            date_column (str): 月日カラム名（mmdd形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            TableNotFoundError: テーブルが存在しない場合
            InvalidFilterError: 無効なフィルタ条件やカラム名の場合
        """
        # 期間フィルタがない場合は通常の取得
        if not start_date and not end_date:
            return self.table_accessor.get_table_data(table_name, filters)

        return self.table_accessor.get_table_data_with_composite_date_period(
            table_name, filters, start_date, end_date, year_column, date_column
        )
