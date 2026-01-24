# BAMEI_IMI_YURAI

- レコード名: 馬名の意味由来

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2 | HY をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1 | 1:初期値　0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10 | 血統登録番号を設定 競走馬マスタへリンク |
| BAMEI |   | 馬名 | 36 | 全角18文字 |
| BAMEI_IMI_YURAI |   | 馬名の意味由来 | 64 | 全角32文字 |