"""RECORD_MASTERテーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import MasterGetter


def main() -> None:
    """メイン関数."""
    getter = MasterGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "record_master"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 競馬場指定
    keibajo_code = "06"
    df = getter.get_record_master(keibajo_code=keibajo_code)
    path = os.path.join(output_dir, f"record_master_keibajo_{keibajo_code}.csv")
    df.to_csv(path, index=False)
    # 距離指定
    kyori = 2500
    df = getter.get_record_master(kyori=kyori)
    path = os.path.join(output_dir, f"record_master_{kyori}m.csv")
    df.to_csv(path, index=False)
    # トラックコード指定
    track_code = "10"
    df = getter.get_record_master(track_code=track_code)
    path = os.path.join(output_dir, f"record_master_track_{track_code}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
