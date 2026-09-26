"""レース表示名取得モジュール."""

from mykeibadb.analytics._cte_helpers import build_race_display_name_cte, race_display_name_expr
from mykeibadb.connection import ConnectionManager


def get_race_display_names(
    manager: ConnectionManager, race_codes: list[str]
) -> dict[str, str]:
    """レースコードごとの表示用レース名を取得する.

    重賞（grade_code が A/B/C/D/F/G/H）かつ JRA開催（keibajo_code が数字）で
    特別競走番号が'0000'以外のレースは、同じ特別競走番号を持つ重賞レースのうち
    開催日が最も新しいレースの競走名本題を返す。それ以外のレースは自身の競走名本題を返す。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_codes (list[str]): レースコードのリスト

    Returns:
        dict[str, str]: race_code -> 表示用レース名の辞書。
            race_shosai に存在しないrace_codeは含まれない。
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
    return {str(row["race_code"]): str(row["display_name"]) for _, row in df.iterrows()}
