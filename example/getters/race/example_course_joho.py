"""COURSE_JOHOテーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import RaceGetter


def main() -> None:
    """メイン関数."""
    getter = RaceGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "course_joho"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 競馬場指定
    keibajo_code = "06"  # 中山
    df = getter.get_course_joho(keibajo_code=keibajo_code)
    path = os.path.join(output_dir, f"course_joho_keibajo_{keibajo_code}.csv")
    df.to_csv(path, index=False)
    # 距離指定
    kyori = [2500, 1600]  # 2500m, 1600m
    df = getter.get_course_joho(kyori=kyori)
    path = os.path.join(output_dir, f"course_joho_{kyori}m.csv")
    df.to_csv(path, index=False)
    # トラックコード指定
    track_code = "10"  # 新潟1000直
    df = getter.get_course_joho(track_code=track_code)
    path = os.path.join(output_dir, f"course_joho_track_{track_code}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
