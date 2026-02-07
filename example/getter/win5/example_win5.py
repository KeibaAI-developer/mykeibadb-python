"""WIN5テーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import Win5Getter


def main() -> None:
    """メイン関数."""
    getter = Win5Getter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "win5"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 期間指定
    start_date = date(2026, 2, 1)
    end_date = date(2026, 2, 28)
    df = getter.get_win5(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"win5_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
