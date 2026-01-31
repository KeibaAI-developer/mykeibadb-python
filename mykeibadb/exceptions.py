"""例外クラス定義.

このモジュールは、mykeibadb-pythonライブラリで使用される例外クラスを定義する。
"""


class MykeibaDBError(Exception):
    """mykeibadb-python基底例外.

    mykeibadb-pythonライブラリの全ての例外の基底クラス。
    """

    pass


class MykeibaDBConnectionError(MykeibaDBError):
    """データベース接続エラー.

    PostgreSQLへの接続失敗やSSH接続失敗時に発生する例外。
    """

    pass


class TableNotFoundError(MykeibaDBError):
    """テーブル存在エラー.

    指定されたテーブルがデータベースに存在しない場合に発生する例外。
    """

    pass


class InvalidFilterError(MykeibaDBError):
    """無効なフィルタ条件エラー.

    不正なフィルタ条件が指定された場合に発生する例外。
    """

    pass


class QueryExecutionError(MykeibaDBError):
    """クエリ実行エラー.

    SQLクエリの実行に失敗した場合に発生する例外。
    """

    pass


class ValidationError(Exception):
    """引数検証エラー."""

    pass
