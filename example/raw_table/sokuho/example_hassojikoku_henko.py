"""HASSOJIKOKU_HENKOテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import SokuhoGetter


def main() -> None:
    """メイン関数."""
    getter = SokuhoGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "hassojikoku_henko"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # レース指定
    race_code = "2025122806050811"  # 有馬記念
    df = getter.get_hassojikoku_henko(race_code=race_code)
    path = os.path.join(output_dir, f"hassojikoku_henko_{race_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定
    start_date = date(2026, 2, 1)
    end_date = date(2026, 2, 28)
    df = getter.get_hassojikoku_henko(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"hassojikoku_henko_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
