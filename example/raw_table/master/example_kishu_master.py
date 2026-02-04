"""KISHU_MASTERテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "kishu_master"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 騎手指定
    kishu_code = "00666"  # 武豊
    df = getter.get_kishu_master(kishu_code=kishu_code)
    path = os.path.join(output_dir, f"kishu_master_{kishu_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定（騎手免許交付年月日基準）
    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)
    df = getter.get_kishu_master(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"kishu_master_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
