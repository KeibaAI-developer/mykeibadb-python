"""着度数集計SQLで使用するCTE生成ヘルパーモジュール."""

from typing import Any, NamedTuple

from mykeibadb.analytics._models import RaceCondition, Subject


class SubjectMapping(NamedTuple):
    """Subject別の列・JOIN情報.

    Attributes:
        group_col (str): GROUP BY / SELECT に使う列式
        name_col (str): 名称フィルタ列（LIKE フィルタ用）
        code_col (str | None): コードフィルタ列。None の場合はコード指定不可
        join_sql (str | None): 追加JOIN SQL。None の場合はJOIN不要
    """

    group_col: str
    name_col: str
    code_col: str | None
    join_sql: str | None


_KM2_JOIN = "JOIN kyosoba_master2 km2 ON u.ketto_toroku_bango = km2.ketto_toroku_bango"

SUBJECT_MAP: dict[Subject, SubjectMapping] = {
    Subject.UMA: SubjectMapping(
        group_col="u.bamei",
        name_col="u.bamei",
        code_col="u.ketto_toroku_bango",
        join_sql=None,
    ),
    Subject.KISHU: SubjectMapping(
        group_col="u.kishumei_ryakusho",
        name_col="u.kishumei_ryakusho",
        code_col="u.kishu_code",
        join_sql=None,
    ),
    Subject.CHOKYOSHI: SubjectMapping(
        group_col="u.chokyoshimei_ryakusho",
        name_col="u.chokyoshimei_ryakusho",
        code_col="u.chokyoshi_code",
        join_sql=None,
    ),
    Subject.BANUSHI: SubjectMapping(
        group_col="u.banushimei_hojinkaku_nashi",
        name_col="u.banushimei_hojinkaku_nashi",
        code_col="u.banushi_code",
        join_sql=None,
    ),
    Subject.SIRE: SubjectMapping(
        group_col="km2.ketto1_bamei",
        name_col="km2.ketto1_bamei",
        code_col=None,
        join_sql=_KM2_JOIN,
    ),
    Subject.SEISANSHA: SubjectMapping(
        group_col="km2.seisanshamei_hojinkaku_nashi",
        name_col="km2.seisanshamei_hojinkaku_nashi",
        code_col=None,
        join_sql=_KM2_JOIN,
    ),
}


# track_code → 左右 のマッピングを逆引きしたセット
_SAYUU_TRACK_CODES: dict[str, tuple[str, ...]] = {
    "左": ("11", "12", "13", "14", "15", "16", "23", "25", "27", "53"),
    "右": ("17", "18", "19", "20", "21", "22", "24", "26", "28"),
    "直": ("10", "29"),
}


def build_race_condition_where(
    condition: RaceCondition,
    params: list[Any],
    include_keibajo_code: bool = True,
) -> list[str]:
    """RaceConditionからWHERE句のpartsリストを生成する.

    course_kubun / week_in_course の組み合わせは build_course_week_cte でCTE処理するため
    ここでは扱わない。course_kubun のみ（week_in_course=None）は WHERE 句として追加する。

    Args:
        condition (RaceCondition): レースフィルタ条件
        params (list[Any]): SQLパラメータリスト（末尾に追加される）
        include_keibajo_code (bool): keibajo_codeをWHERE句に含めるかどうか

    Returns:
        list[str]: WHERE句のpartsリスト

    Raises:
        ValueError: race_shubetsu / shiba_da / sayuu に未対応の値が指定された場合
    """
    where_parts: list[str] = []
    if include_keibajo_code and condition.keibajo_code:
        where_parts.append("r.keibajo_code = %s")
        params.append(condition.keibajo_code)
    if condition.kyori:
        where_parts.append("r.kyori = %s")
        params.append(condition.kyori)
    if condition.year_from:
        where_parts.append("r.kaisai_nen >= %s")
        params.append(condition.year_from)
    if condition.year_to:
        where_parts.append("r.kaisai_nen <= %s")
        params.append(condition.year_to)
    if condition.grade_code:
        where_parts.append("r.grade_code = %s")
        params.append(condition.grade_code)
    if condition.kyoso_joken_codes:
        where_parts.append(
            "GREATEST("
            "NULLIF(TRIM(r.kyoso_joken_code_2sai), '')::INTEGER, "
            "NULLIF(TRIM(r.kyoso_joken_code_3sai), '')::INTEGER, "
            "NULLIF(TRIM(r.kyoso_joken_code_4sai), '')::INTEGER, "
            "NULLIF(TRIM(r.kyoso_joken_code_5sai_ijo), '')::INTEGER, "
            "NULLIF(TRIM(r.kyoso_joken_code_saijakunen), '')::INTEGER"
            ") = ANY(%s::INTEGER[])"
        )
        params.append([int(c) for c in condition.kyoso_joken_codes])
    if condition.race_shubetsu:
        if condition.race_shubetsu == "平地":
            where_parts.append("TRIM(r.track_code) BETWEEN '10' AND '29'")
        elif condition.race_shubetsu == "障害":
            where_parts.append("TRIM(r.track_code) BETWEEN '51' AND '59'")
        else:
            raise ValueError(f"未対応の race_shubetsu です: {condition.race_shubetsu!r}")
    if condition.shiba_da:
        if condition.shiba_da == "芝":
            where_parts.append(
                "(TRIM(r.track_code) BETWEEN '10' AND '22' "
                "OR TRIM(r.track_code) BETWEEN '51' AND '59')"
            )
        elif condition.shiba_da == "ダ":
            where_parts.append("TRIM(r.track_code) BETWEEN '23' AND '29'")
        else:
            raise ValueError(f"未対応の shiba_da です: {condition.shiba_da!r}")
    if condition.babajotai_code:
        where_parts.append(
            "COALESCE("
            "NULLIF(NULLIF(TRIM(r.shiba_babajotai_code), ''), '0'), "
            "NULLIF(NULLIF(TRIM(r.dirt_babajotai_code), ''), '0')"
            ") = %s"
        )
        params.append(condition.babajotai_code)
    if condition.sayuu:
        codes = _SAYUU_TRACK_CODES.get(condition.sayuu)
        if codes is None:
            raise ValueError(f"未対応の sayuu です: {condition.sayuu!r}")
        placeholders = ", ".join(["%s"] * len(codes))
        where_parts.append(f"TRIM(r.track_code) IN ({placeholders})")
        params.extend(list(codes))
    if condition.course_kubun and condition.week_in_course is None:
        where_parts.append("r.course_kubun = %s")
        params.append(condition.course_kubun)
    return where_parts


