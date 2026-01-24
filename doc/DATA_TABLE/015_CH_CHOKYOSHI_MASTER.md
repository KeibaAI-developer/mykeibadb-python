# CHOKYOSHI_MASTER

- レコード名: 調教師マスタ

## カラム一覧

| 名前 | キー | 項目名 | バイト | 説明 |
| --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | CH をセットレコードフォーマットを特定する |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 |
|   |   |   |   | ード削除(提供ミスなどの理由による) |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 |
| CHOKYOSHI_CODE | ○ | 調教師コード | 5.0 |   |
| MASSHO_KUBUN |   | 調教師抹消区分 | 1.0 | 0:現役 1:抹消 |
| MENKYO_KOFU_NENGAPPI |   | 調教師免許交付年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 |
| MENKYO_MASSHO_NENGAPPI |   | 調教師免許抹消年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 |
| SEINENGAPPI |   | 生年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 |
| CHOKYOSHIMEI |   | 調教師名 | 34.0 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 |
| CHOKYOSHIMEI_HANKAKU_KANA |   | 調教師名半角ｶﾅ | 30.0 | 半角30文字　姓15文字＋名15文字　外国人の場合は連続30文字 |
| CHOKYOSHIMEI_RYAKUSHO |   | 調教師名略称 | 8.0 | 全角4文字 |
| CHOKYOSHIMEI_ENG |   | 調教師名欧字 | 80.0 | 半角80文字　姓＋半角空白1文字＋名　フルネームで記載 |
| SEIBETSU_KUBUN |   | 性別区分 | 1.0 | 1:男性　2:女性 |
| TOZAI_SHOZOKU_CODE |   | 調教師東西所属コード | 1.0 | <コード表 2301.東西所属コード>参照 |
| SHOTAI_CHIIKIMEI |   | 招待地域名 | 20.0 | 全角10文字 |
|   |   | <最近重賞勝利情報> | 163.0 | 直近の重賞勝利から順に設定 |
| JUSHO1_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 |
| JUSHO1_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字 |
| JUSHO1_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 |
| JUSHO1_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 |
| JUSHO1_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 |
| JUSHO1_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 |
| JUSHO1_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 |
| JUSHO1_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 |
| JUSHO1_BAMEI |   | 馬名 | 36.0 | 全角18文字 |
| : |   |   |   |   |
| JUSHO3_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 |
| JUSHO3_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字 |
| JUSHO3_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 |
| JUSHO3_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 |
| JUSHO3_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 |
| JUSHO3_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 |
| JUSHO3_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 |
| JUSHO3_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 |
| JUSHO3_BAMEI |   | 馬名 | 36.0 | 全角18文字 |
|   |   | <本年･前年･累計成績情報> | 1052.0 | 現役調教師については本年・前年・累計の順に設定 |
|   |   |   |   | 引退調教師については引退年、引退前年・累計の順に設定 |
| SETTEI_NEN_HONNEN |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) |
| HEICHI_HONSHOKIN_GOKEI_HONNEN |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） |
| SHOGAI_HONSHOKIN_GOKEI_HONNEN |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） |
| HEICHI_FUKASHOKIN_GOKEI_HONNEN |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） |
| SHOGAI_FUKASHOKIN_GOKEI_HONNEN |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） |
| HEICHI_1CHAKU_HONNEN |   | 平地着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| SHOGAI_1CHAKU_HONNEN |   | 障害着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
|   |   | <競馬場別着回数> |   |   |
| SAPPORO_HEICHI_1CHAKU_HONNEN |   | 札幌平地着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| SAPPORO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_1CHAKU_HONNEN |   | 札幌障害着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| SAPPORO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_1CHAKU_HONNEN |   | 函館平地着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HAKODATE_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_1CHAKU_HONNEN |   | 函館障害着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HAKODATE_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_1CHAKU_HONNEN |   | 福島平地着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| FUKUSHIMA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_1CHAKU_HONNEN |   | 福島障害着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| FUKUSHIMA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_1CHAKU_HONNEN |   | 新潟平地着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NIIGATA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_1CHAKU_HONNEN |   | 新潟障害着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NIIGATA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_1CHAKU_HONNEN |   | 東京平地着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| TOKYO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_1CHAKU_HONNEN |   | 東京障害着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| TOKYO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_1CHAKU_HONNEN |   | 中山平地着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NAKAYAMA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_1CHAKU_HONNEN |   | 中山障害着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NAKAYAMA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_1CHAKU_HONNEN |   | 中京平地着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| CHUKYO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_1CHAKU_HONNEN |   | 中京障害着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| CHUKYO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_1CHAKU_HONNEN |   | 京都平地着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KYOTO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_1CHAKU_HONNEN |   | 京都障害着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KYOTO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_1CHAKU_HONNEN |   | 阪神平地着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HANSHIN_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_1CHAKU_HONNEN |   | 阪神障害着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HANSHIN_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_1CHAKU_HONNEN |   | 小倉平地着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KOKURA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_1CHAKU_HONNEN |   | 小倉障害着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KOKURA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   |
|   |   | <距離別着回数> |   |   |
| SHIBA_SHORT_1CHAKU_HONNEN |   | 芝16下・着回数 | 6.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_SHORT_2CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_SHORT_3CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_SHORT_4CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_SHORT_5CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_SHORT_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_1CHAKU_HONNEN |   | 芝22下・着回数 | 6.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_MIDDLE_2CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_3CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_4CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_5CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| SHIBA_LONG_1CHAKU_HONNEN |   | 芝22超・着回数 | 6.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_LONG_2CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_LONG_3CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_LONG_4CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_LONG_5CHAKU_HONNEN |   |   | 6.0 |   |
| SHIBA_LONG_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| DIRT_SHORT_1CHAKU_HONNEN |   | ダ16下・着回数 | 6.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_SHORT_2CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_SHORT_3CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_SHORT_4CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_SHORT_5CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_SHORT_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_1CHAKU_HONNEN |   | ダ22下・着回数 | 6.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_MIDDLE_2CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_3CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_4CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_5CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_CHAKUGAI_HONNEN |   |   | 6.0 |   |
| DIRT_LONG_1CHAKU_HONNEN |   | ダ22超・着回数 | 6.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_LONG_2CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_LONG_3CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_LONG_4CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_LONG_5CHAKU_HONNEN |   |   | 6.0 |   |
| DIRT_LONG_CHAKUGAI_HONNEN |   |   | 6.0 |   |
|   |   | <本年･前年･累計成績情報> | 1052.0 | 現役調教師については本年・前年・累計の順に設定 |
|   |   |   |   | 引退調教師については引退年、引退前年・累計の順に設定 |
| SETTEI_NEN_ZENNEN |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) |
| HEICHI_HONSHOKIN_GOKEI_ZENNEN |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） |
| SHOGAI_HONSHOKIN_GOKEI_ZENNEN |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） |
| HEICHI_FUKASHOKIN_GOKEI_ZENNEN |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） |
| SHOGAI_FUKASHOKIN_GOKEI_ZENNEN |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） |
| HEICHI_1CHAKU_ZENNEN |   | 平地着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| SHOGAI_1CHAKU_ZENNEN |   | 障害着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
|   |   | <競馬場別着回数> |   |   |
| SAPPORO_HEICHI_1CHAKU_ZENNEN |   | 札幌平地着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| SAPPORO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_1CHAKU_ZENNEN |   | 札幌障害着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| SAPPORO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| SAPPORO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_1CHAKU_ZENNEN |   | 函館平地着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HAKODATE_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_1CHAKU_ZENNEN |   | 函館障害着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HAKODATE_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| HAKODATE_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_1CHAKU_ZENNEN |   | 福島平地着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| FUKUSHIMA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_1CHAKU_ZENNEN |   | 福島障害着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| FUKUSHIMA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_1CHAKU_ZENNEN |   | 新潟平地着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NIIGATA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_1CHAKU_ZENNEN |   | 新潟障害着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NIIGATA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| NIIGATA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_1CHAKU_ZENNEN |   | 東京平地着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| TOKYO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_1CHAKU_ZENNEN |   | 東京障害着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| TOKYO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| TOKYO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_1CHAKU_ZENNEN |   | 中山平地着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NAKAYAMA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_1CHAKU_ZENNEN |   | 中山障害着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NAKAYAMA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_1CHAKU_ZENNEN |   | 中京平地着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| CHUKYO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_1CHAKU_ZENNEN |   | 中京障害着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| CHUKYO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| CHUKYO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_1CHAKU_ZENNEN |   | 京都平地着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KYOTO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_1CHAKU_ZENNEN |   | 京都障害着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KYOTO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| KYOTO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_1CHAKU_ZENNEN |   | 阪神平地着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HANSHIN_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_1CHAKU_ZENNEN |   | 阪神障害着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HANSHIN_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| HANSHIN_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_1CHAKU_ZENNEN |   | 小倉平地着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KOKURA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_1CHAKU_ZENNEN |   | 小倉障害着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KOKURA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   |
| KOKURA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
|   |   | <距離別着回数> |   |   |
| SHIBA_SHORT_1CHAKU_ZENNEN |   | 芝16下・着回数 | 6.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_SHORT_2CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_SHORT_3CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_SHORT_4CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_SHORT_5CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_SHORT_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_1CHAKU_ZENNEN |   | 芝22下・着回数 | 6.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_MIDDLE_2CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_3CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_4CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_5CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_MIDDLE_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| SHIBA_LONG_1CHAKU_ZENNEN |   | 芝22超・着回数 | 6.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_LONG_2CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_LONG_3CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_LONG_4CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_LONG_5CHAKU_ZENNEN |   |   | 6.0 |   |
| SHIBA_LONG_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| DIRT_SHORT_1CHAKU_ZENNEN |   | ダ16下・着回数 | 6.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_SHORT_2CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_SHORT_3CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_SHORT_4CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_SHORT_5CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_SHORT_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_1CHAKU_ZENNEN |   | ダ22下・着回数 | 6.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_MIDDLE_2CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_3CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_4CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_5CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_MIDDLE_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
| DIRT_LONG_1CHAKU_ZENNEN |   | ダ22超・着回数 | 6.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_LONG_2CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_LONG_3CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_LONG_4CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_LONG_5CHAKU_ZENNEN |   |   | 6.0 |   |
| DIRT_LONG_CHAKUGAI_ZENNEN |   |   | 6.0 |   |
|   |   | <本年･前年･累計成績情報> | 1052.0 | 現役調教師については本年・前年・累計の順に設定 |
|   |   |   |   | 引退調教師については引退年、引退前年・累計の順に設定 |
| SETTEI_NEN_RUIKEI |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) |
| HEICHI_HONSHOKIN_GOKEI_RUIKEI |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） |
| SHOGAI_HONSHOKIN_GOKEI_RUIKEI |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） |
| HEICHI_FUKASHOKIN_GOKEI_RUIKEI |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） |
| SHOGAI_FUKASHOKIN_GOKEI_RUIKEI |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） |
| HEICHI_1CHAKU_RUIKEI |   | 平地着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| SHOGAI_1CHAKU_RUIKEI |   | 障害着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
|   |   | <競馬場別着回数> |   |   |
| SAPPORO_HEICHI_1CHAKU_RUIKEI |   | 札幌平地着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| SAPPORO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| SAPPORO_SHOGAI_1CHAKU_RUIKEI |   | 札幌障害着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| SAPPORO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| SAPPORO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| HAKODATE_HEICHI_1CHAKU_RUIKEI |   | 函館平地着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HAKODATE_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| HAKODATE_SHOGAI_1CHAKU_RUIKEI |   | 函館障害着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HAKODATE_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| HAKODATE_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_1CHAKU_RUIKEI |   | 福島平地着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| FUKUSHIMA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_1CHAKU_RUIKEI |   | 福島障害着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| FUKUSHIMA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| FUKUSHIMA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| NIIGATA_HEICHI_1CHAKU_RUIKEI |   | 新潟平地着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NIIGATA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| NIIGATA_SHOGAI_1CHAKU_RUIKEI |   | 新潟障害着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NIIGATA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| NIIGATA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| TOKYO_HEICHI_1CHAKU_RUIKEI |   | 東京平地着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| TOKYO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| TOKYO_SHOGAI_1CHAKU_RUIKEI |   | 東京障害着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| TOKYO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| TOKYO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_1CHAKU_RUIKEI |   | 中山平地着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NAKAYAMA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_1CHAKU_RUIKEI |   | 中山障害着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| NAKAYAMA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| NAKAYAMA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| CHUKYO_HEICHI_1CHAKU_RUIKEI |   | 中京平地着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| CHUKYO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| CHUKYO_SHOGAI_1CHAKU_RUIKEI |   | 中京障害着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| CHUKYO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| CHUKYO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| KYOTO_HEICHI_1CHAKU_RUIKEI |   | 京都平地着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KYOTO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| KYOTO_SHOGAI_1CHAKU_RUIKEI |   | 京都障害着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KYOTO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| KYOTO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| HANSHIN_HEICHI_1CHAKU_RUIKEI |   | 阪神平地着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HANSHIN_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| HANSHIN_SHOGAI_1CHAKU_RUIKEI |   | 阪神障害着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| HANSHIN_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| HANSHIN_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| KOKURA_HEICHI_1CHAKU_RUIKEI |   | 小倉平地着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KOKURA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| KOKURA_SHOGAI_1CHAKU_RUIKEI |   | 小倉障害着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） |
| KOKURA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   |
| KOKURA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
|   |   | <距離別着回数> |   |   |
| SHIBA_SHORT_1CHAKU_RUIKEI |   | 芝16下・着回数 | 6.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_SHORT_2CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_SHORT_3CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_SHORT_4CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_SHORT_5CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_SHORT_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| SHIBA_MIDDLE_1CHAKU_RUIKEI |   | 芝22下・着回数 | 6.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_MIDDLE_2CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_MIDDLE_3CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_MIDDLE_4CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_MIDDLE_5CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_MIDDLE_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| SHIBA_LONG_1CHAKU_RUIKEI |   | 芝22超・着回数 | 6.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) |
| SHIBA_LONG_2CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_LONG_3CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_LONG_4CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_LONG_5CHAKU_RUIKEI |   |   | 6.0 |   |
| SHIBA_LONG_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| DIRT_SHORT_1CHAKU_RUIKEI |   | ダ16下・着回数 | 6.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_SHORT_2CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_SHORT_3CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_SHORT_4CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_SHORT_5CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_SHORT_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| DIRT_MIDDLE_1CHAKU_RUIKEI |   | ダ22下・着回数 | 6.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_MIDDLE_2CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_MIDDLE_3CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_MIDDLE_4CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_MIDDLE_5CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_MIDDLE_CHAKUGAI_RUIKEI |   |   | 6.0 |   |
| DIRT_LONG_1CHAKU_RUIKEI |   | ダ22超・着回数 | 6.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) |
| DIRT_LONG_2CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_LONG_3CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_LONG_4CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_LONG_5CHAKU_RUIKEI |   |   | 6.0 |   |
| DIRT_LONG_CHAKUGAI_RUIKEI |   |   | 6.0 |   |