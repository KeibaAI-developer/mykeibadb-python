"""AttrSource の from_dict テスト。"""

import pytest

from mykeibadb.analytics import AttrSource


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


# ---------------------------------------------------------------------------
# 準正常系
# ---------------------------------------------------------------------------
def test_attrsource_from_dict_missing_type_raises() -> None:
    """type キーが存在しない場合に KeyError が発生する。"""
    with pytest.raises(KeyError):
        AttrSource.from_dict({"column": "kyori"})
