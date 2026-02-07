"""データマイニング予想テーブルGetter.

データマイニング予想のテーブル（2テーブル）へのアクセスを提供する。

Tables:
    - DATA_MINING_TIME: タイム型データマイニング予想
    - DATA_MINING_TAISEN: 対戦型データマイニング予想
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.code_converter import convert_keibajo_code
from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_date_range, validate_race_code


class MiningGetter(BaseGetter):
    """データマイニング予想テーブルGetter.

    データマイニング予想の2テーブルに対するアクセスメソッドを提供する。
    """

    def get_data_mining_time(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """DATA_MINING_TIMEテーブルからタイム型データマイニング予想を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): コード値を名称に変換するかどうか

        Returns:
            pd.DataFrame: タイム型データマイニング予想のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        df = self._get_table_with_period_composite_date(
            "DATA_MINING_TIME",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        return self._apply_code_conversions(df, [("keibajo_code", "keibajo", convert_keibajo_code)])

    def get_data_mining_taisen(
        self,
        race_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """DATA_MINING_TAISENテーブルから対戦型データマイニング予想を取得.

        Args:
            race_code (str | list[str] | None): レースコード（16桁）
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）
            convert_codes (bool): コード値を名称に変換するかどうか

        Returns:
            pd.DataFrame: 対戦型データマイニング予想のDataFrame
        """
        validate_race_code(race_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if race_code:
            filters["RACE_CODE"] = race_code
        df = self._get_table_with_period_composite_date(
            "DATA_MINING_TAISEN",
            filters or None,
            start_date,
            end_date,
        )
        if df.empty or not convert_codes:
            return df
        return self._apply_code_conversions(df, [("keibajo_code", "keibajo", convert_keibajo_code)])
