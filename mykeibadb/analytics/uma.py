"""馬情報取得モジュール."""

from typing import Any

import pandas as pd

from mykeibadb.analytics._cte_helpers import build_race_condition_where
from mykeibadb.analytics._models import RaceCondition
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError


def get_uma_rekisen(
    manager: ConnectionManager,
    uma_name: str | None = None,
    ketto_toroku_bango: str | None = None,
    condition: RaceCondition | None = None,
) -> dict[str, Any]:
    """馬の競走成績一覧を取得する.

    uma_name（部分一致）または ketto_toroku_bango（完全一致）で馬を特定し、
    条件に合う競走成績を返す。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        uma_name (str | None): 馬名（部分一致）
        ketto_toroku_bango (str | None): 血統登録番号（完全一致）
        condition (RaceCondition | None): レース絞り込み条件

    Returns:
        dict[str, Any]: success フラグと競走成績リスト。
            キー: success, results（list[dict]）, count（int）

    Raises:
        ValueError: uma_name と ketto_toroku_bango のどちらも指定されていない場合
    """
    if uma_name is None and ketto_toroku_bango is None:
        raise ValueError(
            "uma_name または ketto_toroku_bango のいずれかを指定してください。"
        )
    try:
        params: list[Any] = []
        where_parts: list[str] = [
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]

        if ketto_toroku_bango is not None:
            where_parts.append("u.ketto_toroku_bango = %s")
            params.append(ketto_toroku_bango)
        else:
            where_parts.append("u.bamei LIKE %s")
            params.append(f"%{uma_name}%")

        if condition is not None:
            where_parts.extend(build_race_condition_where(condition, params))

        where_clause = "\n              AND ".join(where_parts)

        sql = f"""
            SELECT
                u.ketto_toroku_bango,
                u.bamei,
                r.kaisai_nen || r.kaisai_gappi AS race_date,
                r.keibajo_code,
                u.race_code,
                u.umaban,
                u.kakutei_chakujun,
                r.kyori,
                r.track_code,
                r.grade_code
            FROM umagoto_race_joho u
            JOIN race_joho r ON u.race_code = r.race_code
            WHERE {where_clause}
            ORDER BY r.kaisai_nen DESC, r.kaisai_gappi DESC, u.race_code
        """

        df = manager.fetch_dataframe(sql, params=tuple(params))
        results = [_row_to_rekisen_dict(r) for _, r in df.iterrows()]
        return {"success": True, "results": results, "count": len(results)}
    except MykeibaDBError as e:
        return {"success": False, "error": str(e), "results": [], "count": 0}


def _row_to_rekisen_dict(r: "pd.Series[Any]") -> dict[str, Any]:
    """競走成績DataFrameの1行をdict変換する."""
    return {
        "ketto_toroku_bango": str(r["ketto_toroku_bango"]),
        "bamei": str(r["bamei"]),
        "race_date": str(r["race_date"]),
        "keibajo_code": str(r["keibajo_code"]),
        "race_code": str(r["race_code"]),
        "umaban": str(r["umaban"]),
        "kakutei_chakujun": str(r["kakutei_chakujun"]),
        "kyori": int(r["kyori"]) if pd.notna(r["kyori"]) else None,
        "track_code": str(r["track_code"]),
        "grade_code": str(r["grade_code"]),
    }
