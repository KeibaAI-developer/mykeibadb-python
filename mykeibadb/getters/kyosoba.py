"""競走馬詳細情報テーブルGetter.

競走馬詳細情報のテーブル（3テーブル）へのアクセスを提供する。

Tables:
    - KYOSOBA_TORIHIKI_KAKAKU2: 競走馬市場取引価格
    - BAMEI_IMI_YURAI: 馬名の意味由来
    - KEITO_JOHO2: 系統情報
"""

from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_ketto_toroku_bango


class KyosobaGetter(BaseGetter):
    """競走馬詳細情報テーブルGetter.

    競走馬詳細情報の3テーブルに対するアクセスメソッドを提供する。
    """

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
        keito_id: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """KEITO_JOHO2テーブルから系統情報を取得.

        Args:
            keito_id (str | list[str] | None): 系統ID

        Returns:
            pd.DataFrame: 系統情報のDataFrame
        """
        filters: dict[str, Any] = {}
        if keito_id:
            filters["KEITO_ID"] = keito_id
        return self.table_accessor.get_table_data("KEITO_JOHO2", filters or None)
