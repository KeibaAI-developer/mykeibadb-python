"""HANSHOKUBA_MASTER2テーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "hanshokuba_master2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 繁殖馬指定
    hanshoku_toroku_bango = "1220052840"  # シーザリオ
    df = getter.get_hanshokuba_master2(hanshoku_toroku_bango=hanshoku_toroku_bango)
    path = os.path.join(output_dir, f"hanshokuba_master2_{hanshoku_toroku_bango}.csv")
    df.to_csv(path, index=False)
    # 期間指定（生年月日）
    start_date = date(2015, 1, 1)
    end_date = date(2015, 12, 31)
    df = getter.get_hanshokuba_master2(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"hanshokuba_master2_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
