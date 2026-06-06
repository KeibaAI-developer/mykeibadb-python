# mykeibadb-python select_entries CTE 最適化仕様書

## 概要

`mykeibadb-python` の `analytics/entry_select.py` が `history`/`fixed` kind の `group_label` 算出に使用している相関サブクエリを CTE 方式（target_horses → horse_hist → attr_agg → JOIN）に置き換え、`select_entries` のパフォーマンスを改善する。リポジトリは `mykeibadb-python`、パッケージは `mykeibadb`。

---

## 目的・背景

PR#41〜#44 の3フェーズ設計移行時、PR#38 で実施された CTE 最適化が失われ、`history`/`fixed` kind の各 metric が47〜264秒かかるようになった（全体の約99%）。原因は `_build_fixed_group_label_expr` が各 CASE WHEN item ごとに同一の相関サブクエリを展開すること（SubPlan が4〜5本重複、cost 約149,527/本、177行 × N本分）。詳細は `doc/DEV_HISTORY/PERFORMANCE.md` を参照。

目標: `history`/`fixed` kind の実行時間を現状47〜264秒 → 1秒未満にする。

---

## ディレクトリ構成

```
mykeibadb-python/
└── mykeibadb/
    └── analytics/
        └── entry_select.py  # _build_group_label_expr の history/fixed ブランチを CTE 方式に変更
```

---

## 依存ライブラリ

新規追加なし。

---

## `entry_select.py` 設計

### 変更スコープ

`select_entries` の呼び出し側インターフェース、フェーズ2/3（`tally_chakujun`/`compute_chakudo`）、`race_col`/`subject`/`boolean_multi` kind の処理は変更しない。

### SQL 構造変更（history / fixed kind 時）

**変更前:** 外側クエリの SELECT 句に相関サブクエリを展開  
**変更後:** CTE 4段構造 + JOIN

新しいヘルパー関数シグネチャ:

```python
def _build_hist_cte_group_label(
    source: AttrSource,
    rows: RowsDef | None,
    params: list[Any],
) -> tuple[list[str], list[Any], str]:
    """history/fixed kind の CTE SQL リストと group_label 式を返す.

    Args:
        source (AttrSource): 属性算出方法
        rows (RowsDef | None): fixed kind のビン定義。history kind は None。
        params (list[Any]): 外側クエリ用パラメータ（末尾にCTEパラメータが追加される）

    Returns:
        tuple[list[str], list[Any], str]:
            - cte_sqls: WITH 節に追加する CTE 文字列のリスト
            - cte_params: CTE 用パラメータ（params に追記済み）
            - group_label_expr: SELECT 句に使う group_label 式
    """
```

### CTE 構造

```
WITH target_horses AS MATERIALIZED (
    -- 外側 condition + filters で絞り込んだエントリ一覧
    SELECT DISTINCT
        u.ketto_toroku_bango,
        u.race_code,
        r.kaisai_nen,
        r.kaisai_gappi,
        u.kishu_code          -- jockey_continuity 用
    FROM umagoto_race_joho u
    JOIN race_shosai r ON u.race_code = r.race_code
    WHERE <outer_condition>
),
horse_hist AS (
    -- 対象馬の全履歴（対象レース日より前）
    SELECT
        th.ketto_toroku_bango,
        th.race_code              AS target_race_code,
        th.kishu_code             AS target_kishu_code,
        u2.kishu_code,
        r2.keibajo_code,
        r2.kaisai_nen,
        r2.kaisai_gappi,
        u2.kakutei_chakujun,
        TRIM(r2.kyosomei_hondai)  AS kyosomei_hondai,
        r2.grade_code,
        TRIM(r2.kyori)::INTEGER   AS kyori_int
    FROM target_horses th
    JOIN umagoto_race_joho u2 ON u2.ketto_toroku_bango = th.ketto_toroku_bango
    JOIN race_shosai r2 ON u2.race_code = r2.race_code
    WHERE (r2.kaisai_nen || r2.kaisai_gappi) < (th.kaisai_nen || th.kaisai_gappi)
),
attr_agg AS (
    -- source.type に応じた集計（ketto_toroku_bango, target_race_code, attr_val）
    ...
)
SELECT u.ketto_toroku_bango, u.race_code, u.umaban,
    <group_label_from_attr_agg> AS group_label
FROM umagoto_race_joho u
JOIN race_shosai r ON u.race_code = r.race_code
LEFT JOIN attr_agg
    ON  attr_agg.ketto_toroku_bango = u.ketto_toroku_bango
    AND attr_agg.target_race_code   = u.race_code
WHERE <outer_condition>
```

