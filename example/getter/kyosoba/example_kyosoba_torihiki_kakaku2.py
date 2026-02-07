"""KYOSOBA_TORIHIKI_KAKAKU2テーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import KyosobaGetter


def main() -> None:
    """メイン関数."""
    getter = KyosobaGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "kyosoba_torihiki_kakaku2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 馬指定
    ketto_toroku_bango = "2021105817"  # ダノンエアズロック
    df = getter.get_kyosoba_torihiki_kakaku2(ketto_toroku_bango=ketto_toroku_bango)
    path = os.path.join(output_dir, f"kyosoba_torihiki_kakaku2_{ketto_toroku_bango}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
