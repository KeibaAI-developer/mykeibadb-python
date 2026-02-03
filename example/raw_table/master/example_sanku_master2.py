"""SANKU_MASTER2テーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "sanku_master2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬指定
    ketto_toroku_bango = "2002100816"  # ディープインパクト
    df = getter.get_sanku_master2(ketto_toroku_bango=ketto_toroku_bango)
    path = os.path.join(output_dir, f"sanku_master2_{ketto_toroku_bango}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
