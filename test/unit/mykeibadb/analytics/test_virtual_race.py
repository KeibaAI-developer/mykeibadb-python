"""VirtualRace・apply_virtual_race の単体テスト."""

import json

import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import VirtualRace, apply_virtual_race
from mykeibadb.analytics.virtual_race import validate_virtual_race_columns

_RACE_CODE = "2099110105041111"


def _entry(umaban: str, ketto: str = "2021105898") -> dict[str, str]:
    """テスト用の出走の行を返す."""
    return {"race_code": _RACE_CODE, "ketto_toroku_bango": ketto, "umaban": umaban}


def _virtual_race(horses: list[dict[str, str]] | None = None) -> VirtualRace:
    """テスト用の仮のレースを返す."""
    return VirtualRace(
        race={"race_code": _RACE_CODE},
        entries=[_entry("01"), _entry("02", "2022105519")],
        horses=horses or [],
    )


# 正常系
def test_apply_virtual_race_prepends_with_to_plain_sql() -> None:
    """WITH の無い SQL に4つの CTE を足し、パラメータを先頭に足す."""
    sql, params = apply_virtual_race("SELECT 1 WHERE x = %s", ("a",), _virtual_race())

    assert sql.startswith("WITH virtual_race_shosai AS MATERIALIZED")
    assert sql.endswith("\nSELECT 1 WHERE x = %s")
    assert sql.count("NOT MATERIALIZED") == 2
    assert sql.count(" AS MATERIALIZED") == 2
    assert "kyosoba_master2" not in sql
    assert params[2:] == ("a",)
    assert json.loads(params[0]) == [{"race_code": _RACE_CODE}]
    assert json.loads(params[1]) == [_entry("01"), _entry("02", "2022105519")]


@pytest.mark.parametrize("keyword", ["WITH", "WITH RECURSIVE"])
def test_apply_virtual_race_prepends_ctes_to_existing_with(keyword: str) -> None:
    """WITH・WITH RECURSIVE で始まる SQL は、CTE の並びの先頭に足す."""
    sql, params = apply_virtual_race(
        f"{keyword} a AS (SELECT %s)\nSELECT * FROM a", (5,), _virtual_race()
    )

    assert sql.startswith(f"{keyword} virtual_race_shosai AS MATERIALIZED")
    assert sql.index("virtual_umagoto_race_joho") < sql.index("a AS (SELECT %s)")
    assert sql.count("WITH") == 1
    assert params[2:] == (5,)


def test_apply_virtual_race_adds_horse_ctes_when_horses_given() -> None:
    """horses がある場合は kyosoba_master2 の CTE も足す."""
    horse = {"ketto_toroku_bango": "000a000001", "ketto1_bamei": "テスト"}
    sql, params = apply_virtual_race("SELECT 1", (), _virtual_race([horse]))

    assert "virtual_kyosoba_master2 AS MATERIALIZED" in sql
    assert "kyosoba_master2 AS NOT MATERIALIZED" in sql
    assert len(params) == 3
    assert json.loads(params[2]) == [horse]


# 準正常系
def test_virtual_race_without_race_code_raises() -> None:
    """race に race_code が無いと ValueError."""
    with pytest.raises(ValueError):
        VirtualRace(race={}, entries=[])


@pytest.mark.parametrize("missing", ["race_code", "ketto_toroku_bango", "umaban"])
def test_virtual_race_entry_without_required_column_raises(missing: str) -> None:
    """entries の行に必須の列が無いと ValueError."""
    entry = _entry("01")
    del entry[missing]
    with pytest.raises(ValueError):
        VirtualRace(race={"race_code": _RACE_CODE}, entries=[entry])


def test_virtual_race_entry_race_code_mismatch_raises() -> None:
    """entries の race_code が race と違うと ValueError."""
    entry = {**_entry("01"), "race_code": "2099110105041112"}
    with pytest.raises(ValueError):
        VirtualRace(race={"race_code": _RACE_CODE}, entries=[entry])


def test_virtual_race_duplicate_umaban_raises() -> None:
    """umaban が重複すると ValueError."""
    with pytest.raises(ValueError):
        VirtualRace(race={"race_code": _RACE_CODE}, entries=[_entry("01"), _entry("01", "x")])


def test_virtual_race_horse_without_ketto_toroku_bango_raises() -> None:
    """horses の行に ketto_toroku_bango が無いと ValueError."""
    with pytest.raises(ValueError):
        _virtual_race([{"ketto1_bamei": "テスト"}])


def test_virtual_race_duplicate_horse_raises() -> None:
    """horses の ketto_toroku_bango が重複すると ValueError."""
    horse = {"ketto_toroku_bango": "000a000001"}
    with pytest.raises(ValueError):
        _virtual_race([horse, horse])


def test_validate_virtual_race_columns_unknown_column_raises(mocker: MockerFixture) -> None:
    """表に無い列名があると ValueError."""
    manager = mocker.MagicMock()
    manager.execute_query.return_value = [("race_code",), ("umaban",), ("ketto_toroku_bango",)]
    virtual_race = VirtualRace(
        race={"race_code": _RACE_CODE, "no_such_column": "x"}, entries=[_entry("01")]
    )

    with pytest.raises(ValueError, match="no_such_column"):
        validate_virtual_race_columns(manager, virtual_race)


def test_validate_virtual_race_columns_known_columns_passes(mocker: MockerFixture) -> None:
    """列名がすべて表にあれば例外にならない."""
    manager = mocker.MagicMock()
    manager.execute_query.return_value = [("race_code",), ("umaban",), ("ketto_toroku_bango",)]

    validate_virtual_race_columns(manager, _virtual_race())
