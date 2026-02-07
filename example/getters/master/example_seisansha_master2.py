"""SEISANSHA_MASTER2テーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "seisansha_master2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 生産者指定
    seisansha_code = "39312600"  # 社台ファーム
    df = getter.get_seisansha_master2(seisansha_code=seisansha_code)
    path = os.path.join(output_dir, f"seisansha_master2_{seisansha_code}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
