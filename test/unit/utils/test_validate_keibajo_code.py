"""validate_keibajo_code関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_keibajo_code

# 正常系


def test_validate_keibajo_code_with_none() -> None:
    """validate_keibajo_code: Noneを渡した場合は何もしない."""
    validate_keibajo_code(None)


def test_validate_keibajo_code_with_valid_single_code() -> None:
    """validate_keibajo_code: 有効な単一コードを渡した場合は正常終了."""
    validate_keibajo_code("06")


def test_validate_keibajo_code_with_valid_list() -> None:
    """validate_keibajo_code: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_keibajo_code(["06", "07"])


def test_validate_keibajo_code_with_alphabetic() -> None:
    """validate_keibajo_code: アルファベットの2桁コードも有効."""
    # 競馬場コードは数字のみのバリデーションがないためアルファベットも許容される
    validate_keibajo_code("AB")


# 準正常系
def test_validate_keibajo_code_with_short_code() -> None:
    """validate_keibajo_code: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="2桁である必要があります"):
        validate_keibajo_code("1")


def test_validate_keibajo_code_with_long_code() -> None:
    """validate_keibajo_code: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="2桁である必要があります"):
        validate_keibajo_code("123")


def test_validate_keibajo_code_with_non_string() -> None:
    """validate_keibajo_code: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_keibajo_code(12)  # type: ignore[arg-type]
