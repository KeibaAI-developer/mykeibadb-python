"""HYOSU6テーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import HyosuGetter


def main() -> None:
    """メイン関数."""
    getter = HyosuGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "hyosu6"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # レース指定
    race_code = "2026013105010101"
    df = getter.get_hyosu6(race_code=race_code)
    path = os.path.join(output_dir, f"hyosu6_{race_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定
    start_date = date(2026, 1, 31)
    end_date = date(2026, 1, 31)
    df = getter.get_hyosu6(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"hyosu6_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
