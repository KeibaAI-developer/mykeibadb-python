"""オッズ関連テーブルGetter.

オッズ関連のテーブル（14テーブル）へのアクセスを提供する。

Tables:
    - ODDS1: オッズ1ベース情報
    - ODDS1_TANSHO: オッズ1単勝
    - ODDS1_FUKUSHO: オッズ1複勝
    - ODDS1_WAKUREN: オッズ1枠連
    - ODDS1_JIKEIRETSU: オッズ1時系列ベース
    - ODDS1_TANSHO_JIKEIRETSU: オッズ1単勝時系列
    - ODDS1_FUKUSHO_JIKEIRETSU: オッズ1複勝時系列
    - ODDS1_WAKUREN_JIKEIRETSU: オッズ1枠連時系列
    - ODDS2_UMAREN: オッズ2馬連
    - ODDS2_UMAREN_JIKEIRETSU: オッズ2馬連時系列
    - ODDS3_WIDE: オッズ3ワイド
    - ODDS4_UMATAN: オッズ4馬単
    - ODDS5_SANRENPUKU: オッズ5三連複
    - ODDS6_SANRENTAN: オッズ6三連単
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_race_code


class OddsGetter(BaseGetter):
    """オッズ関連テーブルGetter.

    オッズ関連の14テーブルに対するアクセスメソッドを提供する。
    """

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
        return self._get_table_with_period_composite_date(
            "ODDS1",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_TANSHO",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_FUKUSHO",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_WAKUREN",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_JIKEIRETSU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_TANSHO_JIKEIRETSU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_FUKUSHO_JIKEIRETSU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS1_WAKUREN_JIKEIRETSU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS2_UMAREN",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS2_UMAREN_JIKEIRETSU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS3_WIDE",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS4_UMATAN",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS5_SANRENPUKU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "ODDS6_SANRENTAN",
            filters or None,
            start_date,
            end_date,
        )
