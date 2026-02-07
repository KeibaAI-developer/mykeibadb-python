"""validate_track_code関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_track_code

# 正常系


def test_validate_track_code_with_none() -> None:
    """validate_track_code: Noneを渡した場合は何もしない."""
    validate_track_code(None)


def test_validate_track_code_with_valid_single_code() -> None:
    """validate_track_code: 有効な単一コードを渡した場合は正常終了."""
    validate_track_code("01")


def test_validate_track_code_with_valid_list() -> None:
    """validate_track_code: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_track_code(["01", "02"])


# 準正常系


def test_validate_track_code_with_short_code() -> None:
    """validate_track_code: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="2桁である必要があります"):
        validate_track_code("1")


def test_validate_track_code_with_long_code() -> None:
    """validate_track_code: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="2桁である必要があります"):
        validate_track_code("123")


def test_validate_track_code_with_non_digit() -> None:
    """validate_track_code: 数字でない文字が含まれる場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_track_code("AB")


def test_validate_track_code_with_non_string() -> None:
    """validate_track_code: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_track_code(12)  # type: ignore[arg-type]
