"""レース名・競走条件クラスのSQL部品とレース表示名取得モジュール."""

import pandas as pd

from mykeibadb.connection import ConnectionManager

# 重賞を表すグレードコード（GRADE_CODE参照。E=特別競走・L=リステッドは含まない）
GRADE_RACE_CODES: frozenset[str] = frozenset({"A", "B", "C", "D", "F", "G", "H"})

# 競走条件コード → クラス名
_JOKEN_CLASS_NAMES: dict[int, str] = {
    701: "新馬",
    703: "未勝利",
    5: "1勝クラス",
    10: "2勝クラス",
    16: "3勝クラス",
    999: "オープン",
}


def race_joken_code_expr(alias: str) -> str:
    """レースの競走条件コード（年齢別の5列の最大値）を整数で返すSQL式を生成する.

    空の列は無視する。5列とも空の場合は NULL を返す。

    Args:
        alias (str): kyoso_joken_code_2sai〜kyoso_joken_code_saijakunen 列を持つ
            テーブルのSQLエイリアス

    Returns:
        str: 競走条件コードの整数を返すGREATEST式
    """
    a = alias
    return (
        "GREATEST("
        f"NULLIF(TRIM({a}.kyoso_joken_code_2sai), '')::INTEGER, "
        f"NULLIF(TRIM({a}.kyoso_joken_code_3sai), '')::INTEGER, "
        f"NULLIF(TRIM({a}.kyoso_joken_code_4sai), '')::INTEGER, "
        f"NULLIF(TRIM({a}.kyoso_joken_code_5sai_ijo), '')::INTEGER, "
        f"NULLIF(TRIM({a}.kyoso_joken_code_saijakunen), '')::INTEGER"
        ")"
    )


def race_joken_class_expr(alias: str) -> str:
    """競走条件コードからクラス名を返すSQL式を生成する.

    701=新馬、703=未勝利、5=1勝クラス、10=2勝クラス、16=3勝クラス、999=オープン。
    それ以外のコードおよび競走条件コードが NULL の場合は NULL を返す。

    Args:
        alias (str): kyoso_joken_code_2sai〜kyoso_joken_code_saijakunen 列を持つ
            テーブルのSQLエイリアス

    Returns:
        str: クラス名を返すCASE式
    """
    whens = "\n".join(
        f"     WHEN {code} THEN '{name}'" for code, name in _JOKEN_CLASS_NAMES.items()
    )
    return f"CASE {race_joken_code_expr(alias)}\n{whens}\nEND"


def build_race_display_name_cte(cte_name: str = "grade_race_latest_names") -> str:
    """重賞レース名統一用CTEのSQL文字列を返す.

    grade_code が重賞（GRADE_RACE_CODES）かつ keibajo_code が数字（JRA開催）で
    特別競走番号が'0000'以外のレースについて、特別競走番号ごとに開催日が最も新しい
    レースの競走名本題（latest_name）を1行にまとめる。race_display_name_expr と
    組み合わせて使う。

    Args:
        cte_name (str): 生成するCTEの名前

    Returns:
        str: CTE SQL文字列（WITHキーワードなし）
    """
    grade_codes = ", ".join(f"'{c}'" for c in sorted(GRADE_RACE_CODES))
    return (
        f"{cte_name} AS (\n"
        f"        SELECT DISTINCT ON (TRIM(tokubetsu_kyoso_bango))\n"
        f"            TRIM(tokubetsu_kyoso_bango) AS tokubetsu_kyoso_bango,\n"
        f"            TRIM(kyosomei_hondai) AS latest_name\n"
        f"        FROM race_shosai\n"
        f"        WHERE grade_code IN ({grade_codes})\n"
        f"          AND keibajo_code ~ '^[0-9]+$'\n"
        f"          AND TRIM(tokubetsu_kyoso_bango) != '0000'\n"
        f"        ORDER BY TRIM(tokubetsu_kyoso_bango), kaisai_nen DESC, kaisai_gappi DESC\n"
        f"    )"
    )


def race_display_name_expr(alias: str, cte_name: str = "grade_race_latest_names") -> str:
    """表示用のレース名を返すSQL式を生成する.

    build_race_display_name_cte で生成したCTEへのLEFT JOINを前提とする
    （JOIN条件: `{cte_name}.tokubetsu_kyoso_bango = TRIM({alias}.tokubetsu_kyoso_bango)`）。
    次の優先順位で表示名を決める。

    1. 重賞（JRA開催・特別競走番号あり）はCTEの最新の競走名本題
    2. 1以外で競走名本題があるレースは、その競走名本題
    3. 競走名本題が無いレースは、race_joken_class_expr のクラス名
    4. どれにも当たらないレースは NULL

    Args:
        alias (str): grade_code / keibajo_code / tokubetsu_kyoso_bango / kyosomei_hondai 列と
            race_joken_code_expr が参照する5列を持つテーブルのSQLエイリアス
        cte_name (str): JOIN対象CTEの名前（build_race_display_name_cteと合わせる）

    Returns:
        str: 表示用レース名を返すSQL式
    """
    grade_codes = ", ".join(f"'{c}'" for c in sorted(GRADE_RACE_CODES))
    a = alias
    return (
        f"COALESCE(\n"
        f"    NULLIF(\n"
        f"        CASE WHEN {a}.grade_code IN ({grade_codes})\n"
        f"                  AND {a}.keibajo_code ~ '^[0-9]+$'\n"
        f"                  AND TRIM({a}.tokubetsu_kyoso_bango) != '0000'\n"
        f"             THEN COALESCE({cte_name}.latest_name, TRIM({a}.kyosomei_hondai))\n"
        f"             ELSE TRIM({a}.kyosomei_hondai)\n"
        f"        END,\n"
        f"        ''),\n"
        f"    {race_joken_class_expr(a)}\n"
        f")"
    )


def get_race_display_names(
    manager: ConnectionManager, race_codes: list[str]
) -> dict[str, str]:
    """レースコードごとの表示用レース名を取得する.

    重賞（grade_code が A/B/C/D/F/G/H）かつ JRA開催（keibajo_code が数字）で
    特別競走番号が'0000'以外のレースは、同じ特別競走番号を持つ重賞レースのうち
    開催日が最も新しいレースの競走名本題を返す。それ以外のレースは自身の競走名本題を返す。
    競走名本題が無いレースは競走条件コードに対応するクラス名を返す。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_codes (list[str]): レースコードのリスト

    Returns:
        dict[str, str]: race_code -> 表示用レース名の辞書。
            race_shosai に存在しないrace_codeと、表示名が決まらないレースは含まれない。
    """
    if not race_codes:
        return {}
    name_cte = build_race_display_name_cte()
    display_name_expr = race_display_name_expr("r")
    sql = (
        f"WITH {name_cte}\n"
        f"SELECT r.race_code, {display_name_expr} AS display_name\n"
        f"FROM race_shosai r\n"
        f"LEFT JOIN grade_race_latest_names\n"
        f"    ON grade_race_latest_names.tokubetsu_kyoso_bango = TRIM(r.tokubetsu_kyoso_bango)\n"
        f"WHERE r.race_code = ANY(%s)"
    )
    df = manager.fetch_dataframe(sql, params=(list(race_codes),))
    return {
        str(row["race_code"]): str(row["display_name"])
        for _, row in df.iterrows()
        if pd.notna(row["display_name"])
    }
