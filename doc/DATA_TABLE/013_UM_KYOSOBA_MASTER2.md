# KYOSOBA_MASTER2

- レコード名: 競走馬マスタ

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   | 2026-01-22 03:37:48 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | UM をセットレコードフォーマットを特定する | UM |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規馬名登録 2:馬名変更 3:再登録(抹消後の再登録) 4:その他更新 9:抹消 | 4 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による) |  |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20260106 |
| KETTO_TOROKU_BANGO | ○ | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 2022105081 |
| MASSHO_KUBUN |   | 競走馬抹消区分 | 1.0 | 0:現役 1:抹消 | 0 |
| TOROKU_NENGAPPI |   | 競走馬登録年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 | 20240606 |
| MASSHO_NENGAPPI |   | 競走馬抹消年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 | 00000000 |
| SEINENGAPPI |   | 生年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 | 20220110 |
| BAMEI |   | 馬名 | 36.0 | 全角18文字 | ミュージアムマイル |
| BAMEI_HANKAKU_KANA |   | 馬名半角ｶﾅ | 36.0 | 半角36文字 | ﾐｭｰｼﾞｱﾑﾏｲﾙ |
| BAMEI_ENG |   | 馬名欧字 | 60.0 | 半角60文字 | Museum Mile(JPN) |
| JRA_SHISETSU_ZAIKYU_FLAG |   | JRA施設在きゅうフラグ | 1.0 | 0:JRA施設に在きゅうしていない。 1:JRA施設の在きゅうしている。 | 0 |
|   |   |   |   | JRA施設とは競馬場およびトレセンなどを指す。　(平成18年6月6日以降設定) |  |
|   |   | 予備 | 19.0 | 予備 |  |
| UMAKIGO_CODE |   | 馬記号コード | 2.0 | <コード表 2204.馬記号コード>参照 | 00 |
| SEIBETSU_CODE |   | 性別コード | 1.0 | <コード表 2202.性別コード>参照 | 1 |
| HINSHU_CODE |   | 品種コード | 1.0 | <コード表 2201.品種コード>参照 | 1 |
| MOSHOKU_CODE |   | 毛色コード | 2.0 | <コード表 2203.毛色コード>参照 | 04 |
|   |   | <3代血統情報> | 46.0 | 父･母･父父･父母･母父･母母･父父父･父父母･父母父･父母母･母父父･母父母･母母父･母母母の順に設定 |  |
| KETTO1_HANSHOKU_TOROKU_BANGO |   | 繁殖登録番号 | 10.0 | 繁殖馬マスタにリンク | 1120002395 |
| KETTO1_BAMEI |   | 馬名 | 36.0 | 全角18文字 ～ 半角36文字 （全角と半角が混在） | リオンディーズ |
|   |   |   |   | 外国の繁殖馬の場合は、16.繁殖馬マスタの10.馬名欧字の頭36バイトを設定。 |  |
| : |   |   |   |   |  |
| KETTO14_HANSHOKU_TOROKU_BANGO |   | 繁殖登録番号 | 10.0 | 繁殖馬マスタにリンク | 1220045090 |
| KETTO14_BAMEI |   | 馬名 | 36.0 | 全角18文字 ～ 半角36文字 （全角と半角が混在） | サンタフェトレイル |
|   |   |   |   | 外国の繁殖馬の場合は、16.繁殖馬マスタの10.馬名欧字の頭36バイトを設定。 |  |
| TOZAI_SHOZOKU_CODE |   | 東西所属コード | 1.0 | <コード表 2301.東西所属コード>参照 | 2 |
| CHOKYOSHI_CODE |   | 調教師コード | 5.0 | 調教師マスタへリンク | 01159 |
| CHOKYOSHIMEI_RYAKUSHO |   | 調教師名略称 | 8.0 | 全角4文字 | 高柳大輔 |
| SHOTAI_CHIIKIMEI |   | 招待地域名 | 20.0 | 全角10文字 |  |
| SEISANSHA_CODE |   | 生産者コード | 8.0 | 生産者マスタへリンク | 37312600 |
| SEISANSHAMEI_HOJINKAKU_NASHI |   | 生産者名(法人格無) | 72.0 | 全角36文字 ～ 半角72文字 （全角と半角が混在） | ノーザンファーム |
|   |   |   |   | 株式会社、有限会社などの法人格を示す文字列が頭もしくは末尾にある場合にそれを削除したものを設定。また、外国生産者の場合は、生産者マスタの8.生産者名欧字の頭70バイトを設定。 |  |
| SANCHIMEI |   | 産地名 | 20.0 | 全角10文字　または　半角20文字　(設定値が英数の場合は半角で設定） | 安平町 |
| BANUSHI_CODE |   | 馬主コード | 6.0 | 馬主マスタへリンク | 226800 |
| BANUSHIMEI_HOJINKAKU_NASHI |   | 馬主名(法人格無) | 64.0 | 全角32文字 ～ 半角64文字 （全角と半角が混在） | サンデーレーシング |
|   |   |   |   | 株式会社、有限会社などの法人格を示す文字列が頭もしくは末尾にある場合にそれを削除したものを設定。また、外国馬主の場合は、馬主マスタの8.馬主名欧字の頭64バイトを設定。 |  |
| HEICHI_HONSHOKIN_RUIKEI |   | 平地本賞金累計 | 9.0 | 単位：百円　（中央の平地本賞金の合計） | 009281000 |
| SHOGAI_HONSHOKIN_RUIKEI |   | 障害本賞金累計 | 9.0 | 単位：百円　（中央の障害本賞金の合計） | 000000000 |
| HEICHI_FUKASHOKIN_RUIKEI |   | 平地付加賞金累計 | 9.0 | 単位：百円　（中央の平地付加賞金の合計） | 000336990 |
| SHOGAI_FUKASHOKIN_RUIKEI |   | 障害付加賞金累計 | 9.0 | 単位：百円　（中央の障害付加賞金の合計） | 000000000 |
| HEICHI_SHUTOKUSHOKIN_RUIKEI |   | 平地収得賞金累計 | 9.0 | 単位：百円　（中央＋中央以外の平地累積収得賞金） | 004600000 |
| SHOGAI_SHUTOKUSHOKIN_RUIKEI |   | 障害収得賞金累計 | 9.0 | 単位：百円　（中央＋中央以外の障害累積収得賞金） | 000000000 |
| SOGO_1CHAKU |   | 総合着回数 | 3.0 | 1着～5着及び着外(6着以下)の回数（中央＋地方＋海外) | 005 |
| SOGO_2CHAKU |   |   | 3.0 |   | 002 |
| SOGO_3CHAKU |   |   | 3.0 |   | 001 |
| SOGO_4CHAKU |   |   | 3.0 |   | 001 |
| SOGO_5CHAKU |   |   | 3.0 |   | 000 |
| SOGO_CHAKUGAI |   |   | 3.0 |   | 001 |
| CHUO_GOKEI_1CHAKU |   | 中央合計着回数 | 3.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 005 |
| CHUO_GOKEI_2CHAKU |   |   | 3.0 |   | 002 |
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
| SHIBA_MIGI_1CHAKU |   | 芝右・着回数 | 3.0 | 芝・右回りコースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 005 |
| SHIBA_MIGI_2CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_MIGI_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_MIGI_4CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_MIGI_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_MIGI_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_HIDARI_1CHAKU |   | 芝左・着回数 | 3.0 | 芝・左回りコースでの1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_HIDARI_2CHAKU |   |   | 3.0 |   | 001 |
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
| SHIBA_RYO_1CHAKU |   | 芝良・着回数 | 3.0 | 芝・良馬場での1着～5着及び着外(6着以下)の回数（中央のみ) | 005 |
| SHIBA_RYO_2CHAKU |   |   | 3.0 |   | 002 |
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
|   |   | <距離別着回数> |   |   |  |
| SHIBA_SHORT_1CHAKU |   | 芝16下・着回数 | 3.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| SHIBA_SHORT_2CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_SHORT_3CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_SHORT_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_SHORT_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_SHORT_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_MIDDLE_1CHAKU |   | 芝22下・着回数 | 3.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 004 |
| SHIBA_MIDDLE_2CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_MIDDLE_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_MIDDLE_4CHAKU |   |   | 3.0 |   | 001 |
| SHIBA_MIDDLE_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_MIDDLE_CHAKUGAI |   |   | 3.0 |   | 000 |
| SHIBA_LONG_1CHAKU |   | 芝22超・着回数 | 3.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 001 |
| SHIBA_LONG_2CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_LONG_3CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_LONG_4CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_LONG_5CHAKU |   |   | 3.0 |   | 000 |
| SHIBA_LONG_CHAKUGAI |   |   | 3.0 |   | 001 |
| DIRT_SHORT_1CHAKU |   | ダ16下・着回数 | 3.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_SHORT_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_SHORT_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_SHORT_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_SHORT_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_SHORT_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_MIDDLE_1CHAKU |   | ダ22下・着回数 | 3.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_MIDDLE_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIDDLE_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIDDLE_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIDDLE_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_MIDDLE_CHAKUGAI |   |   | 3.0 |   | 000 |
| DIRT_LONG_1CHAKU |   | ダ22超・着回数 | 3.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000 |
| DIRT_LONG_2CHAKU |   |   | 3.0 |   | 000 |
| DIRT_LONG_3CHAKU |   |   | 3.0 |   | 000 |
| DIRT_LONG_4CHAKU |   |   | 3.0 |   | 000 |
| DIRT_LONG_5CHAKU |   |   | 3.0 |   | 000 |
| DIRT_LONG_CHAKUGAI |   |   | 3.0 |   | 000 |
| KYAKUSHITSU_KEIKO_NIGE |   | 脚質傾向 | 3.0 | 逃げ回数、先行回数、差し回数、追込回数を設定 | 000 |
|   |   |   |   | 過去出走レースの脚質を判定しカウントしたもの(中央レースのみ) |  |
| KYAKUSHITSU_KEIKO_SENKO |   |   | 3.0 |   | 004 |
| KYAKUSHITSU_KEIKO_SASHI |   |   | 3.0 |   | 005 |
| KYAKUSHITSU_KEIKO_OIKOMI |   |   | 3.0 |   | 001 |
| TOROKU_RACE_SU |   | 登録レース数 | 3.0 | JRA-VANに登録されている成績レース数 | 010 |
