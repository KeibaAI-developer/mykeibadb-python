"""票数関連テーブルGetter.

票数関連のテーブル（10テーブル）へのアクセスを提供する。

Tables:
    - HYOSU1: 票数1ベース情報
    - HYOSU1_TANSHO: 票数1単勝
    - HYOSU1_FUKUSHO: 票数1複勝
    - HYOSU1_WAKUREN: 票数1枠連
    - HYOSU1_UMAREN: 票数1馬連
    - HYOSU1_WIDE: 票数1ワイド
    - HYOSU1_UMATAN: 票数1馬単
    - HYOSU1_SANRENPUKU: 票数1三連複
    - HYOSU6: 票数6ベース情報
    - HYOSU6_SANRENTAN: 票数6三連単
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_race_code


class HyosuGetter(BaseGetter):
    """票数関連テーブルGetter.

    票数関連の10テーブルに対するアクセスメソッドを提供する。
    """

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
        return self._get_table_with_period_composite_date(
            "HYOSU1",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_TANSHO",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_FUKUSHO",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_WAKUREN",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_UMAREN",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_WIDE",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_UMATAN",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU1_SANRENPUKU",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU6",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HYOSU6_SANRENTAN",
            filters or None,
            start_date,
            end_date,
        )
