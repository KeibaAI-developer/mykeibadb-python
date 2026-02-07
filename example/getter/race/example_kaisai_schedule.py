"""KAISAI_SCHEDULEテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import RaceGetter


def main() -> None:
    """メイン関数."""
    getter = RaceGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "kaisai_schedule"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 開催コード指定
    kaisai_code = "20251228060508"
    df = getter.get_kaisai_schedule(kaisai_code=kaisai_code)
    path = os.path.join(output_dir, f"kaisai_schedule_{kaisai_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定
    start_date = date(2025, 12, 1)
    end_date = date(2025, 12, 31)
    df = getter.get_kaisai_schedule(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"kaisai_schedule_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
