# SHUSSOBETSU_CHOKYOSHI

- レコード名: 出走別着度数
- サブレコード: 出走別着度数　調教師別

## カラム一覧

mykeibadb公式ドキュメントに則りカラム名を大文字で記載していますが、データフレームとして取得した際はカラム名は小文字になります。

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   | 2026-01-22 05:26:36 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | CK をセットレコードフォーマットを特定する | CK |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 | 1 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |  |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 19.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20251225            |
| RACE_CODE | ○ | レースコード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 | 2025122806050811 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 | 2025 |
| KAISAI_GAPPI |   | 開催月日 | 19.0 | 該当レース施行月日 各2桁 mmdd形式 | 1228                |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 | 06 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す | 05 |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す | 08 |
| RACE_BANGO |   | レース番号 | 2.0 | 該当レース番号 | 11 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10.0 | 生年(西暦)4桁＋1＋数字5桁 | 2022105081 |
| BAMEI |   | 馬名 | 36.0 | 通常全角18文字。 | ミュージアムマイル |
|   |   | <調教師情報> |   |   |  |
| CHOKYOSHI_CODE |   | 調教師コード | 5.0 | 単位：百円　（中央の平地本賞金の合計） | 01159 |
| CHOKYOSHIMEI |   | 調教師名 | 34.0 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 | 高柳　大輔 |
|   |   | <調教師本年･累計成績情報> | 1220.0 | 本年・累計の順に設定 |  |
| SETTEI_NEN_HONNEN |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) | 2025 |
| HEICHI_HONSHOKIN_GOKEI_HONNEN |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） | 0007960700 |
| SHOGAI_HONSHOKIN_GOKEI_HONNEN |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） | 0000290200 |
| HEICHI_FUKASHOKIN_GOKEI_HONNEN |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） | 0000316980 |
| SHOGAI_FUKASHOKIN_GOKEI_HONNEN |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） | 0000000000 |
| SHIBA_1CHAKU_HONNEN |   | 芝着回数 | 5.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 00010 |
| SHIBA_2CHAKU_HONNEN |   |   | 5.0 |   | 00007 |
| SHIBA_3CHAKU_HONNEN |   |   | 5.0 |   | 00004 |
| SHIBA_4CHAKU_HONNEN |   |   | 5.0 |   | 00009 |
| SHIBA_5CHAKU_HONNEN |   |   | 5.0 |   | 00010 |
| SHIBA_CHAKUGAI_HONNEN |   |   | 5.0 |   | 00048 |
| DIRT_1CHAKU_HONNEN |   | ダート着回数 | 5.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 00015 |
| DIRT_2CHAKU_HONNEN |   |   | 5.0 |   | 00020 |
| DIRT_3CHAKU_HONNEN |   |   | 5.0 |   | 00012 |
| DIRT_4CHAKU_HONNEN |   |   | 5.0 |   | 00009 |
| DIRT_5CHAKU_HONNEN |   |   | 5.0 |   | 00012 |
| DIRT_CHAKUGAI_HONNEN |   |   | 5.0 |   | 00079 |
| SHOGAI_1CHAKU_HONNEN |   | 障害着回数 | 5.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 0002  |
| SHOGAI_2CHAKU_HONNEN |   |   | 5.0 |   | 0001  |
| SHOGAI_3CHAKU_HONNEN |   |   | 5.0 |   | 0003  |
| SHOGAI_4CHAKU_HONNEN |   |   | 5.0 |   | 0000  |
| SHOGAI_5CHAKU_HONNEN |   |   | 5.0 |   | 0003  |
| SHOGAI_CHAKUGAI_HONNEN |   |   | 5.0 |   | 0011  |
| SHIBA_1200_IKA_1CHAKU_HONNEN |   | 芝1200以下・着回数 | 4.0 | 芝･1200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0003 |
| SHIBA_1200_IKA_2CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1200_IKA_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_1200_IKA_4CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1200_IKA_5CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1200_IKA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0013 |
| SHIBA_1201_1400_1CHAKU_HONNEN |   | 芝1201-1400・着回数 | 4.0 | 芝･1201Ｍ以上1400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| SHIBA_1201_1400_2CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_1201_1400_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_1201_1400_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_1201_1400_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_1201_1400_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0004 |
| SHIBA_1401_1600_1CHAKU_HONNEN |   | 芝1401-1600・着回数 | 4.0 | 芝･1401Ｍ以上1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0002 |
| SHIBA_1401_1600_2CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1401_1600_3CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1401_1600_4CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1401_1600_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_1401_1600_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0009 |
| SHIBA_1601_1800_1CHAKU_HONNEN |   | 芝1601-1800・着回数 | 4.0 | 芝･1601Ｍ以上1800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0001 |
| SHIBA_1601_1800_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_1601_1800_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_1601_1800_4CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| SHIBA_1601_1800_5CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1601_1800_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0011 |
| SHIBA_1801_2000_1CHAKU_HONNEN |   | 芝1801-2000・着回数 | 4.0 | 芝･1801Ｍ以上2000M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0003 |
| SHIBA_1801_2000_2CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1801_2000_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_1801_2000_4CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1801_2000_5CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| SHIBA_1801_2000_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0008 |
| SHIBA_2001_2200_1CHAKU_HONNEN |   | 芝2001-2200・着回数 | 4.0 | 芝･2001Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0001 |
| SHIBA_2001_2200_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2001_2200_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2001_2200_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2001_2200_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_2001_2200_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_2201_2400_1CHAKU_HONNEN |   | 芝2201-2400・着回数 | 4.0 | 芝･2201Ｍ以上2400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| SHIBA_2201_2400_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2201_2400_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2201_2400_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2201_2400_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_2201_2400_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0001 |
| SHIBA_2401_2800_1CHAKU_HONNEN |   | 芝2401-2800・着回数 | 4.0 | 芝･2401Ｍ以上2800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| SHIBA_2401_2800_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2401_2800_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2401_2800_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2401_2800_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2401_2800_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_1CHAKU_HONNEN |   | 芝2801以上・着回数 | 4.0 | 芝･2801Ｍ以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| SHIBA_2801_IJO_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1200_IKA_1CHAKU_HONNEN |   | ダ1200以下・着回数 | 4.0 | ダート･1200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0004 |
| DIRT_1200_IKA_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_1200_IKA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_1200_IKA_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1200_IKA_5CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| DIRT_1200_IKA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0014 |
| DIRT_1201_1400_1CHAKU_HONNEN |   | ダ1201-1400・着回数 | 4.0 | ダート･1201Ｍ以上1400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0004 |
| DIRT_1201_1400_2CHAKU_HONNEN |   |   | 4.0 |   | 0009 |
| DIRT_1201_1400_3CHAKU_HONNEN |   |   | 4.0 |   | 0005 |
| DIRT_1201_1400_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1201_1400_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1201_1400_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0022 |
| DIRT_1401_1600_1CHAKU_HONNEN |   | ダ1401-1600・着回数 | 4.0 | ダート･1401Ｍ以上1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_1401_1600_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_1401_1600_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1401_1600_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1401_1600_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_1401_1600_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0005 |
| DIRT_1601_1800_1CHAKU_HONNEN |   | ダ1601-1800・着回数 | 4.0 | ダート･1601Ｍ以上1800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0006 |
| DIRT_1601_1800_2CHAKU_HONNEN |   |   | 4.0 |   | 0009 |
| DIRT_1601_1800_3CHAKU_HONNEN |   |   | 4.0 |   | 0005 |
| DIRT_1601_1800_4CHAKU_HONNEN |   |   | 4.0 |   | 0005 |
| DIRT_1601_1800_5CHAKU_HONNEN |   |   | 4.0 |   | 0008 |
| DIRT_1601_1800_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0030 |
| DIRT_1801_2000_1CHAKU_HONNEN |   | ダ1801-2000・着回数 | 4.0 | ダート･1801Ｍ以上2000M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0001 |
| DIRT_1801_2000_2CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| DIRT_1801_2000_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1801_2000_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1801_2000_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| DIRT_1801_2000_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0006 |
| DIRT_2001_2200_1CHAKU_HONNEN |   | ダ2001-2200・着回数 | 4.0 | ダート･2001Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2001_2200_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2001_2200_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2001_2200_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2001_2200_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2001_2200_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_1CHAKU_HONNEN |   | ダ2201-2400・着回数 | 4.0 | ダート･2201Ｍ以上2400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2201_2400_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0002 |
| DIRT_2401_2800_1CHAKU_HONNEN |   | ダ2401-2800・着回数 | 4.0 | ダート･2401Ｍ以上2800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2401_2800_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_1CHAKU_HONNEN |   | ダ2801以上・着回数 | 4.0 | ダート･2801Ｍ以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2801_IJO_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_SHIBA_1CHAKU_HONNEN |   | 札幌芝・着回数 | 4.0 | 札幌・芝での1着～5着及び着外(6着以下)の回数 | 0000 |
| SAPPORO_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SAPPORO_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0003 |
| HAKODATE_SHIBA_1CHAKU_HONNEN |   | 函館芝・着回数 | 4.0 | 函館・芝での1着～5着及び着外(6着以下)の回数 | 0001 |
| HAKODATE_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| HAKODATE_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HAKODATE_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| HAKODATE_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HAKODATE_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0005 |
| FUKUSHIMA_SHIBA_1CHAKU_HONNEN |   | 福島芝・着回数 | 4.0 | 福島・芝での1着～5着及び着外(6着以下)の回数 | 0000 |
| FUKUSHIMA_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| FUKUSHIMA_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| FUKUSHIMA_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| FUKUSHIMA_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| FUKUSHIMA_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0002 |
| NIIGATA_SHIBA_1CHAKU_HONNEN |   | 新潟芝・着回数 | 4.0 | 新潟・芝での1着～5着及び着外(6着以下)の回数 | 0000 |
| NIIGATA_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| NIIGATA_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NIIGATA_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NIIGATA_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NIIGATA_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0003 |
| TOKYO_SHIBA_1CHAKU_HONNEN |   | 東京芝・着回数 | 4.0 | 東京・芝での1着～5着及び着外(6着以下)の回数 | 0000 |
| TOKYO_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| TOKYO_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| TOKYO_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| TOKYO_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| TOKYO_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0002 |
| NAKAYAMA_SHIBA_1CHAKU_HONNEN |   | 中山芝・着回数 | 4.0 | 中山・芝での1着～5着及び着外(6着以下)の回数 | 0003 |
| NAKAYAMA_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NAKAYAMA_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| NAKAYAMA_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| NAKAYAMA_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| NAKAYAMA_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0002 |
| CHUKYO_SHIBA_1CHAKU_HONNEN |   | 中京芝・着回数 | 4.0 | 中京・芝での1着～5着及び着外(6着以下)の回数 | 0001 |
| CHUKYO_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| CHUKYO_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| CHUKYO_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| CHUKYO_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| CHUKYO_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0008 |
| KYOTO_SHIBA_1CHAKU_HONNEN |   | 京都芝・着回数 | 4.0 | 京都・芝での1着～5着及び着外(6着以下)の回数 | 0002 |
| KYOTO_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| KYOTO_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| KYOTO_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| KYOTO_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| KYOTO_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0007 |
| HANSHIN_SHIBA_1CHAKU_HONNEN |   | 阪神芝・着回数 | 4.0 | 阪神・芝での1着～5着及び着外(6着以下)の回数 | 0002 |
| HANSHIN_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HANSHIN_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HANSHIN_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HANSHIN_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0004 |
| HANSHIN_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0008 |
| KOKURA_SHIBA_1CHAKU_HONNEN |   | 小倉芝・着回数 | 4.0 | 小倉・芝での1着～5着及び着外(6着以下)の回数 | 0001 |
| KOKURA_SHIBA_2CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| KOKURA_SHIBA_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| KOKURA_SHIBA_4CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| KOKURA_SHIBA_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| KOKURA_SHIBA_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0008 |
| SAPPORO_DIRT_1CHAKU_HONNEN |   | 札幌ダ・着回数 | 4.0 | 札幌・ダートでの1着～5着及び着外(6着以下)の回数 | 0000 |
| SAPPORO_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| SAPPORO_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| SAPPORO_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0005 |
| HAKODATE_DIRT_1CHAKU_HONNEN |   | 函館ダ・着回数 | 4.0 | 函館・ダートでの1着～5着及び着外(6着以下)の回数 | 0000 |
| HAKODATE_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HAKODATE_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HAKODATE_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HAKODATE_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| HAKODATE_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0003 |
| FUKUSHIMA_DIRT_1CHAKU_HONNEN |   | 福島ダ・着回数 | 4.0 | 福島・ダートでの1着～5着及び着外(6着以下)の回数 | 0000 |
| FUKUSHIMA_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| FUKUSHIMA_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| FUKUSHIMA_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| FUKUSHIMA_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| FUKUSHIMA_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0004 |
| NIIGATA_DIRT_1CHAKU_HONNEN |   | 新潟ダ・着回数 | 4.0 | 新潟・ダートでの1着～5着及び着外(6着以下)の回数 | 0000 |
| NIIGATA_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NIIGATA_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NIIGATA_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NIIGATA_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| NIIGATA_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0004 |
| TOKYO_DIRT_1CHAKU_HONNEN |   | 東京ダ・着回数 | 4.0 | 東京・ダートでの1着～5着及び着外(6着以下)の回数 | 0001 |
| TOKYO_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| TOKYO_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| TOKYO_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| TOKYO_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| TOKYO_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0005 |
| NAKAYAMA_DIRT_1CHAKU_HONNEN |   | 中山ダ・着回数 | 4.0 | 中山・ダートでの1着～5着及び着外(6着以下)の回数 | 0002 |
| NAKAYAMA_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NAKAYAMA_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NAKAYAMA_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| NAKAYAMA_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| NAKAYAMA_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0002 |
| CHUKYO_DIRT_1CHAKU_HONNEN |   | 中京ダ・着回数 | 4.0 | 中京・ダートでの1着～5着及び着外(6着以下)の回数 | 0006 |
| CHUKYO_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| CHUKYO_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0004 |
| CHUKYO_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| CHUKYO_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| CHUKYO_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0014 |
| KYOTO_DIRT_1CHAKU_HONNEN |   | 京都ダ・着回数 | 4.0 | 京都・ダートでの1着～5着及び着外(6着以下)の回数 | 0001 |
| KYOTO_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0009 |
| KYOTO_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0005 |
| KYOTO_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| KYOTO_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0004 |
| KYOTO_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0018 |
| HANSHIN_DIRT_1CHAKU_HONNEN |   | 阪神ダ・着回数 | 4.0 | 阪神・ダートでの1着～5着及び着外(6着以下)の回数 | 0004 |
| HANSHIN_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| HANSHIN_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| HANSHIN_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| HANSHIN_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| HANSHIN_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0021 |
| KOKURA_DIRT_1CHAKU_HONNEN |   | 小倉ダ・着回数 | 4.0 | 小倉・ダートでの1着～5着及び着外(6着以下)の回数 | 0001 |
| KOKURA_DIRT_2CHAKU_HONNEN |   |   | 4.0 |   | 0003 |
| KOKURA_DIRT_3CHAKU_HONNEN |   |   | 4.0 |   | 0000 |
| KOKURA_DIRT_4CHAKU_HONNEN |   |   | 4.0 |   | 0001 |
| KOKURA_DIRT_5CHAKU_HONNEN |   |   | 4.0 |   | 0002 |
| KOKURA_DIRT_CHAKUGAI_HONNEN |   |   | 4.0 |   | 0003 |
| SAPPORO_SHOGAI_1CHAKU_HONNEN |   | 札幌障・着回数 | 4.0 | 札幌・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| SAPPORO_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_1CHAKU_HONNEN |   | 函館障・着回数 | 4.0 | 函館・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| HAKODATE_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 000  |
| FUKUSHIMA_SHOGAI_1CHAKU_HONNEN |   | 福島障・着回数 | 4.0 | 福島・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| FUKUSHIMA_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| FUKUSHIMA_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| FUKUSHIMA_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| FUKUSHIMA_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 001  |
| FUKUSHIMA_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 001  |
| NIIGATA_SHOGAI_1CHAKU_HONNEN |   | 新潟障・着回数 | 4.0 | 新潟・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| NIIGATA_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| NIIGATA_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 001  |
| NIIGATA_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| NIIGATA_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| NIIGATA_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 000  |
| TOKYO_SHOGAI_1CHAKU_HONNEN |   | 東京障・着回数 | 4.0 | 東京・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| TOKYO_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 001  |
| TOKYO_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| TOKYO_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| TOKYO_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| TOKYO_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 001  |
| NAKAYAMA_SHOGAI_1CHAKU_HONNEN |   | 中山障・着回数 | 4.0 | 中山・障害での1着～5着及び着外(6着以下)の回数 | 002  |
| NAKAYAMA_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| NAKAYAMA_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| NAKAYAMA_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| NAKAYAMA_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 001  |
| NAKAYAMA_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 003  |
| CHUKYO_SHOGAI_1CHAKU_HONNEN |   | 中京障・着回数 | 4.0 | 中京・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| CHUKYO_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| CHUKYO_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| CHUKYO_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| CHUKYO_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| CHUKYO_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 001  |
| KYOTO_SHOGAI_1CHAKU_HONNEN |   | 京都障・着回数 | 4.0 | 京都・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| KYOTO_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 003  |
| HANSHIN_SHOGAI_1CHAKU_HONNEN |   | 阪神障・着回数 | 4.0 | 阪神・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| HANSHIN_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HANSHIN_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 002  |
| HANSHIN_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HANSHIN_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| HANSHIN_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 002  |
| KOKURA_SHOGAI_1CHAKU_HONNEN |   | 小倉障・着回数 | 4.0 | 小倉・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| KOKURA_SHOGAI_2CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KOKURA_SHOGAI_3CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KOKURA_SHOGAI_4CHAKU_HONNEN |   |   | 4.0 |   | 000  |
| KOKURA_SHOGAI_5CHAKU_HONNEN |   |   | 4.0 |   | 001  |
| KOKURA_SHOGAI_CHAKUGAI_HONNEN |   |   | 4.0 |   | 000  |
| SETTEI_NEN_RUIKEI |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) | 0000 |
| HEICHI_HONSHOKIN_GOKEI_RUIKEI |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） | 0038449750 |
| SHOGAI_HONSHOKIN_GOKEI_RUIKEI |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） | 0002166200 |
| HEICHI_FUKASHOKIN_GOKEI_RUIKEI |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） | 0000575190 |
| SHOGAI_FUKASHOKIN_GOKEI_RUIKEI |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） | 0000005460 |
| SHIBA_1CHAKU_RUIKEI |   | 芝着回数 | 5.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 00059 |
| SHIBA_2CHAKU_RUIKEI |   |   | 5.0 |   | 00056 |
| SHIBA_3CHAKU_RUIKEI |   |   | 5.0 |   | 00055 |
| SHIBA_4CHAKU_RUIKEI |   |   | 5.0 |   | 00058 |
| SHIBA_5CHAKU_RUIKEI |   |   | 5.0 |   | 00063 |
| SHIBA_CHAKUGAI_RUIKEI |   |   | 5.0 |   | 00381 |
| DIRT_1CHAKU_RUIKEI |   | ダート着回数 | 5.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 00113 |
| DIRT_2CHAKU_RUIKEI |   |   | 5.0 |   | 00115 |
| DIRT_3CHAKU_RUIKEI |   |   | 5.0 |   | 00114 |
| DIRT_4CHAKU_RUIKEI |   |   | 5.0 |   | 00088 |
| DIRT_5CHAKU_RUIKEI |   |   | 5.0 |   | 00076 |
| DIRT_CHAKUGAI_RUIKEI |   |   | 5.0 |   | 00716 |
| SHOGAI_1CHAKU_RUIKEI |   | 障害着回数 | 4.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 0010  |
| SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 0013  |
| SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 0011  |
| SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 0008  |
| SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 0008  |
| SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0053  |
| SHIBA_1200_IKA_1CHAKU_RUIKEI |   | 芝1200以下・着回数 | 4.0 | 芝･1200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0022 |
| SHIBA_1200_IKA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0017 |
| SHIBA_1200_IKA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0013 |
| SHIBA_1200_IKA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0014 |
| SHIBA_1200_IKA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0012 |
| SHIBA_1200_IKA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0094 |
| SHIBA_1201_1400_1CHAKU_RUIKEI |   | 芝1201-1400・着回数 | 4.0 | 芝･1201Ｍ以上1400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0007 |
| SHIBA_1201_1400_2CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| SHIBA_1201_1400_3CHAKU_RUIKEI |   |   | 4.0 |   | 0011 |
| SHIBA_1201_1400_4CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| SHIBA_1201_1400_5CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| SHIBA_1201_1400_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0038 |
| SHIBA_1401_1600_1CHAKU_RUIKEI |   | 芝1401-1600・着回数 | 4.0 | 芝･1401Ｍ以上1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0011 |
| SHIBA_1401_1600_2CHAKU_RUIKEI |   |   | 4.0 |   | 0016 |
| SHIBA_1401_1600_3CHAKU_RUIKEI |   |   | 4.0 |   | 0011 |
| SHIBA_1401_1600_4CHAKU_RUIKEI |   |   | 4.0 |   | 0009 |
| SHIBA_1401_1600_5CHAKU_RUIKEI |   |   | 4.0 |   | 0013 |
| SHIBA_1401_1600_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0081 |
| SHIBA_1601_1800_1CHAKU_RUIKEI |   | 芝1601-1800・着回数 | 4.0 | 芝･1601Ｍ以上1800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0003 |
| SHIBA_1601_1800_2CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| SHIBA_1601_1800_3CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| SHIBA_1601_1800_4CHAKU_RUIKEI |   |   | 4.0 |   | 0014 |
| SHIBA_1601_1800_5CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| SHIBA_1601_1800_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0057 |
| SHIBA_1801_2000_1CHAKU_RUIKEI |   | 芝1801-2000・着回数 | 4.0 | 芝･1801Ｍ以上2000M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0010 |
| SHIBA_1801_2000_2CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| SHIBA_1801_2000_3CHAKU_RUIKEI |   |   | 4.0 |   | 0012 |
| SHIBA_1801_2000_4CHAKU_RUIKEI |   |   | 4.0 |   | 0011 |
| SHIBA_1801_2000_5CHAKU_RUIKEI |   |   | 4.0 |   | 0013 |
| SHIBA_1801_2000_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0068 |
| SHIBA_2001_2200_1CHAKU_RUIKEI |   | 芝2001-2200・着回数 | 4.0 | 芝･2001Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0003 |
| SHIBA_2001_2200_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2001_2200_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2001_2200_4CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| SHIBA_2001_2200_5CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| SHIBA_2001_2200_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0017 |
| SHIBA_2201_2400_1CHAKU_RUIKEI |   | 芝2201-2400・着回数 | 4.0 | 芝･2201Ｍ以上2400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0003 |
| SHIBA_2201_2400_2CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| SHIBA_2201_2400_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2201_2400_4CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| SHIBA_2201_2400_5CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| SHIBA_2201_2400_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0013 |
| SHIBA_2401_2800_1CHAKU_RUIKEI |   | 芝2401-2800・着回数 | 4.0 | 芝･2401Ｍ以上2800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| SHIBA_2401_2800_2CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| SHIBA_2401_2800_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2401_2800_4CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2401_2800_5CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| SHIBA_2401_2800_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0008 |
| SHIBA_2801_IJO_1CHAKU_RUIKEI |   | 芝2801以上・着回数 | 4.0 | 芝･2801Ｍ以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| SHIBA_2801_IJO_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_4CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_5CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SHIBA_2801_IJO_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0005 |
| DIRT_1200_IKA_1CHAKU_RUIKEI |   | ダ1200以下・着回数 | 4.0 | ダート･1200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0030 |
| DIRT_1200_IKA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0017 |
| DIRT_1200_IKA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0035 |
| DIRT_1200_IKA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0021 |
| DIRT_1200_IKA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0020 |
| DIRT_1200_IKA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0191 |
| DIRT_1201_1400_1CHAKU_RUIKEI |   | ダ1201-1400・着回数 | 4.0 | ダート･1201Ｍ以上1400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0019 |
| DIRT_1201_1400_2CHAKU_RUIKEI |   |   | 4.0 |   | 0038 |
| DIRT_1201_1400_3CHAKU_RUIKEI |   |   | 4.0 |   | 0023 |
| DIRT_1201_1400_4CHAKU_RUIKEI |   |   | 4.0 |   | 0016 |
| DIRT_1201_1400_5CHAKU_RUIKEI |   |   | 4.0 |   | 0010 |
| DIRT_1201_1400_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0128 |
| DIRT_1401_1600_1CHAKU_RUIKEI |   | ダ1401-1600・着回数 | 4.0 | ダート･1401Ｍ以上1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0002 |
| DIRT_1401_1600_2CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| DIRT_1401_1600_3CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| DIRT_1401_1600_4CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| DIRT_1401_1600_5CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| DIRT_1401_1600_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0028 |
| DIRT_1601_1800_1CHAKU_RUIKEI |   | ダ1601-1800・着回数 | 4.0 | ダート･1601Ｍ以上1800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0057 |
| DIRT_1601_1800_2CHAKU_RUIKEI |   |   | 4.0 |   | 0051 |
| DIRT_1601_1800_3CHAKU_RUIKEI |   |   | 4.0 |   | 0044 |
| DIRT_1601_1800_4CHAKU_RUIKEI |   |   | 4.0 |   | 0041 |
| DIRT_1601_1800_5CHAKU_RUIKEI |   |   | 4.0 |   | 0037 |
| DIRT_1601_1800_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0305 |
| DIRT_1801_2000_1CHAKU_RUIKEI |   | ダ1801-2000・着回数 | 4.0 | ダート･1801Ｍ以上2000M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0002 |
| DIRT_1801_2000_2CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| DIRT_1801_2000_3CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| DIRT_1801_2000_4CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| DIRT_1801_2000_5CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| DIRT_1801_2000_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0037 |
| DIRT_2001_2200_1CHAKU_RUIKEI |   | ダ2001-2200・着回数 | 4.0 | ダート･2001Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0003 |
| DIRT_2001_2200_2CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| DIRT_2001_2200_3CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| DIRT_2001_2200_4CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2001_2200_5CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| DIRT_2001_2200_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0014 |
| DIRT_2201_2400_1CHAKU_RUIKEI |   | ダ2201-2400・着回数 | 4.0 | ダート･2201Ｍ以上2400M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2201_2400_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_4CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| DIRT_2201_2400_5CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2201_2400_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0013 |
| DIRT_2401_2800_1CHAKU_RUIKEI |   | ダ2401-2800・着回数 | 4.0 | ダート･2401Ｍ以上2800M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2401_2800_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_4CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_5CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2401_2800_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_1CHAKU_RUIKEI |   | ダ2801以上・着回数 | 4.0 | ダート･2801Ｍ以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 0000 |
| DIRT_2801_IJO_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_4CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_5CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| DIRT_2801_IJO_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0000 |
| SAPPORO_SHIBA_1CHAKU_RUIKEI |   | 札幌芝・着回数 | 4.0 | 札幌・芝での1着～5着及び着外(6着以下)の回数 | 0004 |
| SAPPORO_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| SAPPORO_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| SAPPORO_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| SAPPORO_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| SAPPORO_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0038 |
| HAKODATE_SHIBA_1CHAKU_RUIKEI |   | 函館芝・着回数 | 4.0 | 函館・芝での1着～5着及び着外(6着以下)の回数 | 0004 |
| HAKODATE_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| HAKODATE_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| HAKODATE_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| HAKODATE_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| HAKODATE_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0031 |
| FUKUSHIMA_SHIBA_1CHAKU_RUIKEI |   | 福島芝・着回数 | 4.0 | 福島・芝での1着～5着及び着外(6着以下)の回数 | 0002 |
| FUKUSHIMA_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| FUKUSHIMA_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| FUKUSHIMA_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| FUKUSHIMA_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| FUKUSHIMA_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0014 |
| NIIGATA_SHIBA_1CHAKU_RUIKEI |   | 新潟芝・着回数 | 4.0 | 新潟・芝での1着～5着及び着外(6着以下)の回数 | 0005 |
| NIIGATA_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| NIIGATA_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| NIIGATA_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| NIIGATA_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| NIIGATA_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0032 |
| TOKYO_SHIBA_1CHAKU_RUIKEI |   | 東京芝・着回数 | 4.0 | 東京・芝での1着～5着及び着外(6着以下)の回数 | 0003 |
| TOKYO_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0009 |
| TOKYO_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| TOKYO_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| TOKYO_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| TOKYO_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0020 |
| NAKAYAMA_SHIBA_1CHAKU_RUIKEI |   | 中山芝・着回数 | 4.0 | 中山・芝での1着～5着及び着外(6着以下)の回数 | 0004 |
| NAKAYAMA_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| NAKAYAMA_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| NAKAYAMA_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| NAKAYAMA_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0002 |
| NAKAYAMA_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0014 |
| CHUKYO_SHIBA_1CHAKU_RUIKEI |   | 中京芝・着回数 | 4.0 | 中京・芝での1着～5着及び着外(6着以下)の回数 | 0008 |
| CHUKYO_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| CHUKYO_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0009 |
| CHUKYO_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| CHUKYO_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0013 |
| CHUKYO_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0055 |
| KYOTO_SHIBA_1CHAKU_RUIKEI |   | 京都芝・着回数 | 4.0 | 京都・芝での1着～5着及び着外(6着以下)の回数 | 0011 |
| KYOTO_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| KYOTO_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| KYOTO_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| KYOTO_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| KYOTO_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0051 |
| HANSHIN_SHIBA_1CHAKU_RUIKEI |   | 阪神芝・着回数 | 4.0 | 阪神・芝での1着～5着及び着外(6着以下)の回数 | 0008 |
| HANSHIN_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0012 |
| HANSHIN_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0011 |
| HANSHIN_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0009 |
| HANSHIN_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0014 |
| HANSHIN_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0085 |
| KOKURA_SHIBA_1CHAKU_RUIKEI |   | 小倉芝・着回数 | 4.0 | 小倉・芝での1着～5着及び着外(6着以下)の回数 | 0010 |
| KOKURA_SHIBA_2CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| KOKURA_SHIBA_3CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| KOKURA_SHIBA_4CHAKU_RUIKEI |   |   | 4.0 |   | 0009 |
| KOKURA_SHIBA_5CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| KOKURA_SHIBA_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0041 |
| SAPPORO_DIRT_1CHAKU_RUIKEI |   | 札幌ダ・着回数 | 4.0 | 札幌・ダートでの1着～5着及び着外(6着以下)の回数 | 0001 |
| SAPPORO_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| SAPPORO_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0001 |
| SAPPORO_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| SAPPORO_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| SAPPORO_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0046 |
| HAKODATE_DIRT_1CHAKU_RUIKEI |   | 函館ダ・着回数 | 4.0 | 函館・ダートでの1着～5着及び着外(6着以下)の回数 | 0002 |
| HAKODATE_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| HAKODATE_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0000 |
| HAKODATE_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| HAKODATE_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| HAKODATE_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0034 |
| FUKUSHIMA_DIRT_1CHAKU_RUIKEI |   | 福島ダ・着回数 | 4.0 | 福島・ダートでの1着～5着及び着外(6着以下)の回数 | 0004 |
| FUKUSHIMA_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| FUKUSHIMA_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| FUKUSHIMA_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| FUKUSHIMA_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| FUKUSHIMA_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0026 |
| NIIGATA_DIRT_1CHAKU_RUIKEI |   | 新潟ダ・着回数 | 4.0 | 新潟・ダートでの1着～5着及び着外(6着以下)の回数 | 0010 |
| NIIGATA_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| NIIGATA_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| NIIGATA_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| NIIGATA_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| NIIGATA_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0045 |
| TOKYO_DIRT_1CHAKU_RUIKEI |   | 東京ダ・着回数 | 4.0 | 東京・ダートでの1着～5着及び着外(6着以下)の回数 | 0007 |
| TOKYO_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0010 |
| TOKYO_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0007 |
| TOKYO_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0010 |
| TOKYO_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0006 |
| TOKYO_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0050 |
| NAKAYAMA_DIRT_1CHAKU_RUIKEI |   | 中山ダ・着回数 | 4.0 | 中山・ダートでの1着～5着及び着外(6着以下)の回数 | 0004 |
| NAKAYAMA_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| NAKAYAMA_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| NAKAYAMA_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0003 |
| NAKAYAMA_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| NAKAYAMA_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0032 |
| CHUKYO_DIRT_1CHAKU_RUIKEI |   | 中京ダ・着回数 | 4.0 | 中京・ダートでの1着～5着及び着外(6着以下)の回数 | 0026 |
| CHUKYO_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0028 |
| CHUKYO_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0025 |
| CHUKYO_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0016 |
| CHUKYO_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0012 |
| CHUKYO_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0115 |
| KYOTO_DIRT_1CHAKU_RUIKEI |   | 京都ダ・着回数 | 4.0 | 京都・ダートでの1着～5着及び着外(6着以下)の回数 | 0022 |
| KYOTO_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0022 |
| KYOTO_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0023 |
| KYOTO_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0015 |
| KYOTO_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0010 |
| KYOTO_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0125 |
| HANSHIN_DIRT_1CHAKU_RUIKEI |   | 阪神ダ・着回数 | 4.0 | 阪神・ダートでの1着～5着及び着外(6着以下)の回数 | 0030 |
| HANSHIN_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0031 |
| HANSHIN_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0030 |
| HANSHIN_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0018 |
| HANSHIN_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0019 |
| HANSHIN_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0184 |
| KOKURA_DIRT_1CHAKU_RUIKEI |   | 小倉ダ・着回数 | 4.0 | 小倉・ダートでの1着～5着及び着外(6着以下)の回数 | 0007 |
| KOKURA_DIRT_2CHAKU_RUIKEI |   |   | 4.0 |   | 0008 |
| KOKURA_DIRT_3CHAKU_RUIKEI |   |   | 4.0 |   | 0010 |
| KOKURA_DIRT_4CHAKU_RUIKEI |   |   | 4.0 |   | 0005 |
| KOKURA_DIRT_5CHAKU_RUIKEI |   |   | 4.0 |   | 0004 |
| KOKURA_DIRT_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 0059 |
| SAPPORO_SHOGAI_1CHAKU_RUIKEI |   | 札幌障・着回数 | 4.0 | 札幌・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| SAPPORO_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| SAPPORO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_1CHAKU_RUIKEI |   | 函館障・着回数 | 4.0 | 函館・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| HAKODATE_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| HAKODATE_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 000  |
| FUKUSHIMA_SHOGAI_1CHAKU_RUIKEI |   | 福島障・着回数 | 4.0 | 福島・障害での1着～5着及び着外(6着以下)の回数 | 001  |
| FUKUSHIMA_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| FUKUSHIMA_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| FUKUSHIMA_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| FUKUSHIMA_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| FUKUSHIMA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 008  |
| NIIGATA_SHOGAI_1CHAKU_RUIKEI |   | 新潟障・着回数 | 4.0 | 新潟・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| NIIGATA_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| NIIGATA_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 003  |
| NIIGATA_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| NIIGATA_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| NIIGATA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 009  |
| TOKYO_SHOGAI_1CHAKU_RUIKEI |   | 東京障・着回数 | 4.0 | 東京・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| TOKYO_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 003  |
| TOKYO_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| TOKYO_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| TOKYO_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| TOKYO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 004  |
| NAKAYAMA_SHOGAI_1CHAKU_RUIKEI |   | 中山障・着回数 | 4.0 | 中山・障害での1着～5着及び着外(6着以下)の回数 | 004  |
| NAKAYAMA_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| NAKAYAMA_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| NAKAYAMA_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| NAKAYAMA_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| NAKAYAMA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 009  |
| CHUKYO_SHOGAI_1CHAKU_RUIKEI |   | 中京障・着回数 | 4.0 | 中京・障害での1着～5着及び着外(6着以下)の回数 | 001  |
| CHUKYO_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 003  |
| CHUKYO_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| CHUKYO_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| CHUKYO_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| CHUKYO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 004  |
| KYOTO_SHOGAI_1CHAKU_RUIKEI |   | 京都障・着回数 | 4.0 | 京都・障害での1着～5着及び着外(6着以下)の回数 | 000  |
| KYOTO_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| KYOTO_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| KYOTO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 007  |
| HANSHIN_SHOGAI_1CHAKU_RUIKEI |   | 阪神障・着回数 | 4.0 | 阪神・障害での1着～5着及び着外(6着以下)の回数 | 002  |
| HANSHIN_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| HANSHIN_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| HANSHIN_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 000  |
| HANSHIN_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 001  |
| HANSHIN_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 006  |
| KOKURA_SHOGAI_1CHAKU_RUIKEI |   | 小倉障・着回数 | 4.0 | 小倉・障害での1着～5着及び着外(6着以下)の回数 | 002  |
| KOKURA_SHOGAI_2CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| KOKURA_SHOGAI_3CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| KOKURA_SHOGAI_4CHAKU_RUIKEI |   |   | 4.0 |   | 003  |
| KOKURA_SHOGAI_5CHAKU_RUIKEI |   |   | 4.0 |   | 002  |
| KOKURA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 4.0 |   | 006  |

## 追加カラム一覧

`ShussobetsuGetter.get_shussobetsu_chokyoshi()` メソッドではデフォルトで`convert_codes=True`が指定されており、以下のカラムが追加されます。

|名前|項目名|説明|例|
|:----|:----|:----|----|
|keibajo|競馬場名|KEIBAJO_CODEを場略名(3文字)に変換 <コード表 2001.競馬場コード>参照| 中山 |
