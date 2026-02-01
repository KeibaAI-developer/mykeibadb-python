"""レース関連テーブルGetter.

レース関連のテーブル（7テーブル）へのアクセスを提供する。

Tables:
    - TOKUBETSU_TOROKUBA: 特別登録馬ベース情報
    - TOKUBETSU_TOROKUBAGOTO_JOHO: 特別登録馬毎情報
    - RACE_SHOSAI: レース詳細
    - UMAGOTO_RACE_JOHO: 馬毎レース情報
    - HARAIMODOSHI: 払戻情報
    - KAISAI_SCHEDULE: 開催スケジュール
    - COURSE_JOHO: コース情報
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import (
    validate_kaisai_code,
    validate_keibajo_code,
    validate_ketto_toroku_bango,
    validate_race_code,
    validate_track_code,
)


class RaceGetter(BaseGetter):
    """レース関連テーブルGetter.

    レース関連の7テーブルに対するアクセスメソッドを提供する。
    """

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
        return self._get_table_with_period_composite_date(
            "TOKUBETSU_TOROKUBA",
            filters or None,
            start_date,
            end_date,
        )

    def get_tokubetsu_torokubagoto_joho(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """TOKUBETSU_TOROKUBAGOTO_JOHOテーブルから特別登録馬毎情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 特別登録馬毎情報のDataFrame
        """
        validate_race_code(race_code)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        return self._get_table_with_period_composite_date(
            "TOKUBETSU_TOROKUBAGOTO_JOHO",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "RACE_SHOSAI",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "UMAGOTO_RACE_JOHO",
            filters or None,
            start_date,
            end_date,
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
        return self._get_table_with_period_composite_date(
            "HARAIMODOSHI",
            filters or None,
            start_date,
            end_date,
        )

    def get_kaisai_schedule(
        self,
        kaisai_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """KAISAI_SCHEDULEテーブルから開催スケジュールを取得.

        Args:
            kaisai_code (str | list[str] | None): 開催コード（16桁）
                開催年+月日+競馬場コード+回次+日次+レース番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 開催スケジュールのDataFrame
        """
        validate_kaisai_code(kaisai_code)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["KAISAI_CODE"] = kaisai_code
        return self._get_table_with_period_composite_date(
            "KAISAI_SCHEDULE",
            filters or None,
            start_date,
            end_date,
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
