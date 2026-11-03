"""ran_entry_condition の単体テスト."""

import pytest

from mykeibadb.analytics import ran_entry_condition


# 正常系
@pytest.mark.parametrize("alias", ["u", "u2", "umagoto_race_joho"])
def test_ran_entry_condition_uses_alias_data_kubun_and_race_code(alias: str) -> None:
    """指定したエイリアスの data_kubun と race_code を使う."""
    condition = ran_entry_condition(alias)

    assert f"{alias}.data_kubun = '1'" in condition
    assert f"= {alias}.race_code" in condition


def test_ran_entry_condition_looks_up_race_shosai_in_subquery() -> None:
    """race_shosai はスキーマ修飾なしのサブクエリで引く."""
    condition = ran_entry_condition("u")

    assert "NOT EXISTS (SELECT 1 FROM race_shosai ran_rs" in condition
    assert "ran_rs.data_kubun <> '1'" in condition
    assert "public." not in condition


def test_ran_entry_condition_does_not_wrap_data_kubun_with_trim() -> None:
    """固定長文字列の data_kubun を TRIM で包まない."""
    assert "TRIM" not in ran_entry_condition("u")
