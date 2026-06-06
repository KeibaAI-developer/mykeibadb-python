# mykeibadb-python select_entries CTE 最適化 実装計画書

## PR一覧

| PR | タイトル | 依存 | 状態 |
|----|---------|------|------|
| PR#01 | select_entries の history/fixed kind を CTE 方式に書き換え | なし | - |

---

## ブランチ戦略

- **起点ブランチ:** `develop`
- **マージ先:** `develop`

---

## 全PR共通ルール

Python実装を含む全PRで以下を実施する。

### コーディング規約

- `python-coding-rule` スキルに従う
- `pytest-coding-rule` スキルに従う（テストコードがある場合）

### 静的解析（実装後に必ず実行）

`__init__.py` を含む全対象ファイルに対して実施し、エラーがないことを確認する。

1. `run-isort-check` — importの並び順チェック
2. `run-flake8` — スタイル・文法チェック
3. `run-mypy` — 型チェック

### セルフレビュー（PR作成前に必ず実行）

`code-review` スキルを使いセルフレビューを行い、指摘事項があれば修正してからPRを作成する。

---

## PR#01: select_entries の history/fixed kind を CTE 方式に書き換え

- [ ] PR完了

**ブランチ名:** `fix/select-entries-cte` （起点: `develop` / マージ先: `develop`）

**概要:** `entry_select.py` の `history`/`fixed` kind における相関サブクエリを CTE（target_horses → horse_hist → attr_agg → JOIN）方式に置き換え、select_entries のパフォーマンスを47〜264秒/metric → 1秒未満にする。

**実装ファイル:**

- `mykeibadb/analytics/entry_select.py` — CTE 方式への書き換え
- `test/unit/mykeibadb/analytics/test_entry_select.py` — 既存テスト修正 + CTE 生成テスト追加

**作業内容:**

- [ ] `_build_target_horses_cte` 関数を追加（target_horses CTE の SQL 文字列生成。condition/filters 条件を受け取り MATERIALIZED CTE を返す）
- [ ] `_build_horse_hist_cte` 関数を追加（horse_hist CTE の SQL 文字列生成。target_horses の各馬の全履歴を一括取得）
- [ ] `_build_attr_agg_cte` 関数を追加（source.type 別の attr_agg CTE 生成。career_count / past_finish_count / debut_venue / prev_race_name / jockey_continuity を実装）
- [ ] `_build_hist_cte_group_label` 関数を追加（CTE SQL リスト + group_label 式を返す統合ヘルパー）
- [ ] `_build_group_label_expr` の `history`/`fixed` ブランチを `_build_hist_cte_group_label` 呼び出しに変更
- [ ] `select_entries` の SQL 組み立てに CTE 統合処理を追加（cte_parts に history/fixed 用 CTE を追加 + LEFT JOIN attr_agg を追加）
- [ ] 不要になった `_build_attr_value_expr` / `_build_fixed_group_label_expr` / `_HIST_CORR_PARTS` 等を削除
- [ ] 既存テスト修正 + CTE 生成の正常系テスト追加
- [ ] 静的解析（isort・flake8・mypy）
- [ ] セルフレビュー（code-review）

**完了条件:**

- [ ] `python -c "from mykeibadb.analytics.entry_select import select_entries"` がエラーなく通る
- [ ] pytest が全件パスする
- [ ] `/tmp/perf_probe.py` を使った計測で `history`/`fixed` kind の全 metric が10秒未満になる（目標1秒未満）
- [ ] 静的解析（isort・flake8・mypy）エラーなし
