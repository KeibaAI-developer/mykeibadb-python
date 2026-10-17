"""着度数集計フェーズ3: 着度数・回収率計算モジュール."""

from mykeibadb.analytics._models import ChakudoResult, ChakudoRow, ChakudoTally


def compute_chakudo(tally: ChakudoTally) -> ChakudoResult:
    """ChakudoTally から ChakudoResult（勝率・複勝率・回収率）を計算する.

    DB接続不要の純計算。total=0 のグループは各率を 0.0 とする。

    Args:
        tally (ChakudoTally): フェーズ2で得られた着順集計リスト

    Returns:
        ChakudoResult: グループ別の着度数・回収率集計結果
    """
    rows: list[ChakudoRow] = []
    for gt in tally:
        if gt.total == 0:
            rows.append(
                ChakudoRow(
                    group=gt.group,
                    total=0,
                    wins=0,
                    second=0,
                    third=0,
                    chakugai=0,
                    win_rate=0.0,
                    fukusho_rate=0.0,
                    tansho_kaishuu=0.0,
                    fukusho_kaishuu=0.0,
                )
            )
        else:
            win_rate = round(gt.wins * 100.0 / gt.total, 1)
            fukusho_rate = round((gt.wins + gt.second + gt.third) * 100.0 / gt.total, 1)
            tansho_kaishuu = round(gt.tansho_payout_sum * 1.0 / gt.total, 1)
            fukusho_kaishuu = round(gt.fukusho_payout_sum * 1.0 / gt.total, 1)
            rows.append(
                ChakudoRow(
                    group=gt.group,
                    total=gt.total,
                    wins=gt.wins,
                    second=gt.second,
                    third=gt.third,
                    chakugai=gt.chakugai,
                    win_rate=win_rate,
                    fukusho_rate=fukusho_rate,
                    tansho_kaishuu=tansho_kaishuu,
                    fukusho_kaishuu=fukusho_kaishuu,
                )
            )
    return ChakudoResult(success=True, rows=rows)
