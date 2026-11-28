"""mawari_expr の結合テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import mawari_expr
from mykeibadb.connection import ConnectionManager


# 正常系
@pytest.mark.parametrize(
    ("keibajo_code", "track_code", "expected"),
    [
        ("05", "11", "左"),
        ("A6", "17", "右"),
        ("A8", "11", "左"),
        ("A6", "10", None),
        ("44", "11", None),
    ],
)
def test_mawari_expr_judges_jra_and_overseas_races(
    connection_manager: ConnectionManager,
    keibajo_code: str,
    track_code: str,
    expected: str | None,
) -> None:
    """中央競馬と海外のレースは回りを返し、地方競馬と直線コースは NULL を返す."""
    df = connection_manager.fetch_dataframe(
        f"SELECT {mawari_expr('r')} AS mawari "
        "FROM (VALUES (%s, %s)) AS r(keibajo_code, track_code)",
        (keibajo_code, track_code),
    )

    value = df["mawari"].iloc[0]
    assert (None if value is None else str(value)) == expected