def build_course_week_cte(
    keibajo_code: str | None,
    course_kubun: str,
    week_in_course: int,
    cte_params: list[Any],
) -> tuple[str, str]:
    """コース区分・週番号フィルタ用CTEとJOIN句を生成する.

    同一コース区分内で前回開催日との差が2日超の場合に週番号を+1し、
    14日以上空いた場合は週番号を1にリセットする。
    3日間開催にも対応する。

    Args:
        keibajo_code (str | None): 競馬場コード。Noneの場合は全競馬場が対象。
        course_kubun (str): コース区分（例: 'C'）
        week_in_course (int): コース使用開始からの週番号（1以上の整数）
        cte_params (list[Any]): SQLパラメータリスト（末尾に追加される）

    Returns:
        str: CTE SQL文字列（WITHキーワードなし）
        str: JOIN句

    Raises:
        ValueError: week_in_course が1未満の場合
    """
    if week_in_course < 1:
        raise ValueError(f"week_in_course は1以上の整数を指定してください: {week_in_course!r}")
    keibajo_filter = "AND keibajo_code = %s" if keibajo_code else ""
    if keibajo_code:
        cte_params.append(keibajo_code)
    cte_params.extend([course_kubun, week_in_course])

    cte_sql = f"""
        cw_daily AS (
            SELECT DISTINCT
                keibajo_code, kaisai_nen, kaisai_kai, kaisai_nichime, course_kubun,
                TO_DATE(kaisai_nen || kaisai_gappi, 'YYYYMMDD') AS race_date
            FROM race_shosai
            WHERE course_kubun != '' {keibajo_filter}
        ),
        cw_with_group AS (
            SELECT *,
                SUM(CASE WHEN course_kubun != COALESCE(
                    LAG(course_kubun) OVER (
                        PARTITION BY keibajo_code, kaisai_nen ORDER BY kaisai_kai, kaisai_nichime
                    ), '_'
                ) THEN 1 ELSE 0 END)
                OVER (PARTITION BY keibajo_code, kaisai_nen ORDER BY kaisai_kai, kaisai_nichime)
                AS cw_group_id
            FROM cw_daily
        ),
        cw_with_rn AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY keibajo_code, kaisai_nen, cw_group_id
                    ORDER BY kaisai_kai, kaisai_nichime
                ) AS rn_in_group
            FROM cw_with_group
        ),
        cw_weeks(keibajo_code, kaisai_nen, kaisai_kai, kaisai_nichime, course_kubun,
                 cw_group_id, rn_in_group, race_date, week_in_course) AS (
            SELECT keibajo_code, kaisai_nen, kaisai_kai, kaisai_nichime, course_kubun,
                   cw_group_id, rn_in_group, race_date, 1
            FROM cw_with_rn
            WHERE rn_in_group = 1
            UNION ALL
            SELECT curr.keibajo_code, curr.kaisai_nen, curr.kaisai_kai, curr.kaisai_nichime,
                   curr.course_kubun, curr.cw_group_id, curr.rn_in_group, curr.race_date,
                CASE
                    WHEN (curr.race_date - prev.race_date) >= 14 THEN 1
                    WHEN (curr.race_date - prev.race_date) > 2 THEN prev.week_in_course + 1
                    ELSE prev.week_in_course
                END
            FROM cw_with_rn curr
            JOIN cw_weeks prev ON curr.keibajo_code = prev.keibajo_code
                AND curr.kaisai_nen = prev.kaisai_nen
                AND curr.cw_group_id = prev.cw_group_id
                AND curr.rn_in_group = prev.rn_in_group + 1
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
