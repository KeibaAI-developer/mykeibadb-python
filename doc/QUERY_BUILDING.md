# クエリの組み立て

`TableAccessor` がフィルタ条件からWHERE句を組み立てる際の規則を説明します。

## 列の型による `TRIM()` の分岐

フィルタ列を `TRIM()` で包むかどうかは、**列の型**で決まります。

| 列の型 | WHERE句 |
|---|---|
| `character`（固定長文字列、bpchar） | `col = %s` / `col IN (...)` |
| それ以外 | `TRIM(col) = %s` / `TRIM(col) IN (...)` |

### なぜ分岐するのか

mykeibadbのコード系カラム（`RACE_CODE`・`KETTO_TOROKU_BANGO` など）は固定長文字列で、値が短い場合は空白で埋められます。かつては一致させるために全てのフィルタ列を `TRIM()` で包んでいました。

しかし**列を関数で包むと、その列のインデックスが使われなくなります**。

```
-- TRIMあり
Gather  (cost=1000.00..40886.55 rows=2173) (actual time=24.735..56.128 rows=2)
  ->  Parallel Seq Scan on race_shosai  (actual time=22.617..40.158 rows=0.67 loops=3)
        Filter: (TRIM(BOTH FROM race_code) = ANY (...))
        Rows Removed by Filter: 80597
Execution Time: 56.163 ms

-- TRIMなし
Index Scan using race_shosai_pkey on race_shosai  (actual time=0.024..0.076 rows=24)
  Index Cond: (race_code = ANY (...))
Execution Time: 0.089 ms
```

そして固定長文字列では `TRIM()` は不要です。**PostgreSQLの `character(n)` の比較は末尾空白を無視する**ため、`race_code = '2025122806050811'` は末尾が空白で埋められた値にも一致します。

### 先頭空白について

`TRIM()` は先頭と末尾の**両方**の空白を除去するのに対し、`character(n)` の比較が無視するのは**末尾空白だけ**です。したがって先頭空白を含む値は、`TRIM()` を外すと一致しなくなります。

getterがフィルタへ渡すカラム（`RACE_CODE`・`KETTO_TOROKU_BANGO`・`KISHU_CODE` など14種）が固定長文字列である組（テーブル×カラム）をすべて調べ、**先頭空白を持つ行が存在しないこと**を確認しています。現在の対象は151件です。

この検証は `test/integration/test_trim_removal_equivalence.py::test_no_filter_column_has_leading_space` で行います。対象は `information_schema` から動的に集めるため、テーブルやカラムが増えても検証範囲が自動で広がります。全件を走査するため実行に約2分かかり、`slow` マーカーを付けています。

利用側は `filters` へ任意のカラムを渡せます。上記14種以外のカラムをフィルタに使う場合は、そのカラムに先頭空白がないことを別途確認してください。

### 可変長文字列を対象外にした理由

`character varying` / `text` に末尾空白が入っている可能性は否定できません。`TRIM()` を外すと一致しなくなる恐れがあるため、従来どおり `TRIM()` で包みます。

## 列の型の解決

列の型は `ColumnTypeResolver` が `information_schema.columns` から取得します。

- 問い合わせは**テーブル単位で1回**だけ行い、プロセス内にキャッシュします
- テーブルは `to_regclass` で `search_path` を通して解決します。データ取得クエリがスキーマ非修飾（`SELECT * FROM {table_name}`）で発行されるため、同じテーブルの型を見るためです
- 型を判定できない場合（テーブルやカラムが存在しない、問い合わせに失敗した）は `TRIM()` で包みます。速度は落ちますが結果は正しくなります

キャッシュはテーブル名をキーとし、スキーマは含めません。本ライブラリは `search_path` を設定せず、接続プールは単一のユーザーで接続するため、解決結果はプロセス内で一定であることを前提とします。

## 行の並び

いずれのクエリにも `ORDER BY` はなく、**行の並びは保証しません**。

`TRIM()` の有無で実行計画が変わるため、リスト値フィルタでは行の並びが変わります（全表スキャンの物理順からインデックス順になります）。並びが必要な場合は呼び出し側でソートしてください。
