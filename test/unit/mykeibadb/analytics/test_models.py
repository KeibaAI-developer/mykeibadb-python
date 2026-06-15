"""AttrSource / RaceCondition / GroupBy / EntryFilter の from_dict テスト。"""

from typing import Any

import pytest

from mykeibadb.analytics import AttrSource, Subject, build_entry_filter, parse_rows_def
from mykeibadb.analytics._models import (
    ChokyoFilter,
    ChokyoThreshold,
    GroupBy,
    HistoryFilter,
    RaceColFilter,
    RaceCondition,
    RowsDef,
    SubjectFilter,
)


# ---------------------------------------------------------------------------
# 正常系
# ---------------------------------------------------------------------------
def test_attrsource_from_dict_column() -> None:
    """column フィールドが from_dict で正しく読み取れる。"""
    src = AttrSource.from_dict({"type": "prev_race_col", "column": "kyori"})
    assert src.column == "kyori"


def test_attrsource_from_dict_overseas_label() -> None:
    """overseas_label フィールドが from_dict で正しく読み取れる。"""
    src = AttrSource.from_dict({"type": "prev_race_name", "overseas_label": "海外"})
    assert src.overseas_label == "海外"


def test_attrsource_from_dict_tokubetsu_kyoso_bango() -> None:
    """tokubetsu_kyoso_bango フィールドが from_dict で正しく読み取れる。"""
    src = AttrSource.from_dict(
        {"type": "same_race_prev_year_finish", "tokubetsu_kyoso_bango": "0010"}
    )
    assert src.tokubetsu_kyoso_bango == "0010"


def test_attrsource_from_dict_absent_label_custom() -> None:
    """absent_label を指定した場合に from_dict で正しく読み取れる。"""
    src = AttrSource.from_dict(
        {
            "type": "same_race_prev_year_finish",
            "tokubetsu_kyoso_bango": "0010",
            "absent_label": "前年出走無し",
        }
    )
    assert src.absent_label == "前年出走無し"


def test_attrsource_absent_label_default() -> None:
    """absent_label の既定値は「出走無し」。"""
    src = AttrSource(type="x")
    assert src.absent_label == "出走無し"


def test_attrsource_from_dict_absent_label_default() -> None:
    """absent_label を省略した場合は既定値「出走無し」。"""
    src = AttrSource.from_dict({"type": "same_race_prev_year_finish"})
    assert src.absent_label == "出走無し"


def test_attrsource_from_dict_new_fields_none_by_default() -> None:
    """新フィールドを省略した場合はすべて None。"""
    src = AttrSource.from_dict({"type": "prev_race_name"})
    assert src.column is None
    assert src.overseas_label is None
    assert src.tokubetsu_kyoso_bango is None


def test_attrsource_from_dict_past_race_top_n_count_top_n_none() -> None:
    """past_race_top_n_count で top_n 未指定時は None。"""
    src = AttrSource.from_dict({"type": "past_race_top_n_count"})
    assert src.top_n is None


def test_attrsource_from_dict_past_race_top_n_count_top_n_specified() -> None:
    """past_race_top_n_count で top_n 指定時はそのint値。"""
    src = AttrSource.from_dict({"type": "past_race_top_n_count", "top_n": 1})
    assert src.top_n == 1


def test_attrsource_from_dict_other_type_top_n_default() -> None:
    """past_race_top_n_count 以外で top_n 未指定時は既定値1。"""
    src = AttrSource.from_dict({"type": "sire_condition_finisher"})
    assert src.top_n == 1


def test_attrsource_from_dict_past_race_top_n_count_keibajo_codes_and_filters() -> None:
    """keibajo_codes / filters / grade_codes フィールドが正しく読み取れる。"""
    src = AttrSource.from_dict(
        {
            "type": "past_race_top_n_count",
            "top_n": 1,
            "grade_codes": ["A", "B", "C"],
            "keibajo_codes": ["05"],
            "filters": [{"column": "kyori_int", "op": "==", "value": 2000}],
        }
    )
    assert src.grade_codes == ["A", "B", "C"]
    assert src.keibajo_codes == ["05"]
    assert src.filters == [{"column": "kyori_int", "op": "==", "value": 2000}]


# ---------------------------------------------------------------------------
# 準正常系
# ---------------------------------------------------------------------------
def test_attrsource_from_dict_missing_type_raises() -> None:
    """type キーが存在しない場合に KeyError が発生する。"""
    with pytest.raises(KeyError):
        AttrSource.from_dict({"column": "kyori"})


# ---------------------------------------------------------------------------
# RaceCondition.from_dict 正常系
# ---------------------------------------------------------------------------
def test_race_condition_from_dict_keibajo_codes() -> None:
    """keibajo_codes フィールドが from_dict で正しく読み取れる。"""
    cond = RaceCondition.from_dict({"keibajo_codes": ["09", "08"]})
    assert cond.keibajo_codes == ["09", "08"]


def test_race_condition_from_dict_kaisai_nichime() -> None:
    """kaisai_nichime フィールドが from_dict で int リストに変換される。"""
    cond = RaceCondition.from_dict({"kaisai_nichime": ["4"]})
    assert cond.kaisai_nichime == [4]


def test_race_condition_from_dict_babajotai_codes() -> None:
    """babajotai_codes フィールドが from_dict で正しく読み取れる。"""
    cond = RaceCondition.from_dict({"babajotai_codes": ["1"]})
    assert cond.babajotai_codes == ["1"]


def test_race_condition_from_dict_new_fields_none_by_default() -> None:
    """新フィールドを省略した場合はすべて None。"""
    cond = RaceCondition.from_dict({})
    assert cond.keibajo_codes is None
    assert cond.kaisai_nichime is None
    assert cond.babajotai_codes is None


# ---------------------------------------------------------------------------
# parse_rows_def 正常系・準正常系
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("input_rows", "expected"),
    [
        ({"上位": [1, 3]}, {"上位": (1, 3)}),
        ({"3歳": 3}, {"3歳": 3}),
        ({"芝": "芝"}, {"芝": "芝"}),
    ],
)
def test_parse_rows_def(input_rows: dict[str, Any], expected: RowsDef) -> None:
    """長さ2のリストは (min, max) タプル、int・strはそのまま変換される。"""
    assert parse_rows_def(input_rows) == expected


def test_parse_rows_def_invalid_value_raises() -> None:
    """(min, max) リスト・int・str 以外の値で ValueError が発生する。"""
    with pytest.raises(ValueError):
        parse_rows_def({"NG": {"a": 1}})


# ---------------------------------------------------------------------------
# ChokyoThreshold.from_dict 正常系
# ---------------------------------------------------------------------------
def test_chokyo_threshold_from_dict_required_fields() -> None:
    """course / metric / furlong の必須フィールドが正しく読み取れる。"""
    th = ChokyoThreshold.from_dict({"course": "wood", "metric": "gokei", "furlong": 6})
    assert th.course == "wood"
    assert th.metric == "gokei"
    assert th.furlong == 6
    assert th.max_value is None
    assert th.min_value is None
    assert th.tracen_kubun is None


def test_chokyo_threshold_from_dict_optional_fields() -> None:
    """max_value / min_value / tracen_kubun の任意フィールドが正しく読み取れる。"""
    th = ChokyoThreshold.from_dict(
        {
            "course": "hanro",
            "metric": "lap",
            "furlong": 1,
            "max_value": 115,
            "min_value": 100,
            "tracen_kubun": "0",
        }
    )
    assert th.max_value == 115
    assert th.min_value == 100
    assert th.tracen_kubun == "0"


# ---------------------------------------------------------------------------
# GroupBy.from_dict 正常系・準正常系
# ---------------------------------------------------------------------------
def test_group_by_from_dict_race_col() -> None:
    """kind='race_col' で column が正しく読み取れる。"""
    gb = GroupBy.from_dict({"kind": "race_col", "column": "u.wakuban"})
    assert gb.kind == "race_col"
    assert gb.column == "u.wakuban"


