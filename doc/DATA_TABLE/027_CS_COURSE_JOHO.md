# COURSE_JOHO

- レコード名: コース情報

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2 | CSをセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1 | 1:新規登録 2:更新0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| KEIBAJO_CODE | ○ | 競馬場コード | 2 | <コード表 2001.競馬場コード>参照 |
| KYORI | ○ | 距離 | 4 | 単位：メートル |
| TRACK_CODE | ○ | トラックコード | 2 | <コード表 2009.トラックコード>参照 |
| COURSE_KAISHU_NENGAPPI | ○ | コース改修年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式　(コース改修後、最初に行われた開催日） |
| COURSE_SETSUMEI |   | コース説明 | 6800 | テキスト文 |