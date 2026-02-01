"""テーブルアクセスモジュール.

このモジュールは、mykeibadbデータベースのテーブルへのアクセス機能を提供する。
SQLクエリの生成、テーブル名のバリデーション、フィルタ処理などを行う。
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import InvalidFilterError, TableNotFoundError
from mykeibadb.utils import is_valid_identifier

# サポートする全63テーブルのリスト
SUPPORTED_TABLES: frozenset[str] = frozenset(
    [
        # レース関連（7テーブル）
        "TOKUBETSU_TOROKUBA",
        "TOKUBETSU_TOROKUBAGOTO_JOHO",
        "RACE_SHOSAI",
        "UMAGOTO_RACE_JOHO",
        "HARAIMODOSHI",
        "KAISAI_SCHEDULE",
        "COURSE_JOHO",
        # 票数関連（10テーブル）
        "HYOSU1",
        "HYOSU1_TANSHO",
        "HYOSU1_FUKUSHO",
        "HYOSU1_WAKUREN",
        "HYOSU1_UMAREN",
        "HYOSU1_WIDE",
        "HYOSU1_UMATAN",
        "HYOSU1_SANRENPUKU",
        "HYOSU6",
        "HYOSU6_SANRENTAN",
        # オッズ関連（14テーブル）
        "ODDS1",
        "ODDS1_TANSHO",
        "ODDS1_FUKUSHO",
        "ODDS1_WAKUREN",
        "ODDS1_JIKEIRETSU",
        "ODDS1_TANSHO_JIKEIRETSU",
        "ODDS1_FUKUSHO_JIKEIRETSU",
        "ODDS1_WAKUREN_JIKEIRETSU",
        "ODDS2_UMAREN",
        "ODDS2_UMAREN_JIKEIRETSU",
        "ODDS3_WIDE",
        "ODDS4_UMATAN",
        "ODDS5_SANRENPUKU",
        "ODDS6_SANRENTAN",
        # マスタデータ（8テーブル）
        "KYOSOBA_MASTER2",
        "KISHU_MASTER",
        "CHOKYOSHI_MASTER",
        "SEISANSHA_MASTER2",
        "BANUSHI_MASTER",
        "HANSHOKUBA_MASTER2",
        "SANKU_MASTER2",
        "RECORD_MASTER",
        # 出走別データ（7テーブル）
        "SHUSSOBETSU_BABA",
        "SHUSSOBETSU_KYORI",
        "SHUSSOBETSU_KEIBAJO",
        "SHUSSOBETSU_KISHU",
        "SHUSSOBETSU_CHOKYOSHI",
        "SHUSSOBETSU_BANUSHI",
        "SHUSSOBETSU_SEISANSHA2",
        # 調教データ（2テーブル）
        "HANRO_CHOKYO",
        "WOODCHIP_CHOKYO",
        # 競走馬詳細情報（3テーブル）
        "KYOSOBA_TORIHIKI_KAKAKU2",
        "BAMEI_IMI_YURAI",
        "KEITO_JOHO2",
        # データマイニング予想（2テーブル）
        "DATA_MINING_TIME",
        "DATA_MINING_TAISEN",
        # WIN5（2テーブル）
        "WIN5",
        "WIN5_HARAIMODOSHI",
        # 速報（7テーブル）
        "KYOSOBA_JOGAI_JOHO",
        "BATAIJU",
        "TENKO_BABA_JOTAI",
        "SHUSSOTORIKESHI_KYOSOJOGAI",
        "KISHU_HENKO",
        "HASSOJIKOKU_HENKO",
        "COURSE_HENKO",
        # その他（1テーブル）
        "SHOBUFUKU",
    ]
)


class TableAccessor:
    """テーブルアクセサー.

    テーブルデータ取得の抽象化を提供する。
    SQLクエリの生成、テーブル名のバリデーション、フィルタ処理を行う。

    Attributes:
        connection_manager (ConnectionManager): データベース接続マネージャー
    """

    def __init__(self, connection_manager: ConnectionManager) -> None:
        """テーブルアクセサーを初期化.

        Args:
            connection_manager (ConnectionManager): データベース接続マネージャー
        """
        self.connection_manager = connection_manager

    def get_table_data(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
    ) -> pd.DataFrame:
        """テーブルデータを取得.

        指定されたテーブルからデータを取得し、DataFrameとして返す。
        フィルタを指定することで、条件に合致するレコードのみを取得できる。

        Args:
            table_name (str): テーブル名（例: "RACE_SHOSAI"）
            filters (dict[str, Any] | None): フィルタ条件
                キーはカラム名、値はフィルタ値。
                値がリストの場合はIN句として処理される。

        Returns:
            pd.DataFrame: 取得したデータのDataFrame

        Raises:
            TableNotFoundError: テーブルが存在しない場合
            InvalidFilterError: 無効なフィルタ条件の場合
        """
        _validate_table_name(table_name)
        _validate_filters(filters)

        query, params = _build_query(table_name, filters)
        return self.connection_manager.fetch_dataframe(query, params)

    def get_table_data_with_period(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        date_column: str = "KAISAI_NENGAPPI",
    ) -> pd.DataFrame:
        """期間フィルタ付きでテーブルデータを取得.

        単一の日付カラム（yyyymmdd形式）に対して期間フィルタを適用する。
        フィルタのバリデーションとTRIM処理は通常のget_table_dataと同様に行われる。

        Args:
            table_name (str): テーブル名（例: "RACE_SHOSAI"）
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
        _validate_table_name(table_name)
        _validate_filters(filters)
        _validate_date_column(date_column)

        query, params = _build_query_with_date_range(
            table_name, filters, start_date, end_date, date_column
        )
        return self.connection_manager.fetch_dataframe(query, params)

    def get_table_data_with_year_only_period(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        year_column: str = "SEINEN",
    ) -> pd.DataFrame:
        """年のみのカラムを持つテーブルから期間フィルタ付きでデータを取得.

        年カラム（yyyy形式）に対して期間フィルタを適用する。
        フィルタのバリデーションとTRIM処理は通常のget_table_dataと同様に行われる。

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
        _validate_table_name(table_name)
        _validate_filters(filters)
        _validate_date_column(year_column, "年カラム名")

        query, params = _build_query_with_year_only_range(
            table_name, filters, start_date, end_date, year_column
        )
        return self.connection_manager.fetch_dataframe(query, params)

    def get_table_data_with_composite_date_period(
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
        フィルタのバリデーションとTRIM処理は通常のget_table_dataと同様に行われる。

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
        _validate_table_name(table_name)
        _validate_filters(filters)
        _validate_date_column(year_column, "年カラム名")
        _validate_date_column(date_column, "日付カラム名")

        query, params = _build_query_with_composite_date_range(
            table_name, filters, start_date, end_date, year_column, date_column
        )
        return self.connection_manager.fetch_dataframe(query, params)


def _build_query_with_date_range(
    table_name: str,
    filters: dict[str, Any] | None,
    start_date: date | None,
    end_date: date | None,
    date_column: str,
) -> tuple[str, tuple[str | int, ...] | None]:
    """日付範囲フィルタ付きでSQLクエリを構築.

    単一の日付カラム（yyyymmdd形式）に対して期間フィルタを適用する。
    テーブル名、フィルタ、日付カラム名は事前に検証されている前提。

    Args:
        table_name (str): テーブル名（検証済み）
        filters (dict[str, Any] | None): フィルタ条件（検証済み）
        start_date (date | None): 開始日
        end_date (date | None): 終了日
        date_column (str): 日付カラム名（検証済み、yyyymmdd形式）

    Returns:
        tuple[str, tuple[str | int, ...] | None]: SQLクエリとパラメータのタプル
    """
    base_query, where_clauses, params = _build_base_query_and_params(table_name, filters)

    date_column_lower = date_column.lower()
    if start_date:
        where_clauses.append(f"{date_column_lower} >= %s")
        params.append(start_date.strftime("%Y%m%d"))
    if end_date:
        where_clauses.append(f"{date_column_lower} <= %s")
        params.append(end_date.strftime("%Y%m%d"))

    return _finalize_query(base_query, where_clauses, params)


def _build_query_with_year_only_range(
    table_name: str,
    filters: dict[str, Any] | None,
    start_date: date | None,
    end_date: date | None,
    year_column: str,
) -> tuple[str, tuple[str | int, ...] | None]:
    """年のみの範囲フィルタ付きでSQLクエリを構築.

    年カラム（yyyy形式）に対して期間フィルタを適用する。
    テーブル名、フィルタ、年カラム名は事前に検証されている前提。

    Args:
        table_name (str): テーブル名（検証済み）
        filters (dict[str, Any] | None): フィルタ条件（検証済み）
        start_date (date | None): 開始日（年のみ使用）
        end_date (date | None): 終了日（年のみ使用）
        year_column (str): 年カラム名（検証済み、yyyy形式）

    Returns:
        tuple[str, tuple[str | int, ...] | None]: SQLクエリとパラメータのタプル
    """
    base_query, where_clauses, params = _build_base_query_and_params(table_name, filters)

    year_column_lower = year_column.lower()
    if start_date:
        where_clauses.append(f"{year_column_lower} >= %s")
        params.append(start_date.strftime("%Y"))
    if end_date:
        where_clauses.append(f"{year_column_lower} <= %s")
        params.append(end_date.strftime("%Y"))

    return _finalize_query(base_query, where_clauses, params)


def _build_query_with_composite_date_range(
    table_name: str,
    filters: dict[str, Any] | None,
    start_date: date | None,
    end_date: date | None,
    year_column: str,
    date_column: str,
) -> tuple[str, tuple[str | int, ...] | None]:
    """年月日分離カラムに対して期間フィルタ付きでSQLクエリを構築.

    年カラム（yyyy形式）と月日カラム（mmdd形式）を結合して期間フィルタを適用する。
    テーブル名、フィルタ、カラム名は事前に検証されている前提。

    Args:
        table_name (str): テーブル名（検証済み）
        filters (dict[str, Any] | None): フィルタ条件（検証済み）
        start_date (date | None): 開始日
        end_date (date | None): 終了日
        year_column (str): 年カラム名（検証済み、yyyy形式）
        date_column (str): 月日カラム名（検証済み、mmdd形式）

    Returns:
        tuple[str, tuple[str | int, ...] | None]: SQLクエリとパラメータのタプル
    """
    base_query, where_clauses, params = _build_base_query_and_params(table_name, filters)

    year_column_lower = year_column.lower()
    date_column_lower = date_column.lower()
    if start_date:
        where_clauses.append(f"CONCAT({year_column_lower}, {date_column_lower}) >= %s")
        params.append(start_date.strftime("%Y%m%d"))
    if end_date:
        where_clauses.append(f"CONCAT({year_column_lower}, {date_column_lower}) <= %s")
        params.append(end_date.strftime("%Y%m%d"))

    return _finalize_query(base_query, where_clauses, params)


def _build_query(
    table_name: str,
    filters: dict[str, Any] | None = None,
) -> tuple[str, tuple[str | int, ...] | None]:
    """SQLクエリを構築.

    フィルタ条件に基づいてSELECTクエリを生成する。
    プリペアドステートメントを使用してSQLインジェクションを防ぐ。

    Args:
        table_name (str): テーブル名
        filters (dict[str, Any] | None): フィルタ条件

    Returns:
        tuple[str, tuple[str | int, ...] | None]: SQLクエリとパラメータのタプル
    """
    # ベースクエリ（テーブル名は_validate_table_nameで検証済み）
    # PostgreSQLではテーブル名を小文字として扱う
    base_query = f"SELECT * FROM {table_name.lower()}"  # noqa: S608

    if not filters:
        return base_query, None

    where_clauses: list[str] = []
    params: list[str | int] = []

    for column, value in filters.items():
        # PostgreSQLではカラム名を小文字として扱う
        column_lower = column.lower()
        if isinstance(value, list):
            # IN句を生成
            placeholders = ", ".join(["%s"] * len(value))
            # カラム名は_validate_filtersで検証済み
            # 文字列型の場合はTRIM関数を使って空白を除去して比較
            where_clauses.append(f"TRIM({column_lower}) IN ({placeholders})")  # noqa: S608
            params.extend(value)
        else:
            # 単一値の等価条件（カラム名は_validate_filtersで検証済み）
            # 文字列型の場合はTRIM関数を使って空白を除去して比較
            where_clauses.append(f"TRIM({column_lower}) = %s")  # noqa: S608
            params.append(value)

    query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
    return query, tuple(params)


def _build_base_query_and_params(
    table_name: str,
    filters: dict[str, Any] | None = None,
) -> tuple[str, list[str], list[str | int]]:
    """ベースクエリとWHERE句のパーツを構築.

    _build_queryの内部ロジックを共通化し、追加条件を付与できるようにする。

    Args:
        table_name (str): テーブル名（検証済み）
        filters (dict[str, Any] | None): フィルタ条件（検証済み）

    Returns:
        tuple[str, list[str], list[str | int]]: ベースクエリ、WHERE句リスト、パラメータリスト
    """
    base_query = f"SELECT * FROM {table_name.lower()}"  # noqa: S608
    where_clauses: list[str] = []
    params: list[str | int] = []

    if filters:
        for column, value in filters.items():
            column_lower = column.lower()
            if isinstance(value, list):
                placeholders = ", ".join(["%s"] * len(value))
                where_clauses.append(f"TRIM({column_lower}) IN ({placeholders})")  # noqa: S608
                params.extend(value)
            else:
                where_clauses.append(f"TRIM({column_lower}) = %s")  # noqa: S608
                params.append(value)

    return base_query, where_clauses, params


def _finalize_query(
    base_query: str,
    where_clauses: list[str],
    params: list[str | int],
) -> tuple[str, tuple[str | int, ...] | None]:
    """WHERE句を結合してクエリを完成させる.

    Args:
        base_query (str): ベースクエリ
        where_clauses (list[str]): WHERE句のリスト
        params (list[str | int]): パラメータのリスト

    Returns:
        tuple[str, tuple[str | int, ...] | None]: 完成したクエリとパラメータ
    """
    if where_clauses:
        query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
        return query, tuple(params)
    return base_query, None


def _validate_date_column(column_name: str, label: str = "日付カラム名") -> None:
    """日付カラム名の妥当性を検証.

    Args:
        column_name (str): 検証するカラム名
        label (str): エラーメッセージ用のラベル

    Raises:
        InvalidFilterError: カラム名が不正な場合
    """
    if not is_valid_identifier(column_name):
        raise InvalidFilterError(
            f"無効な{label}です: '{column_name}'. "
            f"カラム名は英数字とアンダースコアのみ使用できます。"
        )


def _validate_table_name(table_name: str) -> None:
    """テーブル名の妥当性を検証.

    Args:
        table_name (str): 検証するテーブル名

    Raises:
        TableNotFoundError: テーブルがサポートされていない場合
    """
    if table_name not in SUPPORTED_TABLES:
        raise TableNotFoundError(
            f"テーブル '{table_name}' はサポートされていません。 "
            f"サポートされているテーブルについてはdoc/DATA_TABLE.mdを参照してください。"
        )


def _validate_filters(filters: dict[str, Any] | None) -> None:
    """フィルタ条件の妥当性を検証.

    Args:
        filters (dict[str, Any] | None): 検証するフィルタ条件

    Raises:
        InvalidFilterError: フィルタ条件が不正な場合
    """
    if filters is None:
        return

    for key, value in filters.items():
        # カラム名のバリデーション（SQLインジェクション対策）
        if not is_valid_identifier(key):
            raise InvalidFilterError(
                f"無効なカラム名です: '{key}'. "
                f"カラム名は英数字とアンダースコアのみ使用できます。"
            )

        # 値の型チェック
        if isinstance(value, list):
            if len(value) == 0:
                raise InvalidFilterError(f"フィルタ値のリストが空です: キー='{key}'")
            for item in value:
                if not isinstance(item, (str, int)):
                    raise InvalidFilterError(
                        f"無効なフィルタ値の型です: キー='{key}', "
                        f"値='{item}', 型={type(item).__name__}. "
                        f"strまたはintを指定してください。"
                    )
        elif not isinstance(value, (str, int)):
            raise InvalidFilterError(
                f"無効なフィルタ値の型です: キー='{key}', "
                f"値='{value}', 型={type(value).__name__}. "
                f"str, int, またはそれらのリストを指定してください。"
            )
