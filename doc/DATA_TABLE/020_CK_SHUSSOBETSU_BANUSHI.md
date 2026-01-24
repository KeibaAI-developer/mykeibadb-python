# SHUSSOBETSU_BANUSHI

- レコード名: 出走別着度数
- サブレコード: 出走別着度数　馬主別

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | CK をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| RACE_CODE | ○ | レースコード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 |
| KAISAI_GAPPI |   | 開催月日 | 4.0 | 該当レース施行月日 各2桁 mmdd形式 |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す |
| RACE_BANGO |   | レース番号 | 2.0 | 該当レース番号 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10.0 | 生年(西暦)4桁＋1＋数字5桁 |
| BAMEI |   | 馬名 | 36.0 | 通常全角18文字。 |
|   |   | <馬主情報> |   |   |
| BANUSHI_CODE |   | 馬主コード | 6.0 |   |
| BANUSHIMEI_HOJINKAKU_ARI |   | 馬主名(法人格有) | 64.0 | 全角32文字 ～ 半角64文字 （全角と半角が混在） |
|   |   |   |   | 外国馬主の場合は、8.馬主名欧字の頭64バイトを設定。 |
| BANUSHIMEI_HOJINKAKU_NASHI |   | 馬主名(法人格無) | 64.0 | 全角32文字 ～ 半角64文字 （全角と半角が混在） |
|   |   |   |   | 株式会社、有限会社などの法人格を示す文字列が頭もしくは末尾にある場合にそれを削除したものを設定 |
|   |   |   |   | また、外国馬主の場合は、8.馬主名欧字の頭64バイトを設定。 |
|   |   | <本年･累計成績情報> | 60.0 | 本年・累計の順に設定 |
| SETTEI_NEN_HONNEN |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) |
| HONSHOKIN_GOKEI_HONNEN |   | 本賞金合計 | 10.0 | 単位：百円　（中央の本賞金の合計） |
| FUKASHOKIN_GOKEI_HONNEN |   | 付加賞金合計 | 10.0 | 単位：百円　（中央の付加賞金の合計） |
| CHUO_GOKEI_1CHAKU_HONNEN |   | 着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| CHUO_GOKEI_2CHAKU_HONNEN |   |   | 6.0 |   |
| CHUO_GOKEI_3CHAKU_HONNEN |   |   | 6.0 |   |
| CHUO_GOKEI_4CHAKU_HONNEN |   |   | 6.0 |   |
| CHUO_GOKEI_5CHAKU_HONNEN |   |   | 6.0 |   |
| CHUO_GOKEI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| SETTEI_NEN_RUIKEI |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) |
| HONSHOKIN_GOKEI_RUIKEI |   | 本賞金合計 | 10.0 | 単位：百円　（中央の本賞金の合計） |
| FUKASHOKIN_GOKEI_RUIKEI |   | 付加賞金合計 | 10.0 | 単位：百円　（中央の付加賞金の合計） |
| CHUO_GOKEI_1CHAKU_RUIKEI |   | 着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| CHUO_GOKEI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_4CHAKU_RUIKEI |   |   |   |   |
| CHUO_GOKEI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |