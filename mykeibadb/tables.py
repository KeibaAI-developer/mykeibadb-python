"""テーブルアクセスモジュール.

このモジュールは、mykeibadbデータベースのテーブルへのアクセス機能を提供する。
SQLクエリの生成、テーブル名のバリデーション、フィルタ処理などを行う。
"""

from typing import Any

import pandas as pd

from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import InvalidFilterError, TableNotFoundError
from mykeibadb.utils import is_valid_identifier

# サポートする全63テーブルのリスト
SUPPORTED_TABLES: frozenset[str] = frozenset(
    [
        # レース関連（5テーブル）
        "TOKUBETSU_TOROKUBA",
        "TOKUBETSU_TOROKUBAGOTO_JOHO",
        "RACE_SHOSAI",
        "UMAGOTO_RACE_JOHO",
        "HARAIMODOSHI",
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
        # 開催情報（1テーブル）
        "KAISAI_SCHEDULE",
        # コース情報（1テーブル）
        "COURSE_JOHO",
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
    base_query = f"SELECT * FROM {table_name}"  # noqa: S608

    if not filters:
        return base_query, None

    where_clauses: list[str] = []
    params: list[str | int] = []

    for column, value in filters.items():
        if isinstance(value, list):
            # IN句を生成
            placeholders = ", ".join(["%s"] * len(value))
            # カラム名は_validate_filtersで検証済み
            where_clauses.append(f"{column} IN ({placeholders})")  # noqa: S608
            params.extend(value)
        else:
            # 単一値の等価条件（カラム名は_validate_filtersで検証済み）
            where_clauses.append(f"{column} = %s")  # noqa: S608
            params.append(value)

    query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
    return query, tuple(params)
