# SEISANSHA_MASTER2

- レコード名: 生産者マスタ

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | BR をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| SEISANSHA_CODE | ○ | 生産者コード | 8.0 |   |
| SEISANSHAMEI_HOJINKAKU_ARI |   | 生産者名(法人格有) | 72.0 | 全角36文字 ～ 半角72文字 （全角と半角が混在） |
|   |   |   |   | 外国生産者の場合は、8.生産者名欧字の頭70バイトを設定。 |
| SEISANSHAMEI_HOJINKAKU_NASHI |   | 生産者名(法人格無) | 72.0 | 全角36文字 ～ 半角72文字 （全角と半角が混在） |
|   |   |   |   | 株式会社、有限会社などの法人格を示す文字列が頭もしくは末尾にある場合にそれを削除したものを設定。また、外国生産者の場合は、8.生産者名欧字の頭70バイトを設定。 |
| SEISANSHAMEI_HANKAKU_KANA |   | 生産者名半角ｶﾅ | 72.0 | 半角72文字 |
|   |   |   |   | 日本語半角ｶﾅを設定(半角ｶﾅ以外の文字は設定しない)　外国生産者については設定しない。 |
| SEISANSHAMEI_ENG |   | 生産者名欧字 | 168.0 | 全角84文字 ～ 半角168文字 (全角と半角が混在) |
|   |   |   |   | アルファベット等以外の特殊文字については、全角で設定。 |
| SEISANSHA_JUSHO_JICHISHOMEI |   | 生産者住所自治省名 | 20.0 | 全角10文字　生産者の所在地を示す |
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
|   |   | <本年･累計成績情報> | 60.0 | 本年・累計の順に設定 |
| SETTEI_NEN_RUIKEI |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) |
| HONSHOKIN_GOKEI_RUIKEI |   | 本賞金合計 | 10.0 | 単位：百円　（中央の本賞金の合計） |
| FUKASHOKIN_GOKEI_RUIKEI |   | 付加賞金合計 | 10.0 | 単位：百円　（中央の付加賞金の合計） |
| CHUO_GOKEI_1CHAKU_RUIKEI |   | 着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| CHUO_GOKEI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUO_GOKEI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |