# RECORD_MASTER

- レコード名: レコードマスタ

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2 | RC をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1 | 1:初期値　0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| RECORD_SHIKIBETSU_KUBUN | ○ | レコード識別区分 | 1 | 1:コースレコード 2:ＧⅠレコード |
| RACE_CODE | ○ | レースコード | 16 | 開催年+月日+競馬場コード+回次+日次+レース番号 |
| KAISAI_NEN |   | 開催年 | 4 | 該当レース施行年 西暦4桁 yyyy形式 |
| KAISAI_GAPPI |   | 開催月日 | 4 | 該当レース施行月日 各2桁 mmdd形式 |
| KEIBAJO_CODE |   | 競馬場コード | 2 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す |
| RACE_BANGO |   | レース番号 | 2 | 該当レース番号 |
| TOKUBETSU_KYOSO_BANGO | ○ | 特別競走番号 | 4 | ＧⅠレコードのみのキー |
| KYOSOMEI_HONDAI |   | 競走名本題 | 60 | 全角30文字 |
| GRADE_CODE |   | グレードコード | 1 | <コード表 2003.グレードコード>参照 |
| KYOSO_SHUBETSU_CODE | ○ | 競走種別コード | 2 | <コード表 2005.競走種別コード>参照 |
| KYORI | ○ | 距離 | 4 | 単位:メートル |
| TRACK_CODE | ○ | トラックコード | 2 | <コード表 2009.トラックコード>参照 |
| RECORD_KUBUN |   | レコード区分 | 1 | 1:基準タイム　2:レコードタイム　3:参考タイム　4:備考タイム |
| RECORD_TIME |   | レコードタイム | 4 | 9分99秒9 |
| TENKO_CODE |   | 天候コード | 1 | <コード表 2011.天候コード>参照 |
| SHIBA_BABAJOTAI_CODE |   | 芝馬場状態コード | 1 | <コード表 2010.馬場状態コード>参照 |
| DIRT_BABAJOTAI_CODE |   | ダート馬場状態コード | 1 | <コード表 2010.馬場状態コード>参照 |
|   |   | <レコード保持馬情報> | 130 | 同着を考慮し繰返し3回 |
| HOJIUMA1_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10 | 生年(西暦)4桁＋品種1桁＋数字5桁 |
| HOJIUMA1_BAMEI |   | 馬名 | 36 | 全角18文字 |
| HOJIUMA1_UMAKIGO_CODE |   | 馬記号コード | 2 | <コード表 2204.馬記号コード>参照 |
| HOJIUMA1_SEIBETSU_CODE |   | 性別コード | 1 | <コード表 2202.性別コード>参照 |
| HOJIUMA1_CHOKYOSHI_CODE |   | 調教師コード | 5 |   |
| HOJIUMA1_CHOKYOSHIMEI |   | 調教師名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |
| HOJIUMA1_FUTAN_JURYO |   | 負担重量 | 3 | 単位:0.1kg |
| HOJIUMA1_KISHU_CODE |   | 騎手コード | 5 |   |
| HOJIUMA1_KISHUMEI |   | 騎手名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |
| HOJIUMA2_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10 | 生年(西暦)4桁＋品種1桁＋数字5桁 |
| HOJIUMA2_BAMEI |   | 馬名 | 36 | 全角18文字 |
| HOJIUMA2_UMAKIGO_CODE |   | 馬記号コード | 2 | <コード表 2204.馬記号コード>参照 |
| HOJIUMA2_SEIBETSU_CODE |   | 性別コード | 1 | <コード表 2202.性別コード>参照 |
| HOJIUMA2_CHOKYOSHI_CODE |   | 調教師コード | 5 |   |
| HOJIUMA2_CHOKYOSHIMEI |   | 調教師名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |
| HOJIUMA2_FUTAN_JURYO |   | 負担重量 | 3 | 単位:0.1kg |
| HOJIUMA2_KISHU_CODE |   | 騎手コード | 5 |   |
| HOJIUMA2_KISHUMEI |   | 騎手名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |
| HOJIUMA3_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10 | 生年(西暦)4桁＋品種1桁＋数字5桁 |
| HOJIUMA3_BAMEI |   | 馬名 | 36 | 全角18文字 |
| HOJIUMA3_UMAKIGO_CODE |   | 馬記号コード | 2 | <コード表 2204.馬記号コード>参照 |
| HOJIUMA3_SEIBETSU_CODE |   | 性別コード | 1 | <コード表 2202.性別コード>参照 |
| HOJIUMA3_CHOKYOSHI_CODE |   | 調教師コード | 5 |   |
| HOJIUMA3_CHOKYOSHIMEI |   | 調教師名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |
| HOJIUMA3_FUTAN_JURYO |   | 負担重量 | 3 | 単位:0.1kg |
| HOJIUMA3_KISHU_CODE |   | 騎手コード | 5 |   |
| HOJIUMA3_KISHUMEI |   | 騎手名 | 34 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |