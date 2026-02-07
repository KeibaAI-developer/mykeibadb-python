# RECORD_MASTER

- レコード名: レコードマスタ

## カラム一覧

mykeibadb公式ドキュメントに則りカラム名を大文字で記載していますが、データフレームとして取得した際はカラム名は小文字になります。

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19 |   | 2026-01-22 03:35:07 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2 | RC をセットレコードフォーマットを特定する | RC |
| DATA_KUBUN |   | データ区分 | 1 | 1:初期値　0:該当レコード削除(提供ミスなどの理由による) | 1 |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20251229 |
| RECORD_SHIKIBETSU_KUBUN | ○ | レコード識別区分 | 1 | 1:コースレコード 2:ＧⅠレコード | 2 |
| RACE_CODE | ○ | レースコード | 16 | 開催年+月日+競馬場コード+回次+日次+レース番号 | 2002081804030411 |
| KAISAI_NEN |   | 開催年 | 4 | 該当レース施行年 西暦4桁 yyyy形式 | 2002 |
| KAISAI_GAPPI |   | 開催月日 | 4 | 該当レース施行月日 各2桁 mmdd形式 | 0818 |
| KEIBAJO_CODE |   | 競馬場コード | 2 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 | 04 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す | 03 |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す | 04 |
| RACE_BANGO |   | レース番号 | 2 | 該当レース番号 | 11 |
| TOKUBETSU_KYOSO_BANGO | ○ | 特別競走番号 | 4 | ＧⅠレコードのみのキー | 0000 |
| KYOSOMEI_HONDAI |   | 競走名本題 | 60 | 全角30文字 | アイビスサマーダッシュ |
| GRADE_CODE |   | グレードコード | 1 | <コード表 2003.グレードコード>参照 | C |
| KYOSO_SHUBETSU_CODE | ○ | 競走種別コード | 2 | <コード表 2005.競走種別コード>参照 | 13 |
| KYORI | ○ | 距離 | 4 | 単位:メートル | 1000 |
| TRACK_CODE | ○ | トラックコード | 2 | <コード表 2009.トラックコード>参照 | 10 |
| RECORD_KUBUN |   | レコード区分 | 1 | 1:基準タイム　2:レコードタイム　3:参考タイム　4:備考タイム | 2 |
| RECORD_TIME |   | レコードタイム | 4 | 9分99秒9 | 0537 |
| TENKO_CODE |   | 天候コード | 1 | <コード表 2011.天候コード>参照 | 1 |
| SHIBA_BABAJOTAI_CODE |   | 芝馬場状態コード | 1 | <コード表 2010.馬場状態コード>参照 | 1 |
| DIRT_BABAJOTAI_CODE |   | ダート馬場状態コード | 1 | <コード表 2010.馬場状態コード>参照 | 0 |
|   |   | <レコード保持馬情報> | 130 | 同着を考慮し繰返し3回 |  |
| HOJIUMA1_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10 | 生年(西暦)4桁＋品種1桁＋数字5桁 | 1998103333 |
| HOJIUMA1_BAMEI |   | 馬名 | 36 | 全角18文字 | カルストンライトオ |
| HOJIUMA1_UMAKIGO_CODE |   | 馬記号コード | 2 | <コード表 2204.馬記号コード>参照 | 04 |
| HOJIUMA1_SEIBETSU_CODE |   | 性別コード | 1 | <コード表 2202.性別コード>参照 | 1 |
| HOJIUMA1_CHOKYOSHI_CODE |   | 調教師コード | 5 |   | 01032 |
| HOJIUMA1_CHOKYOSHIMEI |   | 調教師名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 | 大根田　裕之 |
| HOJIUMA1_FUTAN_JURYO |   | 負担重量 | 3 | 単位:0.1kg | 560 |
| HOJIUMA1_KISHU_CODE |   | 騎手コード | 5 |   | 00597 |
| HOJIUMA1_KISHUMEI |   | 騎手名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 | 大西　直宏 |
| HOJIUMA2_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10 | 生年(西暦)4桁＋品種1桁＋数字5桁 | 0000000000 |
| HOJIUMA2_BAMEI |   | 馬名 | 36 | 全角18文字 |  |
| HOJIUMA2_UMAKIGO_CODE |   | 馬記号コード | 2 | <コード表 2204.馬記号コード>参照 | 00 |
| HOJIUMA2_SEIBETSU_CODE |   | 性別コード | 1 | <コード表 2202.性別コード>参照 | 0 |
| HOJIUMA2_CHOKYOSHI_CODE |   | 調教師コード | 5 |   | 00000 |
| HOJIUMA2_CHOKYOSHIMEI |   | 調教師名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |  |
| HOJIUMA2_FUTAN_JURYO |   | 負担重量 | 3 | 単位:0.1kg | 000 |
| HOJIUMA2_KISHU_CODE |   | 騎手コード | 5 |   | 00000 |
| HOJIUMA2_KISHUMEI |   | 騎手名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |  |
| HOJIUMA3_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10 | 生年(西暦)4桁＋品種1桁＋数字5桁 | 0000000000 |
| HOJIUMA3_BAMEI |   | 馬名 | 36 | 全角18文字 |  |
| HOJIUMA3_UMAKIGO_CODE |   | 馬記号コード | 2 | <コード表 2204.馬記号コード>参照 | 00 |
| HOJIUMA3_SEIBETSU_CODE |   | 性別コード | 1 | <コード表 2202.性別コード>参照 | 0 |
| HOJIUMA3_CHOKYOSHI_CODE |   | 調教師コード | 5 |   | 00000 |
| HOJIUMA3_CHOKYOSHIMEI |   | 調教師名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |  |
| HOJIUMA3_FUTAN_JURYO |   | 負担重量 | 3 | 単位:0.1kg | 000 |
| HOJIUMA3_KISHU_CODE |   | 騎手コード | 5 |   | 00000 |
| HOJIUMA3_KISHUMEI |   | 騎手名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |  |

