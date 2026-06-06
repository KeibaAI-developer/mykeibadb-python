# analytics パフォーマンス劣化調査

## 症状

g1_predict の `gen_predict.py`（東京優駿、過去10年集計）が **約16分** かかる。
旧実装（keiba-data-interface で DataFrame 取得 → pandas 集計）では1分未満だった。
mykeibadb-python を3フェーズ設計（PR#41〜#44）に移行してから劣化した。

## 計測結果

東京優駿（`keibajo_code=05`, `kyori=2400`, `shiba_da=芝`, `2016〜2025`, 対象177エントリ）の
各 metric 実測時間。`fetch_dataframe` をラップして計測。

| metric | source.type | GroupBy.kind | 時間 |
|---|---|---|---|
| キャリア | career_count | history(dynamic→fixed) | **263.9s** |
| 勝利数 | past_finish_count | fixed | **189.1s** |
| 重賞勝利数 | past_finish_count | fixed | **188.9s** |
| 継続騎乗 | jockey_continuity | fixed | **131.6s** |
| 東京勝利数 | past_finish_count | fixed | **122.9s** |
| デビュー | debut_venue | history | **99.1s** |
| 前走レース | prev_race_name | history | **46.9s** |
| 枠順 | gate_number | race_col | 0.60s |
| 人気 | popularity | race_col | 0.66s |
| 脚質 | running_style | race_col | 0.67s |
| 騎手 | jockey_name | subject | 0.61s |
| 生産者 | breeder_name | subject | 0.69s |
| 種牡馬 | sire_name | subject | 0.62s |
| 父実績 | sire_condition_finisher | boolean_multi | 0.82s |

**`history` / `fixed`（馬の過去履歴から属性を算出する）kind の6 metric が全体の約99%（約1043秒）を占める。**
`race_col` / `subject` / `boolean_multi` は全て1秒未満で正常。

各 metric の内訳を見ると、遅いのは全てフェーズ1の `select_entries`（188〜263秒）であり、
フェーズ2の `tally_chakujun` は一律0.55〜0.57秒で問題ない。

## 原因

`select_entries`（`entry_select.py`）が `history` / `fixed` kind の `group_label` を
**相関サブクエリ**で算出していることが原因。`勝利数` metric の実行計画（`EXPLAIN`）:

```
Nested Loop  (cost=1000.43..9764687.45 rows=13)
  ->  Gather → Parallel Seq Scan on race_shosai r   ← 対象レース絞り込み（177行相当）
  ->  Index Scan on umagoto_race_joho u
  SubPlan 1  ->  Aggregate (cost=149527)   ← 過去成績COUNTの相関サブクエリ
  SubPlan 2  ->  Aggregate (cost=149527)   ← 同一サブクエリの重複
  SubPlan 3  ->  Aggregate (cost=149527)   ← 〃
  SubPlan 4  ->  Aggregate (cost=149527)   ← 〃
  SubPlan 5  ->  Aggregate (cost=149527)   ← 〃
```

### 問題1: 同一の相関サブクエリを CASE の WHEN 句ごとに重複実行

`_build_fixed_group_label_expr`（`entry_select.py`）は、rows の各 item（例: 0勝/1勝/2勝/3勝以上）
ごとに **同じ過去成績算出サブクエリを丸ごと展開** する。上の計画では SubPlan が5つ。
1頭の過去成績を求めるのに同一COUNTを4〜5回計算しており、完全な重複。
item 数に比例してコストが増える。

### 問題2: 相関サブクエリが外側の全行に対して評価される

SubPlan の cost は1つあたり約149527。これが外側 Nested Loop の各行ごとに再評価される。
さらにサブクエリ内の `CAST(u2.kakutei_chakujun AS INTEGER) BETWEEN 1 AND N` は
関数適用のためインデックスが効かず、`ketto_toroku_bango` で絞った後の各馬の全履歴を
読んで毎回フィルタしている。

### 問題3: PR#38 の最適化が3フェーズ化で巻き戻った

削除された旧 `entry_attr.py`（`analyze_entry_attr_chakudo`）は、PR#38
「`entry_attr` を CTE ベースに書き直し」で **相関サブクエリを CTE に置き換える最適化** を
実施済みだった。docstring にも「相関サブクエリを避けるため、対象馬を事前に target_horses CTE で
絞り込み、その馬の全履歴を horse_hist CTE で一括取得した後、属性値を集計する」と明記されていた。

