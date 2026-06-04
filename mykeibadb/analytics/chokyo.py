"""調教データ取得・分析モジュール."""

from typing import Any

import pandas as pd

from mykeibadb.analytics._cte_helpers import build_payout_ctes
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError

_WOOD_VALID = "w.time_gokei_6furlong NOT IN ('0000', '9999')"
_HANRO_VALID = "h.time_gokei_4furlong NOT IN ('0000', '9999')"


def get_uma_chokyo(
    manager: ConnectionManager,
    race_id: str,
    horse_num: int,
) -> dict[str, Any]:
    """馬の調教データを取得する.

    race_id と horse_num でレースを特定し、そのレース当日より前の
    ウッドチップ・坂路調教データを返す。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_id (str): レースID（race_code）
        horse_num (int): 馬番（1〜18）

    Returns:
        dict[str, Any]: success フラグと調教データのリスト。
            キー: success, race_date, ketto_toroku_bango,
                  wood_records（list）, hanro_records（list）
    """
    try:
        umaban_str = f"{horse_num:02}"
        info_sql = """
            SELECT u.ketto_toroku_bango,
                   r.kaisai_nen || r.kaisai_gappi AS race_date
            FROM umagoto_race_joho u
            JOIN race_joho r ON u.race_code = r.race_code
            WHERE u.race_code = %s
              AND u.umaban = %s
        """
        info_df = manager.fetch_dataframe(info_sql, params=(race_id, umaban_str))
        if info_df.empty:
            return {"success": True, "race_date": None, "ketto_toroku_bango": None,
                    "wood_records": [], "hanro_records": []}

        ketto = str(info_df.iloc[0]["ketto_toroku_bango"])
        race_date = str(info_df.iloc[0]["race_date"])

        wood_sql = """
            SELECT tracen_kubun, chokyo_nengappi, chokyo_jikoku,
                   time_gokei_6furlong, time_gokei_5furlong, time_gokei_4furlong,
                   laptime_1furlong, laptime_2furlong, laptime_3furlong
            FROM woodchip_chokyo
            WHERE ketto_toroku_bango = %s
              AND time_gokei_6furlong NOT IN ('0000', '9999')
              AND chokyo_nengappi < %s
            ORDER BY chokyo_nengappi DESC, chokyo_jikoku DESC
        """
        wood_df = manager.fetch_dataframe(wood_sql, params=(ketto, race_date))

        hanro_sql = """
            SELECT tracen_kubun, chokyo_nengappi, chokyo_jikoku,
                   time_gokei_4furlong,
                   lap_time_1furlong, lap_time_2furlong,
                   lap_time_3furlong, lap_time_4furlong
            FROM hanro_chokyo
            WHERE ketto_toroku_bango = %s
              AND time_gokei_4furlong NOT IN ('0000', '9999')
              AND chokyo_nengappi < %s
            ORDER BY chokyo_nengappi DESC, chokyo_jikoku DESC
        """
        hanro_df = manager.fetch_dataframe(hanro_sql, params=(ketto, race_date))

        wood_records = [_row_to_wood_record(r) for _, r in wood_df.iterrows()]
        hanro_records = [_row_to_hanro_record(r) for _, r in hanro_df.iterrows()]

        return {
            "success": True,
            "race_date": race_date,
            "ketto_toroku_bango": ketto,
            "wood_records": wood_records,
            "hanro_records": hanro_records,
        }
    except MykeibaDBError as e:
        return {"success": False, "error": str(e)}


