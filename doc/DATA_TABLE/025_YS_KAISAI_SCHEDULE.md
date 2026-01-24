# KAISAI_SCHEDULE

- レコード名: 開催スケジュール

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | YSをセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:開催予定(年末時点)　2:開催予定(開催直前時点)　3:開催終了(成績確定時点) |
|   |   |   |   | 9:開催中止　0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| KAISAI_CODE | ○ | 開催コード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 |
| KAISAI_GAPPI |   | 開催月日 | 4.0 | 該当レース施行月日 各2桁 mmdd形式 |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す |
| YOBI_CODE |   | 曜日コード | 1.0 | 該当レース施行曜日 <コード表 2002.曜日コード>参照 |
|   |   | <重賞案内> | 118.0 |   |
| JUSHO1_TOKUBETSU_KYOSO_BANGO |   | 特別競走番号 | 4.0 | 重賞レースのみ設定 原則的には過去の同一レースと一致する番号(多数例外有り) |
| JUSHO1_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字　レース名の本題 |
| JUSHO1_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 |
| JUSHO1_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 |
| JUSHO1_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 |
| JUSHO1_JUSHO_KAIJI |   | 重賞回次[第N回] | 3.0 | そのレースの重賞としての通算回数を示す |
| JUSHO1_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 |
|   |   |   |   | ※国際グレード表記(G) または その他の重賞表記（Jpn）の判別方法については、特記事項を参照。 |
| JUSHO1_KYOSO_SHUBETSU_CODE |   | 競走種別コード | 2.0 | <コード表 2005.競走種別コード>参照 |
| JUSHO1_KYOSO_KIGO_CODE |   | 競走記号コード | 3.0 | <コード表 2006.競走記号コード>参照 |
| JUSHO1_JURYO_SHUBETSU_CODE |   | 重量種別コード | 1.0 | <コード表 2008.重量種別コード>参照 |
| JUSHO1_KYORI |   | 距離 | 4.0 | 単位:メートル |
| JUSHO1_TRACK_CODE |   | トラックコード | 2.0 | <コード表 2009.トラックコード>参照 |
| JUSHO2_TOKUBETSU_KYOSO_BANGO |   | 特別競走番号 | 4.0 | 重賞レースのみ設定 原則的には過去の同一レースと一致する番号(多数例外有り) |
| JUSHO2_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字　レース名の本題 |
| JUSHO2_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 |
| JUSHO2_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 |
| JUSHO2_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 |
| JUSHO2_JUSHO_KAIJI |   | 重賞回次[第N回] | 3.0 | そのレースの重賞としての通算回数を示す |
| JUSHO2_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 |
|   |   |   |   | ※国際グレード表記(G) または その他の重賞表記（Jpn）の判別方法については、特記事項を参照。 |
| JUSHO2_KYOSO_SHUBETSU_CODE |   | 競走種別コード | 2.0 | <コード表 2005.競走種別コード>参照 |
| JUSHO2_KYOSO_KIGO_CODE |   | 競走記号コード | 3.0 | <コード表 2006.競走記号コード>参照 |
| JUSHO2_JURYO_SHUBETSU_CODE |   | 重量種別コード | 1.0 | <コード表 2008.重量種別コード>参照 |
| JUSHO2_KYORI |   | 距離 | 4.0 | 単位:メートル |
| JUSHO2_TRACK_CODE |   | トラックコード | 2.0 | <コード表 2009.トラックコード>参照 |
| JUSHO3_TOKUBETSU_KYOSO_BANGO |   | 特別競走番号 | 4.0 | 重賞レースのみ設定 原則的には過去の同一レースと一致する番号(多数例外有り) |
| JUSHO3_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字　レース名の本題 |
| JUSHO3_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 |
| JUSHO3_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 |
| JUSHO3_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 |
| JUSHO3_JUSHO_KAIJI |   | 重賞回次[第N回] | 3.0 | そのレースの重賞としての通算回数を示す |
| JUSHO3_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 |
|   |   |   |   | ※国際グレード表記(G) または その他の重賞表記（Jpn）の判別方法については、特記事項を参照。 |
| JUSHO3_KYOSO_SHUBETSU_CODE |   | 競走種別コード | 2.0 | <コード表 2005.競走種別コード>参照 |
| JUSHO3_KYOSO_KIGO_CODE |   | 競走記号コード | 3.0 | <コード表 2006.競走記号コード>参照 |
| JUSHO3_JURYO_SHUBETSU_CODE |   | 重量種別コード | 1.0 | <コード表 2008.重量種別コード>参照 |
| JUSHO3_KYORI |   | 距離 | 4.0 | 単位:メートル |
| JUSHO3_TRACK_CODE |   | トラックコード | 2.0 | <コード表 2009.トラックコード>参照 |