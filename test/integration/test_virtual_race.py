"""仮のレースの結合テスト.

DB に無いレースコードの仮のレースで、get_race_entry_groups が値を返すことを確認する。
"""

import pytest

from mykeibadb.analytics import (
    AttrSource,
    GroupBy,
    Subject,
    VirtualRace,
    get_race_entry_groups,
)
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError

_RACE_CODE = "2099110105041111"
_LEGAREIRA = "2021105898"
_OTHER_HORSE = "2022105519"
_VIRTUAL_HORSE = "000a000001"


def _entry(umaban: str, ketto: str, **columns: str) -> dict[str, str]:
    """仮の出走の行を返す."""
    return {
        "race_code": _RACE_CODE,
        "ketto_toroku_bango": ketto,
        "umaban": umaban,
        "wakuban": str((int(umaban) + 1) // 2),
        "ijo_kubun_code": "0",
        **columns,
    }


def _virtual_race(horses: list[dict[str, str]] | None = None) -> VirtualRace:
    """仮のレースを返す."""
    return VirtualRace(
        race={
            "race_code": _RACE_CODE,
            "kaisai_nen": "2099",
            "kaisai_gappi": "1101",
            "keibajo_code": "05",
            "kyori": "2400",
        },
        entries=[
            _entry("01", _LEGAREIRA, kishumei_ryakusho="テスト騎手", kishu_code="05339"),
            _entry("02", _OTHER_HORSE, kishumei_ryakusho="別騎手", kishu_code="00000"),
            _entry("03", _VIRTUAL_HORSE, kishumei_ryakusho="外国騎手", kishu_code="05339"),
        ],
        horses=horses if horses is not None else [],
    )


# 正常系
def test_virtual_race_race_col_returns_column_values(
    connection_manager: ConnectionManager,
) -> None:
    """race_col で仮の出走の列の値が返る."""
    result = get_race_entry_groups(
        connection_manager,
        _RACE_CODE,
        GroupBy(kind="race_col", column="u.wakuban"),
        virtual_race=_virtual_race(),
    )

    assert result == {1: "1", 2: "1", 3: "2"}


def test_virtual_race_subject_returns_jockey_names(
    connection_manager: ConnectionManager,
) -> None:
    """subject(騎手) で仮の出走の騎手名が返る."""
    result = get_race_entry_groups(
        connection_manager,
        _RACE_CODE,
        GroupBy(kind="subject", subject=Subject.KISHU),
        virtual_race=_virtual_race(),
    )

    assert result == {1: "テスト騎手", 2: "別騎手", 3: "外国騎手"}


def test_virtual_race_fixed_career_count_is_none_for_virtual_horse(
    connection_manager: ConnectionManager,
) -> None:
    """fixed(キャリア) で、DB にある馬は経験馬、過去走の無い仮の馬は None になる."""
    horse = {"ketto_toroku_bango": _VIRTUAL_HORSE, "ketto1_bamei": "テスト父"}
    result = get_race_entry_groups(
        connection_manager,
        _RACE_CODE,
        GroupBy(
            kind="fixed",
            source=AttrSource(type="career_count"),
            rows={"初出走": 0, "経験馬": (1, 9999)},
        ),
        virtual_race=_virtual_race([horse]),
    )

    assert result[1] == "経験馬"
    assert result[3] is None


def test_virtual_race_subject_sire_returns_virtual_horse_sire_name(
    connection_manager: ConnectionManager,
) -> None:
    """subject(種牡馬) で、仮の競走馬の行の父の名前が返る."""
    horse = {"ketto_toroku_bango": _VIRTUAL_HORSE, "ketto1_bamei": "テスト父"}
    result = get_race_entry_groups(
        connection_manager,
        _RACE_CODE,
        GroupBy(kind="subject", subject=Subject.SIRE),
        virtual_race=_virtual_race([horse]),
    )

    assert result[3] == "テスト父"
    assert result[1] is not None and result[1] != "テスト父"


def test_virtual_race_jockey_continuity_without_jockey_code_is_none(
    connection_manager: ConnectionManager,
) -> None:
    """騎手コードが 00000 の出走は、継続騎乗の値が None になる."""
    result = get_race_entry_groups(
        connection_manager,
        _RACE_CODE,
        GroupBy(
            kind="fixed",
            source=AttrSource(type="jockey_continuity"),
            rows={"継続": "継続", "乗り戻り": "乗り戻り", "テン乗り": "テン乗り"},
        ),
        virtual_race=_virtual_race(),
    )

    assert result[2] is None
    assert result[1] in ("継続", "乗り戻り", "テン乗り")


def test_virtual_race_does_not_affect_query_without_virtual_race(
    connection_manager: ConnectionManager,
) -> None:
    """仮のレースを指定した後でも、指定しない呼び出しでは仮のレースの出走馬が見つからない."""
    group_by = GroupBy(kind="race_col", column="u.wakuban")
    get_race_entry_groups(connection_manager, _RACE_CODE, group_by, virtual_race=_virtual_race())

    with pytest.raises(MykeibaDBError):
        get_race_entry_groups(connection_manager, _RACE_CODE, group_by)


# 準正常系
def test_virtual_race_unknown_column_raises(connection_manager: ConnectionManager) -> None:
    """表に無い列名を含む仮のレースは ValueError."""
    virtual_race = VirtualRace(
        race={"race_code": _RACE_CODE, "no_such_column": "x"},
        entries=[_entry("01", _LEGAREIRA)],
    )

    with pytest.raises(ValueError, match="no_such_column"):
        get_race_entry_groups(
            connection_manager,
            _RACE_CODE,
            GroupBy(kind="race_col", column="u.wakuban"),
            virtual_race=virtual_race,
        )
