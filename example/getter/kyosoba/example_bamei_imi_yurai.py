"""BAMEI_IMI_YURAIテーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import KyosobaGetter


def main() -> None:
    """メイン関数."""
    getter = KyosobaGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "bamei_imi_yurai"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬指定
    ketto_toroku_bango = "2022105081"  # ミュージアムマイル
    df = getter.get_bamei_imi_yurai(ketto_toroku_bango=ketto_toroku_bango)
    path = os.path.join(output_dir, f"bamei_imi_yurai_{ketto_toroku_bango}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
