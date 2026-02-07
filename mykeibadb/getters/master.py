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

from mykeibadb.code_converter import (
    convert_babajotai_code,
    convert_grade_code,
    convert_hinshu_code,
    convert_ijo_kubun_code,
    convert_keibajo_code,
    convert_kijo_shikaku_code,
    convert_kishu_minarai_code,
    convert_kyoso_shubetsu_code,
    convert_moshoku_code,
    convert_seibetsu_code,
    convert_tenko_code,
    convert_tozai_shozoku_code,
    convert_track_code,
    convert_uma_kigo_code,
)
from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import (
    validate_banushi_code,
    validate_chokyoshi_code,
    validate_date_range,
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
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """KYOSOBA_MASTER2テーブルから競走馬マスタを取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            start_date (date | None): 開始日（生年月日基準）
            end_date (date | None): 終了日（生年月日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 競走馬マスタのDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        df = self._get_table_with_period(
            "KYOSOBA_MASTER2", filters or None, start_date, end_date, "SEINENGAPPI"
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        df["umakigo"] = df["umakigo_code"].map(convert_uma_kigo_code)
        df["seibetsu"] = df["seibetsu_code"].map(convert_seibetsu_code)
        df["hinshu"] = df["hinshu_code"].map(convert_hinshu_code)
        df["moshoku"] = df["moshoku_code"].map(convert_moshoku_code)
        df["tozai_shozoku"] = df["tozai_shozoku_code"].map(convert_tozai_shozoku_code)
        return df

    def get_kishu_master(
        self,
        kishu_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """KISHU_MASTERテーブルから騎手マスタを取得.

        Args:
            kishu_code (str | list[str] | None): 騎手コード
            start_date (date | None): 開始日（騎手免許交付年月日基準）
            end_date (date | None): 終了日（騎手免許交付年月日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 騎手マスタのDataFrame
        """
        validate_kishu_code(kishu_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if kishu_code:
            filters["KISHU_CODE"] = kishu_code
        df = self._get_table_with_period(
            "KISHU_MASTER", filters or None, start_date, end_date, "MENKYO_KOFU_NENGAPPI"
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        df["kijo_shikaku"] = df["kijo_shikaku_code"].map(convert_kijo_shikaku_code)
        df["kishu_minarai"] = df["kishu_minarai_code"].map(convert_kishu_minarai_code)
        df["tozai_shozoku"] = df["tozai_shozoku_code"].map(convert_tozai_shozoku_code)
        df["hatsukijo1_ijokubun"] = df["hatsukijo1_ijokubun_code"].map(convert_ijo_kubun_code)
        df["hatsukijo2_ijokubun"] = df["hatsukijo2_ijokubun_code"].map(convert_ijo_kubun_code)
        for i in range(1, 4):
            df[f"jusho{i}_grade"] = df[f"jusho{i}_grade_code"].map(convert_grade_code)
        return df

    def get_chokyoshi_master(
        self,
        chokyoshi_code: str | list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """CHOKYOSHI_MASTERテーブルから調教師マスタを取得.

        Args:
            chokyoshi_code (str | list[str] | None): 調教師コード
            start_date (date | None): 開始日（調教師免許交付年月日基準）
            end_date (date | None): 終了日（調教師免許交付年月日基準）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 調教師マスタのDataFrame
        """
        validate_chokyoshi_code(chokyoshi_code)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if chokyoshi_code:
            filters["CHOKYOSHI_CODE"] = chokyoshi_code
        df = self._get_table_with_period(
            "CHOKYOSHI_MASTER", filters or None, start_date, end_date, "MENKYO_KOFU_NENGAPPI"
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        df["tozai_shozoku"] = df["tozai_shozoku_code"].map(convert_tozai_shozoku_code)
        for i in range(1, 4):
            df[f"jusho{i}_grade"] = df[f"jusho{i}_grade_code"].map(convert_grade_code)
        return df

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
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """HANSHOKUBA_MASTER2テーブルから繁殖馬マスタを取得.

        Args:
            hanshoku_toroku_bango (str | list[str] | None): 繁殖登録番号
            start_date (date | None): 開始日（生年基準、年のみ使用）
            end_date (date | None): 終了日（生年基準、年のみ使用）
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 繁殖馬マスタのDataFrame
        """
        validate_hanshoku_toroku_bango(hanshoku_toroku_bango)
        validate_date_range(start_date, end_date)
        filters: dict[str, Any] = {}
        if hanshoku_toroku_bango:
            filters["HANSHOKU_TOROKU_BANGO"] = hanshoku_toroku_bango
        df = self._get_table_with_year_only_period(
            "HANSHOKUBA_MASTER2", filters or None, start_date, end_date, "SEINEN"
        )
        if df.empty or not convert_codes:
            return df
        # コード変換
        df["seibetsu"] = df["seibetsu_code"].map(convert_seibetsu_code)
        df["hinshu"] = df["hinshu_code"].map(convert_hinshu_code)
        df["moshoku"] = df["moshoku_code"].map(convert_moshoku_code)
        return df

    def get_sanku_master2(
        self,
        ketto_toroku_bango: str | list[str] | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """SANKU_MASTER2テーブルから産駒マスタを取得.

        Args:
            ketto_toroku_bango (str | list[str] | None): 血統登録番号
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: 産駒マスタのDataFrame
        """
        validate_ketto_toroku_bango(ketto_toroku_bango)
        filters: dict[str, Any] = {}
        if ketto_toroku_bango:
            filters["KETTO_TOROKU_BANGO"] = ketto_toroku_bango
        df = self.table_accessor.get_table_data("SANKU_MASTER2", filters or None)
        if df.empty or not convert_codes:
            return df
        # コード変換
        df["seibetsu"] = df["seibetsu_code"].map(convert_seibetsu_code)
        df["hinshu"] = df["hinshu_code"].map(convert_hinshu_code)
        df["moshoku"] = df["moshoku_code"].map(convert_moshoku_code)
        return df

    def get_record_master(
        self,
        keibajo_code: str | list[str] | None = None,
        kyori: int | list[int] | None = None,
        track_code: str | list[str] | None = None,
        convert_codes: bool = True,
    ) -> pd.DataFrame:
        """RECORD_MASTERテーブルからレコードマスタを取得.

        Args:
            keibajo_code (str | list[str] | None): 競馬場コード
            kyori (int | list[int] | None): 距離
            track_code (str | list[str] | None): トラックコード
            convert_codes (bool): 各種コードを名称に変換するかどうかのフラグ

        Returns:
            pd.DataFrame: レコードマスタのDataFrame
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
        df = self.table_accessor.get_table_data("RECORD_MASTER", filters or None)
        if df.empty or not convert_codes:
            return df
        # コード変換
        df["keibajo"] = df["keibajo_code"].map(convert_keibajo_code)
        df["grade"] = df["grade_code"].map(convert_grade_code)
        df["kyoso_shubetsu"] = df["kyoso_shubetsu_code"].map(convert_kyoso_shubetsu_code)
        df["track"] = df["track_code"].map(convert_track_code)
        df["tenko"] = df["tenko_code"].map(convert_tenko_code)
        df["shiba_babajotai"] = df["shiba_babajotai_code"].map(convert_babajotai_code)
        df["dirt_babajotai"] = df["dirt_babajotai_code"].map(convert_babajotai_code)
        for i in range(1, 4):
            df[f"hojiuma{i}_umakigo"] = df[f"hojiuma{i}_umakigo_code"].map(convert_uma_kigo_code)
            df[f"hojiuma{i}_seibetsu"] = df[f"hojiuma{i}_seibetsu_code"].map(convert_seibetsu_code)
        return df
