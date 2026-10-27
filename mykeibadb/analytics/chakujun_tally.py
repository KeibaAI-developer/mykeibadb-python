"""着度数集計フェーズ2: 着順収集・集計モジュール."""

from typing import Any

from mykeibadb.analytics._cte_helpers import build_payout_ctes
from mykeibadb.analytics._models import ChakudoTally, EntrySet, GroupTally
from mykeibadb.connection import ConnectionManager


def tally_chakujun(manager: ConnectionManager, entries: EntrySet) -> ChakudoTally:
    """EntrySet の着順・払戻を収集し group_label ごとに集計して ChakudoTally を返す.

    Args:
        manager (ConnectionManager): DB接続マネージャ
        entries (EntrySet): フェーズ1で得られたエントリリスト

    Returns:
        ChakudoTally: グループ別着順カウント・払戻合計のリスト。entries が空の場合は空リスト。

    Raises:
        QueryExecutionError: DBエラーが発生した場合
    """
    if not entries:
        return []

    params: list[Any] = []
    placeholders = ", ".join(["(%s, %s, %s)"] * len(entries))
    for entry in entries:
        params.extend([entry.race_code, entry.umaban, entry.group_label])

    payout_ctes = build_payout_ctes()

    sql = f"""
        WITH
        {payout_ctes},
        entries(race_code, umaban, group_label) AS (
            VALUES {placeholders}
        )
        SELECT
            e.group_label,
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE TRIM(u.kakutei_chakujun) = '01') AS wins,
            COUNT(*) FILTER (WHERE TRIM(u.kakutei_chakujun) = '02') AS second,
            COUNT(*) FILTER (WHERE TRIM(u.kakutei_chakujun) = '03') AS third,
            COUNT(*) FILTER (
                WHERE TRIM(u.kakutei_chakujun) NOT IN ('01', '02', '03')
            ) AS chakugai,
            COALESCE(SUM(tp.payout), 0) AS tansho_payout_sum,
            COALESCE(SUM(fp.payout), 0) AS fukusho_payout_sum
        FROM entries e
        JOIN umagoto_race_joho u ON e.race_code = u.race_code AND e.umaban = u.umaban
        LEFT JOIN tansho_payouts tp ON e.race_code = tp.race_code AND e.umaban = tp.umaban
        LEFT JOIN fukusho_payouts fp ON e.race_code = fp.race_code AND e.umaban = fp.umaban
        GROUP BY e.group_label
        ORDER BY e.group_label
    """

    df = manager.fetch_dataframe(sql, params=tuple(params))
    return [
        GroupTally(
            group=str(row["group_label"]),
            total=int(row["total"]),
            wins=int(row["wins"]),
            second=int(row["second"]),
            third=int(row["third"]),
            chakugai=int(row["chakugai"]),
            tansho_payout_sum=int(row["tansho_payout_sum"]),
            fukusho_payout_sum=int(row["fukusho_payout_sum"]),
        )
        for _, row in df.iterrows()
    ]
