"""海外のレースを含む継続騎乗の結合テスト.

カランダガンの過去走は次のとおり（新しい順）。

- 2026年英チャンピオンS: スミヨン騎手（騎手コード 00000）
- 2026年キングジョージ6世&QES など: バルザローナ騎手（騎手コード 00000）
- 2025年ジャパンC: バルザローナ騎手（騎手コード 05504）
- 2025年英チャンピオンS: バルザローナ騎手（騎手コード 00000）
"""

import pytest

from mykeibadb.analytics import (
    AttrSource,
    GroupBy,
    RaceCondition,
    Subject,
    SubjectFilter,
    VirtualRace,
    get_race_entry_groups,
)
from mykeibadb.analytics.entry_select import select_entries
from mykeibadb.connection import ConnectionManager

_CALANDAGAN = "2021190001"
_JAPAN_CUP_2025 = "2025113005050812"
_VIRTUAL_RACE_CODE = "2099112905050812"
_GROUP_BY = GroupBy(
    kind="fixed",
    source=AttrSource(type="jockey_continuity"),
    rows={"継続": "継続", "乗り戻り": "乗り戻り", "テン乗り": "テン乗り"},
)


# 正常系
def test_jockey_continuity_matches_overseas_jockey_name_in_previous_race(
    connection_manager: ConnectionManager,
) -> None:
    """前走が騎手コード 00000 の海外のレースでも、騎手名が同じなら継続と判定する."""
    entries = select_entries(
        connection_manager,
        filters=[SubjectFilter(subject=Subject.UMA, code=_CALANDAGAN)],
        condition=RaceCondition(year_from="2025", year_to="2025", tokubetsu_kyoso_bango="0015"),
        group_by=_GROUP_BY,
    )

    labels = {e.race_code: e.group_label for e in entries}
    assert labels[_JAPAN_CUP_2025] == "継続"


@pytest.mark.parametrize(
    ("kishu_code", "expected"),
    [("05271", "継続"), ("05504", "乗り戻り"), ("01126", "テン乗り")],
)
def test_jockey_continuity_judges_overseas_history_by_jockey_name(
    connection_manager: ConnectionManager,
    kishu_code: str,
    expected: str,
) -> None:
    """騎手コード 00000 の過去走を騎手名で比べ、継続・乗り戻り・テン乗りを判定する."""
    virtual_race = VirtualRace(
        race={
            "race_code": _VIRTUAL_RACE_CODE,
            "kaisai_nen": "2099",
            "kaisai_gappi": "1129",
            "keibajo_code": "05",
            "kyori": "2400",
        },
        entries=[
            {
                "race_code": _VIRTUAL_RACE_CODE,
                "ketto_toroku_bango": _CALANDAGAN,
                "umaban": "01",
                "wakuban": "1",
                "ijo_kubun_code": "0",
                "kishu_code": kishu_code,
            }
        ],
        horses=[],
    )

    result = get_race_entry_groups(
        connection_manager, _VIRTUAL_RACE_CODE, _GROUP_BY, virtual_race=virtual_race
    )

    assert result[1] == expected
