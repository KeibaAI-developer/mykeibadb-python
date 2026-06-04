"""_cte_helpers モジュールの単体テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import build_course_week_cte, build_payout_ctes


# 正常系
def test_build_course_week_cte_returns_cte_and_join_sql() -> None:
    """keibajo指定ありでCTE SQLとJOIN句が返る."""
    params: list[object] = []
    cte_sql, join_sql = build_course_week_cte("05", "C", 1, params)
    assert "cw_target" in cte_sql
    assert "week_in_course" in cte_sql
    assert "JOIN cw_target" in join_sql
    assert params == ["05", "C", 1]


def test_build_course_week_cte_without_keibajo() -> None:
    """keibajo=NoneでもCTE SQLが生成され、パラメータにkeibajoが含まれない."""
    params: list[object] = []
    cte_sql, join_sql = build_course_week_cte(None, "B", 2, params)
    assert "cw_target" in cte_sql
    assert "AND keibajo_code = %s" not in cte_sql
    assert params == ["B", 2]


def test_build_course_week_cte_appends_to_existing_params() -> None:
    """既存パラメータリストの末尾にパラメータが追加される."""
    params: list[object] = ["existing"]
    build_course_week_cte("05", "A", 3, params)
    assert params[0] == "existing"
    assert params[-1] == 3


def test_build_course_week_cte_join_sql_has_all_join_columns() -> None:
    """JOIN句が keibajo_code / kaisai_nen / kaisai_kai / kaisai_nichime を含む."""
    params: list[object] = []
    _, join_sql = build_course_week_cte(None, "C", 1, params)
    assert "keibajo_code" in join_sql
    assert "kaisai_nen" in join_sql
    assert "kaisai_kai" in join_sql
    assert "kaisai_nichime" in join_sql


# 準正常系
def test_build_course_week_cte_week_zero_is_valid() -> None:
    """week_in_course=0でもエラーなくCTEが生成される."""
    params: list[object] = []
    cte_sql, _ = build_course_week_cte(None, "C", 0, params)
    assert "cw_target" in cte_sql
    assert params[-1] == 0


def test_build_payout_ctes_returns_string() -> None:
    """build_payout_ctesが文字列を返す."""
    result = build_payout_ctes()
    assert isinstance(result, str)
    assert "tansho_payouts" in result
    assert "fukusho_payouts" in result


def test_build_payout_ctes_has_haraimodoshi_reference() -> None:
    """払い戻しCTEがharaimodoshiテーブルを参照する."""
    result = build_payout_ctes()
    assert "haraimodoshi" in result


def test_build_payout_ctes_filters_invalid_values() -> None:
    """払い戻しCTEが正規表現フィルタを含む."""
    result = build_payout_ctes()
    assert "^[0-9]+$" in result


@pytest.mark.parametrize(
    "course_kubun, week_in_course",
    [
        ("C", 1),
        ("B", 3),
        ("A", 5),
    ],
)
def test_build_course_week_cte_various_params(course_kubun: str, week_in_course: int) -> None:
    """様々なコース区分・週番号でCTEが生成できる."""
    params: list[object] = []
    cte_sql, _ = build_course_week_cte(None, course_kubun, week_in_course, params)
    assert "cw_target" in cte_sql
    assert course_kubun in params
    assert week_in_course in params
