"""TOKUBETSU_TOROKUBAGOTO_JOHOテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import RaceGetter


def main() -> None:
    """メイン関数."""
    getter = RaceGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "tokubetsu_torokubagoto_joho"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # レース指定
    race_code = "2025122806050811"
    df = getter.get_tokubetsu_torokubagoto_joho(race_code=race_code)
    path = os.path.join(output_dir, f"tokubetsu_torokubagoto_joho_{race_code}.csv")
    df.to_csv(path, index=False)

    # 期間指定
    start_date = date(2026, 1, 1)
    end_date = date(2026, 1, 31)
    df = getter.get_tokubetsu_torokubagoto_joho(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"tokubetsu_torokubagoto_joho_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
