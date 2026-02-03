"""速報テーブルGetter.

速報のテーブル（7テーブル）へのアクセスを提供する。

Tables:
    - KYOSOBA_JOGAI_JOHO: 競走馬除外情報
    - BATAIJU: 馬体重情報
    - TENKO_BABA_JOTAI: 天候馬場状態情報
    - SHUSSOTORIKESHI_KYOSOJOGAI: 出走取消・競走除外情報
    - KISHU_HENKO: 騎手変更情報
    - HASSOJIKOKU_HENKO: 発走時刻変更情報
    - COURSE_HENKO: コース変更情報
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import (
    validate_date_range,
    validate_kaisai_code,
    validate_ketto_toroku_bango,
    validate_race_code,
)


class SokuhoGetter(BaseGetter):
    """速報テーブルGetter.

    速報の7テーブルに対するアクセスメソッドを提供する。
    """

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
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        return self._get_table_with_period_composite_date(
            "KYOSOBA_JOGAI_JOHO",
            filters or None,
            start_date,
            end_date,
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
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period_composite_date(
            "BATAIJU",
            filters or None,
            start_date,
            end_date,
        )

    def get_tenko_baba_jotai(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """TENKO_BABA_JOTAIテーブルから天候馬場状態情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 天候馬場状態情報のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period_composite_date(
            "TENKO_BABA_JOTAI",
            filters or None,
            start_date,
            end_date,
        )

    def get_shussotorikeshi_kyosojogai(
        self,
        kaisai_code: str | list[str] | None = None,
        umaban: int | list[int] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """SHUSSOTORIKESHI_KYOSOJOGAIテーブルから出走取消・競走除外情報を取得.

        Args:
            kaisai_code (str | list[str] | None): レースコード（14桁）
            umaban (int | list[int] | None): 馬番（1～18）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 出走取消・競走除外情報のDataFrame
        """
        validate_kaisai_code(kaisai_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["RACE_CODE"] = kaisai_code  # mykeibadb側のミスと思われる
        if umaban:
            if isinstance(umaban, list):
                filters["UMABAN"] = [f"{u:02}" for u in umaban]
            else:
                filters["UMABAN"] = f"{umaban:02}"
        return self._get_table_with_period_composite_date(
            "SHUSSOTORIKESHI_KYOSOJOGAI",
            filters or None,
            start_date,
            end_date,
        )

    def get_kishu_henko(
        self,
        race_code: str | list[str] | None = None,
        umaban: int | list[int] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KISHU_HENKOテーブルから騎手変更情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            umaban (int | list[int] | None): 馬番（1～18）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 騎手変更情報のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if umaban:
            if isinstance(umaban, list):
                filters["UMABAN"] = [f"{u:02}" for u in umaban]
            else:
                filters["UMABAN"] = f"{umaban:02}"
        return self._get_table_with_period_composite_date(
            "KISHU_HENKO",
            filters or None,
            start_date,
            end_date,
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
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period_composite_date(
            "HASSOJIKOKU_HENKO",
            filters or None,
            start_date,
            end_date,
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
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period_composite_date(
            "COURSE_HENKO",
            filters or None,
            start_date,
            end_date,
        )
