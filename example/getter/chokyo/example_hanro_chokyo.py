"""HANRO_CHOKYOテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import ChokyoGetter


def main() -> None:
    """メイン関数."""
    getter = ChokyoGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "hanro_chokyo"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬指定
    ketto_toroku_bango = "2022105081"
    df = getter.get_hanro_chokyo(ketto_toroku_bango=ketto_toroku_bango)
    path = os.path.join(output_dir, f"hanro_chokyo_{ketto_toroku_bango}.csv")
    df.to_csv(path, index=False)

    # トレセン区分指定
    tracen_kubun = "1"
    df = getter.get_hanro_chokyo(tracen_kubun=tracen_kubun)
    path = os.path.join(output_dir, f"hanro_chokyo_{tracen_kubun}.csv")
    df.to_csv(path, index=False)

    # 期間指定
    start_date = date(2025, 12, 20)
    end_date = date(2025, 12, 28)
    df = getter.get_hanro_chokyo(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"hanro_chokyo_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
