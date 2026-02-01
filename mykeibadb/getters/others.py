"""その他テーブルGetter.

その他のテーブル（1テーブル）へのアクセスを提供する。

Tables:
    - SHOBUFUKU: 勝負服情報
"""

from typing import Any

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_banushi_code


class OthersGetter(BaseGetter):
    """その他テーブルGetter.

    その他の1テーブルに対するアクセスメソッドを提供する。
    """

    def get_shobufuku(
        self,
        banushi_code: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """SHOBUFUKUテーブルから勝負服情報を取得.

        Args:
            banushi_code (str | list[str] | None): 馬主コード

        Returns:
            pd.DataFrame: 勝負服情報のDataFrame
        """
        validate_banushi_code(banushi_code)
        filters: dict[str, Any] = {}
        if banushi_code:
            filters["BANUSHI_CODE"] = banushi_code
        return self.table_accessor.get_table_data("SHOBUFUKU", filters or None)
