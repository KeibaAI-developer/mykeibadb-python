# SANKU_MASTER2

- レコード名: 産駒マスタ

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | SK をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁＋数字5桁 |
| SEINENGAPPI |   | 生年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 |
| SEIBETSU_CODE |   | 性別コード | 1.0 | <コード表 2202.性別コード>参照 |
| HINSHU_CODE |   | 品種コード | 1.0 | <コード表 2201.品種コード>参照 |
| MOSHOKU_CODE |   | 毛色コード | 2.0 | <コード表 2203.毛色コード>参照 |
| MOCHIKOMI_KUBUN |   | 産駒持込区分 | 1.0 | 0:内国産 1:持込 2:輸入内国産扱い 3:輸入 |
| YUNYU_NEN |   | 輸入年 | 4.0 | 西暦4桁 |
| SEISANSHA_CODE |   | 生産者コード | 8.0 | 生産者マスタにリンク |
| SANCHI_MEI |   | 産地名 | 20.0 | 全角10文字 |
| KETTO1_HANSHOKU_TOROKU_BANGO |   | 3代血統 繁殖登録番号 | 10.0 | 父･母･父父･父母･母父･母母･父父父･父父母･父母父･父母母･母父父･母父母･母母父･母母母の順に設定 |
| KETTO2_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO3_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO4_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO5_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO6_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO7_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO8_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO9_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO10_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO11_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO12_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO13_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |
| KETTO14_HANSHOKU_TOROKU_BANGO |   |   | 10.0 |   |