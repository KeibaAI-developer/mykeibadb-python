"""ODDS2_UMAREN_JIKEIRETSUテーブル取得のサンプルスクリプト."""

import os
from datetime import date
from pathlib import Path

from mykeibadb.getters import OddsGetter


def main() -> None:
    """メイン関数."""
    getter = OddsGetter()
    script_dir = Path(__file__).parent
    output_dir = Path(os.path.join(script_dir, "odds2_umaren_jikeiretsu"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # レース指定
    race_code = "2025122806050811"
    df = getter.get_odds2_umaren_jikeiretsu(race_code=race_code)
    path = os.path.join(output_dir, f"odds2_umaren_jikeiretsu_{race_code}.csv")
    df.to_csv(path, index=False)
    # 期間指定
    start_date = date(2025, 12, 28)
    end_date = date(2025, 12, 28)
    df = getter.get_odds2_umaren_jikeiretsu(start_date=start_date, end_date=end_date)
    path = os.path.join(output_dir, f"odds2_umaren_jikeiretsu_{start_date}_{end_date}.csv")
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
