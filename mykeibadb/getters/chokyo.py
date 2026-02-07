"""調教データテーブルGetter.

調教データのテーブル（2テーブル）へのアクセスを提供する。

Tables:
    - HANRO_CHOKYO: 坂路調教情報
    - WOODCHIP_CHOKYO: ウッドチップ調教情報
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_date_range, validate_ketto_toroku_bango, validate_tracen_kubun


class ChokyoGetter(BaseGetter):
    """調教データテーブルGetter.

    調教データの2テーブルに対するアクセスメソッドを提供する。
    """

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
        validate_date_range(start_date, end_date)
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
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        if tracen_kubun:
            filters["TRACEN_KUBUN"] = tracen_kubun
        return self._get_table_with_period(
            "WOODCHIP_CHOKYO", filters or None, start_date, end_date, "CHOKYO_NENGAPPI"
        )
