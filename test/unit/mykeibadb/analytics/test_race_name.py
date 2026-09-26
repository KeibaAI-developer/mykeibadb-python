"""get_race_display_names の単体テスト."""

import pandas as pd
from pytest_mock import MockerFixture

from mykeibadb.analytics import get_race_display_names


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
