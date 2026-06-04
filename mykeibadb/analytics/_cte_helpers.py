"""着度数集計SQLで使用するCTE生成ヘルパーモジュール."""

from typing import Any


def build_course_week_cte(
    keibajo: str | None,
    course_kubun: str,
    week_in_course: int,
    cte_params: list[Any],
) -> tuple[str, str]:
    """コース区分・週番号フィルタ用CTEとJOIN句を生成する.

    同一コース区分の使用開始から2日間を1週として週番号を計算し、
    指定コース・週番号の開催日のみに絞り込むCTEを生成する。

    Args:
        keibajo (str | None): 競馬場コード。Noneの場合は全競馬場が対象。
        course_kubun (str): コース区分（例: 'C'）
        week_in_course (int): コース使用開始からの週番号（0以上の整数）
        cte_params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: CTE SQL文字列（WITHキーワードなし）
        str: JOIN句
    """
    keibajo_filter = "AND keibajo_code = %s" if keibajo else ""
    if keibajo:
        cte_params.append(keibajo)
    cte_params.extend([course_kubun, week_in_course])

    cte_sql = f"""
        cw_daily AS (
            SELECT DISTINCT keibajo_code, kaisai_nen, kaisai_kai, kaisai_nichime, course_kubun
            FROM race_shosai
            WHERE course_kubun != '' {keibajo_filter}
        ),
        cw_with_prev AS (
            SELECT *,
                LAG(course_kubun) OVER (
                    PARTITION BY keibajo_code, kaisai_nen ORDER BY kaisai_kai, kaisai_nichime
                ) AS prev_course
            FROM cw_daily
        ),
        cw_with_group AS (
            SELECT *,
                SUM(CASE WHEN course_kubun != COALESCE(prev_course, '_') THEN 1 ELSE 0 END)
                    OVER (PARTITION BY keibajo_code, kaisai_nen ORDER BY kaisai_kai, kaisai_nichime)
                    AS cw_group_id
            FROM cw_with_prev
        ),
        cw_weeks AS (
            SELECT *,
                CEIL(
                    ROW_NUMBER() OVER (
                        PARTITION BY keibajo_code, kaisai_nen, cw_group_id
                        ORDER BY kaisai_kai, kaisai_nichime
                    ) / 2.0
                )::INT AS week_in_course
            FROM cw_with_group
        ),
        cw_target AS (
            SELECT keibajo_code, kaisai_nen, kaisai_kai, kaisai_nichime
            FROM cw_weeks
            WHERE course_kubun = %s AND week_in_course = %s
        )"""

    join_sql = """JOIN cw_target ON r.keibajo_code = cw_target.keibajo_code
            AND r.kaisai_nen = cw_target.kaisai_nen
            AND r.kaisai_kai = cw_target.kaisai_kai
            AND r.kaisai_nichime = cw_target.kaisai_nichime"""

    return cte_sql, join_sql


def build_payout_ctes() -> str:
    """単勝・複勝払い戻しJOIN用のCTE SQL文字列を返す.

    haraimodoshiテーブルから単勝・複勝の払い戻し金額を正規化するCTEを生成する。
    CTE名: tansho_payouts, fukusho_payouts

    Returns:
        str: CTE SQL文字列（WITHキーワードなし、複数CTE）
    """
    return """fukusho_payouts AS (
            SELECT race_code, fukusho1_umaban AS umaban,
                   CAST(TRIM(fukusho1_haraimodoshikin) AS INTEGER) AS payout
            FROM haraimodoshi
            WHERE TRIM(fukusho1_haraimodoshikin) ~ '^[0-9]+$'
              AND TRIM(fukusho1_haraimodoshikin)::INTEGER > 0
            UNION ALL
            SELECT race_code, fukusho2_umaban,
                   CAST(TRIM(fukusho2_haraimodoshikin) AS INTEGER)
            FROM haraimodoshi WHERE TRIM(fukusho2_haraimodoshikin) ~ '^[0-9]+$'
              AND TRIM(fukusho2_haraimodoshikin)::INTEGER > 0
            UNION ALL
            SELECT race_code, fukusho3_umaban,
                   CAST(TRIM(fukusho3_haraimodoshikin) AS INTEGER)
            FROM haraimodoshi WHERE TRIM(fukusho3_haraimodoshikin) ~ '^[0-9]+$'
              AND TRIM(fukusho3_haraimodoshikin)::INTEGER > 0
        ),
        tansho_payouts AS (
            SELECT race_code, tansho1_umaban AS umaban,
                   CAST(TRIM(tansho1_haraimodoshikin) AS INTEGER) AS payout
            FROM haraimodoshi WHERE TRIM(tansho1_haraimodoshikin) ~ '^[0-9]+$'
              AND TRIM(tansho1_haraimodoshikin)::INTEGER > 0
        )"""
