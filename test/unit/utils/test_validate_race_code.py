"""validate_race_code関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_race_code

# 正常系


def test_validate_race_code_with_none() -> None:
    """validate_race_code: Noneを渡した場合は何もしない."""
    validate_race_code(None)


def test_validate_race_code_with_valid_single_code() -> None:
    """validate_race_code: 有効な単一コードを渡した場合は正常終了."""
    validate_race_code("2025010306010101")


def test_validate_race_code_with_valid_list() -> None:
    """validate_race_code: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_race_code(["2025010306010101", "2025010306010102"])


def test_validate_race_code_with_boundary_month_01() -> None:
    """validate_race_code: 月が01の場合は正常終了."""
    validate_race_code("2025010106010101")


def test_validate_race_code_with_boundary_month_12() -> None:
    """validate_race_code: 月が12の場合は正常終了."""
    validate_race_code("2025120106010101")


def test_validate_race_code_with_boundary_day_01() -> None:
    """validate_race_code: 日が01の場合は正常終了."""
    validate_race_code("2025010106010101")


def test_validate_race_code_with_boundary_day_31() -> None:
    """validate_race_code: 日が31の場合は正常終了."""
    validate_race_code("2025013106010101")


def test_validate_race_code_with_boundary_race_01() -> None:
    """validate_race_code: レース番号が01の場合は正常終了."""
    validate_race_code("2025010306010101")


def test_validate_race_code_with_boundary_race_12() -> None:
    """validate_race_code: レース番号が12の場合は正常終了."""
    validate_race_code("2025010306010112")


# 準正常系


def test_validate_race_code_with_short_code() -> None:
    """validate_race_code: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="16桁である必要があります"):
        validate_race_code("12345")


def test_validate_race_code_with_long_code() -> None:
    """validate_race_code: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="16桁である必要があります"):
        validate_race_code("12345678901234567")


def test_validate_race_code_with_non_digit_year() -> None:
    """validate_race_code: 年部分が数字でない場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="年部分は数字である必要があります"):
        validate_race_code("ABCD010306010101")


def test_validate_race_code_with_non_digit_month() -> None:
    """validate_race_code: 月部分が数字でない場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="月部分は数字である必要があります"):
        validate_race_code("2025AB0306010101")


def test_validate_race_code_with_non_digit_day() -> None:
    """validate_race_code: 日部分が数字でない場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="日部分は数字である必要があります"):
        validate_race_code("202501AB06010101")


def test_validate_race_code_with_non_digit_kai() -> None:
    """validate_race_code: 回次部分が数字でない場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="回次部分は数字である必要があります"):
        validate_race_code("2025010306AB0101")


def test_validate_race_code_with_non_digit_nichi() -> None:
    """validate_race_code: 日次部分が数字でない場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="日次部分は数字である必要があります"):
        validate_race_code("202501030601AB01")


def test_validate_race_code_with_non_digit_race() -> None:
    """validate_race_code: レース番号部分が数字でない場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="レース番号部分は数字である必要があります"):
        validate_race_code("20250103060101AB")


def test_validate_race_code_with_month_00() -> None:
    """validate_race_code: 月が00でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="月部分が不正です"):
        validate_race_code("2025000106010101")


def test_validate_race_code_with_month_13() -> None:
    """validate_race_code: 月が13でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="月部分が不正です"):
        validate_race_code("2025130106010101")


def test_validate_race_code_with_day_00() -> None:
    """validate_race_code: 日が00でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="日部分が不正です"):
        validate_race_code("2025010006010101")


def test_validate_race_code_with_day_32() -> None:
    """validate_race_code: 日が32でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="日部分が不正です"):
        validate_race_code("2025013206010101")


def test_validate_race_code_with_race_00() -> None:
    """validate_race_code: レース番号が00でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="レース番号部分が不正です"):
        validate_race_code("2025010306010100")


def test_validate_race_code_with_race_13() -> None:
    """validate_race_code: レース番号が13でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="レース番号部分が不正です"):
        validate_race_code("2025010306010113")


def test_validate_race_code_with_non_string() -> None:
    """validate_race_code: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_race_code(12345)  # type: ignore[arg-type]


def test_validate_race_code_with_list_containing_non_string() -> None:
    """validate_race_code: リストに文字列でない要素が含まれる場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="文字列である必要があります"):
        validate_race_code(["2025010306010101", 12345])  # type: ignore[list-item]
