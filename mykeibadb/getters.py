"""テーブルデータ取得関数群.

このモジュールは、各テーブルに対してキーや期間を指定してデータを取得する関数を提供する。
各関数は指定されたフィルタ条件に従ってテーブルからデータを取得し、DataFrameとして返す。
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.config import ConfigManager
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import InvalidFilterError
from mykeibadb.tables import TableAccessor
from mykeibadb.utils import (
    is_valid_identifier,
    validate_banushi_code,
    validate_chokyoshi_code,
    validate_hanshoku_toroku_bango,
    validate_kaisai_code,
    validate_keibajo_code,
    validate_ketto_toroku_bango,
    validate_kishu_code,
    validate_race_code,
    validate_seisansha_code,
    validate_tracen_kubun,
    validate_track_code,
)


class TableGetters:
    """テーブルデータ取得クラス.

    各テーブルに対してキーや期間を指定してデータを取得するメソッドを提供する。

    Attributes:
        connection_manager (ConnectionManager): データベース接続マネージャー
        table_accessor (TableAccessor): テーブルアクセサー
    """

    def __init__(self) -> None:
        """テーブルデータ取得クラスを初期化.

        環境変数から設定を読み込み、データベース接続を確立する。
        """
        config = ConfigManager.from_env()
        self.connection_manager = ConnectionManager(config)
        self.table_accessor = TableAccessor(self.connection_manager)

    # =========================================================================
    # レース関連テーブル
    # =========================================================================

    def get_tokubetsu_torokuba(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """TOKUBETSU_TOROKUBAテーブルから特別登録馬ベース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 特別登録馬ベース情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "TOKUBETSU_TOROKUBA", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_tokubetsu_torokubagoto_joho(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """TOKUBETSU_TOROKUBAGOTO_JOHOテーブルから特別登録馬毎情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 特別登録馬毎情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "TOKUBETSU_TOROKUBAGOTO_JOHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_race_shosai(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """RACE_SHOSAIテーブルからレース詳細を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: レース詳細情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "RACE_SHOSAI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_umagoto_race_joho(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """UMAGOTO_RACE_JOHOテーブルから馬毎レース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 馬毎レース情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "UMAGOTO_RACE_JOHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_haraimodoshi(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HARAIMODOSHIテーブルから払戻情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 払戻情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HARAIMODOSHI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # 票数関連テーブル
    # =========================================================================

    def get_hyosu1(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1テーブルから票数1ベース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1ベース情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_tansho(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_TANSHOテーブルから票数1単勝情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1単勝情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_TANSHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_fukusho(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_FUKUSHOテーブルから票数1複勝情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1複勝情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_FUKUSHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_wakuren(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_WAKURENテーブルから票数1枠連情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1枠連情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_WAKUREN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_umaren(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_UMARENテーブルから票数1馬連情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1馬連情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_UMAREN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_wide(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_WIDEテーブルから票数1ワイド情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1ワイド情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_WIDE", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_umatan(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_UMATANテーブルから票数1馬単情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1馬単情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_UMATAN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu1_sanrenpuku(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU1_SANRENPUKUテーブルから票数1三連複情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数1三連複情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU1_SANRENPUKU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu6(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU6テーブルから票数6ベース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数6ベース情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU6", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hyosu6_sanrentan(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HYOSU6_SANRENTANテーブルから票数6三連単情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 票数6三連単情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HYOSU6_SANRENTAN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # オッズ関連テーブル
    # =========================================================================

    def get_odds1(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1テーブルからオッズ1ベース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1ベース情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_tansho(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_TANSHOテーブルからオッズ1単勝情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1単勝情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_TANSHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_fukusho(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_FUKUSHOテーブルからオッズ1複勝情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1複勝情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_FUKUSHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_wakuren(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_WAKURENテーブルからオッズ1枠連情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1枠連情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_WAKUREN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_jikeiretsu(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_JIKEIRETSUテーブルからオッズ1時系列ベース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1時系列ベース情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_JIKEIRETSU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_tansho_jikeiretsu(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_TANSHO_JIKEIRETSUテーブルからオッズ1単勝時系列情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1単勝時系列情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_TANSHO_JIKEIRETSU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_fukusho_jikeiretsu(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_FUKUSHO_JIKEIRETSUテーブルからオッズ1複勝時系列情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1複勝時系列情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_FUKUSHO_JIKEIRETSU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds1_wakuren_jikeiretsu(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS1_WAKUREN_JIKEIRETSUテーブルからオッズ1枠連時系列情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ1枠連時系列情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS1_WAKUREN_JIKEIRETSU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds2_umaren(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS2_UMARENテーブルからオッズ2馬連情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ2馬連情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS2_UMAREN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds2_umaren_jikeiretsu(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS2_UMAREN_JIKEIRETSUテーブルからオッズ2馬連時系列情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ2馬連時系列情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS2_UMAREN_JIKEIRETSU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds3_wide(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS3_WIDEテーブルからオッズ3ワイド情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ3ワイド情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS3_WIDE", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds4_umatan(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS4_UMATANテーブルからオッズ4馬単情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ4馬単情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS4_UMATAN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds5_sanrenpuku(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS5_SANRENPUKUテーブルからオッズ5三連複情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ5三連複情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS5_SANRENPUKU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_odds6_sanrentan(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """ODDS6_SANRENTANテーブルからオッズ6三連単情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: オッズ6三連単情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "ODDS6_SANRENTAN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # マスタデータテーブル
    # =========================================================================

    def get_kyosoba_master2(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KYOSOBA_MASTER2テーブルから競走馬マスタを取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（生年月日基準）
            end_date (date | None): 終了日（生年月日基準）

        Returns:
            pd.DataFrame: 競走馬マスタのDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "KYOSOBA_MASTER2", filters or None, start_date, end_date, "SEINENGAPPI"
        )

    def get_kishu_master(
        self,
        kishu_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KISHU_MASTERテーブルから騎手マスタを取得.

        Args:
            kishu_code (str | list[str] | None): 騎手コード
            start_date (date | None): 開始日（騎手免許交付年月日基準）
            end_date (date | None): 終了日（騎手免許交付年月日基準）

        Returns:
            pd.DataFrame: 騎手マスタのDataFrame
        """
        validate_kishu_code(kishu_code)
        filters: dict[str, Any] = {}
        if kishu_code:
            filters["KISHU_CODE"] = kishu_code
        return self._get_table_with_period(
            "KISHU_MASTER", filters or None, start_date, end_date, "MENKYO_KOFU_NENGAPPI"
        )

    def get_chokyoshi_master(
        self,
        chokyoshi_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """CHOKYOSHI_MASTERテーブルから調教師マスタを取得.

        Args:
            chokyoshi_code (str | list[str] | None): 調教師コード
            start_date (date | None): 開始日（調教師免許交付年月日基準）
            end_date (date | None): 終了日（調教師免許交付年月日基準）

        Returns:
            pd.DataFrame: 調教師マスタのDataFrame
        """
        validate_chokyoshi_code(chokyoshi_code)
        filters: dict[str, Any] = {}
        if chokyoshi_code:
            filters["CHOKYOSHI_CODE"] = chokyoshi_code
        return self._get_table_with_period(
            "CHOKYOSHI_MASTER", filters or None, start_date, end_date, "MENKYO_KOFU_NENGAPPI"
        )

    def get_seisansha_master2(
        self,
        seisansha_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """SEISANSHA_MASTER2テーブルから生産者マスタを取得.

        Args:
            seisansha_code (str | list[str] | None): 生産者コード

        Returns:
            pd.DataFrame: 生産者マスタのDataFrame
        """
        validate_seisansha_code(seisansha_code)
        filters: dict[str, Any] = {}
        if seisansha_code:
            filters["SEISANSHA_CODE"] = seisansha_code
        return self.table_accessor.get_table_data("SEISANSHA_MASTER2", filters or None)

    def get_banushi_master(
        self,
        banushi_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """BANUSHI_MASTERテーブルから馬主マスタを取得.

        Args:
            banushi_code (str | list[str] | None): 馬主コード

        Returns:
            pd.DataFrame: 馬主マスタのDataFrame
        """
        validate_banushi_code(banushi_code)
        filters: dict[str, Any] = {}
        if banushi_code:
            filters["BANUSHI_CODE"] = banushi_code
        return self.table_accessor.get_table_data("BANUSHI_MASTER", filters or None)

    def get_hanshokuba_master2(
        self,
        hanshoku_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HANSHOKUBA_MASTER2テーブルから繁殖馬マスタを取得.

        Args:
            hanshoku_toroku_bango (str | list[str] | None): 繁殖登録番号
            start_date (date | None): 開始日（生年基準、年のみ指定）
            end_date (date | None): 終了日（生年基準、年のみ指定）

        Returns:
            pd.DataFrame: 繁殖馬マスタのDataFrame
        """
        validate_hanshoku_toroku_bango(hanshoku_toroku_bango)
        filters: dict[str, Any] = {}
        if hanshoku_toroku_bango:
            filters["HANSHOKU_TOROKU_BANGO"] = hanshoku_toroku_bango
        return self._get_table_with_period(
            "HANSHOKUBA_MASTER2", filters or None, start_date, end_date, "SEINEN"
        )

    def get_sanku_master2(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """SANKU_MASTER2テーブルから産駒マスタを取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号

        Returns:
            pd.DataFrame: 産駒マスタのDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self.table_accessor.get_table_data("SANKU_MASTER2", filters or None)

    def get_record_master(
        self,
        keibajo_code: str | list[str] | None = None,
        kyori: int | list[int] | None = None,
        track_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """RECORD_MASTERテーブルからレコードマスタを取得.

        Args:
            keibajo_code (str | list[str] | None): 競馬場コード
            kyori (int | list[int] | None): 距離
            track_code (str | list[str] | None): トラックコード

        Returns:
            pd.DataFrame: レコードマスタのDataFrame
        """
        validate_keibajo_code(keibajo_code)
        validate_track_code(track_code)
        filters: dict[str, Any] = {}
        if keibajo_code:
            filters["KEIBAJO_CODE"] = keibajo_code
        if kyori:
            filters["KYORI"] = kyori
        if track_code:
            filters["TRACK_CODE"] = track_code
        return self.table_accessor.get_table_data("RECORD_MASTER", filters or None)

    # =========================================================================
    # 出走別データテーブル
    # =========================================================================

    def get_shussobetsu_baba(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_BABAテーブルから出走別馬場別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別馬場別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_BABA", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussobetsu_kyori(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_KYORIテーブルから出走別距離別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別距離別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_KYORI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussobetsu_keibajo(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_KEIBAJOテーブルから出走別競馬場別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別競馬場別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_KEIBAJO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussobetsu_kishu(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_KISHUテーブルから出走別騎手別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別騎手別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_KISHU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussobetsu_chokyoshi(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_CHOKYOSHIテーブルから出走別調教師別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別調教師別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_CHOKYOSHI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussobetsu_banushi(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_BANUSHIテーブルから出走別馬主別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別馬主別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_BANUSHI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussobetsu_seisansha2(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOBETSU_SEISANSHA2テーブルから出走別生産者別情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走別生産者別情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOBETSU_SEISANSHA2", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # 調教データテーブル
    # =========================================================================

    def get_hanro_chokyo(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
        tracen_kubun: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HANRO_CHOKYOテーブルから坂路調教情報を取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            tracen_kubun (str | list[str] | None): トレセン区分（0:美浦、1:栗東）
            start_date (date | None): 開始日（調教年月日基準）
            end_date (date | None): 終了日（調教年月日基準）

        Returns:
            pd.DataFrame: 坂路調教情報のDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        validate_tracen_kubun(tracen_kubun)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        if tracen_kubun:
            filters["TRACEN_KUBUN"] = tracen_kubun
        return self._get_table_with_period(
            "HANRO_CHOKYO", filters or None, start_date, end_date, "CHOKYO_NENGAPPI"
        )

    def get_woodchip_chokyo(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
        tracen_kubun: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """WOODCHIP_CHOKYOテーブルからウッドチップ調教情報を取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            tracen_kubun (str | list[str] | None): トレセン区分（0:美浦、1:栗東）
            start_date (date | None): 開始日（調教年月日基準）
            end_date (date | None): 終了日（調教年月日基準）

        Returns:
            pd.DataFrame: ウッドチップ調教情報のDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        validate_tracen_kubun(tracen_kubun)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        if tracen_kubun:
            filters["TRACEN_KUBUN"] = tracen_kubun
        return self._get_table_with_period(
            "WOODCHIP_CHOKYO", filters or None, start_date, end_date, "CHOKYO_NENGAPPI"
        )

    # =========================================================================
    # 開催・コース情報テーブル
    # =========================================================================

    def get_kaisai_schedule(
        self,
        kaisai_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KAISAI_SCHEDULEテーブルから開催スケジュールを取得.

        Args:
            kaisai_code (str | list[str] | None): 開催コード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 開催スケジュールのDataFrame
        """
        validate_kaisai_code(kaisai_code)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["KAISAI_CODE"] = kaisai_code
        return self._get_table_with_period(
            "KAISAI_SCHEDULE", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_course_joho(
        self,
        keibajo_code: str | list[str] | None = None,
        kyori: int | list[int] | None = None,
        track_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """COURSE_JOHOテーブルからコース情報を取得.

        Args:
            keibajo_code (str | list[str] | None): 競馬場コード
            kyori (int | list[int] | None): 距離
            track_code (str | list[str] | None): トラックコード

        Returns:
            pd.DataFrame: コース情報のDataFrame
        """
        validate_keibajo_code(keibajo_code)
        validate_track_code(track_code)
        filters: dict[str, Any] = {}
        if keibajo_code:
            filters["KEIBAJO_CODE"] = keibajo_code
        if kyori:
            filters["KYORI"] = kyori
        if track_code:
            filters["TRACK_CODE"] = track_code
        return self.table_accessor.get_table_data("COURSE_JOHO", filters or None)

    # =========================================================================
    # 競走馬詳細情報テーブル
    # =========================================================================

    def get_kyosoba_torihiki_kakaku2(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """KYOSOBA_TORIHIKI_KAKAKU2テーブルから競走馬市場取引価格を取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号

        Returns:
            pd.DataFrame: 競走馬市場取引価格のDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self.table_accessor.get_table_data("KYOSOBA_TORIHIKI_KAKAKU2", filters or None)

    def get_bamei_imi_yurai(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """BAMEI_IMI_YURAIテーブルから馬名の意味由来を取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号

        Returns:
            pd.DataFrame: 馬名の意味由来のDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self.table_accessor.get_table_data("BAMEI_IMI_YURAI", filters or None)

    def get_keito_joho2(
        self,
        keito_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """KEITO_JOHO2テーブルから系統情報を取得.

        Args:
            keito_code (str | list[str] | None): 系統コード

        Returns:
            pd.DataFrame: 系統情報のDataFrame
        """
        filters: dict[str, Any] = {}
        if keito_code:
            filters["KEITO_CODE"] = keito_code
        return self.table_accessor.get_table_data("KEITO_JOHO2", filters or None)

    # =========================================================================
    # データマイニング予想テーブル
    # =========================================================================

    def get_data_mining_time(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """DATA_MINING_TIMEテーブルからタイム型データマイニング予想を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: タイム型データマイニング予想のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "DATA_MINING_TIME", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_data_mining_taisen(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """DATA_MINING_TAISENテーブルから対戦型データマイニング予想を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 対戦型データマイニング予想のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "DATA_MINING_TAISEN", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # WIN5テーブル
    # =========================================================================

    def get_win5(
        self,
        kaisai_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """WIN5テーブルから重勝式ベース情報を取得.

        Args:
            kaisai_code (str | list[str] | None): 開催コード
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 重勝式ベース情報のDataFrame
        """
        validate_kaisai_code(kaisai_code)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["KAISAI_CODE"] = kaisai_code
        return self._get_table_with_period(
            "WIN5", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_win5_haraimodoshi(
        self,
        kaisai_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """WIN5_HARAIMODOSHIテーブルから重勝式払戻情報を取得.

        Args:
            kaisai_code (str | list[str] | None): 開催コード
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 重勝式払戻情報のDataFrame
        """
        validate_kaisai_code(kaisai_code)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["KAISAI_CODE"] = kaisai_code
        return self._get_table_with_period(
            "WIN5_HARAIMODOSHI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # 速報テーブル
    # =========================================================================

    def get_kyosoba_jogai_joho(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KYOSOBA_JOGAI_JOHOテーブルから競走馬除外情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 競走馬除外情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "KYOSOBA_JOGAI_JOHO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_bataiju(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """BATAIJUテーブルから馬体重情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 馬体重情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "BATAIJU", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_tenko_baba_jotai(
        self,
        kaisai_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """TENKO_BABA_JOTAIテーブルから天候馬場状態情報を取得.

        Args:
            kaisai_code (str | list[str] | None): 開催コード
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 天候馬場状態情報のDataFrame
        """
        validate_kaisai_code(kaisai_code)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["KAISAI_CODE"] = kaisai_code
        return self._get_table_with_period(
            "TENKO_BABA_JOTAI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_shussotorikeshi_kyosojogai(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOTORIKESHI_KYOSOJOGAIテーブルから出走取消・競走除外情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走取消・競走除外情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "SHUSSOTORIKESHI_KYOSOJOGAI", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_kishu_henko(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KISHU_HENKOテーブルから騎手変更情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 騎手変更情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period(
            "KISHU_HENKO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_hassojikoku_henko(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """HASSOJIKOKU_HENKOテーブルから発走時刻変更情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 発走時刻変更情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "HASSOJIKOKU_HENKO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    def get_course_henko(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """COURSE_HENKOテーブルからコース変更情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: コース変更情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period(
            "COURSE_HENKO", filters or None, start_date, end_date, "KAISAI_GAPPI"
        )

    # =========================================================================
    # その他テーブル
    # =========================================================================

    def get_shobufuku(
        self,
        banushi_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """SHOBUFUKUテーブルから勝負服情報を取得.

        Args:
            banushi_code (str | list[str] | None): 馬主コード

        Returns:
            pd.DataFrame: 勝負服情報のDataFrame
        """
        validate_banushi_code(banushi_code)
        filters: dict[str, Any] = {}
        if banushi_code:
            filters["BANUSHI_CODE"] = banushi_code
        return self.table_accessor.get_table_data("SHOBUFUKU", filters or None)

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
