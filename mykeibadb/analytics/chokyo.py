"""調教データ取得・分析モジュール."""

from typing import Any

import pandas as pd

from mykeibadb.analytics._cte_helpers import build_payout_ctes, build_race_condition_where
from mykeibadb.analytics._models import RaceCondition
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError

_WOOD_VALID = "w.time_gokei_6furlong NOT IN ('0000', '9999')"
_HANRO_VALID = "h.time_gokei_4furlong NOT IN ('0000', '9999')"


def get_uma_chokyo(
    manager: ConnectionManager,
    race_code: str | None = None,
    horse_num: int | None = None,
    ketto_toroku_bango: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict[str, Any]:
    """馬の調教データを取得する.

    指定方法は2通り（排他）:
      - race_code + horse_num: レース起点。前走〜当日の調教窓を自動設定
      - ketto_toroku_bango: 血統登録番号で直接指定。date_from/date_toで窓指定

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_code (str | None): レースコード（horse_numと併用）
        horse_num (int | None): 馬番（race_codeと併用）
        ketto_toroku_bango (str | None): 血統登録番号（直接指定）
        date_from (str | None): 調教日下限（yyyymmdd、ketto指定時）
        date_to (str | None): 調教日上限（yyyymmdd、ketto指定時）

    Returns:
        dict[str, Any]: success フラグと調教データのリスト。
            キー: success, race_date, ketto_toroku_bango,
                  wood_records（list）, hanro_records（list）

    Raises:
        ValueError: 指定方法が不正な場合
    """
    if race_code is not None and horse_num is not None:
        return _get_chokyo_by_race(manager, race_code, horse_num)
    if ketto_toroku_bango is not None:
        return _get_chokyo_by_ketto(manager, ketto_toroku_bango, date_from, date_to)
    raise ValueError(
        "race_code+horse_num または ketto_toroku_bango のいずれかを指定してください。"
    )


def _get_chokyo_by_race(
    manager: ConnectionManager,
    race_code: str,
    horse_num: int,
) -> dict[str, Any]:
    """レースコード・馬番から調教データを取得する."""
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
        info_df = manager.fetch_dataframe(info_sql, params=(race_code, umaban_str))
        if info_df.empty:
            return {"success": True, "race_date": None, "ketto_toroku_bango": None,
                    "wood_records": [], "hanro_records": []}

        ketto = str(info_df.iloc[0]["ketto_toroku_bango"])
        race_date = str(info_df.iloc[0]["race_date"])

        prev_sql = """
            SELECT r2.kaisai_nen || r2.kaisai_gappi AS prev_race_date
            FROM umagoto_race_joho u2
            JOIN race_joho r2 ON u2.race_code = r2.race_code
            WHERE u2.ketto_toroku_bango = %s
              AND (r2.kaisai_nen || r2.kaisai_gappi) < %s
              AND u2.kakutei_chakujun ~ '^[0-9]{2}$'
              AND u2.kakutei_chakujun != '00'
            ORDER BY r2.kaisai_nen DESC, r2.kaisai_gappi DESC
            LIMIT 1
        """
        prev_df = manager.fetch_dataframe(prev_sql, params=(ketto, race_date))
        prev_race_date = str(prev_df.iloc[0]["prev_race_date"]) if not prev_df.empty else None

        wood_params: tuple[Any, ...]
        wood_date_cond: str
        if prev_race_date is not None:
            wood_params = (ketto, prev_race_date, race_date)
            wood_date_cond = "AND w.chokyo_nengappi > %s AND w.chokyo_nengappi < %s"
        else:
            wood_params = (ketto, race_date)
            wood_date_cond = "AND w.chokyo_nengappi < %s"

        wood_sql = f"""
            SELECT w.tracen_kubun, w.chokyo_nengappi, w.chokyo_jikoku,
                   w.time_gokei_6furlong, w.time_gokei_5furlong, w.time_gokei_4furlong,
                   w.laptime_1furlong, w.laptime_2furlong, w.laptime_3furlong
            FROM woodchip_chokyo w
            WHERE w.ketto_toroku_bango = %s
              AND {_WOOD_VALID}
              {wood_date_cond}
            ORDER BY w.chokyo_nengappi DESC, w.chokyo_jikoku DESC
        """
        wood_df = manager.fetch_dataframe(wood_sql, params=wood_params)

        hanro_date_filter_sql = (
            "AND h.chokyo_nengappi > %s AND h.chokyo_nengappi < %s"
            if prev_race_date
            else "AND h.chokyo_nengappi < %s"
        )
        hanro_params: tuple[Any, ...]
        if prev_race_date is not None:
            hanro_params = (ketto, prev_race_date, race_date)
        else:
            hanro_params = (ketto, race_date)

        hanro_sql = f"""
            SELECT h.tracen_kubun, h.chokyo_nengappi, h.chokyo_jikoku,
                   h.time_gokei_4furlong,
                   h.lap_time_1furlong, h.lap_time_2furlong,
                   h.lap_time_3furlong, h.lap_time_4furlong
            FROM hanro_chokyo h
            WHERE h.ketto_toroku_bango = %s
              AND {_HANRO_VALID}
              {hanro_date_filter_sql}
            ORDER BY h.chokyo_nengappi DESC, h.chokyo_jikoku DESC
        """
        hanro_df = manager.fetch_dataframe(hanro_sql, params=hanro_params)

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


def _get_chokyo_by_ketto(
    manager: ConnectionManager,
    ketto_toroku_bango: str,
    date_from: str | None,
    date_to: str | None,
) -> dict[str, Any]:
    """血統登録番号から調教データを取得する."""
    try:
        wood_parts: list[str] = ["w.ketto_toroku_bango = %s", _WOOD_VALID]
        wood_params: list[Any] = [ketto_toroku_bango]
        if date_from is not None:
            wood_parts.append("w.chokyo_nengappi >= %s")
            wood_params.append(date_from)
        if date_to is not None:
            wood_parts.append("w.chokyo_nengappi <= %s")
            wood_params.append(date_to)

        wood_sql = f"""
            SELECT w.tracen_kubun, w.chokyo_nengappi, w.chokyo_jikoku,
                   w.time_gokei_6furlong, w.time_gokei_5furlong, w.time_gokei_4furlong,
                   w.laptime_1furlong, w.laptime_2furlong, w.laptime_3furlong
            FROM woodchip_chokyo w
            WHERE {" AND ".join(wood_parts)}
            ORDER BY w.chokyo_nengappi DESC, w.chokyo_jikoku DESC
        """
        wood_df = manager.fetch_dataframe(wood_sql, params=tuple(wood_params))

        hanro_parts: list[str] = ["h.ketto_toroku_bango = %s", _HANRO_VALID]
        hanro_params: list[Any] = [ketto_toroku_bango]
        if date_from is not None:
            hanro_parts.append("h.chokyo_nengappi >= %s")
            hanro_params.append(date_from)
        if date_to is not None:
            hanro_parts.append("h.chokyo_nengappi <= %s")
            hanro_params.append(date_to)

        hanro_sql = f"""
            SELECT h.tracen_kubun, h.chokyo_nengappi, h.chokyo_jikoku,
                   h.time_gokei_4furlong,
                   h.lap_time_1furlong, h.lap_time_2furlong,
                   h.lap_time_3furlong, h.lap_time_4furlong
            FROM hanro_chokyo h
            WHERE {" AND ".join(hanro_parts)}
            ORDER BY h.chokyo_nengappi DESC, h.chokyo_jikoku DESC
        """
        hanro_df = manager.fetch_dataframe(hanro_sql, params=tuple(hanro_params))

        wood_records = [_row_to_wood_record(r) for _, r in wood_df.iterrows()]
        hanro_records = [_row_to_hanro_record(r) for _, r in hanro_df.iterrows()]

        return {
            "success": True,
            "race_date": None,
            "ketto_toroku_bango": ketto_toroku_bango,
            "wood_records": wood_records,
            "hanro_records": hanro_records,
        }
    except MykeibaDBError as e:
        return {"success": False, "error": str(e)}


def analyze_chokyo_seiseki(
    manager: ConnectionManager,
    condition: RaceCondition | None = None,
) -> dict[str, Any]:
    """調教タイプ別のレース成績を集計する.

    対象レースの出走馬について、レース当日より前の坂路・ウッドチップ調教データの
    有無でグループ分けし、着度数・回収率を集計する。
    グループ: 「坂路+ウッド」「ウッドのみ」「坂路のみ」「なし」

    Args:
        manager (ConnectionManager): DB接続マネージャ
        condition (RaceCondition | None): レース絞り込み条件

    Returns:
        dict[str, Any]: success フラグと集計結果。
            キー: success, rows（list[dict]）
    """
    try:
        params: list[Any] = []

        where_parts: list[str] = [
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]
        if condition is not None:
            where_parts.extend(build_race_condition_where(condition, params))

        where_clause = "\n              AND ".join(where_parts)

        payout_ctes = build_payout_ctes()

        sql = f"""
            WITH RECURSIVE {payout_ctes},
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