3フェーズ設計（PR#41〜#44）で `select_entries` を新規実装した際、この CTE 方式が採用されず、
属性算出が相関サブクエリに戻ってしまった。これがユーザーの「PR#40時点では速かった」という
記憶と一致する。

## 他実装との比較

### 旧 entry_attr.py（PR#38、CTE 方式・高速）

```
WITH target_horses AS (対象エントリを condition で絞り込み),     -- 1回
     horse_hist AS (対象馬の全履歴を一括取得),                    -- 1回
     attr_agg AS (属性値を1回だけ集計),                          -- 1回
     grouped AS (CASE WHEN で attr_val をビン分類)               -- サブクエリ重複なし
SELECT ... FROM grouped GROUP BY grp
```

属性算出が **馬ごとに1回** で済み、CASE は集計済みの `attr_val` を参照するだけ。
1分析が1クエリで完結。

### jvlink-mcp-server（参考元・1クエリ集約方式）

`high_level_api.py` は **1分析 = 1クエリ**。`WHERE` で対象を絞り、
`GROUP BY + SUM(CASE WHEN KakuteiJyuni=1 THEN 1 ELSE 0 END)` で着度数を集約する。
相関サブクエリは皆無、JOIN は `NL_RA`（レース）/`NL_UM`（馬）への直結のみ。

ただし jvlink は「特定の主体（騎手・種牡馬）の成績集計」が中心で、
「馬の過去履歴に依存する横断的な属性別集計（前走別・デビュー地別・過去勝利数別）」は
そもそも提供していない。g1_predict の傾向表はこの横断集計が必須のため、
jvlink の実装をそのまま流用することはできない。

## 解決策

### 案A: `select_entries` の属性算出を CTE 方式に戻す（推奨）

`history` / `fixed` kind の `group_label` を相関サブクエリではなく、
旧 `entry_attr.py` と同じ CTE 方式（target_horses → horse_hist → attr_agg → JOIN）で算出する。

- **効果:** 問題1〜3を一括解消。属性は馬ごとに1回だけ算出され、CASE の重複も消える。
  PR#38 で実証済みの最適化を3フェーズ構造に再適用するだけ。
- **3フェーズ設計を維持:** フェーズ1の内部実装を変えるのみ。フェーズ2/3はそのまま。
- **複雑条件と両立:** `filters`（SubjectFilter/HistoryFilter/ChokyoFilter）の INTERSECT 構造とも共存可能。
- **汎用性を維持:** g1_predict・mcp-server 双方の呼び出しインターフェース（`analyze_chakudo`）は不変。
- **コスト:** `entry_select.py` の `_build_group_label_expr` 系を CTE 生成に書き換える中規模改修。

### 案B: keiba-data-interface で DataFrame 取得 → pandas 集計

対象エントリ（177頭）と対象馬の全履歴を1〜2クエリで取得し、pandas で属性算出・集計する。
SQL の相関サブクエリを完全に回避できる。

- **懸念:** 「複雑条件（filters）」「3フェーズ分割」「汎用性」を pandas 側でどう体系的に
  担保するかの設計が別途必要。条件が緩いクエリでは取得 DataFrame が巨大化するリスク。
- 案Aで目標性能（数秒）に到達できるため、現時点では案Aを優先する。

### 案C: 案A + DB スキーマ最適化（追加施策）

案Aに加え、インデックス不可述語を解消するとさらに速くなる:

- `TRIM(r.kyori)::INTEGER = %s`、`CAST(u.kakutei_chakujun AS INTEGER)` など
  関数適用述語が `race_shosai` / `umagoto_race_joho` のインデックスを無効化している。
- 正規化済み列の追加や式インデックス（`CREATE INDEX ON race_shosai ((TRIM(kyori)::int))`）で改善可能。
- ただしスキーマ変更は data サブモジュール側の取り込み処理にも影響するため別タスクとする。

## 推奨

**案A**（`select_entries` を CTE 方式に書き換え）を採用する。
3フェーズ設計・複雑条件・汎用性をすべて維持したまま、最小の設計変更で PR#38 相当の性能に戻せる。
余力があれば案Cのインデックス最適化を後続で実施する。
