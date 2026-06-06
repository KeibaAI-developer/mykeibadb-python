"""compute_chakudo の単体テスト."""

from mykeibadb.analytics._models import GroupTally
from mykeibadb.analytics.chakudo_compute import compute_chakudo


def _make_gt(
    group: str = "全体",
    total: int = 10,
    wins: int = 2,
    second: int = 1,
    third: int = 1,
    chakugai: int = 6,
    tansho: int = 2000,
    fukusho: int = 1200,
) -> GroupTally:
    return GroupTally(
        group=group,
        total=total,
        wins=wins,
        second=second,
        third=third,
        chakugai=chakugai,
        tansho_payout_sum=tansho,
        fukusho_payout_sum=fukusho,
    )


# 正常系
def test_compute_chakudo_win_rate_calculated_correctly() -> None:
    """wins / total * 100 が win_rate に設定される."""
    result = compute_chakudo([_make_gt(total=10, wins=3)])

    assert result.success is True
    assert result.rows[0].win_rate == 30.0


def test_compute_chakudo_fukusho_rate_calculated_correctly() -> None:
    """(wins + second + third) / total * 100 が fukusho_rate に設定される."""
    result = compute_chakudo([_make_gt(total=10, wins=3, second=2, third=1)])

    assert result.rows[0].fukusho_rate == 60.0


def test_compute_chakudo_tansho_kaishuu_calculated_correctly() -> None:
    """tansho_payout_sum / total が tansho_kaishuu に設定される."""
    result = compute_chakudo([_make_gt(total=10, tansho=1500)])

    assert result.rows[0].tansho_kaishuu == 150.0


def test_compute_chakudo_fukusho_kaishuu_calculated_correctly() -> None:
    """fukusho_payout_sum / total が fukusho_kaishuu に設定される."""
    result = compute_chakudo([_make_gt(total=10, fukusho=800)])

    assert result.rows[0].fukusho_kaishuu == 80.0


def test_compute_chakudo_rates_rounded_to_one_decimal() -> None:
    """率は小数点1桁に丸められる."""
    result = compute_chakudo([_make_gt(total=3, wins=1, second=1, third=0)])

    assert result.rows[0].win_rate == 33.3
    assert result.rows[0].fukusho_rate == 66.7


# total=0 のケース
def test_compute_chakudo_all_rates_zero_when_total_zero() -> None:
    """total=0 のとき全率が 0.0 になる."""
    result = compute_chakudo([_make_gt(total=0)])

    row = result.rows[0]
    assert row.win_rate == 0.0
    assert row.fukusho_rate == 0.0
    assert row.tansho_kaishuu == 0.0
    assert row.fukusho_kaishuu == 0.0


def test_compute_chakudo_total_zero_row_has_zero_counts() -> None:
    """total=0 のとき wins/second/third/chakugai も 0 になる."""
    result = compute_chakudo([_make_gt(total=0)])

    row = result.rows[0]
    assert row.wins == 0
    assert row.second == 0
    assert row.third == 0
    assert row.chakugai == 0


# 複数グループ
def test_compute_chakudo_multiple_groups_stored_in_rows() -> None:
    """複数グループがそれぞれ ChakudoRow として rows に格納される."""
    result = compute_chakudo(
        [
            _make_gt(group="キタサンブラック", total=5, wins=2),
            _make_gt(group="ディープインパクト", total=8, wins=1),
        ]
    )

    assert result.success is True
    assert len(result.rows) == 2
    groups = {r.group for r in result.rows}
    assert groups == {"キタサンブラック", "ディープインパクト"}


def test_compute_chakudo_empty_tally_returns_empty_rows() -> None:
    """空 ChakudoTally で rows が空の ChakudoResult が返る."""
    result = compute_chakudo([])

    assert result.success is True
    assert result.rows == []


def test_compute_chakudo_group_name_preserved() -> None:
    """GroupTally.group が ChakudoRow.group にそのまま格納される."""
    result = compute_chakudo([_make_gt(group="東京芝2400m")])

    assert result.rows[0].group == "東京芝2400m"


def test_compute_chakudo_count_fields_preserved() -> None:
    """wins/second/third/chakugai/total が ChakudoRow にそのまま格納される."""
    result = compute_chakudo(
        [_make_gt(total=20, wins=5, second=3, third=2, chakugai=10)]
    )

    row = result.rows[0]
    assert row.total == 20
    assert row.wins == 5
    assert row.second == 3
    assert row.third == 2
    assert row.chakugai == 10
