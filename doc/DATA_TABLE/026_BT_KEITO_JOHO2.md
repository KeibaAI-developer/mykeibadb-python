# KEITO_JOHO2

- レコード名: 系統情報

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2 | BTをセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1 | 1:新規登録 2:更新0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| HANSHOKU_TOROKU_BANGO |   | 繁殖登録番号 | 10 |   |
| KEITO_ID | ○ | 系統ID | 30 | 2桁ごとに系譜を表現するID。詳しくは特記事項を参照 |
| KEITO_MEI |   | 系統名 | 36 | サンデーサイレンス系など、その系統の名称 |
| KEITO_SETSUMEI |   | 系統説明 | 6800 | テキスト文 |