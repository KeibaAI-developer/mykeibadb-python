"""WIN5テーブルGetter.

WIN5のテーブル（2テーブル）へのアクセスを提供する。

Tables:
    - WIN5: 重勝式ベース情報
    - WIN5_HARAIMODOSHI: 重勝式払戻情報
"""

from datetime import date

import pandas as pd

from mykeibadb.getters.base import BaseGetter
from mykeibadb.utils import validate_date_range


class Win5Getter(BaseGetter):
    """WIN5テーブルGetter.

    WIN5の2テーブルに対するアクセスメソッドを提供する。
    """

    def get_win5(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """WIN5テーブルから重勝式ベース情報を取得.

        Args:
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 重勝式ベース情報のDataFrame
        """
        validate_date_range(start_date, end_date)
        return self._get_table_with_period_composite_date(
            "WIN5",
            None,
            start_date,
            end_date,
        )

    def get_win5_haraimodoshi(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """WIN5_HARAIMODOSHIテーブルから重勝式払戻情報を取得.

        Args:
            start_date (date | None): 開始日（開催日基準）
            end_date (date | None): 終了日（開催日基準）

        Returns:
            pd.DataFrame: 重勝式払戻情報のDataFrame
        """
        validate_date_range(start_date, end_date)
        return self._get_table_with_period_composite_date(
            "WIN5_HARAIMODOSHI",
            None,
            start_date,
            end_date,
        )
