"""SHUSSOBETSU_SEISANSHA2テーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import ShussobetsuGetter


def main() -> None:
    """メイン関数."""
    getter = ShussobetsuGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "shussobetsu_seisansha2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # レース指定
    race_code = "2025122806050811"
    df = getter.get_shussobetsu_seisansha2(race_code=race_code)
    path = os.path.join(output_dir, f"shussobetsu_seisansha2_{race_code}.csv")
    df.to_csv(path, index=False)

    # 馬指定
    ketto_toroku_bango = "2022105081"
    df = getter.get_shussobetsu_seisansha2(ketto_toroku_bango=ketto_toroku_bango)
    path = os.path.join(output_dir, f"shussobetsu_seisansha2_{ketto_toroku_bango}.csv")
    df.to_csv(path, index=False)

    # 期間指定
    start_date = date(2025, 12, 28)
    end_date = date(2025, 12, 28)
    df = getter.get_shussobetsu_seisansha2(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"shussobetsu_seisansha2_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
