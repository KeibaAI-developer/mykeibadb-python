# mykeibadb.analytics モジュール 実装計画書

## PR一覧

| PR | タイトル | 依存 | 状態 |
|----|---------|------|------|
| PR#01 | analytics 基盤（_models / _cte_helpers） | なし | ✅ |
| PR#02 | analyze_chakudo 実装 | PR#01 | ✅ |
| PR#03 | analyze_entry_attr_chakudo 実装 | PR#01, PR#02 | ✅ |
| PR#04 | 調教分析関数 + 公開API完成 | PR#01〜PR#03 | - |

---

## 全PR共通ルール

### ブランチ運用

- 起点ブランチは `develop`
- 各PRは `develop` からブランチを切り、`develop` にマージする

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

## PR#01: analytics 基盤（_models / _cte_helpers）

- [x] PR完了

**ブランチ名:** `feature/mykeibadb-analytics-base`
**起点・マージ先:** `develop`

**概要:** `mykeibadb.analytics` モジュールの基盤となるデータモデルとCTEヘルパーを実装する。後続PR全ての依存元。

**実装ファイル:**

- `mykeibadb/analytics/__init__.py` — モジュール骨格（エクスポートは後続PRで追記）
- `mykeibadb/analytics/_models.py` — ChakudoRow / ChakudoResult / AttrSource / RowsDef / EntryAttrDef
- `mykeibadb/analytics/_cte_helpers.py` — build_course_week_cte / build_payout_ctes
- `test/unit/mykeibadb/analytics/test_cte_helpers.py` — CTEヘルパーのテスト

**作業内容:**

- [x] `mykeibadb/analytics/` ディレクトリ作成
- [x] `_models.py` 実装（ChakudoRow, ChakudoResult, AttrSource, RowsDef, EntryAttrDef）
- [x] `_cte_helpers.py` 実装（build_course_week_cte, build_payout_ctes）
- [x] `__init__.py` 骨格作成
- [x] `test_cte_helpers.py` 実装
- [x] 静的解析（isort・flake8・mypy）
- [x] セルフレビュー（code-review）

**完了条件:**

- [x] `pytest test/unit/mykeibadb/analytics/test_cte_helpers.py -v` が全件パス
- [x] 静的解析エラーなし

---

## PR#02: analyze_chakudo 実装

- [x] PR完了

**ブランチ名:** `feature/mykeibadb-analytics-chakudo`
**起点・マージ先:** `develop`

**概要:** グループ別着度数・勝率・回収率を集計する `analyze_chakudo` を実装する。`mykeibadb-mcp-server` の `analyze_race_chakudo` を汎用化して移植。

**実装ファイル:**

- `mykeibadb/analytics/chakudo.py` — analyze_chakudo
- `mykeibadb/analytics/__init__.py` — analyze_chakudo / ChakudoRow / ChakudoResult のエクスポート追加
- `test/unit/mykeibadb/analytics/test_chakudo.py` — テスト

**作業内容:**

- [x] `chakudo.py` 実装
  - `kakutei_chakujun ~ '^[0-9]{2}$'` で取消除外
  - `haraimodoshi` テーブルJOINで回収率計算
  - `course_kubun` + `week_in_course` 両方指定時に `build_course_week_cte` でCTE生成
  - 片方のみ指定時は `ValueError` を raise
- [x] `__init__.py` にエクスポート追加
- [x] `test_chakudo.py` 実装（正常系・準正常系）
- [x] 静的解析（isort・flake8・mypy）
- [x] セルフレビュー（code-review）

**完了条件:**

- [x] `pytest test/unit/mykeibadb/analytics/test_chakudo.py -v` が全件パス
- [x] 静的解析エラーなし

---

## PR#03: analyze_entry_attr_chakudo 実装

- [x] PR完了

**ブランチ名:** `feature/mykeibadb-analytics-entry-attr`
**起点・マージ先:** `develop`

**概要:** 出走馬属性（過去実績・前走情報等）でグループ分けした着度数・回収率を集計する `analyze_entry_attr_chakudo` を実装する。`source.type` の4種すべてに対応。

**実装ファイル:**

- `mykeibadb/analytics/entry_attr.py` — analyze_entry_attr_chakudo
- `mykeibadb/analytics/__init__.py` — analyze_entry_attr_chakudo / AttrSource / EntryAttrDef のエクスポート追加
- `test/unit/mykeibadb/analytics/test_entry_attr.py` — テスト

**作業内容:**

- [x] `entry_attr.py` 実装
  - `attr_def` が `dict` の場合は `EntryAttrDef.from_dict` で変換
  - `source.type` 対応:
    - `"past_finish_count"`: `chakujun <= top_n` の出走回数集計（grade_codes / keibajo_code / kyori フィルタ）
    - `"career_count"`: 全キャリア戦数
    - `"prev_race_name"`: 直前レース名をサブクエリで取得
    - `"debut_venue"`: 初出走の競馬場コードをサブクエリで取得
  - 未対応 `type` 指定時は `ValueError` を raise
- [x] `__init__.py` にエクスポート追加
- [x] `test_entry_attr.py` 実装（source.type 4種の正常系・準正常系）
- [x] 静的解析（isort・flake8・mypy）
- [x] セルフレビュー（code-review）

**完了条件:**

- [x] `pytest test/unit/mykeibadb/analytics/test_entry_attr.py -v` が全件パス
- [x] `source.type` 全4種のテストが存在する
- [x] 静的解析エラーなし

---

## PR#04: 調教分析関数 + 公開API完成

- [ ] PR完了

**ブランチ名:** `feature/mykeibadb-analytics-chokyo`
**起点・マージ先:** `develop`

**概要:** 調教分析関数 `get_uma_chokyo` / `analyze_chokyo_debut_seiseki` を実装し、`__init__.py` を全エクスポートで完成させる。

**実装ファイル:**

- `mykeibadb/analytics/chokyo.py` — get_uma_chokyo / analyze_chokyo_debut_seiseki
- `mykeibadb/analytics/__init__.py` — get_uma_chokyo / analyze_chokyo_debut_seiseki のエクスポート追加（公開API完成）
- `test/unit/mykeibadb/analytics/test_chokyo.py` — テスト

**作業内容:**

- [ ] `chokyo.py` 実装（get_uma_chokyo, analyze_chokyo_debut_seiseki）
- [ ] `__init__.py` を SPEC.md の公開API定義通りに完成させる
- [ ] `test_chokyo.py` 実装（正常系・準正常系）
- [ ] 静的解析（isort・flake8・mypy）
- [ ] セルフレビュー（code-review）

**完了条件:**

- [ ] `pytest test/unit/mykeibadb/analytics/ -v` が全件パス
- [ ] `from mykeibadb.analytics import analyze_chakudo, analyze_entry_attr_chakudo, get_uma_chokyo, analyze_chokyo_debut_seiseki` が正常にimportできる
- [ ] 静的解析エラーなし
