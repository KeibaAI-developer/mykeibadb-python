# HASSOJIKOKU_HENKO

- レコード名: 発走時刻変更

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | TC をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:初期値 |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| RACE_CODE | ◯ | レースコード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 |
| KAISAI_GAPPI |   | 開催月日 | 4.0 | 該当レース施行月日 各2桁 mmdd形式 |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す |
| RACE_BANGO |   | レース番号 | 2.0 | 該当レース番号 |
| HAPPYO_TSUIKIHI_JIFUN |   | 発表月日時分 | 8.0 | 月日時分各2桁 |
|   |   | <変更後情報> |   |   |
| HENKOGO_HASSO_JIKOKU |   | 変更後 発走時刻 | 4.0 | 時分各2桁 hhmm形式 |
|   |   | <変更前情報> |   |   |
| HENKOMAE_HASSO_JIKOKU |   | 変更前 発走時刻 | 4.0 | 時分各2桁 hhmm形式 |