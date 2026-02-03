"""マスタデータテーブルGetter.

マスタデータのテーブル（8テーブル）へのアクセスを提供する。

Tables:
    - KYOSOBA_MASTER2: 競走馬マスタ
    - KISHU_MASTER: 騎手マスタ
    - CHOKYOSHI_MASTER: 調教師マスタ
    - SEISANSHA_MASTER2: 生産者マスタ
    - BANUSHI_MASTER: 馬主マスタ
    - HANSHOKUBA_MASTER2: 繁殖馬マスタ
    - SANKU_MASTER2: 産駒マスタ
    - RECORD_MASTER: レコードマスタ
"""

from datetime import date
from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import (
    validate_banushi_code,
    validate_chokyoshi_code,
    validate_hanshoku_toroku_bango,
    validate_keibajo_code,
    validate_ketto_toroku_bango,
    validate_kishu_code,
    validate_seisansha_code,
    validate_track_code,
)


class MasterGetter(BaseGetter):
    """マスタデータテーブルGetter.

    マスタデータの8テーブルに対するアクセスメソッドを提供する。
    """

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
            start_date (date | None): 開始日（生年基準、年のみ使用）
            end_date (date | None): 終了日（生年基準、年のみ使用）

        Returns:
            pd.DataFrame: 繁殖馬マスタのDataFrame
        """
        validate_hanshoku_toroku_bango(hanshoku_toroku_bango)
        filters: dict[str, Any] = {}
        if hanshoku_toroku_bango:
            filters["HANSHOKU_TOROKU_BANGO"] = hanshoku_toroku_bango
        return self._get_table_with_year_only_period(
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
            filters["KYORI"] = str(kyori)
        if track_code:
            filters["TRACK_CODE"] = track_code
        return self.table_accessor.get_table_data("RECORD_MASTER", filters or None)
