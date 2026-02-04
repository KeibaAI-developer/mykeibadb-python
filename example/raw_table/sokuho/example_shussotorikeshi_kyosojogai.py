"""SHUSSOTORIKESHI_KYOSOJOGAIテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import SokuhoGetter


def main() -> None:
    """メイン関数."""
    getter = SokuhoGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "shussotorikeshi_kyosojogai"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # 開催指定
    kaisai_code = "20251228060508"
    df = getter.get_shussotorikeshi_kyosojogai(kaisai_code=kaisai_code)
    path = os.path.join(output_dir, f"shussotorikeshi_kyosojogai_{kaisai_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定
    start_date = date(2026, 1, 1)
    end_date = date(2026, 1, 31)
    df = getter.get_shussotorikeshi_kyosojogai(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"shussotorikeshi_kyosojogai_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)
    # 馬番指定
    umaban = 9
    df = getter.get_shussotorikeshi_kyosojogai(umaban=umaban)
    path = os.path.join(output_dir, f"shussotorikeshi_kyosojogai_umaban{umaban}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
