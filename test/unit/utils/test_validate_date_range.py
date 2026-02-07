"""validate_date_range関数のテスト."""

from datetime import date

import pytest

from mykeibadb.exceptions import ValidationError
from mykeibadb.utils import validate_date_range

# 正常系


def test_validate_date_range_with_both_none() -> None:
    """validate_date_range: 両方Noneの場合は正常終了."""
    validate_date_range(None, None)


def test_validate_date_range_with_start_date_none() -> None:
    """validate_date_range: start_dateがNoneの場合は正常終了."""
    validate_date_range(None, date(2025, 12, 31))


def test_validate_date_range_with_end_date_none() -> None:
    """validate_date_range: end_dateがNoneの場合は正常終了."""
    validate_date_range(date(2025, 1, 1), None)


def test_validate_date_range_with_valid_range() -> None:
    """validate_date_range: start_dateがend_date以前の場合は正常終了."""
    validate_date_range(date(2025, 1, 1), date(2025, 12, 31))


def test_validate_date_range_with_same_date() -> None:
    """validate_date_range: start_dateとend_dateが同じ日付の場合は正常終了."""
    validate_date_range(date(2025, 6, 15), date(2025, 6, 15))


def test_validate_date_range_with_consecutive_dates() -> None:
    """validate_date_range: 連続した日付の場合は正常終了."""
    validate_date_range(date(2025, 6, 15), date(2025, 6, 16))


def test_validate_date_range_with_one_year_range() -> None:
    """validate_date_range: 1年の範囲で正常終了."""
    validate_date_range(date(2024, 1, 1), date(2024, 12, 31))


def test_validate_date_range_with_cross_year() -> None:
    """validate_date_range: 年をまたぐ範囲で正常終了."""
    validate_date_range(date(2024, 12, 31), date(2025, 1, 1))


# 準正常系


def test_validate_date_range_with_start_after_end() -> None:
    """validate_date_range: start_dateがend_dateより後の場合はValidationError."""
    with pytest.raises(
        ValidationError,
        match=r"start_date \(2025-12-31\) はend_date \(2025-01-01\) 以前である必要があります",
    ):
        validate_date_range(date(2025, 12, 31), date(2025, 1, 1))


def test_validate_date_range_with_large_gap() -> None:
    """validate_date_range: start_dateとend_dateの差が大きい場合もValidationError."""
    with pytest.raises(
        ValidationError,
        match=r"start_date \(2025-12-31\) はend_date \(2024-01-01\) 以前である必要があります",
    ):
        validate_date_range(date(2025, 12, 31), date(2024, 1, 1))


def test_validate_date_range_with_one_day_difference_reversed() -> None:
    """validate_date_range: 1日だけ逆転している場合もValidationError."""
    with pytest.raises(
        ValidationError,
        match=r"start_date \(2025-06-16\) はend_date \(2025-06-15\) 以前である必要があります",
    ):
        validate_date_range(date(2025, 6, 16), date(2025, 6, 15))
