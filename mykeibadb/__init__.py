"""mykeibadb-python: JRA競馬データベースへのPythonアクセスライブラリ

このライブラリは、mykeibadbで構築されたPostgreSQLデータベースから
競馬データを取得するための統一的なインターフェースを提供します。
"""

__version__ = "0.1.0"

from mykeibadb.config import ConfigManager
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import InvalidFilterError, MykeibaDBError, TableNotFoundError
from mykeibadb.getters import TableGetters
from mykeibadb.tables import TableAccessor

__all__ = [
    "__version__",
    "ConfigManager",
    "ConnectionManager",
    "MykeibaDBError",
    "TableNotFoundError",
    "InvalidFilterError",
    "TableAccessor",
    "TableGetters",
]
