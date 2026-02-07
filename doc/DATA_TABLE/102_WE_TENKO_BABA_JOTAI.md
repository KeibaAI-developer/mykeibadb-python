# TENKO_BABA_JOTAI

- レコード名: 天候馬場状態

## カラム一覧

mykeibadb公式ドキュメントに則りカラム名を大文字で記載していますが、データフレームとして取得した際はカラム名は小文字になります。

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   | 2026-02-01 10:36:56 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | WE をセットレコードフォーマットを特定する | WE |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:初期値 | 1 |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20260131 |
| RACE_CODE | ○ | レースコード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 ※**注意事項参照** | 20260201050102 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 | 2026 |
| KAISAI_GAPPI |   | 開催月日 | 4.0 | 該当レース施行月日 各2桁 mmdd形式 | 0201 |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 | 05 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す | 01 |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す | 02 |
| HAPPYO_TSUIKIHI_JIFUN | ◯ | 発表月日時分 | 8.0 | 月日時分各2桁 | 00000000 |
| HENKO_SHIKIBETU | ◯ | 変更識別 | 1.0 | 1:天候馬場初期状態　2:天候変更　3:馬場状態変更 | 1 |
|   |   |   |   | 1:初期状態の時は天候・馬場ともに有効値を設定。 |  |
|   |   |   |   | 2:天候変更の時は天候(変更後・変更前)のみ有効値を設定。(馬場は初期値) |  |
|   |   |   |   | 3:馬場状態変更の時は馬場(変更後・変更前)のみ有効値を設定。(天候は初期値) |  |
|   |   | <現在状態情報> |   | 現在の天候馬場の状態を設定 |  |
| TENKO_JOTAI_GENZAI |   | 天候状態 | 1.0 | <コード表 2011.天候コード>参照 | 1 |
| BABA_JOTAI_SHIBA_GENZAI |   | 馬場状態・芝 | 1.0 | <コード表 2010.馬場状態コード>参照 | 1 |
| BABA_JOTAI_DIRT_GENZAI |   | 馬場状態・ダート | 1.0 | <コード表 2010.馬場状態コード>参照 | 1 |
|   |   | <変更前状態情報> |   | 変更前直前の天候馬場状態を設定 |  |
| TENKO_JOTAI_HENKOMAE |   | 天候状態 | 1.0 | <コード表 2011.天候コード>参照 | 0 |
| BABA_JOTAI_SHIBA_HENKOMAE |   | 馬場状態・芝 | 1.0 | <コード表 2010.馬場状態コード>参照 | 0 |
| BABA_JOTAI_DIRT_HENKOMA |   | 馬場状態・ダート | 1.0 | <コード表 2010.馬場状態コード>参照 | 0 |

## 注意事項

`RACE_CODE`の実際の値は14桁の開催コードになっています。  
JV-Linkもしくはmykeibadbのバグと思われます。
## 追加カラム一覧

`SokuhoGetter.get_tenko_baba_jotai()` メソッドではデフォルトで`convert_codes=True`が指定されており、以下のカラムが追加されます。

|名前|項目名|説明|例|
|:----|:----|:----|----|
|keibajo|競馬場名|KEIBAJO_CODEを場略名(3文字)に変換 <コード表 2001.競馬場コード>参照| 東京 |
|tenko_jotai_genzai_name|現在の天候|TENKO_JOTAI_GENZAIを名称に変換 <コード表 2011.天候コード>参照| 晴 |
|baba_jotai_shiba_genzai_name|現在の芝馬場状態|BABA_JOTAI_SHIBA_GENZAIを名称に変換 <コード表 2010.馬場状態コード>参照| 良 |
|baba_jotai_dirt_genzai_name|現在のダート馬場状態|BABA_JOTAI_DIRT_GENZAIを名称に変換 <コード表 2010.馬場状態コード>参照| 良 |
|tenko_jotai_henkomae_name|変更前の天候|TENKO_JOTAI_HENKOMAEを名称に変換 <コード表 2011.天候コード>参照|  |
|baba_jotai_shiba_henkomae_name|変更前の芝馬場状態|BABA_JOTAI_SHIBA_HENKOMAEを名称に変換 <コード表 2010.馬場状態コード>参照|  |
|baba_jotai_dirt_henkoma_name|変更前のダート馬場状態|BABA_JOTAI_DIRT_HENKOMAを名称に変換 <コード表 2010.馬場状態コード>参照|  |
