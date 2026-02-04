"""KYOSOBA_MASTER2テーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "kyosoba_master2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬指定
    ketto_toroku_bango = "2022105081"  # ミュージアムマイル
    df = getter.get_kyosoba_master2(ketto_toroku_bango=ketto_toroku_bango)
    path = os.path.join(output_dir, f"kyosoba_master2_{ketto_toroku_bango}.csv")
    df.to_csv(path, index=False)
    # 期間指定（生年月日）
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    df = getter.get_kyosoba_master2(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"kyosoba_master2_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
