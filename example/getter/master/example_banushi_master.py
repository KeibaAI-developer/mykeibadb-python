"""BANUSHI_MASTERテーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "banushi_master"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬主指定
    banushi_code = "232031"  # 藤田晋
    df = getter.get_banushi_master(banushi_code=banushi_code)
    path = os.path.join(output_dir, f"banushi_master_{banushi_code}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
