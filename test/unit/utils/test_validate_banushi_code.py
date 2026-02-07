"""validate_banushi_code関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_banushi_code

# 正常系


def test_validate_banushi_code_with_none() -> None:
    """validate_banushi_code: Noneを渡した場合は何もしない."""
    validate_banushi_code(None)


def test_validate_banushi_code_with_valid_single_code() -> None:
    """validate_banushi_code: 有効な単一コードを渡した場合は正常終了."""
    validate_banushi_code("000001")


def test_validate_banushi_code_with_valid_list() -> None:
    """validate_banushi_code: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_banushi_code(["000001", "000002"])


def test_validate_banushi_code_with_alphanumeric() -> None:
    """validate_banushi_code: 英数字混合の6桁コードも有効."""
    # 馬主コードは数字のみのバリデーションがないため英数字混合も許容される
    validate_banushi_code("A00001")


# 準正常系


def test_validate_banushi_code_with_short_code() -> None:
    """validate_banushi_code: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="6桁である必要があります"):
        validate_banushi_code("12345")


def test_validate_banushi_code_with_long_code() -> None:
    """validate_banushi_code: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="6桁である必要があります"):
        validate_banushi_code("1234567")


def test_validate_banushi_code_with_non_string() -> None:
    """validate_banushi_code: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_banushi_code(123456)  # type: ignore[arg-type]
