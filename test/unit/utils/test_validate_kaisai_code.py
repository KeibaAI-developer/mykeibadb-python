"""validate_kaisai_code関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_kaisai_code

# 正常系


def test_validate_kaisai_code_with_none() -> None:
    """validate_kaisai_code: Noneを渡した場合は何もしない."""
    validate_kaisai_code(None)


def test_validate_kaisai_code_with_valid_single_code() -> None:
    """validate_kaisai_code: 有効な単一コードを渡した場合は正常終了."""
    validate_kaisai_code("20250103060100")


def test_validate_kaisai_code_with_valid_list() -> None:
    """validate_kaisai_code: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_kaisai_code(["20250103060100", "20250103060200"])


# 準正常系


def test_validate_kaisai_code_with_short_code() -> None:
    """validate_kaisai_code: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="14桁である必要があります"):
        validate_kaisai_code("123456789012")


def test_validate_kaisai_code_with_long_code() -> None:
    """validate_kaisai_code: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="14桁である必要があります"):
        validate_kaisai_code("123456789012345")


def test_validate_kaisai_code_with_non_digit() -> None:
    """validate_kaisai_code: 数字でない文字が含まれる場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_kaisai_code("ABCDEFGHIJKLMN")


def test_validate_kaisai_code_with_mixed_characters() -> None:
    """validate_kaisai_code: 数字と文字が混在する場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_kaisai_code("2025010306010A")


def test_validate_kaisai_code_with_non_string() -> None:
    """validate_kaisai_code: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_kaisai_code(12345678901234)  # type: ignore[arg-type]