def analyze_chokyo_debut_seiseki(
    manager: ConnectionManager,
    race_name: str | None = None,
    keibajo: str | None = None,
    kyori: int | None = None,
    year_from: str | None = None,
    year_to: str | None = None,
) -> dict[str, Any]:
    """調教タイプ別の新馬・未勝利戦成績を集計する.

    対象レースの出走馬について、レース当日より前の坂路・ウッドチップ調教データの
    有無でグループ分けし、着度数・回収率を集計する。
    グループ: 「坂路+ウッド」「ウッドのみ」「坂路のみ」「なし」

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_name (str | None): レース名フィルタ（部分一致）
        keibajo (str | None): 競馬場コードフィルタ
        kyori (int | None): 距離フィルタ
        year_from (str | None): 集計開始年（YYYY形式）
        year_to (str | None): 集計終了年（YYYY形式）

    Returns:
        dict[str, Any]: success フラグと集計結果。
            キー: success, rows（list[dict]）
    """
    try:
        params: list[Any] = []

        where_parts: list[str] = [
            "r.kyoso_joken_code_saijakunen IN ('701', '703')",
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]
        if race_name:
            where_parts.append("r.race_name LIKE %s")
            params.append(f"%{race_name}%")
        if keibajo:
            where_parts.append("r.keibajo_code = %s")
            params.append(keibajo)
        if kyori:
            where_parts.append("r.kyori = %s")
            params.append(kyori)
        if year_from:
            where_parts.append("r.kaisai_nen >= %s")
            params.append(year_from)
        if year_to:
            where_parts.append("r.kaisai_nen <= %s")
            params.append(year_to)

        where_clause = "\n              AND ".join(where_parts)

        payout_ctes = build_payout_ctes()

        sql = f"""
            WITH {payout_ctes},
            base AS (
                SELECT
                    CASE
                        WHEN has_wood AND has_hanro THEN '坂路+ウッド'
                        WHEN has_wood THEN 'ウッドのみ'
                        WHEN has_hanro THEN '坂路のみ'
                        ELSE 'なし'
                    END AS grp,
                    sq.kakutei_chakujun,
                    sq.umaban,
                    sq.race_code
                FROM (
                    SELECT
                        u.ketto_toroku_bango,
                        u.kakutei_chakujun,
                        u.umaban,
                        u.race_code,
                        EXISTS (
                            SELECT 1 FROM woodchip_chokyo w
                            WHERE w.ketto_toroku_bango = u.ketto_toroku_bango
                              AND w.chokyo_nengappi < (r.kaisai_nen || r.kaisai_gappi)
                              AND {_WOOD_VALID}
                        ) AS has_wood,
                        EXISTS (
                            SELECT 1 FROM hanro_chokyo h
                            WHERE h.ketto_toroku_bango = u.ketto_toroku_bango
                              AND h.chokyo_nengappi < (r.kaisai_nen || r.kaisai_gappi)
                              AND {_HANRO_VALID}
                        ) AS has_hanro
                    FROM umagoto_race_joho u
                    JOIN race_joho r ON u.race_code = r.race_code
                    WHERE {where_clause}
                ) sq
            )
            SELECT
                grp,
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE kakutei_chakujun = '01') AS wins,
                COUNT(*) FILTER (WHERE kakutei_chakujun = '02') AS second,
                COUNT(*) FILTER (WHERE kakutei_chakujun = '03') AS third,
                COUNT(*) FILTER (
                    WHERE kakutei_chakujun NOT IN ('01', '02', '03')
                ) AS chakugai,
                ROUND(
                    COUNT(*) FILTER (WHERE kakutei_chakujun = '01')
                    * 100.0 / NULLIF(COUNT(*), 0), 1
                ) AS win_rate,
                ROUND(
                    COUNT(*) FILTER (WHERE kakutei_chakujun IN ('01', '02', '03'))
                    * 100.0 / NULLIF(COUNT(*), 0), 1
                ) AS fukusho_rate,
                ROUND(
                    COALESCE(SUM(tp.payout), 0) * 1.0 / NULLIF(COUNT(*), 0), 1
                ) AS tansho_kaishuu,
                ROUND(
                    COALESCE(SUM(fp.payout), 0) * 1.0 / NULLIF(COUNT(*), 0), 1
                ) AS fukusho_kaishuu
            FROM base
            LEFT JOIN tansho_payouts tp
                ON base.race_code = tp.race_code AND base.umaban = tp.umaban
            LEFT JOIN fukusho_payouts fp
                ON base.race_code = fp.race_code AND base.umaban = fp.umaban
            GROUP BY grp
            ORDER BY MIN(CASE grp
                WHEN '坂路+ウッド' THEN 0
                WHEN 'ウッドのみ' THEN 1
                WHEN '坂路のみ' THEN 2
                ELSE 3
            END)
        """

        df = manager.fetch_dataframe(sql, params=tuple(params))
        rows = [_row_to_result_dict(r) for _, r in df.iterrows()]
        return {"success": True, "rows": rows}
    except MykeibaDBError as e:
        return {"success": False, "error": str(e)}


def _row_to_wood_record(r: "pd.Series[Any]") -> dict[str, Any]:
    """ウッドチップ調教DataFrameの1行をdict変換する."""
    tracen = "美浦" if str(r["tracen_kubun"]) == "0" else "栗東"
    return {
        "course_type": "ウッドチップ",
        "tracen": tracen,
        "date": str(r["chokyo_nengappi"]),
        "jikoku": str(r["chokyo_jikoku"]),
        "time_6f": str(r["time_gokei_6furlong"]),
        "time_5f": str(r["time_gokei_5furlong"]),
        "time_4f": str(r["time_gokei_4furlong"]),
        "lap_1f": str(r["laptime_1furlong"]),
        "lap_2f": str(r["laptime_2furlong"]),
        "lap_3f": str(r["laptime_3furlong"]),
    }


def _row_to_hanro_record(r: "pd.Series[Any]") -> dict[str, Any]:
    """坂路調教DataFrameの1行をdict変換する."""
    tracen = "美浦" if str(r["tracen_kubun"]) == "0" else "栗東"
    return {
        "course_type": "坂路",
        "tracen": tracen,
        "date": str(r["chokyo_nengappi"]),
        "jikoku": str(r["chokyo_jikoku"]),
        "time_4f": str(r["time_gokei_4furlong"]),
        "lap_1f": str(r["lap_time_1furlong"]),
        "lap_2f": str(r["lap_time_2furlong"]),
        "lap_3f": str(r["lap_time_3furlong"]),
        "lap_4f": str(r["lap_time_4furlong"]),
    }


def _row_to_result_dict(r: "pd.Series[Any]") -> dict[str, Any]:
    """集計結果DataFrameの1行をdict変換する."""
    return {
        "group": str(r["grp"]),
        "total": int(r["total"]),
        "wins": int(r["wins"]),
        "second": int(r["second"]),
        "third": int(r["third"]),
        "chakugai": int(r["chakugai"]),
        "win_rate": float(r["win_rate"]) if pd.notna(r["win_rate"]) else 0.0,
        "fukusho_rate": float(r["fukusho_rate"]) if pd.notna(r["fukusho_rate"]) else 0.0,
        "tansho_kaishuu": (
            float(r["tansho_kaishuu"]) if pd.notna(r["tansho_kaishuu"]) else 0.0
        ),
        "fukusho_kaishuu": (
            float(r["fukusho_kaishuu"]) if pd.notna(r["fukusho_kaishuu"]) else 0.0
        ),
    }
