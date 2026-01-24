# KYOSOBA_TORIHIKI_KAKAKU2

- レコード名: 競走馬市場取引価格

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2 | HS をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1 | 1:初期値　0:該当レコード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10 | 血統登録番号を設定 競走馬マスタへリンク |
| CHICHI_HANSHOKU_TOROKU_BANGO |   | 父馬 繁殖登録番号 | 10 | 繁殖馬マスタへリンク |
| HAHA_HANSHOKU_TOROKU_BANGO |   | 母馬 繁殖登録番号 | 10 | 繁殖馬マスタへリンク |
| SEINEN |   | 生年 | 4 | XXXX年 競走馬の生年を設定 |
| SHUSAISHA_SHIJO_CODE | ○ | 主催者・市場コード | 6 | 主催者・市場毎にユニークとなる値を設定する。 |
| SHUSAISHA_MEISHO |   | 主催者名称 | 40 | 市場の主催者の名称を設定 |
| SHIJO_MEISHO |   | 市場の名称 | 80 | 市場の名称を設定 |
| KAISAI_KIKAN_KAISHIBI | ○ | 市場の開催期間(開始日) | 8 | 市場の開催期間（開始日)を設定。XXXX年XX月XX日同一馬が複数回取引されることを考慮してキー設定。 |
| KAISAI_KIKAN_SHURYOBI |   | 市場の開催期間(終了日) | 8 | 市場の開催期間（終了日)を設定。XXXX年XX月XX日 |
| TORIHIKIJI_NENREI |   | 取引時の競走馬の年齢 | 1 | 0：0歳　1:1歳　2:2歳　3：3歳など　設定値が年齢に対応 |
| TORIHIKI_KAKAKU |   | 取引価格 | 10 | 単位 円 |