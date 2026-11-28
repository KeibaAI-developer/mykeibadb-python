"""グループ別着度数・回収率集計モジュール."""

from mykeibadb.analytics._models import ChakudoResult, EntryFilter, GroupBy, RaceCondition
from mykeibadb.analytics.chakudo_compute import compute_chakudo
from mykeibadb.analytics.chakujun_tally import tally_chakujun
from mykeibadb.analytics.entry_select import select_entries
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import MykeibaDBError


def analyze_chakudo(
    manager: ConnectionManager,
    filters: list[EntryFilter],
    condition: RaceCondition | None = None,
    group_by: GroupBy | None = None,
) -> ChakudoResult:
    """3フェーズ着度数集計を実行してグループ別着度数・勝率・回収率を返す.

    フェーズ1（エントリ選択）→ フェーズ2（着順収集）→ フェーズ3（着度数計算）を連結する。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        filters (list[EntryFilter]): エントリフィルタリスト
        condition (RaceCondition | None): レース絞り込み条件
        group_by (GroupBy | None): グループ分け軸

    Returns:
        ChakudoResult: グループ別集計結果。DBエラー時は success=False。

    Raises:
        ValueError: condition.course_kubun と week_in_course のどちらか一方のみ指定した場合
        ValueError: group_by.kind が未対応の場合

    Note:
        RaceColFilter.column および GroupBy.column は SQL に直接埋め込まれるため、
        必ず信頼済みの列名を渡すこと。危険トークン（';', '--', '/*'）は検証するが、
        完全な SQLインジェクション防御ではない。
    """
    try:
        entries = select_entries(manager, filters, condition, group_by)
        tally = tally_chakujun(manager, entries)
        return compute_chakudo(tally)
    except MykeibaDBError as e:
        return ChakudoResult(success=False, error=str(e))
