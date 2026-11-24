"""kyori_expr の結合テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import kyori_expr
from mykeibadb.connection import ConnectionManager


# 正常系
@pytest.mark.parametrize(
    ("keibajo_code", "kyori", "expected"),
    [
        ("A6", "2390", 2400),
        ("A6", "1990", 2000),
        ("C7", "2410", 2400),
        ("A8", "2050", 2100),
        ("05", "2400", 2400),
        ("44", "1990", 1990),
    ],
)
def test_kyori_expr_rounds_only_overseas_distance(
    connection_manager: ConnectionManager,
    keibajo_code: str,
    kyori: str,
    expected: int,
) -> None:
    """海外のレースの距離だけ100m単位に四捨五入する."""
    df = connection_manager.fetch_dataframe(
        f"SELECT {kyori_expr('r')} AS kyori " "FROM (VALUES (%s, %s)) AS r(keibajo_code, kyori)",
        (keibajo_code, kyori),
    )

    assert df["kyori"].iloc[0] == expected
