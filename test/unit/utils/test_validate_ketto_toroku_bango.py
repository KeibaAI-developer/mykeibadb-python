"""validate_ketto_toroku_bango関数のテスト."""

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_ketto_toroku_bango

# 正常系


def test_validate_ketto_toroku_bango_with_none() -> None:
    """validate_ketto_toroku_bango: Noneを渡した場合は何もしない."""
    validate_ketto_toroku_bango(None)


def test_validate_ketto_toroku_bango_with_valid_single_code() -> None:
    """validate_ketto_toroku_bango: 有効な単一コードを渡した場合は正常終了."""
    validate_ketto_toroku_bango("2022100001")


def test_validate_ketto_toroku_bango_with_valid_list() -> None:
    """validate_ketto_toroku_bango: 有効な複数コードのリストを渡した場合は正常終了."""
    validate_ketto_toroku_bango(["2022100001", "2022100002"])


# 準正常系


def test_validate_ketto_toroku_bango_with_short_code() -> None:
    """validate_ketto_toroku_bango: 桁数不足でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="10桁である必要があります"):
        validate_ketto_toroku_bango("12345")


def test_validate_ketto_toroku_bango_with_long_code() -> None:
    """validate_ketto_toroku_bango: 桁数超過でValidationErrorが発生."""
    with pytest.raises(ValidationError, match="10桁である必要があります"):
        validate_ketto_toroku_bango("12345678901")


def test_validate_ketto_toroku_bango_with_non_digit() -> None:
    """validate_ketto_toroku_bango: 数字でない文字が含まれる場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_ketto_toroku_bango("ABCDEFGHIJ")


def test_validate_ketto_toroku_bango_with_mixed_characters() -> None:
    """validate_ketto_toroku_bango: 数字と文字が混在する場合ValidationErrorが発生."""
    with pytest.raises(ValidationError, match="数字のみで構成される必要があります"):
        validate_ketto_toroku_bango("202210000A")


def test_validate_ketto_toroku_bango_with_non_string() -> None:
    """validate_ketto_toroku_bango: 文字列でない場合TypeErrorが発生."""
    with pytest.raises(TypeError):
        validate_ketto_toroku_bango(1234567890)  # type: ignore[arg-type]


def test_validate_ketto_toroku_bango_with_list_containing_non_string() -> None:
    """validate_ketto_toroku_bango: リストに文字列でない要素がある場合エラー."""
    with pytest.raises(ValidationError, match="文字列である必要があります"):
        validate_ketto_toroku_bango(["2022100001", 1234567890])  # type: ignore[list-item]
