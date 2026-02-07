"""KEITO_JOHO2テーブル取得のサンプルスクリプト."""

import os
from pathlib import Path

from mykeibadb.getters import KyosobaGetter


def main() -> None:
    """メイン関数."""
    getter = KyosobaGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "keito_joho2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 系統ID指定
    keito_id = "0101080201010201"  # サンデーサイレンス系
    df = getter.get_keito_joho2(keito_id=keito_id)
    path = os.path.join(output_dir, f"keito_joho2_{keito_id}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
