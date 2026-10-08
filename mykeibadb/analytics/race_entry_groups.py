"""指定レースの出走馬のグループ値取得モジュール."""

import re
from typing import Any

import pandas as pd

from mykeibadb.analytics._models import GroupBy
from mykeibadb.analytics.entry_select import _build_entry_select_sql
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError

_RACE_CODE_PATTERN = re.compile(r"^[0-9]{16}$")
# 出走取消・発走除外・競走除外の異常区分コード
_EXCLUDED_IJO_KUBUN_CODES = ("1", "2", "3")


def get_race_entry_groups(
    manager: ConnectionManager,
    race_code: str,
    group_by: GroupBy,
) -> dict[int, str | None]:
    """指定レースの出走馬ごとに、group_by のグループの値を返す.

    analyze_chakudo と同じ group_by の解釈（race_col / subject / history / fixed）で値を求める。
    確定着順の有無は問わない。出走取消・発走除外・競走除外（異常区分コード 1〜3）の馬は含めない。
    過去走を使う属性（前走・過去の実績・調教・父馬の好走など）は、そのレースの開催日より前の記録から
    求める。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_code (str): 16桁のレースコード
        group_by (GroupBy): グループ分け軸

    Returns:
        dict[int, str | None]: 馬番 -> グループの値。値が求まらない馬（前走が無いなど）は None。

    Raises:
        ValueError: race_code が16桁の数字でない場合
        ValueError: group_by.kind が未対応の場合
        MykeibaDBError: 指定レースの出走馬が DB に無い場合、または DB エラーの場合
    """
    if not _RACE_CODE_PATTERN.fullmatch(race_code):
        raise ValueError(f"race_code は16桁の数字で指定してください: {race_code!r}")

    params: list[Any] = []

    def build_entry_where(where_params: list[Any]) -> list[str]:
        where_params.extend([race_code, list(_EXCLUDED_IJO_KUBUN_CODES)])
        return ["u.race_code = %s", "NOT (u.ijo_kubun_code = ANY(%s))"]

    sql = _build_entry_select_sql(
        group_by, params, [], "", build_entry_where, history_before_race=True
    )
    df = manager.fetch_dataframe(sql, params=tuple(params))
    if df.empty:
        raise MykeibaDBError(f"出走馬が見つかりません: race_code={race_code}")
    return {
        int(row["umaban"]): None if pd.isna(row["group_label"]) else str(row["group_label"])
        for _, row in df.iterrows()
    }
