"""列の型を解決するモジュール.

このモジュールは、テーブルの列の型をinformation_schemaから解決する機能を提供する。
SQLのWHERE句で列を`TRIM()`で包むかどうかの判定に使う。

固定長文字列（bpchar）の列は、PostgreSQLの比較が末尾空白を無視するため`TRIM()`が
不要である。列を関数で包むとその列のインデックスが使われなくなるため、不要な`TRIM()`は
付けないほうがよい。
"""

import logging

from mykeibadb.connection import ConnectionManager

# information_schemaが返す固定長文字列の型名
_BLANK_PADDED_CHAR_TYPE = "character"

# 指定したテーブルの全列の型を取得するクエリ
_COLUMN_TYPE_QUERY = (
    "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s"
)


class ColumnTypeResolver:
    """テーブルの列の型を解決する.

    `information_schema.columns` からテーブル単位で列の型を取得し、プロセス内に
    キャッシュする。同じテーブルの複数の列を問い合わせても、データベースへの
    問い合わせは1回だけ行われる。

    テーブル名・カラム名は大文字小文字を区別せずに解決する。呼び出し側が
    `RACE_CODE` と `race_code` のどちらの表記でも渡しうるため。

    Attributes:
        connection_manager (ConnectionManager): データベース接続マネージャー
    """

    def __init__(
        self,
        connection_manager: ConnectionManager,
        logger: logging.Logger | None = None,
    ) -> None:
        """列の型リゾルバを初期化.

        Args:
            connection_manager (ConnectionManager): データベース接続マネージャー
            logger (logging.Logger | None): ロガーインスタンス
        """
        self._logger = logger or logging.getLogger(__name__)
        self.connection_manager = connection_manager
        # テーブル名（小文字）→ {カラム名（小文字）: 型名}
        self._column_types: dict[str, dict[str, str]] = {}

    def is_blank_padded_char(self, table_name: str, column_name: str) -> bool:
        """指定した列が固定長文字列（bpchar）かどうかを返す.

        型を判定できない場合（テーブルやカラムが存在しない、問い合わせに失敗した）は
        Falseを返す。呼び出し側が`TRIM()`を付ける側へ倒せるようにするためで、
        速度は落ちるが結果は正しくなる。

        Args:
            table_name (str): テーブル名
            column_name (str): カラム名

        Returns:
            bool: 固定長文字列の場合True。判定できない場合はFalse
        """
        column_types = self._get_column_types(table_name)
        return column_types.get(column_name.lower()) == _BLANK_PADDED_CHAR_TYPE

    def _get_column_types(self, table_name: str) -> dict[str, str]:
        """指定したテーブルの全列の型を取得する.

        取得済みのテーブルはキャッシュから返す。問い合わせに失敗した場合は空の辞書を
        キャッシュへ格納し、同じテーブルへ繰り返し問い合わせないようにする。

        Args:
            table_name (str): テーブル名

        Returns:
            dict[str, str]: カラム名（小文字）→ 型名。取得できない場合は空の辞書
        """
        key = table_name.lower()
        if key in self._column_types:
            return self._column_types[key]

        try:
            rows = self.connection_manager.execute_query(_COLUMN_TYPE_QUERY, (key,))
        except Exception:
            self._logger.exception("列の型の取得に失敗しました: table=%s", table_name)
            self._column_types[key] = {}
            return self._column_types[key]

        column_types = {str(column).lower(): str(data_type) for column, data_type in rows}
        self._logger.debug(
            "列の型を取得しました: table=%s, カラム数=%d", table_name, len(column_types)
        )
        self._column_types[key] = column_types
        return column_types
