"""validate_tracen_kubun関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_tracen_kubun

# 正常系


def test_validate_tracen_kubun_with_none() -> None:
    """validate_tracen_kubun: Noneを渡した場合は何もしない."""
    validate_tracen_kubun(None)


def test_validate_tracen_kubun_with_valid_single_code() -> None:
    """validate_tracen_kubun: 有効な単一コードを渡した場合は正常終了."""
    validate_tracen_kubun("1")


def test_validate_tracen_kubun_with_valid_list() -> None:
    """validate_tracen_kubun: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_tracen_kubun(["1", "2"])


def test_validate_tracen_kubun_with_long_string() -> None:
    """validate_tracen_kubun: 長い文字列も有効."""
    # トレセン区分は長さのバリデーションがないため長い文字列も許容される
    validate_tracen_kubun("RITTO")


# 準正常系


def test_validate_tracen_kubun_with_non_string() -> None:
    """validate_tracen_kubun: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_tracen_kubun(1)  # type: ignore[arg-type]


def test_validate_tracen_kubun_with_list_containing_non_string() -> None:
    """validate_tracen_kubun: リストに文字列でない要素がある場合エラー."""
    with pytest.raises(ValidationError, match="文字列である必要があります"):
        validate_tracen_kubun(["1", 2])  # type: ignore[list-item]
