"""基底Getterクラス.

すべてのGetterクラスが継承する基底クラスを提供する。
共通の初期化処理とヘルパーメソッドを含む。
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.config import ConfigManager, DBConfig
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import InvalidFilterError
from mykeibadb.tables import TableAccessor
from mykeibadb.utils import is_valid_identifier


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

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any] | None): フィルタ条件
            start_date (date | None): 開始日
            end_date (date | None): 終了日
            date_column (str): 日付カラム名（yyyymmdd形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame
        """
        query_filters = dict(filters) if filters else {}

        # 期間フィルタがある場合は別途WHERE句を構築
        if start_date or end_date:
            return self._get_table_with_date_range(
                table_name, query_filters, start_date, end_date, date_column
            )

        return self.table_accessor.get_table_data(table_name, query_filters or None)

    def _get_table_with_date_range(
        self,
        table_name: str,
        filters: dict[str, Any],
        start_date: date | None,
        end_date: date | None,
        date_column: str,
    ) -> pd.DataFrame:
        """期間範囲フィルタ付きでテーブルデータを取得.

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any]): フィルタ条件
            start_date (date | None): 開始日
            end_date (date | None): 終了日
            date_column (str): 日付カラム名

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            InvalidFilterError: テーブル名、カラム名が無効な場合
        """
        # SQLインジェクション対策: 識別子を検証
        if not is_valid_identifier(table_name):
            raise InvalidFilterError(
                f"無効なテーブル名です: '{table_name}'. "
                f"テーブル名は英数字とアンダースコアのみ使用できます。"
            )

        if not is_valid_identifier(date_column):
            raise InvalidFilterError(
                f"無効な日付カラム名です: '{date_column}'. "
                f"カラム名は英数字とアンダースコアのみ使用できます。"
            )

        # 期間フィルタ用のカスタムクエリを構築
        base_query = f"SELECT * FROM {table_name}"  # noqa: S608

        where_clauses: list[str] = []
        params: list[str | int] = []

        # 既存フィルタを追加
        for column, value in filters.items():
            # SQLインジェクション対策: カラム名を検証
            if not is_valid_identifier(column):
                raise InvalidFilterError(
                    f"無効なカラム名です: '{column}'. "
                    f"カラム名は英数字とアンダースコアのみ使用できます。"
                )

            if isinstance(value, list):
                placeholders = ", ".join(["%s"] * len(value))
                where_clauses.append(f"{column} IN ({placeholders})")
                params.extend(value)
            else:
                where_clauses.append(f"{column} = %s")
                params.append(value)

        # 期間フィルタを追加
        if start_date:
            where_clauses.append(f"{date_column} >= %s")
            params.append(start_date.strftime("%Y%m%d"))
        if end_date:
            where_clauses.append(f"{date_column} <= %s")
            params.append(end_date.strftime("%Y%m%d"))

        if where_clauses:
            query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
        else:
            query = base_query

        return self.connection_manager.fetch_dataframe(query, tuple(params) if params else None)

    def _get_table_with_year_only_period(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        year_column: str = "SEINEN",
    ) -> pd.DataFrame:
        """年のみのカラムを持つテーブルから期間フィルタ付きでデータを取得.

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any] | None): フィルタ条件
            start_date (date | None): 開始日（年のみ使用）
            end_date (date | None): 終了日（年のみ使用）
            year_column (str): 年カラム名（yyyy形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame
        """
        query_filters = dict(filters) if filters else {}

        # 期間フィルタがある場合は別途WHERE句を構築
        if start_date or end_date:
            return self._get_table_with_year_only_range(
                table_name, query_filters, start_date, end_date, year_column
            )

        return self.table_accessor.get_table_data(table_name, query_filters or None)

    def _get_table_with_year_only_range(
        self,
        table_name: str,
        filters: dict[str, Any],
        start_date: date | None,
        end_date: date | None,
        year_column: str,
    ) -> pd.DataFrame:
        """年のみのカラムに対して期間範囲フィルタ付きでテーブルデータを取得.

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any]): フィルタ条件
            start_date (date | None): 開始日（年のみ使用）
            end_date (date | None): 終了日（年のみ使用）
            year_column (str): 年カラム名（yyyy形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            InvalidFilterError: テーブル名、カラム名が無効な場合
        """
        # SQLインジェクション対策: 識別子を検証
        if not is_valid_identifier(table_name):
            raise InvalidFilterError(
                f"無効なテーブル名です: '{table_name}'. "
                f"テーブル名は英数字とアンダースコアのみ使用できます。"
            )

        if not is_valid_identifier(year_column):
            raise InvalidFilterError(
                f"無効な年カラム名です: '{year_column}'. "
                f"カラム名は英数字とアンダースコアのみ使用できます。"
            )

        # 期間フィルタ用のカスタムクエリを構築
        base_query = f"SELECT * FROM {table_name}"  # noqa: S608

        where_clauses: list[str] = []
        params: list[str | int] = []

        # 既存フィルタを追加
        for column, value in filters.items():
            # SQLインジェクション対策: カラム名を検証
            if not is_valid_identifier(column):
                raise InvalidFilterError(
                    f"無効なカラム名です: '{column}'. "
                    f"カラム名は英数字とアンダースコアのみ使用できます。"
                )

            if isinstance(value, list):
                placeholders = ", ".join(["%s"] * len(value))
                where_clauses.append(f"{column} IN ({placeholders})")
                params.extend(value)
            else:
                where_clauses.append(f"{column} = %s")
                params.append(value)

        # 期間フィルタを追加（年のみで比較）
        if start_date:
            where_clauses.append(f"{year_column} >= %s")
            params.append(start_date.strftime("%Y"))
        if end_date:
            where_clauses.append(f"{year_column} <= %s")
            params.append(end_date.strftime("%Y"))

        if where_clauses:
            query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
        else:
            query = base_query

        return self.connection_manager.fetch_dataframe(query, tuple(params) if params else None)

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

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any] | None): フィルタ条件
            start_date (date | None): 開始日
            end_date (date | None): 終了日
            year_column (str): 年カラム名（yyyy形式）
            date_column (str): 月日カラム名（mmdd形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame
        """
        query_filters = dict(filters) if filters else {}

        # 期間フィルタがある場合は別途WHERE句を構築
        if start_date or end_date:
            return self._get_table_with_composite_date_range(
                table_name, query_filters, start_date, end_date, year_column, date_column
            )

        return self.table_accessor.get_table_data(table_name, query_filters or None)

    def _get_table_with_composite_date_range(
        self,
        table_name: str,
        filters: dict[str, Any],
        start_date: date | None,
        end_date: date | None,
        year_column: str,
        date_column: str,
    ) -> pd.DataFrame:
        """年月日が分離されたカラムに対して期間範囲フィルタ付きでテーブルデータを取得.

        Args:
            table_name (str): テーブル名
            filters (dict[str, Any]): フィルタ条件
            start_date (date | None): 開始日
            end_date (date | None): 終了日
            year_column (str): 年カラム名（yyyy形式）
            date_column (str): 月日カラム名（mmdd形式）

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            InvalidFilterError: テーブル名、カラム名が無効な場合
        """
        # SQLインジェクション対策: 識別子を検証
        if not is_valid_identifier(table_name):
            raise InvalidFilterError(
                f"無効なテーブル名です: '{table_name}'. "
                f"テーブル名は英数字とアンダースコアのみ使用できます。"
            )

        if not is_valid_identifier(year_column):
            raise InvalidFilterError(
                f"無効な年カラム名です: '{year_column}'. "
                f"カラム名は英数字とアンダースコアのみ使用できます。"
            )

        if not is_valid_identifier(date_column):
            raise InvalidFilterError(
                f"無効な日付カラム名です: '{date_column}'. "
                f"カラム名は英数字とアンダースコアのみ使用できます。"
            )

        # 期間フィルタ用のカスタムクエリを構築
        base_query = f"SELECT * FROM {table_name}"  # noqa: S608

        where_clauses: list[str] = []
        params: list[str | int] = []

        # 既存フィルタを追加
        for column, value in filters.items():
            # SQLインジェクション対策: カラム名を検証
            if not is_valid_identifier(column):
                raise InvalidFilterError(
                    f"無効なカラム名です: '{column}'. "
                    f"カラム名は英数字とアンダースコアのみ使用できます。"
                )

            if isinstance(value, list):
                placeholders = ", ".join(["%s"] * len(value))
                where_clauses.append(f"{column} IN ({placeholders})")
                params.extend(value)
            else:
                where_clauses.append(f"{column} = %s")
                params.append(value)

        # 期間フィルタを追加（年と月日を結合した文字列で比較）
        if start_date:
            where_clauses.append(f"CONCAT({year_column}, {date_column}) >= %s")
            params.append(start_date.strftime("%Y%m%d"))
        if end_date:
            where_clauses.append(f"CONCAT({year_column}, {date_column}) <= %s")
            params.append(end_date.strftime("%Y%m%d"))

        if where_clauses:
            query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
        else:
            query = base_query

        return self.connection_manager.fetch_dataframe(query, tuple(params) if params else None)
