"""海外のレースの着順を競馬場コードと競走名本題で引く結合テスト.

2025年のドバイシーマクラシック（競馬場コード C7）で、2025年のジャパンCの出走馬は
ダノンデサイルが1着、カランダガンが2着、シンエンペラーが7着だった。
"""

from mykeibadb.analytics import AttrSource, GroupBy, RaceCondition
from mykeibadb.analytics.entry_select import select_entries
from mykeibadb.connection import ConnectionManager

_DANON_DECILE = "2021105143"
_CALANDAGAN = "2021190001"
_SHIN_EMPEROR = "2021110048"
_JAPAN_CUP_2025 = "2025113005050812"


# 正常系
def test_tokubetsu_race_finish_reads_overseas_race_by_venue_and_name(
    connection_manager: ConnectionManager,
) -> None:
    """競馬場コードと競走名本題で指定した海外のレースの着順を返し、出ていない馬は不出走にする."""
    entries = select_entries(
        connection_manager,
        filters=[],
        condition=RaceCondition(year_from="2025", year_to="2025", tokubetsu_kyoso_bango="0015"),
        group_by=GroupBy(
            kind="history",
            source=AttrSource(
                type="tokubetsu_race_finish",
                keibajo_codes=["C7"],
                race_names=["ドバイシーマクラシック"],
                year_offset=0,
                absent_label="出走なし",
            ),
        ),
    )

    labels = {
        e.ketto_toroku_bango: e.group_label for e in entries if e.race_code == _JAPAN_CUP_2025
    }
    assert labels[_DANON_DECILE] == "1"
    assert labels[_CALANDAGAN] == "2"
    assert labels[_SHIN_EMPEROR] == "7"
    others = {
        label
        for ketto, label in labels.items()
        if ketto not in {_DANON_DECILE, _CALANDAGAN, _SHIN_EMPEROR}
    }
    assert others == {"出走なし"}