## 追加カラム一覧

`MasterGetter.get_record_master()` メソッドではデフォルトで`convert_codes=True`が指定されており、以下のカラムが追加されます。

|名前|項目名|説明|例|
|:----|:----|:----|----|
|keibajo|競馬場名|KEIBAJO_CODEを場略名(3文字)に変換 <コード表 2001.競馬場コード>参照| 新潟 |
|grade|グレード|GRADE_CODEを名称に変換 <コード表 2003.グレードコード>参照| GIII |
|kyoso_shubetsu|競走種別|KYOSO_SHUBETSU_CODEを略名(8文字)に変換 <コード表 2005.競走種別コード>参照| サラ系３歳以上 |
|track|トラック|TRACK_CODEを略名(6文字)に変換 <コード表 2009.トラックコード>参照| 芝・直 |
|tenko|天候|TENKO_CODEを名称に変換 <コード表 2011.天候コード>参照| 晴 |
|shiba_babajotai|芝馬場状態|SHIBA_BABAJOTAI_CODEを名称に変換 <コード表 2010.馬場状態コード>参照| 良 |
|dirt_babajotai|ダート馬場状態|DIRT_BABAJOTAI_CODEを名称に変換 <コード表 2010.馬場状態コード>参照|  |
|hojiuma1_umakigo|保持馬1 馬記号|HOJIUMA1_UMAKIGO_CODEを名称に変換 <コード表 2204.馬記号コード>参照| 抽 |
|hojiuma1_seibetsu|保持馬1 性別|HOJIUMA1_SEIBETSU_CODEを略に変換 <コード表 2202.性別コード>参照| 牡 |
|hojiuma2_umakigo|保持馬2 馬記号|HOJIUMA2_UMAKIGO_CODEを名称に変換 <コード表 2204.馬記号コード>参照|  |
|hojiuma2_seibetsu|保持馬2 性別|HOJIUMA2_SEIBETSU_CODEを略に変換 <コード表 2202.性別コード>参照|  |
|hojiuma3_umakigo|保持馬3 馬記号|HOJIUMA3_UMAKIGO_CODEを名称に変換 <コード表 2204.馬記号コード>参照|  |
|hojiuma3_seibetsu|保持馬3 性別|HOJIUMA3_SEIBETSU_CODEを略に変換 <コード表 2202.性別コード>参照|  |
