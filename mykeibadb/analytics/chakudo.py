"""グループ別着度数・回収率集計モジュール."""

from typing import Any

from mykeibadb.analytics._cte_helpers import build_course_week_cte, build_payout_ctes
from mykeibadb.analytics._models import ChakudoResult, ChakudoRow
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError


def analyze_chakudo(
    manager: ConnectionManager,
    group_expr: str,
    sort_expr: str,
    race_name: str | None = None,
    keibajo: str | None = None,
    kyori: int | None = None,
    year_from: str | None = None,
    year_to: str | None = None,
    grade: str | None = None,
    course_kubun: str | None = None,
    week_in_course: int | None = None,
) -> ChakudoResult:
    """グループ別着度数・勝率・回収率を集計する.

    Args:
        manager (ConnectionManager): DB接続マネージャ
        group_expr (str): GROUP BY に使用するSQL式
        sort_expr (str): base CTE の SELECT で sort_key を生成するSQL式（ASC/DESC等のORDER BY句断片は含めない）
        race_name (str | None): レース名フィルタ（部分一致）
        keibajo (str | None): 競馬場コードフィルタ
        kyori (int | None): 距離フィルタ
        year_from (str | None): 集計開始年（YYYY形式）
        year_to (str | None): 集計終了年（YYYY形式）
        grade (str | None): グレードコードフィルタ
        course_kubun (str | None): コース区分（week_in_course と同時指定必須）
        week_in_course (int | None): コース使用開始からの週番号（course_kubun と同時指定必須）

    Returns:
        ChakudoResult: グループ別集計結果

    Raises:
        ValueError: course_kubun と week_in_course のどちらか一方のみ指定した場合
        ValueError: group_expr または sort_expr に危険なSQLトークン（';', '--', '/*'）が含まれる場合

    Note:
        group_expr / sort_expr は SQL に直接埋め込まれるため、必ず信頼済みの式を渡すこと。
        危険トークンの除去は最低限の保護であり、完全なSQLインジェクション防御ではない。
    """
    _dangerous_tokens = (";", "--", "/*")
    for expr_name, expr in (("group_expr", group_expr), ("sort_expr", sort_expr)):
        if any(tok in expr for tok in _dangerous_tokens):
            raise ValueError(f"{expr_name} に危険なSQLトークンが含まれています: {expr!r}")

    if (course_kubun is None) != (week_in_course is None):
        raise ValueError(
            "course_kubun と week_in_course は両方同時に指定するか、両方 None にしてください。"
        )

    try:
        params: list[Any] = []
        cte_parts: list[str] = []
        join_sql = ""
        using_cw = False

        if course_kubun is not None and week_in_course is not None:
            cte_sql, join_sql = build_course_week_cte(keibajo, course_kubun, week_in_course, params)
            cte_parts.append(cte_sql)
            using_cw = True

        cte_parts.append(build_payout_ctes())

        where_parts: list[str] = [
            "u.kakutei_chakujun ~ '^[0-9]{2}$'",
            "u.kakutei_chakujun != '00'",
        ]
        if race_name:
            where_parts.append("r.race_name LIKE %s")
            params.append(f"%{race_name}%")
        if keibajo and not using_cw:
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
        if grade:
            where_parts.append("r.grade_code = %s")
            params.append(grade)

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
