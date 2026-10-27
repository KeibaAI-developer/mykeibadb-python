"""race_name モジュールの単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import (
    build_race_display_name_cte,
    get_race_display_names,
    race_display_name_expr,
    race_joken_class_expr,
    race_joken_code_expr,
)


def _make_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DataFrameを生成する."""
    return pd.DataFrame(rows)


# 正常系
def test_get_race_display_names_returns_mapping(mocker: MockerFixture) -> None:
    """race_code -> display_name の辞書が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df(
        [
            {"race_code": "2017090209060911", "display_name": "産経賞セントウルステークス"},
            {"race_code": "2023060305020811", "display_name": "安田記念"},
        ]
    )

    result = get_race_display_names(
        manager, ["2017090209060911", "2023060305020811"]
    )

    assert result == {
        "2017090209060911": "産経賞セントウルステークス",
        "2023060305020811": "安田記念",
    }


def test_get_race_display_names_uses_any_with_race_codes(mocker: MockerFixture) -> None:
    """race_codesがANY(%s)のパラメータとして渡される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df([])

    get_race_display_names(manager, ["2017090209060911"])

    sql = manager.fetch_dataframe.call_args[0][0]
    params = manager.fetch_dataframe.call_args[1]["params"]
    assert "r.race_code = ANY(%s)" in sql
    assert "grade_race_latest_names" in sql
    assert params == (["2017090209060911"],)


def test_get_race_display_names_empty_race_codes_returns_empty_dict(
    mocker: MockerFixture,
) -> None:
    """race_codesが空リストの場合は空dictを返しDBに問い合わせない."""
    manager = mocker.MagicMock()

    result = get_race_display_names(manager, [])

    assert result == {}
    manager.fetch_dataframe.assert_not_called()


def test_get_race_display_names_returns_class_name_for_race_without_title(
    mocker: MockerFixture,
) -> None:
    """競走名本題の無いレースはクラス名が返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df(
        [{"race_code": "2023060305020811", "display_name": "1勝クラス"}]
    )

    result = get_race_display_names(manager, ["2023060305020811"])

    assert result == {"2023060305020811": "1勝クラス"}
    sql = manager.fetch_dataframe.call_args[0][0]
    assert "WHEN 5 THEN '1勝クラス'" in sql


def test_get_race_display_names_excludes_null_display_name(mocker: MockerFixture) -> None:
    """表示名がNULLのレースは返り値に含まれない."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _make_df(
        [
            {"race_code": "2017090209060911", "display_name": "産経賞セントウルステークス"},
            {"race_code": "2023060305020811", "display_name": None},
        ]
    )

    result = get_race_display_names(manager, ["2017090209060911", "2023060305020811"])

    assert result == {"2017090209060911": "産経賞セントウルステークス"}


# race_joken_code_expr
def test_race_joken_code_expr_takes_greatest_of_five_columns() -> None:
    """5列の最大値を整数で返し、空の列はNULLIFで無視する式になる."""
    expr = race_joken_code_expr("r")
    assert expr.startswith("GREATEST(")
    for col in (
        "kyoso_joken_code_2sai",
        "kyoso_joken_code_3sai",
        "kyoso_joken_code_4sai",
        "kyoso_joken_code_5sai_ijo",
        "kyoso_joken_code_saijakunen",
    ):
        assert f"NULLIF(TRIM(r.{col}), '')::INTEGER" in expr


# race_joken_class_expr
@pytest.mark.parametrize(
    ("code", "name"),
    [
        (701, "新馬"),
        (703, "未勝利"),
        (5, "1勝クラス"),
        (10, "2勝クラス"),
        (16, "3勝クラス"),
        (999, "オープン"),
    ],
)
def test_race_joken_class_expr_maps_code_to_class_name(code: int, name: str) -> None:
    """競走条件コードごとにクラス名を返す分岐が含まれる."""
    expr = race_joken_class_expr("r")
    assert f"WHEN {code} THEN '{name}'" in expr


def test_race_joken_class_expr_returns_null_for_other_codes() -> None:
    """対応の無いコードはELSE無しのCASE式でNULLになる."""
    expr = race_joken_class_expr("r")
    assert expr.startswith("CASE GREATEST(")
    assert "r.kyoso_joken_code_2sai" in expr
    assert "ELSE" not in expr
    assert expr.endswith("END")


# build_race_display_name_cte / race_display_name_expr
def test_build_race_display_name_cte_default_name() -> None:
    """既定のCTE名でgrade_race_latest_namesが生成される."""
    cte_sql = build_race_display_name_cte()
    assert cte_sql.startswith("grade_race_latest_names AS (")
    assert "GRADE_CODE" not in cte_sql
    assert "grade_code IN ('A', 'B', 'C', 'D', 'F', 'G', 'H')" in cte_sql
    assert "keibajo_code ~ '^[0-9]+$'" in cte_sql
    assert "TRIM(tokubetsu_kyoso_bango) != '0000'" in cte_sql
    assert "DISTINCT ON (TRIM(tokubetsu_kyoso_bango))" in cte_sql
    assert "ORDER BY TRIM(tokubetsu_kyoso_bango), kaisai_nen DESC, kaisai_gappi DESC" in cte_sql


def test_build_race_display_name_cte_custom_name() -> None:
    """cte_nameを指定するとその名前でCTEが生成される."""
    cte_sql = build_race_display_name_cte(cte_name="custom_names")
    assert cte_sql.startswith("custom_names AS (")


def test_race_display_name_expr_unifies_grade_race_names() -> None:
    """重賞は条件を満たすとCTEの最新名に統一される."""
    expr = race_display_name_expr("r")
    assert "r.grade_code IN ('A', 'B', 'C', 'D', 'F', 'G', 'H')" in expr
    assert "r.keibajo_code ~ '^[0-9]+$'" in expr
    assert "TRIM(r.tokubetsu_kyoso_bango) != '0000'" in expr
    assert "COALESCE(grade_race_latest_names.latest_name, TRIM(r.kyosomei_hondai))" in expr


def test_race_display_name_expr_uses_own_title_then_class_name() -> None:
    """重賞以外は自身の競走名本題を使い、空ならクラス名、それも無ければNULLになる."""
    expr = race_display_name_expr("r")
    assert "ELSE TRIM(r.kyosomei_hondai)" in expr
    assert "NULLIF(\n        CASE WHEN" in expr
    assert race_joken_class_expr("r") in expr
    assert "ELSE" not in expr.split("END,", 1)[1]


def test_race_display_name_expr_custom_cte_name() -> None:
    """cte_nameを指定するとJOIN先CTE名がその名前になる."""
    expr = race_display_name_expr("horse_hist", cte_name="custom_names")
    assert "COALESCE(custom_names.latest_name, TRIM(horse_hist.kyosomei_hondai))" in expr
