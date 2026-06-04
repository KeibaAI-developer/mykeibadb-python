"""グループ別着度数・回収率集計モジュール."""

from typing import Any

from mykeibadb.analytics._cte_helpers import (
    SUBJECT_MAP,
    build_course_week_cte,
    build_payout_ctes,
    build_race_condition_where,
)
from mykeibadb.analytics._models import ChakudoResult, ChakudoRow, RaceCondition, Subject
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
        ValueError: condition.week_in_course が1未満の場合
        ValueError: group_expr または sort_expr に危険なSQLトークン（';', '--', '/*'）が含まれる場合

    Note:
        group_expr / sort_expr は SQL に直接埋め込まれるため、必ず信頼済みの式を渡すこと。
        危険トークンの除去は最低限の保護であり、完全なSQLインジェクション防御ではない。
    """
    _validate_expressions(group_expr, sort_expr)
    _validate_course_week(condition)
    return _run_chakudo_sql(manager, group_expr, sort_expr, condition)


def analyze_subject_chakudo(
    manager: ConnectionManager,
    subject: Subject,
    name: str | None = None,
    code: str | None = None,
    condition: RaceCondition | None = None,
) -> ChakudoResult:
    """主体（馬/騎手/調教師/馬主/種牡馬/生産者）別の着度数・勝率・回収率を集計する.

    主体名でグループ化し、name（部分一致）またはcode（完全一致）でフィルタする。
    code指定時はcodeを優先する。種牡馬/生産者はcode非対応のためnameのみ。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        subject (Subject): 集計主体
        name (str | None): 主体名（部分一致フィルタ）
        code (str | None): 主体コード（完全一致フィルタ。code対応主体のみ）
        condition (RaceCondition | None): レース絞り込み条件

    Returns:
        ChakudoResult: 主体別集計結果（ChakudoRow.group = 主体名）

    Raises:
        ValueError: code非対応の主体にcodeを指定した場合
    """
    mapping = SUBJECT_MAP[subject]
    if code is not None and mapping.code_col is None:
        raise ValueError(
            f"{subject.value} はコード指定に対応していません。name を使用してください。"
        )

    extra_join = mapping.join_sql or ""
    extra_where: list[str] = []
    extra_params: list[Any] = []

    if code is not None and mapping.code_col is not None:
        extra_where.append(f"{mapping.code_col} = %s")
        extra_params.append(code)
    elif name is not None:
        extra_where.append(f"{mapping.name_col} LIKE %s")
        extra_params.append(f"%{name}%")

    return _run_chakudo_sql(
        manager,
        mapping.group_col,
        mapping.group_col,
        condition,
        extra_join=extra_join,
        extra_where=extra_where,
        extra_params=extra_params,
    )


def _validate_expressions(group_expr: str, sort_expr: str) -> None:
    """group_expr / sort_expr に危険なSQLトークンが含まれていないか検証する.

    Args:
        group_expr (str): GROUP BY に使用するSQL式
        sort_expr (str): ソートキー生成SQL式

    Raises:
        ValueError: 危険なSQLトークンが含まれる場合
    """
    _dangerous_tokens = (";", "--", "/*")
    for expr_name, expr in (("group_expr", group_expr), ("sort_expr", sort_expr)):
        if any(tok in expr for tok in _dangerous_tokens):
            raise ValueError(f"{expr_name} に危険なSQLトークンが含まれています: {expr!r}")


def _validate_course_week(condition: RaceCondition | None) -> None:
    """course_kubun / week_in_course の組み合わせを検証する.

    Args:
        condition (RaceCondition | None): レース絞り込み条件

    Raises:
        ValueError: course_kubun と week_in_course のどちらか一方のみ指定した場合
    """
    cond_kubun = condition.course_kubun if condition else None
    cond_week = condition.week_in_course if condition else None
    if (cond_kubun is None) != (cond_week is None):
        raise ValueError(
            "condition.course_kubun と condition.week_in_course は"
            "両方同時に指定するか、両方 None にしてください。"
        )


def _run_chakudo_sql(
    manager: ConnectionManager,
    group_expr: str,
    sort_expr: str,
    condition: RaceCondition | None = None,
    extra_join: str = "",
    extra_where: list[str] | None = None,
    extra_params: list[Any] | None = None,
) -> ChakudoResult:
    """着度数・回収率集計SQLを組み立てて実行する共有ヘルパー.

    Args:
        manager (ConnectionManager): DB接続マネージャ
        group_expr (str): GROUP BY に使用するSQL式
        sort_expr (str): ソートキー生成SQL式
        condition (RaceCondition | None): レース絞り込み条件
        extra_join (str): base CTE の FROM に追加するJOIN SQL
        extra_where (list[str] | None): base CTE の WHERE に追加するパーツリスト
        extra_params (list[Any] | None): extra_where に対応するパラメータ

    Returns:
        ChakudoResult: グループ別集計結果
    """
    cond_kubun = condition.course_kubun if condition else None
    cond_week = condition.week_in_course if condition else None

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
        if extra_where:
            where_parts.extend(extra_where)
            params.extend(extra_params or [])

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
            {extra_join}
            WHERE {where_clause}
        )"""
        )

        sql = f"""
            WITH RECURSIVE {", ".join(cte_parts)}
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
