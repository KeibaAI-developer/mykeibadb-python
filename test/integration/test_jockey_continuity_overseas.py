"""海外のレースを含む継続騎乗の結合テスト.

カランダガンは2025年のジャパンC（騎手コードあり）の前走が海外のレース（騎手コード 00000）で、
どちらもバルザローナ騎手が乗っている。
"""

from mykeibadb.analytics import (
    AttrSource,
    GroupBy,
    RaceCondition,
    Subject,
    SubjectFilter,
)
from mykeibadb.analytics.entry_select import select_entries
from mykeibadb.connection import ConnectionManager

_CALANDAGAN = "2021190001"
_JAPAN_CUP_2025 = "2025113005050812"
_SOURCE = AttrSource(type="jockey_continuity")
_JAPAN_CUP_2025_CONDITION = RaceCondition(
    year_from="2025", year_to="2025", tokubetsu_kyoso_bango="0015"
)


# 正常系
def test_jockey_continuity_group_by_matches_overseas_jockey_name(
    connection_manager: ConnectionManager,
) -> None:
    """group_by で、前走が騎手コード 00000 の海外のレースでも騎手名で継続と判定する."""
    entries = select_entries(
        connection_manager,
        filters=[SubjectFilter(subject=Subject.UMA, code=_CALANDAGAN)],
        condition=_JAPAN_CUP_2025_CONDITION,
        group_by=GroupBy(
            kind="fixed",
            source=_SOURCE,
            rows={"継続": "継続", "乗り戻り": "乗り戻り", "テン乗り": "テン乗り"},
        ),
    )

    labels = {e.race_code: e.group_label for e in entries}
    assert labels[_JAPAN_CUP_2025] == "継続"