def test_group_by_from_dict_subject() -> None:
    """kind='subject' で subject が Subject に変換される。"""
    gb = GroupBy.from_dict({"kind": "subject", "subject": "kishu"})
    assert gb.kind == "subject"
    assert gb.subject == Subject.KISHU


def test_group_by_from_dict_history() -> None:
    """kind='history' で source が AttrSource に変換される。"""
    gb = GroupBy.from_dict(
        {"kind": "history", "source": {"type": "debut_venue"}}
    )
    assert gb.kind == "history"
    assert gb.source is not None
    assert gb.source.type == "debut_venue"


def test_group_by_from_dict_fixed() -> None:
    """kind='fixed' で source と rows が正しく変換される。"""
    gb = GroupBy.from_dict(
        {
            "kind": "fixed",
            "source": {"type": "career_count"},
            "rows": {"初出走": 0, "経験馬": [1, 9999]},
        }
    )
    assert gb.kind == "fixed"
    assert gb.source is not None
    assert gb.source.type == "career_count"
    assert gb.rows == {"初出走": 0, "経験馬": (1, 9999)}


@pytest.mark.parametrize(
    "d",
    [
        {"kind": "race_col"},
        {"kind": "subject"},
        {"kind": "history"},
        {"kind": "fixed", "source": {"type": "career_count"}},
        {"kind": "unknown"},
    ],
)
def test_group_by_from_dict_missing_field_or_unsupported_kind_raises(d: dict[str, Any]) -> None:
    """必須フィールド欠落・未対応 kind で ValueError が発生する。"""
    with pytest.raises(ValueError):
        GroupBy.from_dict(d)


# ---------------------------------------------------------------------------
# build_entry_filter 正常系・準正常系
# ---------------------------------------------------------------------------
def test_build_entry_filter_race_col() -> None:
    """type='race_col' で RaceColFilter が生成される。"""
    f = build_entry_filter(
        {"type": "race_col", "column": "u.wakuban", "values": ["1", "2"]}
    )
    assert isinstance(f, RaceColFilter)
    assert f.column == "u.wakuban"
    assert f.values == ["1", "2"]


def test_build_entry_filter_subject() -> None:
    """type='subject' で SubjectFilter が生成され subject が Subject に変換される。"""
    f = build_entry_filter({"type": "subject", "subject": "kishu", "name": "ルメール"})
    assert isinstance(f, SubjectFilter)
    assert f.subject == Subject.KISHU
    assert f.name == "ルメール"


def test_build_entry_filter_history_range_cond() -> None:
    """type='history' で cond が (min, max) タプルに変換される。"""
    f = build_entry_filter(
        {"type": "history", "source": {"type": "career_count"}, "cond": [1, 3]}
    )
    assert isinstance(f, HistoryFilter)
    assert f.source.type == "career_count"
    assert f.cond == (1, 3)


def test_build_entry_filter_history_scalar_cond() -> None:
    """type='history' で cond が int/str の場合はそのまま変換される。"""
    f = build_entry_filter(
        {"type": "history", "source": {"type": "debut_venue"}, "cond": "05"}
    )
    assert isinstance(f, HistoryFilter)
    assert f.cond == "05"


def test_build_entry_filter_chokyo() -> None:
    """type='chokyo' で ChokyoFilter が生成され condition が ChokyoThreshold に変換される。"""
    f = build_entry_filter(
        {
            "type": "chokyo",
            "condition": [{"course": "wood", "metric": "gokei", "furlong": 6, "max_value": 825}],
        }
    )
    assert isinstance(f, ChokyoFilter)
    assert len(f.condition) == 1
    assert f.condition[0].course == "wood"
    assert f.condition[0].max_value == 825


def test_build_entry_filter_unsupported_type_raises() -> None:
    """未対応の type で ValueError が発生する。"""
    with pytest.raises(ValueError):
        build_entry_filter({"type": "unknown"})
