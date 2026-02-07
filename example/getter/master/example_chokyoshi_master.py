"""CHOKYOSHI_MASTERテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "chokyoshi_master"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 調教師指定
    chokyoshi_code = "01126"  # 木村哲也
    df = getter.get_chokyoshi_master(chokyoshi_code=chokyoshi_code)
    path = os.path.join(output_dir, f"chokyoshi_master_{chokyoshi_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定（調教師免許交付年月日）
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    df = getter.get_chokyoshi_master(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"chokyoshi_master_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
