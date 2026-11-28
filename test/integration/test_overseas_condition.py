"""overseas_condition の結合テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import overseas_condition
from mykeibadb.connection import ConnectionManager


# 正常系
@pytest.mark.parametrize(
    ("keibajo_code", "expected"),
    [("A6", True), ("C7", True), ("05", False), ("10", False), ("44", False)],
)
def test_overseas_condition_is_true_for_alphabetic_keibajo_code(
    connection_manager: ConnectionManager,
    keibajo_code: str,
    expected: bool,
) -> None:
    """競馬場コードが英字で始まるときだけ真になる."""
    df = connection_manager.fetch_dataframe(
        f"SELECT {overseas_condition('r')} AS overseas FROM (VALUES (%s)) AS r(keibajo_code)",
        (keibajo_code,),
    )

    assert bool(df["overseas"].iloc[0]) is expected
