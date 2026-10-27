"""レース表示名の結合テスト.

get_race_display_names が DB 上のレースに対して表示名を返すことを確認する。
"""

import pytest

from mykeibadb.analytics import get_race_display_names
from mykeibadb.connection import ConnectionManager


def _find_race_code(connection_manager: ConnectionManager, where: str) -> str:
    """条件に当たる JRA 開催のレースを1件探してレースコードを返す.

    Args:
        connection_manager: データベース接続マネージャー
        where: race_shosai を絞り込む SQL の条件

    Returns:
        str: レースコード。見つからない場合はテストをスキップする。
    """
    df = connection_manager.fetch_dataframe(
        "SELECT race_code FROM race_shosai "
        f"WHERE keibajo_code ~ '^[0-9]+$' AND {where} "
        "ORDER BY race_code DESC LIMIT 1"
    )
    if df.empty:
        pytest.skip(f"条件に当たるレースがありません: {where}")
    return str(df.iloc[0]["race_code"])


# 正常系
def test_get_race_display_names_returns_class_name_for_race_without_title(
    connection_manager: ConnectionManager,
) -> None:
    """競走名本題が無い2勝クラスのレースは「2勝クラス」が返る."""
    race_code = _find_race_code(
        connection_manager,
        "TRIM(kyosomei_hondai) = '' "
        "AND GREATEST("
        "NULLIF(TRIM(kyoso_joken_code_2sai), '')::INTEGER, "
        "NULLIF(TRIM(kyoso_joken_code_3sai), '')::INTEGER, "
        "NULLIF(TRIM(kyoso_joken_code_4sai), '')::INTEGER, "
        "NULLIF(TRIM(kyoso_joken_code_5sai_ijo), '')::INTEGER, "
        "NULLIF(TRIM(kyoso_joken_code_saijakunen), '')::INTEGER) = 10",
    )

    result = get_race_display_names(connection_manager, [race_code])

    assert result == {race_code: "2勝クラス"}


def test_get_race_display_names_returns_title_for_non_grade_race(
    connection_manager: ConnectionManager,
) -> None:
    """競走名本題がある重賞以外のレースは、その競走名本題が返る."""
    race_code = _find_race_code(
        connection_manager,
        "TRIM(kyosomei_hondai) != '' AND grade_code NOT IN ('A', 'B', 'C', 'D', 'F', 'G', 'H')",
    )
    title = connection_manager.fetch_dataframe(
        "SELECT TRIM(kyosomei_hondai) AS title FROM race_shosai WHERE race_code = %s",
        params=(race_code,),
    ).iloc[0]["title"]

    result = get_race_display_names(connection_manager, [race_code])

    assert result == {race_code: title}


def test_get_race_display_names_returns_latest_title_for_grade_race(
    connection_manager: ConnectionManager,
) -> None:
    """重賞は、同じ特別競走番号の重賞のうち開催日が最も新しいレースの競走名本題が返る."""
    race_code = _find_race_code(
        connection_manager,
        "grade_code = 'A' AND TRIM(tokubetsu_kyoso_bango) != '0000'",
    )
    latest_title = connection_manager.fetch_dataframe(
        "SELECT TRIM(r2.kyosomei_hondai) AS title "
        "FROM race_shosai r JOIN race_shosai r2 "
        "ON TRIM(r2.tokubetsu_kyoso_bango) = TRIM(r.tokubetsu_kyoso_bango) "
        "WHERE r.race_code = %s AND r2.keibajo_code ~ '^[0-9]+$' "
        "AND r2.grade_code IN ('A', 'B', 'C', 'D', 'F', 'G', 'H') "
        "ORDER BY r2.kaisai_nen DESC, r2.kaisai_gappi DESC LIMIT 1",
        params=(race_code,),
    ).iloc[0]["title"]

    result = get_race_display_names(connection_manager, [race_code])

    assert result == {race_code: latest_title}
