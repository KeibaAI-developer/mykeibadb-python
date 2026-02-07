# SHUSSOBETSU_BABA

- レコード名: 出走別着度数
- サブレコード: 出走別着度数　馬場別

## カラム一覧

mykeibadb公式ドキュメントに則りカラム名を大文字で記載していますが、データフレームとして取得した際はカラム名は小文字になります。

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   | 2026-01-22 05:25:23 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | CK をセットレコードフォーマットを特定する | CK |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 | 1 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |  |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20250911 |
| RACE_CODE | ◯ | レースコード | 16.0 | 開催年+月日+競馬場コード+回次+日次+レース番号 | 2025091506040511 |
| KAISAI_NEN |   | 開催年 | 4.0 | 該当レース施行年 西暦4桁 yyyy形式 | 2025 |
| KAISAI_GAPPI |   | 開催月日 | 4.0 | 該当レース施行月日 各2桁 mmdd形式 | 0915 |
| KEIBAJO_CODE |   | 競馬場コード | 2.0 | 該当レース施行競馬場 <コード表 2001.競馬場コード>参照 | 06 |
| KAISAI_KAIJI |   | 開催回[第N回] | 2.0 | 該当レース施行回 その競馬場でその年の何回目の開催かを示す | 04 |
| KAISAI_NICHIJI |   | 開催日目[N日目] | 2.0 | 該当レース施行日目 そのレース施行回で何日目の開催かを示す | 05 |
| RACE_BANGO |   | レース番号 | 2.0 | 該当レース番号 | 11 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10.0 | 生年(西暦)4桁＋1＋数字5桁 | 2022105081 |
| BAMEI |   | 馬名 | 36.0 | 通常全角18文字。 | ミュージアムマイル |
| HEICHI_HONSHOKIN_RUIKEI |   | 平地本賞金累計 | 9.0 | 単位：百円　（中央の平地本賞金の合計） | 002541000 |
| SHOGAI_HONSHOKIN_RUIKEI |   | 障害本賞金累計 | 9.0 | 単位：百円　（中央の障害本賞金の合計） | 000000000 |
| HEICHI_FUKASHOKIN_RUIKEI |   | 平地付加賞金累計 | 9.0 | 単位：百円　（中央の平地付加賞金の合計） | 000284790 |
| SHOGAI_FUKASHOKIN_RUIKEI |   | 障害付加賞金累計 | 9.0 | 単位：百円　（中央の障害付加賞金の合計） | 000000000 |
| HEICHI_SHUTOKUSHOKIN_RUIKEI |   | 平地収得賞金累計 | 9.0 | 単位：百円　（中央＋中央以外の平地累積収得賞金） | 001230000 |
| SHOGAI_SHUTOKUSHOKIN_RUIKEI |   | 障害収得賞金累計 | 9.0 | 単位：百円　（中央＋中央以外の障害累積収得賞金） | 000000000 |
| SOGO_1CHAKU |   | 総合着回数 | 3.0 | 1着～5着及び着外(6着以下)の回数（中央＋地方＋海外) | 003 |
| SOGO_2CHAKU |   |   | 3.0 |   | 001 |
| SOGO_3CHAKU |   |   | 3.0 |   | 001 |
| SOGO_4CHAKU |   |   | 3.0 |   | 001 |
| SOGO_5CHAKU |   |   | 3.0 |   | 000 |
| SOGO_CHAKUGAI |   |   | 3.0 |   | 001 |
| CHUO_GOKEI_1CHAKU |   | 中央合計着回数 | 3.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 003 |
| CHUO_GOKEI_2CHAKU |   |   | 3.0 |   | 001 |
| CHUO_GOKEI_3CHAKU |   |   | 3.0 |   | 001 |
| CHUO_GOKEI_4CHAKU |   |   | 3.0 |   | 001 |
| CHUO_GOKEI_5CHAKU |   |   | 3.0 |   | 000 |
| CHUO_GOKEI_CHAKUGAI |   |   | 3.0 |   | 001 |
|   |   | <馬場別着回数> |   |   |  |
| SHIBA_CHOKU_1CHAKU |   | 芝直・着回数 | 3.0 | 芝・直線コースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_CHOKU_2CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_CHOKU_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_CHOKU_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_CHOKU_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_CHOKU_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_MIGI_1CHAKU |   | 芝右・着回数 | 3.0 | 芝・右回りコースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 003 |
| SHIBA_MIGI_2CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_MIGI_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_MIGI_4CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_MIGI_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_MIGI_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_HIDARI_1CHAKU |   | 芝左・着回数 | 3.0 | 芝・左回りコースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_HIDARI_2CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_HIDARI_3CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_HIDARI_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_HIDARI_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_HIDARI_CHAKUGAI |   |   | 3.0 |   | 001 |
| DIRT_CHOKU_1CHAKU |   | ダ直・着回数 | 3.0 | ダート・直線コースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_CHOKU_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_CHOKU_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_CHOKU_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_CHOKU_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_CHOKU_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_MIGI_1CHAKU |   | ダ右・着回数 | 3.0 | ダート・右回りコースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_MIGI_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIGI_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIGI_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIGI_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIGI_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_HIDARI_1CHAKU |   | ダ左・着回数 | 3.0 | ダート・左回りコースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_HIDARI_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_HIDARI_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_HIDARI_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_HIDARI_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_HIDARI_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHOGAI_1CHAKU |   | 障害・着回数 | 3.0 | 障害レースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHOGAI_2CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_3CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_4CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_5CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_CHAKUGAI |   |   | 3.0 |   | 000 |
|   |   | <馬場状態別着回数> |   |   |  |
| SHIBA_RYO_1CHAKU |   | 芝良・着回数 | 3.0 | 芝・良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 003 |
| SHIBA_RYO_2CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_RYO_3CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_RYO_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_RYO_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_RYO_CHAKUGAI |   |   | 3.0 |   | 001 |
| SHIBA_YAYAOMO_1CHAKU |   | 芝稍・着回数 | 3.0 | 芝・稍重馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_YAYAOMO_2CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_YAYAOMO_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_YAYAOMO_4CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_YAYAOMO_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_YAYAOMO_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_OMO_1CHAKU |   | 芝重・着回数 | 3.0 | 芝・重馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_OMO_2CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_OMO_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_OMO_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_OMO_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_OMO_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_FURYO_1CHAKU |   | 芝不・着回数 | 3.0 | 芝・不良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_FURYO_2CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_FURYO_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_FURYO_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_FURYO_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_FURYO_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_RYO_1CHAKU |   | ダ良・着回数 | 3.0 | ダート・良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_RYO_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_RYO_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_RYO_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_RYO_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_RYO_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_YAYAOMO_1CHAKU |   | ダ稍・着回数 | 3.0 | ダート・稍重馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_YAYAOMO_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_YAYAOMO_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_YAYAOMO_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_YAYAOMO_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_YAYAOMO_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_OMO_1CHAKU |   | ダ重・着回数 | 3.0 | ダート・重馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_OMO_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_OMO_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_OMO_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_OMO_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_OMO_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_FURYO_1CHAKU |   | ダ不・着回数 | 3.0 | ダート・不良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_FURYO_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_FURYO_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_FURYO_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_FURYO_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_FURYO_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHOGAI_RYO_1CHAKU |   | 障良・着回数 | 3.0 | 障害レース・良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHOGAI_RYO_2CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_RYO_3CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_RYO_4CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_RYO_5CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_RYO_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHOGAI_YAYAOMO_1CHAKU |   | 障稍・着回数 | 3.0 | 障害レース・稍重馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHOGAI_YAYAOMO_2CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_YAYAOMO_3CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_YAYAOMO_4CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_YAYAOMO_5CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_YAYAOMO_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHOGAI_OMO_1CHAKU |   | 障重・着回数 | 3.0 | 障害レース・重馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHOGAI_OMO_2CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_OMO_3CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_OMO_4CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_OMO_5CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_OMO_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHOGAI_FURYO_1CHAKU |   | 障不・着回数 | 3.0 | 障害レース・不良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHOGAI_FURYO_2CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_FURYO_3CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_FURYO_4CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_FURYO_5CHAKU |   |   | 3.0 |   | 000 |
| SHOGAI_FURYO_CHAKUGAI |   |   | 3.0 |   | 000 |

## 追加カラム一覧

`ShussobetsuGetter.get_shussobetsu_baba()` メソッドではデフォルトで`convert_codes=True`が指定されており、以下のカラムが追加されます。

|名前|項目名|説明|例|
|:----|:----|:----|----|
|keibajo|競馬場名|KEIBAJO_CODEを場略名(3文字)に変換 <コード表 2001.競馬場コード>参照| 中山 |
