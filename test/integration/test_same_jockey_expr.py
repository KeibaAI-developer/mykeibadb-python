"""same_jockey_expr の結合テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import kishu_master_name_key_expr, same_jockey_expr
from mykeibadb.connection import ConnectionManager


# 正常系
@pytest.mark.parametrize(
    ("past_code", "past_ryakusho", "target_code", "target_kishumei", "expected"),
    [
        ("00000", "ビュイッ", "05495", "Ｗ．ビュイック", True),
        ("00000", "ムーア　", "05366", "Ｒ．ムーア", True),
        ("00000", "デムーロ", "05473", "Ｃ．デムーロ", True),
        ("00000", "武豊　　", "00666", "武　豊", True),
        ("00000", "スミヨン", "05504", "Ｍ．バルザローナ", False),
        ("05212", "Ｍ．デム", "05212", "Ｍ．デムーロ", True),
        ("05212", "Ｍ．デム", "05473", "Ｃ．デムーロ", False),
    ],
)
def test_same_jockey_expr_compares_name_when_past_code_is_missing(
    connection_manager: ConnectionManager,
    past_code: str,
    past_ryakusho: str,
    target_code: str,
    target_kishumei: str,
    expected: bool,
) -> None:
    """過去走の騎手コードが 00000 のときは騎手名、それ以外は騎手コードで比べる."""
    name_key = kishu_master_name_key_expr("t.kishumei")
    df = connection_manager.fetch_dataframe(
        f"SELECT {same_jockey_expr('p', 't.kishu_code', name_key)} AS same "
        "FROM (VALUES (%s, %s)) AS p(kishu_code, kishumei_ryakusho) "
        "CROSS JOIN (VALUES (%s, %s)) AS t(kishu_code, kishumei)",
        (past_code, past_ryakusho, target_code, target_kishumei),
    )

    assert bool(df["same"].iloc[0]) is expected
