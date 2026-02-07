"""SHOBUFUKUテーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import OthersGetter


def main() -> None:
    """メイン関数."""
    getter = OthersGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "shobufuku"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬主コード指定
    banushi_code = "232031"  # 藤田晋
    df = getter.get_shobufuku(banushi_code=banushi_code)
    path = os.path.join(output_dir, f"shobufuku_{banushi_code}.csv")
    df.to_csv(path, index=False)
    # 全件取得
    df = getter.get_shobufuku()
    path = os.path.join(output_dir, "shobufuku_all.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
