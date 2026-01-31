"""validate_kishu_code関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_kishu_code

# 正常系


def test_validate_kishu_code_with_none() -> None:
    """validate_kishu_code: Noneを渡した場合は何もしない."""
    validate_kishu_code(None)


def test_validate_kishu_code_with_valid_single_code() -> None:
    """validate_kishu_code: 有効な単一コードを渡した場合は正常終了."""
    validate_kishu_code("00001")


def test_validate_kishu_code_with_valid_list() -> None:
    """validate_kishu_code: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_kishu_code(["00001", "00002"])


# 準正常系


def test_validate_kishu_code_with_short_code() -> None:
    """validate_kishu_code: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="5桁である必要があります"):
        validate_kishu_code("1234")


def test_validate_kishu_code_with_long_code() -> None:
    """validate_kishu_code: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="5桁である必要があります"):
        validate_kishu_code("123456")


def test_validate_kishu_code_with_non_digit() -> None:
    """validate_kishu_code: 数字でない文字が含まれる場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_kishu_code("ABCDE")


def test_validate_kishu_code_with_mixed_characters() -> None:
    """validate_kishu_code: 数字と文字が混在する場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_kishu_code("0000A")


def test_validate_kishu_code_with_non_string() -> None:
    """validate_kishu_code: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_kishu_code(12345)  # type: ignore[arg-type]