`target_horses` の `<outer_condition>` と最終 SELECT の `<outer_condition>` は同一（RaceCondition + EntryFilter）。

### attr_agg ロジック（source.type 別）

| source.type | attr_val | horse_hist フィルタ条件 |
|---|---|---|
| `career_count` | `COUNT(*)` | 有効着順（`kakutei_chakujun ~ '^[0-9]{2}$' AND kakutei_chakujun != '00'`） |
| `past_finish_count` | `COUNT(*) FILTER (WHERE CAST(kakutei_chakujun AS INT) BETWEEN 1 AND top_n [AND grade/keibajo/kyori条件])` | 有効着順 |
| `debut_venue` | デビュー戦の `keibajo_code`（kaisai_nen/kaisai_gappi ASC の最初の行） | 有効着順 |
| `prev_race_name` | 前走の `TRIM(kyosomei_hondai)`（kaisai_nen/kaisai_gappi DESC の最初の行） | `kyosomei_hondai != ''` |
| `jockey_continuity` | 前走騎手コードと今回騎手コードの比較結果（`'継続'`/`'乗り戻り'`/`'テン乗り'`） | 有効着順 |

`debut_venue` / `prev_race_name` は `DISTINCT ON (ketto_toroku_bango, target_race_code)` を使い、ORDER BY で先頭1行を取得する。

### fixed kind の group_label 式

`attr_agg.attr_val` に対する CASE WHEN 式（相関サブクエリの重複なし）:

```sql
CASE
    WHEN attr_agg.attr_val::INTEGER BETWEEN %s AND %s THEN %s
    WHEN attr_agg.attr_val::INTEGER = %s THEN %s
    ...
    ELSE NULL
END
```

### history kind の group_label 式

`attr_agg.attr_val::TEXT` をそのまま使用。

### 変更しない処理

- `race_col` kind: `group_by.column::TEXT` を SELECT 句に直接使用
- `subject` kind: JOIN + `mapping.group_col`
- `sire_condition_finisher` source.type: 実行時間 <1秒のため現状維持

---

## エラーハンドリング方針

- フォールバック処理は実装しない。失敗時は例外を発生させる
- 未対応の `source.type` は `ValueError` を発生させる（現状維持）
- `attr_agg` の結果が NULL の場合（キャリアなし等）は group_label が NULL になり `Entry` に含まれない（現状と同一挙動）

---

## 実装順序

1. `mykeibadb/analytics/entry_select.py` — `_build_target_horses_cte` 関数を追加（target_horses CTE の SQL 文字列生成）
2. `mykeibadb/analytics/entry_select.py` — `_build_horse_hist_cte` 関数を追加（horse_hist CTE の SQL 文字列生成）
3. `mykeibadb/analytics/entry_select.py` — `_build_attr_agg_cte` 関数を source.type 別に実装（career_count / past_finish_count / debut_venue / prev_race_name / jockey_continuity）
4. `mykeibadb/analytics/entry_select.py` — `_build_hist_cte_group_label` 関数を追加（CTE 一式 + group_label 式を返す）
5. `mykeibadb/analytics/entry_select.py` — `_build_group_label_expr` の `history`/`fixed` ブランチを `_build_hist_cte_group_label` 呼び出しに変更し、`select_entries` の SQL 組み立てに CTE 統合処理を追加
6. `mykeibadb/analytics/entry_select.py` — 不要になった `_build_attr_value_expr` / `_build_fixed_group_label_expr` 等の関数を削除
7. `test/unit/mykeibadb/analytics/test_entry_select.py` — 既存テスト修正 + CTE 生成の正常系テスト追加
