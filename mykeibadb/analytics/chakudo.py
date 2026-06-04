"""グループ別着度数・回収率集計モジュール."""

from typing import Any

from mykeibadb.analytics._cte_helpers import (
    build_course_week_cte,
    build_payout_ctes,
    build_race_condition_where,
)
from mykeibadb.analytics._models import ChakudoResult, ChakudoRow, RaceCondition
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError


def analyze_chakudo(
    manager: ConnectionManager,
    group_expr: str,
    sort_expr: str,
    condition: RaceCondition | None = None,
) -> ChakudoResult:
    """グループ別着度数・勝率・回収率を集計する.

    Args:
        manager (ConnectionManager): DB接続マネージャ
        group_expr (str): GROUP BY に使用するSQL式
        sort_expr (str): base CTE の SELECT で sort_key を生成するSQL式（ASC/DESC等のORDER BY句断片は含めない）
        condition (RaceCondition | None): レース絞り込み条件。
            condition.course_kubun と condition.week_in_course は両方同時に指定するか、
            両方 None にすること。

    Returns:
        ChakudoResult: グループ別集計結果

    Raises:
        ValueError: condition.course_kubun と condition.week_in_course のどちらか一方のみ指定した場合
        ValueError: group_expr または sort_expr に危険なSQLトークン（';', '--', '/*'）が含まれる場合

    Note:
        group_expr / sort_expr は SQL に直接埋め込まれるため、必ず信頼済みの式を渡すこと。
        危険トークンの除去は最低限の保護であり、完全なSQLインジェクション防御ではない。
    """
    _dangerous_tokens = (";", "--", "/*")
    for expr_name, expr in (("group_expr", group_expr), ("sort_expr", sort_expr)):
        if any(tok in expr for tok in _dangerous_tokens):
            raise ValueError(f"{expr_name} に危険なSQLトークンが含まれています: {expr!r}")

    cond_kubun = condition.course_kubun if condition else None
    cond_week = condition.week_in_course if condition else None
    if (cond_kubun is None) != (cond_week is None):
        raise ValueError(
            "condition.course_kubun と condition.week_in_course は"
            "両方同時に指定するか、両方 None にしてください。"
        )

    try:
        params: list[Any] = []
        cte_parts: list[str] = []
        join_sql = ""
        using_cw = False

        if cond_kubun is not None and cond_week is not None:
            keibajo_code = condition.keibajo_code if condition else None
            cte_sql, join_sql = build_course_week_cte(
                keibajo_code, cond_kubun, cond_week, params
            )
            cte_parts.append(cte_sql)
            using_cw = True

        cte_parts.append(build_payout_ctes())

        where_parts: list[str] = [
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]
        if condition is not None:
            where_parts.extend(
                build_race_condition_where(condition, params, include_keibajo_code=not using_cw)
            )

        where_clause = "\n              AND ".join(where_parts)
        cte_parts.append(
            f"""base AS (
            SELECT
                {group_expr} AS grp,
                {sort_expr} AS sort_key,
                u.kakutei_chakujun,
                u.umaban,
                u.race_code
            FROM umagoto_race_joho u
            JOIN race_joho r ON u.race_code = r.race_code
            {join_sql}
            WHERE {where_clause}
        )"""
        )

        sql = f"""
            WITH {", ".join(cte_parts)}
            SELECT
                grp,
                sort_key,
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
            GROUP BY grp, sort_key
            ORDER BY sort_key
        """

        df = manager.fetch_dataframe(sql, params=tuple(params))
        rows = [ChakudoRow.from_series(row) for _, row in df.iterrows()]
        return ChakudoResult(success=True, rows=rows)
    except MykeibaDBError as e:
        return ChakudoResult(success=False, error=str(e))
