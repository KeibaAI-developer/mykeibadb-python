# SHUSSOBETSU_KEIBAJO

- レコード名: 出走別着度数
- サブレコード: 出走別着度数　競馬場別

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   | 2026-01-22 05:26:36 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | CK をセットレコードフォーマットを特定する | CK |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 | 1 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |  |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20251225 |
| RACE_CODE | ○ | レースコード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 | 2025122806050811 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 | 2025 |
| KAISAI_GAPPI |   | 開催月日 | 4.0 | 該当レース施行月日 各2桁 mmdd形式 | 1228 |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 | 06 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す | 05 |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す | 08 |
| RACE_BANGO |   | レース番号 | 2.0 | 該当レース番号 | 11 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10.0 | 生年(西暦)4桁＋1＋数字5桁 | 2022105081 |
| BAMEI |   | 馬名 | 36.0 | 通常全角18文字。 | ミュージアムマイル |
|   |   | <競馬場別着回数> |   |   |  |
| SAPPORO_SHIBA_1CHAKU |   | 札幌芝・着回数 | 3.0 | 札幌・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| SAPPORO_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| HAKODATE_SHIBA_1CHAKU |   | 函館芝・着回数 | 3.0 | 函館・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| HAKODATE_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHIBA_1CHAKU |   | 福島芝・着回数 | 3.0 | 福島・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| FUKUSHIMA_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| NIIGATA_SHIBA_1CHAKU |   | 新潟芝・着回数 | 3.0 | 新潟・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| NIIGATA_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| TOKYO_SHIBA_1CHAKU |   | 東京芝・着回数 | 3.0 | 東京・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| TOKYO_SHIBA_2CHAKU |   |   | 3.0 |   | 001 |
| TOKYO_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHIBA_CHAKUGAI |   |   | 3.0 |   | 001 |
| NAKAYAMA_SHIBA_1CHAKU |   | 中山芝・着回数 | 3.0 | 中山・芝での1着～5着及び着外(6着以下)の回数 | 002 |
| NAKAYAMA_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHIBA_4CHAKU |   |   | 3.0 |   | 001 |
| NAKAYAMA_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| CHUKYO_SHIBA_1CHAKU |   | 中京芝・着回数 | 3.0 | 中京・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| CHUKYO_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHIBA_3CHAKU |   |   | 3.0 |   | 001 |
| CHUKYO_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| KYOTO_SHIBA_1CHAKU |   | 京都芝・着回数 | 3.0 | 京都・芝での1着～5着及び着外(6着以下)の回数 | 002 |
| KYOTO_SHIBA_2CHAKU |   |   | 3.0 |   | 001 |
| KYOTO_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| HANSHIN_SHIBA_1CHAKU |   | 阪神芝・着回数 | 3.0 | 阪神・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| HANSHIN_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| KOKURA_SHIBA_1CHAKU |   | 小倉芝・着回数 | 3.0 | 小倉・芝での1着～5着及び着外(6着以下)の回数 | 000 |
| KOKURA_SHIBA_2CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHIBA_3CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHIBA_4CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHIBA_5CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHIBA_CHAKUGAI |   |   | 3.0 |   | 000 |
| SAPPORO_DIRT_1CHAKU |   | 札幌ダ・着回数 | 3.0 | 札幌・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| SAPPORO_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| HAKODATE_DIRT_1CHAKU |   | 函館ダ・着回数 | 3.0 | 函館・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| HAKODATE_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| FUKUSHIMA_DIRT_1CHAKU |   | 福島ダ・着回数 | 3.0 | 福島・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| FUKUSHIMA_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| NIIGATA_DIRT_1CHAKU |   | 新潟ダ・着回数 | 3.0 | 新潟・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| NIIGATA_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| TOKYO_DIRT_1CHAKU |   | 東京ダ・着回数 | 3.0 | 東京・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| TOKYO_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| NAKAYAMA_DIRT_1CHAKU |   | 中山ダ・着回数 | 3.0 | 中山・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| NAKAYAMA_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| CHUKYO_DIRT_1CHAKU |   | 中京ダ・着回数 | 3.0 | 中京・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| CHUKYO_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| KYOTO_DIRT_1CHAKU |   | 京都ダ・着回数 | 3.0 | 京都・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| KYOTO_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| HANSHIN_DIRT_1CHAKU |   | 阪神ダ・着回数 | 3.0 | 阪神・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| HANSHIN_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| KOKURA_DIRT_1CHAKU |   | 小倉ダ・着回数 | 3.0 | 小倉・ダートでの1着～5着及び着外(6着以下)の回数 | 000 |
| KOKURA_DIRT_2CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_DIRT_3CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_DIRT_4CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_DIRT_5CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_DIRT_CHAKUGAI |   |   | 3.0 |   | 000 |
| SAPPORO_SHOGAI_1CHAKU |   | 札幌障・着回数 | 3.0 | 札幌・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| SAPPORO_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| SAPPORO_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| HAKODATE_SHOGAI_1CHAKU |   | 函館障・着回数 | 3.0 | 函館・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| HAKODATE_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| HAKODATE_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHOGAI_1CHAKU |   | 福島障・着回数 | 3.0 | 福島・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| FUKUSHIMA_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| FUKUSHIMA_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| NIIGATA_SHOGAI_1CHAKU |   | 新潟障・着回数 | 3.0 | 新潟・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| NIIGATA_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| NIIGATA_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| TOKYO_SHOGAI_1CHAKU |   | 東京障・着回数 | 3.0 | 東京・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| TOKYO_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| TOKYO_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHOGAI_1CHAKU |   | 中山障・着回数 | 3.0 | 中山・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| NAKAYAMA_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| NAKAYAMA_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| CHUKYO_SHOGAI_1CHAKU |   | 中京障・着回数 | 3.0 | 中京・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| CHUKYO_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| CHUKYO_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| KYOTO_SHOGAI_1CHAKU |   | 京都障・着回数 | 3.0 | 京都・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| KYOTO_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| KYOTO_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| HANSHIN_SHOGAI_1CHAKU |   | 阪神障・着回数 | 3.0 | 阪神・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| HANSHIN_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| HANSHIN_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| KOKURA_SHOGAI_1CHAKU |   | 小倉障・着回数 | 3.0 | 小倉・障害での1着～5着及び着外(6着以下)の回数 | 000 |
| KOKURA_SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| KOKURA_SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
| KYAKUSHITSU_KEIKO_NIGE |   | 脚質傾向 | 3.0 | 逃げ回数、先行回数、差し回数、追込回数を設定 | 000 |
|   |   |   |   | 過去出走レースの脚質を判定しカウントしたもの(中央レースのみ) |  |
| KYAKUSHITSU_KEIKO_SENKO |   |   | 3.0 |   | 004 |
| KYAKUSHITSU_KEIKO_SASHI |   |   | 3.0 |   | 005 |
| KYAKUSHITSU_KEIKO_OIKOMI |   |   | 3.0 |   | 000 |
| TOROKU_RACE_SU |   | 登録レース数 | 3.0 | JRA-VANに登録されている成績レース数 | 009 |
