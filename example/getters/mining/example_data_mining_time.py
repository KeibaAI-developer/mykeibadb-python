"""DATA_MINING_TIMEテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import MiningGetter


def main() -> None:
    """メイン関数."""
    getter = MiningGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "data_mining_time"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # レース指定
    race_code = "2025122806050811"  # 有馬記念
    df = getter.get_data_mining_time(race_code=race_code)
    path = os.path.join(output_dir, f"data_mining_time_{race_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定
    start_date = date(2025, 12, 1)
    end_date = date(2025, 12, 31)
    df = getter.get_data_mining_time(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"data_mining_time_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
