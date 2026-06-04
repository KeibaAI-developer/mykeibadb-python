# レビュー: feature/mykeibadb-analytics-entry-attr

## 概要

- **対象**: develop → feature/mykeibadb-analytics-entry-attr
- **レビュー日**: 2026-06-04
- **レビュー対象ファイル数**: 3ファイル（entry_attr.py / __init__.py / test_entry_attr.py）

## 指摘事項

### 1. ChakudoRow 変換ロジックの重複

| 項目 | 内容 |
|------|------|
| 重要度 | Warning |
| 場所 | `mykeibadb/analytics/entry_attr.py` L143-163、`mykeibadb/analytics/chakudo.py` L141-162 |

**指摘内容**

DataFrameの行を `ChakudoRow` に変換する処理が `chakudo.py` と `entry_attr.py` で完全に同一。
PR#04 の `chokyo.py` でも同様のコードが必要になる可能性が高く、このままでは3箇所に同じコードが存在することになる。DRY原則違反。

**修正案**

`_cte_helpers.py` または `_models.py` にプライベートヘルパー関数として切り出す。

```python
# mykeibadb/analytics/_cte_helpers.py などに追加
def _row_from_series(row: "pd.Series[object]") -> ChakudoRow:
    """DataFrameの1行からChakudoRowを生成する."""
    return ChakudoRow(
        group=str(row["grp"]),
        total=int(row["total"]),
        wins=int(row["wins"]),
        second=int(row["second"]),
        third=int(row["third"]),
        chakugai=int(row["chakugai"]),
        win_rate=float(row["win_rate"]) if pd.notna(row["win_rate"]) else 0.0,
        fukusho_rate=float(row["fukusho_rate"]) if pd.notna(row["fukusho_rate"]) else 0.0,
        tansho_kaishuu=float(row["tansho_kaishuu"]) if pd.notna(row["tansho_kaishuu"]) else 0.0,
        fukusho_kaishuu=float(row["fukusho_kaishuu"]) if pd.notna(row["fukusho_kaishuu"]) else 0.0,
    )
```

## まとめ

| 重要度 | 件数 |
|--------|------|
| Critical | 0 |
| Warning | 1 |
| Suggestion | 0 |

指摘1件（Warning）。修正して PR を作成すること。
