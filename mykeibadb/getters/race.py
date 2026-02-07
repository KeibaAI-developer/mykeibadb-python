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

from collections.abc import Callable
from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.code_converter import (
    convert_babajotai_code,
    convert_chakusa_code,
    convert_grade_code,
    convert_hinshu_code,
    convert_ijo_kubun_code,
    convert_juryo_shubetsu_code,
    convert_keibajo_code,
    convert_kishu_minarai_code,
    convert_kyoso_joken_code,
    convert_kyoso_kigo_code,
    convert_kyoso_shubetsu_code,
    convert_moshoku_code,
    convert_seibetsu_code,
    convert_tenko_code,
    convert_tozai_shozoku_code,
    convert_track_code,
    convert_uma_kigo_code,
    convert_yobi_code,
)
from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import (
    validate_date_range,
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
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """TOKUBETSU_TOROKUBAテーブルから特別登録馬ベース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 特別登録馬ベース情報のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        df = self._get_table_with_period_composite_date(
            "TOKUBETSU_TOROKUBA",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        conversions: list[tuple[str, str, Callable[[str], str]]] = [
            ("keibajo_code", "keibajo", convert_keibajo_code),
            ("yobi_code", "yobi", convert_yobi_code),
            ("grade_code", "grade", convert_grade_code),
            ("kyoso_shubetsu_code", "kyoso_shubetsu", convert_kyoso_shubetsu_code),
            ("kyoso_kigo_code", "kyoso_kigo", convert_kyoso_kigo_code),
            ("juryo_shubetsu_code", "juryo_shubetsu", convert_juryo_shubetsu_code),
            ("kyoso_joken_code_2sai", "kyoso_joken_2sai", convert_kyoso_joken_code),
            ("kyoso_joken_code_3sai", "kyoso_joken_3sai", convert_kyoso_joken_code),
            ("kyoso_joken_code_4sai", "kyoso_joken_4sai", convert_kyoso_joken_code),
            ("kyoso_joken_code_5sai_ijo", "kyoso_joken_5sai_ijo", convert_kyoso_joken_code),
            ("kyoso_joken_code_saijakunen", "kyoso_joken_saijakunen", convert_kyoso_joken_code),
            ("track_code", "track", convert_track_code),
        ]
        return self._apply_code_conversions(df, conversions)

    def get_tokubetsu_torokubagoto_joho(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """TOKUBETSU_TOROKUBAGOTO_JOHOテーブルから特別登録馬毎情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 特別登録馬毎情報のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        df = self._get_table_with_period_composite_date(
            "TOKUBETSU_TOROKUBAGOTO_JOHO",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        conversions: list[tuple[str, str, Callable[[str], str]]] = [
            ("keibajo_code", "keibajo", convert_keibajo_code),
            ("umakigo_code", "umakigo", convert_uma_kigo_code),
            ("seibetsu_code", "seibetsu", convert_seibetsu_code),
            ("tozai_shozoku_code", "tozai_shozoku", convert_tozai_shozoku_code),
        ]
        return self._apply_code_conversions(df, conversions)

    def get_race_shosai(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """RACE_SHOSAIテーブルからレース詳細を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: レース詳細情報のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        df = self._get_table_with_period_composite_date(
            "RACE_SHOSAI",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        conversions: list[tuple[str, str, Callable[[str], str]]] = [
            ("keibajo_code", "keibajo", convert_keibajo_code),
            ("yobi_code", "yobi", convert_yobi_code),
            ("grade_code", "grade", convert_grade_code),
            ("kyoso_shubetsu_code", "kyoso_shubetsu", convert_kyoso_shubetsu_code),
            ("kyoso_kigo_code", "kyoso_kigo", convert_kyoso_kigo_code),
            ("juryo_shubetsu_code", "juryo_shubetsu", convert_juryo_shubetsu_code),
            ("kyoso_joken_code_2sai", "kyoso_joken_2sai", convert_kyoso_joken_code),
            ("kyoso_joken_code_3sai", "kyoso_joken_3sai", convert_kyoso_joken_code),
            ("kyoso_joken_code_4sai", "kyoso_joken_4sai", convert_kyoso_joken_code),
            ("kyoso_joken_code_5sai_ijo", "kyoso_joken_5sai_ijo", convert_kyoso_joken_code),
            ("kyoso_joken_code_saijakunen", "kyoso_joken_saijakunen", convert_kyoso_joken_code),
            ("track_code", "track", convert_track_code),
            ("tenko_code", "tenko", convert_tenko_code),
            ("shiba_babajotai_code", "shiba_babajotai", convert_babajotai_code),
            ("dirt_babajotai_code", "dirt_babajotai", convert_babajotai_code),
        ]
        return self._apply_code_conversions(df, conversions)

    def get_umagoto_race_joho(
        self,
        race_code: str | list[str] | None = None,
        ketto_toroku_bango: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """UMAGOTO_RACE_JOHOテーブルから馬毎レース情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 馬毎レース情報のDataFrame
        """
        validate_race_code(race_code)
        validate_ketto_toroku_bango(ketto_toroku_bango)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        df = self._get_table_with_period_composite_date(
            "UMAGOTO_RACE_JOHO",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        conversions: list[tuple[str, str, Callable[[str], str]]] = [
            ("keibajo_code", "keibajo", convert_keibajo_code),
            ("umakigo_code", "umakigo", convert_uma_kigo_code),
            ("seibetsu_code", "seibetsu", convert_seibetsu_code),
            ("hinshu_code", "hinshu", convert_hinshu_code),
            ("moshoku_code", "moshoku", convert_moshoku_code),
            ("tozai_shozoku_code", "tozai_shozoku", convert_tozai_shozoku_code),
            ("kishu_minarai_code", "kishu_minarai", convert_kishu_minarai_code),
            ("ijo_kubun_code", "ijo_kubun", convert_ijo_kubun_code),
            ("chakusa_code1", "chakusa1", convert_chakusa_code),
            ("chakusa_code2", "chakusa2", convert_chakusa_code),
            ("chakusa_code3", "chakusa3", convert_chakusa_code),
        ]
        return self._apply_code_conversions(df, conversions)

    def get_haraimodoshi(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """HARAIMODOSHIテーブルから払戻情報を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 払戻情報のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        df = self._get_table_with_period_composite_date(
            "HARAIMODOSHI",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        return self._apply_code_conversions(df, [("keibajo_code", "keibajo", convert_keibajo_code)])

    def get_kaisai_schedule(
        self,
        kaisai_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """KAISAI_SCHEDULEテーブルから開催スケジュールを取得.

        Args:
            kaisai_code (str | list[str] | None): 開催コード（16桁）
                開催年+月日+競馬場コード+回次+日次+レース番号
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 開催スケジュールのDataFrame
        """
        validate_kaisai_code(kaisai_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if kaisai_code:
            filters["KAISAI_CODE"] = kaisai_code
        df = self._get_table_with_period_composite_date(
            "KAISAI_SCHEDULE",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        conversions: list[tuple[str, str, Callable[[str], str]]] = [
            ("keibajo_code", "keibajo", convert_keibajo_code),
            ("yobi_code", "yobi", convert_yobi_code),
        ]
        for i in range(1, 4):
            prefix = f"jusho{i}_"
            conversions.extend(
                [
                    (f"{prefix}grade_code", f"{prefix}grade", convert_grade_code),
                    (
                        f"{prefix}kyoso_shubetsu_code",
                        f"{prefix}kyoso_shubetsu",
                        convert_kyoso_shubetsu_code,
                    ),
                    (f"{prefix}kyoso_kigo_code", f"{prefix}kyoso_kigo", convert_kyoso_kigo_code),
                    (
                        f"{prefix}juryo_shubetsu_code",
                        f"{prefix}juryo_shubetsu",
                        convert_juryo_shubetsu_code,
                    ),
                    (f"{prefix}track_code", f"{prefix}track", convert_track_code),
                ]
            )
        return self._apply_code_conversions(df, conversions)

    def get_course_joho(
        self,
        keibajo_code: str | list[str] | None = None,
        kyori: int | list[int] | None = None,
        track_code: str | list[str] | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """COURSE_JOHOテーブルからコース情報を取得.

        Args:
            keibajo_code (str | list[str] | None): 競馬場コード
            kyori (int | list[int] | None): 距離
            track_code (str | list[str] | None): トラックコード
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: コース情報のDataFrame
        """
        validate_keibajo_code(keibajo_code)
        validate_track_code(track_code)
        filters: dict[str, Any] = {}
        if keibajo_code:
            filters["KEIBAJO_CODE"] = keibajo_code
        if kyori:
            if isinstance(kyori, list):
                filters["KYORI"] = [str(k) for k in kyori]
            else:
                filters["KYORI"] = str(kyori)
        if track_code:
            filters["TRACK_CODE"] = track_code
        df = self.table_accessor.get_table_data("COURSE_JOHO", filters or None)
        if df.empty or not convert_codes:
            return df
        # コード変換
        conversions: list[tuple[str, str, Callable[[str], str]]] = [
            ("keibajo_code", "keibajo", convert_keibajo_code),
            ("track_code", "track", convert_track_code),
        ]
        return self._apply_code_conversions(df, conversions)
