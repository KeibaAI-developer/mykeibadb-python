# レビュー: feature/race-condition-multi-value
## 概要
- 対象: origin/develop -> HEAD
- レビュー日: 2026-06-13
- レビュー対象ファイル数: 4

## 指摘事項
### 1. from_dictで複数指定フィールドの型検証がなく、不正な外部入力を内部状態へ取り込める
| 項目 | 内容 |
|------|------|
| 重要度 | Warning |
| 場所 | mykeibadb/analytics/_models.py L170 |

**指摘内容**
`keibajo_codes` と `baba` は `d.get(...)` の値をそのまま `RaceCondition` に渡しており、`kaisai_nichime` も iterable 前提で変換しています。外部入力が `{"keibajo_codes": "09"}` のような文字列だった場合、後段の `list(condition.keibajo_codes)` で `["0", "9"]` に分解されます。`{"kaisai_nichime": 4}` のような単一値では `TypeError` になります。OWASPの観点でも、外部入力の構造・要素型・許容値を境界で検証していないため、予期しないWHERE条件や500系エラーにつながります。

**修正案**
`from_dict` で `list` / `tuple` など許容する型を明示し、要素型と値域を検証してください。例えば `keibajo_codes` は `list[str]` かつコード形式、`kaisai_nichime` は整数化可能な配列、`baba` は `{"良", "稍重", "重", "不良"}` のいずれかに限定し、不正値は `ValueError` として扱うのが安全です。併せて単一値を受け付ける仕様にするなら、明示的にリストへ正規化してください。

### 2. babajotai_codeとbabaを同時指定すると同じ概念の条件がANDで二重適用される
| 項目 | 内容 |
|------|------|
| 重要度 | Warning |
| 場所 | mykeibadb/analytics/_cte_helpers.py L153 |

**指摘内容**
既存の `babajotai_code` と新規の `baba` はどちらも `shiba_babajotai_code / dirt_babajotai_code` の有効値を絞り込む条件です。現状は両方が指定されると `= %s` と `= ANY(%s::TEXT[])` がANDで追加され、矛盾する入力では結果が0件になります。入力ミスを静かに空結果へ変換するため、利用側から原因を特定しづらくなります。

**修正案**
`babajotai_code` と `baba` はどちらか一方のみ許可する、または `baba` をコードへ正規化して同一条件として統合する方針を明示してください。同時指定を禁止する場合は `build_race_condition_where` または `RaceCondition.from_dict` で `ValueError` を返すと、準正常系としてテストしやすくなります。

### 3. 馬場状態コード取得SQLが重複しており保守時に差分が出やすい
| 項目 | 内容 |
|------|------|
| 重要度 | Suggestion |
| 場所 | mykeibadb/analytics/_cte_helpers.py L184 |

**指摘内容**
`babajotai_code` と `baba` のWHERE句で、`COALESCE(NULLIF(NULLIF(TRIM(...` から始まる馬場状態コード取得式が重複しています。今後、空値や `"0"` の扱い、別カラム対応などを変更する際に片方だけ修正漏れするリスクがあります。

**修正案**
`_build_babajotai_code_expr(race_alias: str) -> str` のようなprivate helper、またはprivate定数テンプレートに切り出し、`= %s` と `= ANY(%s::TEXT[])` の差分だけを呼び出し側に残してください。不要なメソッド化は避けるべきですが、このケースは同一SQL断片のDRY化として保守性向上が見込めます。

### 4. 新規テストが正常系に偏っており、準正常系・異常系とparametrize活用が不足している
| 項目 | 内容 |
|------|------|
| 重要度 | Suggestion |
| 場所 | test/unit/mykeibadb/analytics/test_models.py L76 |

**指摘内容**
`RaceCondition.from_dict` の新規テストは正常系と省略時のみで、`keibajo_codes` が文字列、`kaisai_nichime` が単一intや数値化不能文字列、`baba` が未対応値といった準正常系・異常系がありません。また、`keibajo_codes` / `kaisai_nichime` / `baba` の単純な読み取り確認は構造が近く、個別関数に分けるより `pytest.mark.parametrize` でまとめる方が意図と期待値を見通しやすくなります。

**修正案**
正常系は `parametrize` で入力辞書・期待属性・期待値を表にし、異常系も不正入力ごとに `parametrize` で `ValueError` または `TypeError` を検証してください。テストクラスは未使用のままで問題ありませんが、コメント上の「正常系」セクションに異常系テストを混在させないよう分類を揃えるとレビュー観点に合います。

### 5. keibajo_codeとkeibajo_codesの関係が命名から読み取りにくく、誤用しやすい
| 項目 | 内容 |
|------|------|
| 重要度 | Suggestion |
| 場所 | mykeibadb/analytics/_models.py L117 |

**指摘内容**
`keibajo_code` と `keibajo_codes` は単数・複数の同一概念に見えますが、docstringでは「ORではなく独立したIN条件」とされており、実装上も両方指定時はAND条件になります。命名だけでは「複数指定版に置き換わった」と誤解しやすく、呼び出し側が両方を指定して意図せず絞り込みすぎる可能性があります。

**修正案**
APIとしては `keibajo_codes` に統一し、単一値は1要素リストへ正規化するのが最も分かりやすいです。後方互換が必要な場合は同時指定を禁止するか、`keibajo_code` を `keibajo_codes` に統合する変換ルールを `from_dict` のdocstringとテストで明示してください。

## まとめ
| 重要度 | 件数 |
|--------|------|
| Critical | 0 |
| Warning | 2 |
| Suggestion | 3 |
