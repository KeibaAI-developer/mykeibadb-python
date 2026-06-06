"""調教データ取得・分析モジュール."""

from typing import Any

import pandas as pd

from mykeibadb.analytics._chokyo_helpers import build_threshold_where, resolve_threshold_col
from mykeibadb.analytics._cte_helpers import build_payout_ctes, build_race_condition_where
from mykeibadb.analytics._models import ChokyoCondition, RaceCondition
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
      - race_code + horse_num: 指定レースより前かつ前走よりあとの調教データを取得
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
    use_race = race_code is not None or horse_num is not None
    use_ketto = ketto_toroku_bango is not None
    if use_race and use_ketto:
        raise ValueError(
            "race_code+horse_num と ketto_toroku_bango は同時に指定できません。"
        )
    if use_race:
        if race_code is None or horse_num is None:
            raise ValueError("race_code と horse_num は両方同時に指定してください。")
        return _get_chokyo_by_race(manager, race_code, horse_num)
    if use_ketto:
        assert ketto_toroku_bango is not None
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
            JOIN race_shosai r ON u.race_code = r.race_code
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
            JOIN race_shosai r2 ON u2.race_code = r2.race_code
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


def analyze_chokyo_debut_seiseki(
    manager: ConnectionManager,
    debut_date_from: str,
    debut_date_to: str,
    condition: ChokyoCondition,
) -> dict[str, Any]:
    """デビュー前調教条件を満たした馬のデビュー後勝利率を集計する.

    指定期間にデビューした馬のうち、デビュー前の調教データが ChokyoCondition を
    満たす馬を抽出し、同期間内の勝利率を集計する。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        debut_date_from (str): デビュー期間開始日（yyyymmdd形式）
        debut_date_to (str): デビュー期間終了日（yyyymmdd形式）
        condition (ChokyoCondition): 調教閾値条件のリスト

    Returns:
        dict[str, Any]: success フラグと集計結果。
            キー: success, debut_date_from, debut_date_to, total, winners, win_rate

    Raises:
        ValueError: condition内に未対応の course または metric が含まれる場合、もしくは furlong が正の整数でない場合

    Note:
        condition が空リストの場合はデビュー期間の全馬を対象として集計する。
    """
    for t in condition:
        resolve_threshold_col(t)

    wood_thresholds = [t for t in condition if t.course == "wood"]
    hanro_thresholds = [t for t in condition if t.course == "hanro"]
    use_wood = bool(wood_thresholds)
    use_hanro = bool(hanro_thresholds)

    try:
        cte_parts: list[str] = []
        sql_params: list[Any] = []

        cte_parts.append("""
    debut_horses AS (
        SELECT ketto_toroku_bango,
               MIN(kaisai_nen || kaisai_gappi) AS debut_date
        FROM umagoto_race_joho
        WHERE kakutei_chakujun ~ '^[0-9]{2}$'
          AND kakutei_chakujun != '00'
        GROUP BY ketto_toroku_bango
        HAVING MIN(kaisai_nen || kaisai_gappi) BETWEEN %s AND %s
    )""")
        sql_params.extend([debut_date_from, debut_date_to])

        if use_wood:
            wood_conds: list[str] = []
            for t in wood_thresholds:
                wood_conds.extend(build_threshold_where(t, "w", sql_params))
            wood_where = " AND ".join(wood_conds)
            cte_parts.append(f"""
    wood_qualified AS (
        SELECT DISTINCT w.ketto_toroku_bango
        FROM woodchip_chokyo w
        JOIN debut_horses d ON w.ketto_toroku_bango = d.ketto_toroku_bango
        WHERE w.chokyo_nengappi < d.debut_date
          AND {wood_where}
    )""")

        if use_hanro:
            hanro_conds: list[str] = []
            for t in hanro_thresholds:
                hanro_conds.extend(build_threshold_where(t, "h", sql_params))
            hanro_where = " AND ".join(hanro_conds)
            cte_parts.append(f"""
    hanro_qualified AS (
        SELECT DISTINCT h.ketto_toroku_bango
        FROM hanro_chokyo h
        JOIN debut_horses d ON h.ketto_toroku_bango = d.ketto_toroku_bango
        WHERE h.chokyo_nengappi < d.debut_date
          AND {hanro_where}
    )""")

        cte_parts.append("""
    winners AS (
        SELECT DISTINCT ketto_toroku_bango
        FROM umagoto_race_joho
        WHERE kakutei_chakujun = '01'
          AND kaisai_nen || kaisai_gappi BETWEEN %s AND %s
    )""")
        sql_params.extend([debut_date_from, debut_date_to])

        if use_wood and use_hanro:
            qualified_from = (
                "(SELECT ketto_toroku_bango FROM wood_qualified "
                "INTERSECT "
                "SELECT ketto_toroku_bango FROM hanro_qualified) qualified"
            )
        elif use_wood:
            qualified_from = "wood_qualified qualified"
        elif use_hanro:
            qualified_from = "hanro_qualified qualified"
        else:
            qualified_from = "debut_horses qualified"

        cte_sql = ",".join(cte_parts)
        sql = f"""
    WITH {cte_sql}
    SELECT
        COUNT(DISTINCT qualified.ketto_toroku_bango) AS total,
        COUNT(DISTINCT CASE WHEN winners.ketto_toroku_bango IS NOT NULL
            THEN qualified.ketto_toroku_bango END) AS winners
    FROM {qualified_from}
    LEFT JOIN winners ON qualified.ketto_toroku_bango = winners.ketto_toroku_bango
        """

        df = manager.fetch_dataframe(sql, params=tuple(sql_params))
        row = df.iloc[0]
        total = int(row["total"])
        win_count = int(row["winners"])
        return {
            "success": True,
            "debut_date_from": debut_date_from,
            "debut_date_to": debut_date_to,
            "total": total,
            "winners": win_count,
            "win_rate": round(win_count / total * 100, 1) if total > 0 else 0.0,
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
                    JOIN race_shosai r ON u.race_code = r.race_code
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
