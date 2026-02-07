# KISHU_MASTER

- レコード名: 騎手マスタ

## カラム一覧

mykeibadb公式ドキュメントに則りカラム名を大文字で記載していますが、データフレームとして取得した際はカラム名は小文字になります。

| 名前 | キー | 項目名 | バイト | 説明 | 例 |
| --- | --- | --- | --- | --- | --- |
| INSERT_TIMESTAMP |   | テーブル作成時間 | 19.0 |   | 2026-01-31 11:17:45 |
| UPDATE_TIMESTAMP |   | テーブル更新時間 | 19.0 | (現在未使用) | 0000-00-00 00:00:00 |
| RECORD_SHUBETSU_ID |   | レコード種別ID | 2.0 | KS をセットレコードフォーマットを特定する | KS |
| DATA_KUBUN |   | データ区分 | 1.0 | 1:新規登録 2:更新 | 2 |
|   |   |   |   | 0:該当レコード削除(提供ミスなどの理由による |  |
| DATA_SAKUSEI_NENGAPPI |   | データ作成年月日 | 8.0 | 西暦4桁＋月日各2桁 yyyymmdd 形式 | 20260126 |
| KISHU_CODE | ○ | 騎手コード | 5.0 |   | 00666 |
| MASSHO_KUBUN |   | 騎手抹消区分 | 1.0 | 0:現役 1:抹消 | 0 |
| MENKYO_KOFU_NENGAPPI |   | 騎手免許交付年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 | 19870301 |
| MENKYO_MASSHO_NENGAPPI |   | 騎手免許抹消年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 | 00000000 |
| SEINENGAPPI |   | 生年月日 | 8.0 | 年4桁(西暦)＋月日各2桁 yyyymmdd 形式 | 19690315 |
| KISHUMEI |   | 騎手名 | 34.0 | 全角17文字　姓＋全角空白1文字＋名　外国人の場合は連続17文字 | 武　豊 |
|   |   | 予備 | 34.0 |   |  |
| KISHUMEI_HANKAKU_KANA |   | 騎手名半角ｶﾅ | 30.0 | 半角30文字　姓15文字＋名15文字　外国人の場合は連続30文字 | ﾀｹ             ﾕﾀｶ |
| KISHUMEI_RYAKUSHO |   | 騎手名略称 | 8.0 | 全角4文字 | 武豊 |
| KISHUMEI_ENG |   | 騎手名欧字 | 80.0 | 半角80文字　姓＋半角空白1文字＋名　フルネームで記載 | Yutaka Take |
| SEIBETSU_KUBUN |   | 性別区分 | 1.0 | 1:男性　2:女性 | 1 |
| KIJO_SHIKAKU_CODE |   | 騎乗資格コード | 1.0 | <コード表 2302.騎乗資格コード>参照 | 2 |
| KISHU_MINARAI_CODE |   | 騎手見習コード | 1.0 | <コード表 2303.騎手見習コード>参照 | 0 |
| TOZAI_SHOZOKU_CODE |   | 騎手東西所属コード | 1.0 | <コード表 2301.東西所属コード>参照 | 2 |
| SHOTAI_CHIIKIMEI |   | 招待地域名 | 20.0 | 全角10文字 | 　　　　　　　　　　 |
| SHOZOKU_CHOKYOSHI_CODE |   | 所属調教師コード | 5.0 | 騎手の所属厩舎の調教師コード、フリー騎手の場合はALL0を設定 | 00000 |
| SHOZOKU_CHOKYOSHIMEI_RYAKUSHO |   | 所属調教師名略称 | 8.0 | 全角4文字 | 　　　　 |
|   |   | <初騎乗情報> | 67.0 | 平地初騎乗・障害初騎乗の順に設定 |  |
| HATSUKIJO1_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 | 1987030109010204 |
| HATSUKIJO1_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 | 15 |
| HATSUKIJO1_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 1984104395 |
| HATSUKIJO1_BAMEI |   | 馬名 | 36.0 | 全角18文字 | アグネスディクター |
| HATSUKIJO1_KAKUTEI_CHAKUJUN |   | 確定着順 | 2.0 |   | 02 |
| HATSUKIJO1_IJOKUBUN_CODE |   | 異常区分コード | 1.0 | <コード表 2101.異常区分コード>参照 | 0 |
| HATSUKIJO2_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 | 0000000000000000 |
| HATSUKIJO2_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 | 00 |
| HATSUKIJO2_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 0000000000 |
| HATSUKIJO2_BAMEI |   | 馬名 | 36.0 | 全角18文字 |  |
| HATSUKIJO2_KAKUTEI_CHAKUJUN |   | 確定着順 | 2.0 |   | 00 |
| HATSUKIJO2_IJOKUBUN_CODE |   | 異常区分コード | 1.0 | <コード表 2101.異常区分コード>参照 | 0 |
|   |   |   |   |   |  |
|   |   | <初勝利情報> | 64.0 | 平地初騎乗・障害初騎乗の順に設定 |  |
| HATSUSHORI1_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 | 1987030709010303 |
| HATSUSHORI1_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 | 11 |
| HATSUSHORI1_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 1984104395 |
| HATSUSHORI1_BAMEI |   | 馬名 | 36.0 | 全角18文字 | アグネスディクター |
| HATSUSHORI2_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 | 0000000000000000 |
| HATSUSHORI2_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 | 00 |
| HATSUSHORI2_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 0000000000 |
| HATSUSHORI2_BAMEI |   | 馬名 | 36.0 | 全角18文字 |  |
|   |   | <最近重賞勝利情報> | 163.0 | 直近の重賞勝利から順に設定 |  |
| JUSHO1_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 | 2025072707030207 |
| JUSHO1_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字 | 東海ステークス |
| JUSHO1_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 | 東海ステークス |
| JUSHO1_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 | 東海Ｓ |
| JUSHO1_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 | 東海Ｓ |
| JUSHO1_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 | C |
| JUSHO1_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 | 16 |
| JUSHO1_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 2020105599 |
| JUSHO1_BAMEI |   | 馬名 | 36.0 | 全角18文字 | ヤマニンウルス |
| : |   |   |   |   |  |
| JUSHO3_RACE_CODE |   | 年月日場回日R | 16.0 | レース詳細のキー情報 | 2025060105021212 |
| JUSHO3_KYOSOMEI_HONDAI |   | 競走名本題 | 60.0 | 全角30文字 | 目黒記念 |
| JUSHO3_KYOSOMEI_RYAKUSHO_10 |   | 競走名略称10文字 | 20.0 | 全角10文字 | 目黒記念 |
| JUSHO3_KYOSOMEI_RYAKUSHO_6 |   | 競走名略称6文字 | 12.0 | 全角6文字 | 目黒記念 |
| JUSHO3_KYOSOMEI_RYAKUSHO_3 |   | 競走名略称3文字 | 6.0 | 全角3文字 | 目黒記 |
| JUSHO3_GRADE_CODE |   | グレードコード | 1.0 | <コード表 2003.グレードコード>参照 | B |
| JUSHO3_SHUSSO_TOSU |   | 出走頭数 | 2.0 | 登録頭数から出走取消と競走除外･発走除外を除いた頭数 | 18 |
| JUSHO3_KETTO_TOROKU_BANGO |   | 血統登録番号 | 10.0 | 生年(西暦)4桁＋品種1桁<コード表2201.品種コード>参照＋数字5桁 | 2021105369 |
| JUSHO3_BAMEI |   | 馬名 | 36.0 | 全角18文字 | アドマイヤテラ |
|   |   | <本年･前年･累計成績情報> | 1052.0 | 現役騎手については本年・前年・累計の順に設定 |  |
|   |   |   |   | 引退騎手については引退年、引退前年・累計の順に設定 |  |
| SETTEI_NEN_HONNEN |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) | 2026 |
| HEICHI_HONSHOKIN_GOKEI_HONNEN |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） | 0001557300 |
| SHOGAI_HONSHOKIN_GOKEI_HONNEN |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） | 0000000000 |
| HEICHI_FUKASHOKIN_GOKEI_HONNEN |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） | 0000017030 |
| SHOGAI_FUKASHOKIN_GOKEI_HONNEN |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） | 0000000000 |
| HEICHI_1CHAKU_HONNEN |   | 平地着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 000005 |
| HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000008 |
| HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000008 |
| HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000005 |
| HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000008 |
| HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000025 |
| SHOGAI_1CHAKU_HONNEN |   | 障害着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 000000 |
| SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
|   |   | <競馬場別着回数> |   |   |  |
| SAPPORO_HEICHI_1CHAKU_HONNEN |   | 札幌平地着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| SAPPORO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_1CHAKU_HONNEN |   | 札幌障害着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| SAPPORO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_1CHAKU_HONNEN |   | 函館平地着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HAKODATE_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_1CHAKU_HONNEN |   | 函館障害着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HAKODATE_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_1CHAKU_HONNEN |   | 福島平地着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| FUKUSHIMA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_1CHAKU_HONNEN |   | 福島障害着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| FUKUSHIMA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_1CHAKU_HONNEN |   | 新潟平地着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NIIGATA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_1CHAKU_HONNEN |   | 新潟障害着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NIIGATA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_1CHAKU_HONNEN |   | 東京平地着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| TOKYO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_1CHAKU_HONNEN |   | 東京障害着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| TOKYO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_1CHAKU_HONNEN |   | 中山平地着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NAKAYAMA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_1CHAKU_HONNEN |   | 中山障害着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NAKAYAMA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_1CHAKU_HONNEN |   | 中京平地着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| CHUKYO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_1CHAKU_HONNEN |   | 中京障害着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| CHUKYO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| KYOTO_HEICHI_1CHAKU_HONNEN |   | 京都平地着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000005 |
| KYOTO_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000008 |
| KYOTO_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000008 |
| KYOTO_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000005 |
| KYOTO_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000008 |
| KYOTO_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000025 |
| KYOTO_SHOGAI_1CHAKU_HONNEN |   | 京都障害着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KYOTO_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_1CHAKU_HONNEN |   | 阪神平地着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HANSHIN_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_1CHAKU_HONNEN |   | 阪神障害着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HANSHIN_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_1CHAKU_HONNEN |   | 小倉平地着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KOKURA_HEICHI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_1CHAKU_HONNEN |   | 小倉障害着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KOKURA_SHOGAI_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
|   |   | <距離別着回数> |   |   |  |
| SHIBA_SHORT_1CHAKU_HONNEN |   | 芝16下・着回数 | 6.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000002 |
| SHIBA_SHORT_2CHAKU_HONNEN |   |   | 6.0 |   | 000002 |
| SHIBA_SHORT_3CHAKU_HONNEN |   |   | 6.0 |   | 000002 |
| SHIBA_SHORT_4CHAKU_HONNEN |   |   | 6.0 |   | 000001 |
| SHIBA_SHORT_5CHAKU_HONNEN |   |   | 6.0 |   | 000004 |
| SHIBA_SHORT_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000005 |
| SHIBA_MIDDLE_1CHAKU_HONNEN |   | 芝22下・着回数 | 6.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000001 |
| SHIBA_MIDDLE_2CHAKU_HONNEN |   |   | 6.0 |   | 000001 |
| SHIBA_MIDDLE_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHIBA_MIDDLE_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHIBA_MIDDLE_5CHAKU_HONNEN |   |   | 6.0 |   | 000001 |
| SHIBA_MIDDLE_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000007 |
| SHIBA_LONG_1CHAKU_HONNEN |   | 芝22超・着回数 | 6.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000000 |
| SHIBA_LONG_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHIBA_LONG_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHIBA_LONG_4CHAKU_HONNEN |   |   | 6.0 |   | 000001 |
| SHIBA_LONG_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| SHIBA_LONG_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000001 |
| DIRT_SHORT_1CHAKU_HONNEN |   | ダ16下・着回数 | 6.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000001 |
| DIRT_SHORT_2CHAKU_HONNEN |   |   | 6.0 |   | 000002 |
| DIRT_SHORT_3CHAKU_HONNEN |   |   | 6.0 |   | 000004 |
| DIRT_SHORT_4CHAKU_HONNEN |   |   | 6.0 |   | 000002 |
| DIRT_SHORT_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| DIRT_SHORT_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000004 |
| DIRT_MIDDLE_1CHAKU_HONNEN |   | ダ22下・着回数 | 6.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000001 |
| DIRT_MIDDLE_2CHAKU_HONNEN |   |   | 6.0 |   | 000003 |
| DIRT_MIDDLE_3CHAKU_HONNEN |   |   | 6.0 |   | 000002 |
| DIRT_MIDDLE_4CHAKU_HONNEN |   |   | 6.0 |   | 000001 |
| DIRT_MIDDLE_5CHAKU_HONNEN |   |   | 6.0 |   | 000003 |
| DIRT_MIDDLE_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000008 |
| DIRT_LONG_1CHAKU_HONNEN |   | ダ22超・着回数 | 6.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000000 |
| DIRT_LONG_2CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| DIRT_LONG_3CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| DIRT_LONG_4CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| DIRT_LONG_5CHAKU_HONNEN |   |   | 6.0 |   | 000000 |
| DIRT_LONG_CHAKUGAI_HONNEN |   |   | 6.0 |   | 000000 |
|   |   | <本年･前年･累計成績情報> | 1052.0 | 現役騎手については本年・前年・累計の順に設定 |  |
|   |   |   |   | 引退騎手については引退年、引退前年・累計の順に設定 |  |
| SETTEI_NEN_ZENNEN |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) | 2025 |
| HEICHI_HONSHOKIN_GOKEI_ZENNEN |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） | 0020822100 |
| SHOGAI_HONSHOKIN_GOKEI_ZENNEN |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） | 0000000000 |
| HEICHI_FUKASHOKIN_GOKEI_ZENNEN |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） | 0000165220 |
| SHOGAI_FUKASHOKIN_GOKEI_ZENNEN |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） | 0000000000 |
| HEICHI_1CHAKU_ZENNEN |   | 平地着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 000072 |
| HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000073 |
| HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000068 |
| HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000062 |
| HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000059 |
| HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000241 |
| SHOGAI_1CHAKU_ZENNEN |   | 障害着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 000000 |
| SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
|   |   | <競馬場別着回数> |   |   |  |
| SAPPORO_HEICHI_1CHAKU_ZENNEN |   | 札幌平地着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000007 |
| SAPPORO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000010 |
| SAPPORO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000008 |
| SAPPORO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000009 |
| SAPPORO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000007 |
| SAPPORO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000027 |
| SAPPORO_SHOGAI_1CHAKU_ZENNEN |   | 札幌障害着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| SAPPORO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_1CHAKU_ZENNEN |   | 函館平地着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000014 |
| HAKODATE_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000009 |
| HAKODATE_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000012 |
| HAKODATE_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000008 |
| HAKODATE_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000007 |
| HAKODATE_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000021 |
| HAKODATE_SHOGAI_1CHAKU_ZENNEN |   | 函館障害着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HAKODATE_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_1CHAKU_ZENNEN |   | 福島平地着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| FUKUSHIMA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000001 |
| FUKUSHIMA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000004 |
| FUKUSHIMA_SHOGAI_1CHAKU_ZENNEN |   | 福島障害着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| FUKUSHIMA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_1CHAKU_ZENNEN |   | 新潟平地着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NIIGATA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000002 |
| NIIGATA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000003 |
| NIIGATA_SHOGAI_1CHAKU_ZENNEN |   | 新潟障害着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NIIGATA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_1CHAKU_ZENNEN |   | 東京平地着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000006 |
| TOKYO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000004 |
| TOKYO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000007 |
| TOKYO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000009 |
| TOKYO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000004 |
| TOKYO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000021 |
| TOKYO_SHOGAI_1CHAKU_ZENNEN |   | 東京障害着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| TOKYO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_1CHAKU_ZENNEN |   | 中山平地着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NAKAYAMA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000001 |
| NAKAYAMA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000001 |
| NAKAYAMA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000002 |
| NAKAYAMA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000004 |
| NAKAYAMA_SHOGAI_1CHAKU_ZENNEN |   | 中山障害着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NAKAYAMA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_1CHAKU_ZENNEN |   | 中京平地着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000013 |
| CHUKYO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000009 |
| CHUKYO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000011 |
| CHUKYO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000009 |
| CHUKYO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000009 |
| CHUKYO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000028 |
| CHUKYO_SHOGAI_1CHAKU_ZENNEN |   | 中京障害着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| CHUKYO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| KYOTO_HEICHI_1CHAKU_ZENNEN |   | 京都平地着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000016 |
| KYOTO_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000019 |
| KYOTO_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| KYOTO_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000011 |
| KYOTO_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000013 |
| KYOTO_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000066 |
| KYOTO_SHOGAI_1CHAKU_ZENNEN |   | 京都障害着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KYOTO_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_1CHAKU_ZENNEN |   | 阪神平地着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000016 |
| HANSHIN_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000019 |
| HANSHIN_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| HANSHIN_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| HANSHIN_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000016 |
| HANSHIN_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000067 |
| HANSHIN_SHOGAI_1CHAKU_ZENNEN |   | 阪神障害着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HANSHIN_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_1CHAKU_ZENNEN |   | 小倉平地着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KOKURA_HEICHI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_1CHAKU_ZENNEN |   | 小倉障害着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KOKURA_SHOGAI_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_3CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_4CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
|   |   | <距離別着回数> |   |   |  |
| SHIBA_SHORT_1CHAKU_ZENNEN |   | 芝16下・着回数 | 6.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000012 |
| SHIBA_SHORT_2CHAKU_ZENNEN |   |   | 6.0 |   | 000024 |
| SHIBA_SHORT_3CHAKU_ZENNEN |   |   | 6.0 |   | 000016 |
| SHIBA_SHORT_4CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| SHIBA_SHORT_5CHAKU_ZENNEN |   |   | 6.0 |   | 000020 |
| SHIBA_SHORT_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000073 |
| SHIBA_MIDDLE_1CHAKU_ZENNEN |   | 芝22下・着回数 | 6.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000021 |
| SHIBA_MIDDLE_2CHAKU_ZENNEN |   |   | 6.0 |   | 000018 |
| SHIBA_MIDDLE_3CHAKU_ZENNEN |   |   | 6.0 |   | 000017 |
| SHIBA_MIDDLE_4CHAKU_ZENNEN |   |   | 6.0 |   | 000018 |
| SHIBA_MIDDLE_5CHAKU_ZENNEN |   |   | 6.0 |   | 000014 |
| SHIBA_MIDDLE_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000058 |
| SHIBA_LONG_1CHAKU_ZENNEN |   | 芝22超・着回数 | 6.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000003 |
| SHIBA_LONG_2CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| SHIBA_LONG_3CHAKU_ZENNEN |   |   | 6.0 |   | 000003 |
| SHIBA_LONG_4CHAKU_ZENNEN |   |   | 6.0 |   | 000003 |
| SHIBA_LONG_5CHAKU_ZENNEN |   |   | 6.0 |   | 000002 |
| SHIBA_LONG_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000016 |
| DIRT_SHORT_1CHAKU_ZENNEN |   | ダ16下・着回数 | 6.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000011 |
| DIRT_SHORT_2CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| DIRT_SHORT_3CHAKU_ZENNEN |   |   | 6.0 |   | 000012 |
| DIRT_SHORT_4CHAKU_ZENNEN |   |   | 6.0 |   | 000010 |
| DIRT_SHORT_5CHAKU_ZENNEN |   |   | 6.0 |   | 000008 |
| DIRT_SHORT_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000052 |
| DIRT_MIDDLE_1CHAKU_ZENNEN |   | ダ22下・着回数 | 6.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000025 |
| DIRT_MIDDLE_2CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| DIRT_MIDDLE_3CHAKU_ZENNEN |   |   | 6.0 |   | 000018 |
| DIRT_MIDDLE_4CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| DIRT_MIDDLE_5CHAKU_ZENNEN |   |   | 6.0 |   | 000015 |
| DIRT_MIDDLE_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000042 |
| DIRT_LONG_1CHAKU_ZENNEN |   | ダ22超・着回数 | 6.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000000 |
| DIRT_LONG_2CHAKU_ZENNEN |   |   | 6.0 |   | 000001 |
| DIRT_LONG_3CHAKU_ZENNEN |   |   | 6.0 |   | 000002 |
| DIRT_LONG_4CHAKU_ZENNEN |   |   | 6.0 |   | 000001 |
| DIRT_LONG_5CHAKU_ZENNEN |   |   | 6.0 |   | 000000 |
| DIRT_LONG_CHAKUGAI_ZENNEN |   |   | 6.0 |   | 000000 |
|   |   | <本年･前年･累計成績情報> | 1052.0 | 現役騎手については本年・前年・累計の順に設定 |  |
|   |   |   |   | 引退騎手については引退年、引退前年・累計の順に設定 |  |
| SETTEI_NEN_RUIKEI |   | 設定年 | 4.0 | 成績情報に設定されている年度(西暦) | 0000 |
| HEICHI_HONSHOKIN_GOKEI_RUIKEI |   | 平地本賞金合計 | 10.0 | 単位：百円　（中央の平地本賞金の合計） | 0974937150 |
| SHOGAI_HONSHOKIN_GOKEI_RUIKEI |   | 障害本賞金合計 | 10.0 | 単位：百円　（中央の障害本賞金の合計） | 0000000000 |
| HEICHI_FUKASHOKIN_GOKEI_RUIKEI |   | 平地付加賞金合計 | 10.0 | 単位：百円　（中央の平地付加賞金の合計） | 0018306915 |
| SHOGAI_FUKASHOKIN_GOKEI_RUIKEI |   | 障害付加賞金合計 | 10.0 | 単位：百円　（中央の障害付加賞金の合計） | 0000000000 |
| HEICHI_1CHAKU_RUIKEI |   | 平地着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 004630 |
| HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 003526 |
| HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 002842 |
| HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 002481 |
| HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 002128 |
| HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 009918 |
| SHOGAI_1CHAKU_RUIKEI |   | 障害着回数 | 6.0 | 1着～5着及び着外(6着以下)の回数（中央のみ) | 000000 |
| SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
|   |   | <競馬場別着回数> |   |   |  |
| SAPPORO_HEICHI_1CHAKU_RUIKEI |   | 札幌平地着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000167 |
| SAPPORO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000130 |
| SAPPORO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000097 |
| SAPPORO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000090 |
| SAPPORO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000073 |
| SAPPORO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000326 |
| SAPPORO_SHOGAI_1CHAKU_RUIKEI |   | 札幌障害着回数 | 6.0 | 札幌競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| SAPPORO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| SAPPORO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| HAKODATE_HEICHI_1CHAKU_RUIKEI |   | 函館平地着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000140 |
| HAKODATE_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000099 |
| HAKODATE_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000091 |
| HAKODATE_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000068 |
| HAKODATE_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000055 |
| HAKODATE_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000285 |
| HAKODATE_SHOGAI_1CHAKU_RUIKEI |   | 函館障害着回数 | 6.0 | 函館競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HAKODATE_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HAKODATE_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_HEICHI_1CHAKU_RUIKEI |   | 福島平地着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000017 |
| FUKUSHIMA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000011 |
| FUKUSHIMA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000013 |
| FUKUSHIMA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000009 |
| FUKUSHIMA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000007 |
| FUKUSHIMA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000035 |
| FUKUSHIMA_SHOGAI_1CHAKU_RUIKEI |   | 福島障害着回数 | 6.0 | 福島競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| FUKUSHIMA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| FUKUSHIMA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| NIIGATA_HEICHI_1CHAKU_RUIKEI |   | 新潟平地着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000026 |
| NIIGATA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000018 |
| NIIGATA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000013 |
| NIIGATA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000013 |
| NIIGATA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000012 |
| NIIGATA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000064 |
| NIIGATA_SHOGAI_1CHAKU_RUIKEI |   | 新潟障害着回数 | 6.0 | 新潟競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NIIGATA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NIIGATA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| TOKYO_HEICHI_1CHAKU_RUIKEI |   | 東京平地着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000478 |
| TOKYO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000387 |
| TOKYO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000325 |
| TOKYO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000266 |
| TOKYO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000273 |
| TOKYO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 001338 |
| TOKYO_SHOGAI_1CHAKU_RUIKEI |   | 東京障害着回数 | 6.0 | 東京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| TOKYO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| TOKYO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| NAKAYAMA_HEICHI_1CHAKU_RUIKEI |   | 中山平地着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000240 |
| NAKAYAMA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000177 |
| NAKAYAMA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000169 |
| NAKAYAMA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000139 |
| NAKAYAMA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000108 |
| NAKAYAMA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000549 |
| NAKAYAMA_SHOGAI_1CHAKU_RUIKEI |   | 中山障害着回数 | 6.0 | 中山競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| NAKAYAMA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| NAKAYAMA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| CHUKYO_HEICHI_1CHAKU_RUIKEI |   | 中京平地着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000357 |
| CHUKYO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000313 |
| CHUKYO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000254 |
| CHUKYO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000198 |
| CHUKYO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000188 |
| CHUKYO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000898 |
| CHUKYO_SHOGAI_1CHAKU_RUIKEI |   | 中京障害着回数 | 6.0 | 中京競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| CHUKYO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| CHUKYO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| KYOTO_HEICHI_1CHAKU_RUIKEI |   | 京都平地着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 001454 |
| KYOTO_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 001094 |
| KYOTO_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000852 |
| KYOTO_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000781 |
| KYOTO_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000612 |
| KYOTO_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 002967 |
| KYOTO_SHOGAI_1CHAKU_RUIKEI |   | 京都障害着回数 | 6.0 | 京都競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KYOTO_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KYOTO_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| HANSHIN_HEICHI_1CHAKU_RUIKEI |   | 阪神平地着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 001353 |
| HANSHIN_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 001024 |
| HANSHIN_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000806 |
| HANSHIN_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000722 |
| HANSHIN_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000645 |
| HANSHIN_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 002738 |
| HANSHIN_SHOGAI_1CHAKU_RUIKEI |   | 阪神障害着回数 | 6.0 | 阪神競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| HANSHIN_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| HANSHIN_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
| KOKURA_HEICHI_1CHAKU_RUIKEI |   | 小倉平地着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000398 |
| KOKURA_HEICHI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000273 |
| KOKURA_HEICHI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000222 |
| KOKURA_HEICHI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000195 |
| KOKURA_HEICHI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000155 |
| KOKURA_HEICHI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000718 |
| KOKURA_SHOGAI_1CHAKU_RUIKEI |   | 小倉障害着回数 | 6.0 | 小倉競馬場での1着～5着及び着外(6着以下)の回数（中央のみ） | 000000 |
| KOKURA_SHOGAI_2CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_3CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_4CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_5CHAKU_RUIKEI |   |   | 6.0 |   | 000000 |
| KOKURA_SHOGAI_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000000 |
|   |   | <距離別着回数> |   |   |  |
| SHIBA_SHORT_1CHAKU_RUIKEI |   | 芝16下・着回数 | 6.0 | 芝･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 001227 |
| SHIBA_SHORT_2CHAKU_RUIKEI |   |   | 6.0 |   | 000914 |
| SHIBA_SHORT_3CHAKU_RUIKEI |   |   | 6.0 |   | 000741 |
| SHIBA_SHORT_4CHAKU_RUIKEI |   |   | 6.0 |   | 000708 |
| SHIBA_SHORT_5CHAKU_RUIKEI |   |   | 6.0 |   | 000582 |
| SHIBA_SHORT_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 002892 |
| SHIBA_MIDDLE_1CHAKU_RUIKEI |   | 芝22下・着回数 | 6.0 | 芝･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 001062 |
| SHIBA_MIDDLE_2CHAKU_RUIKEI |   |   | 6.0 |   | 000785 |
| SHIBA_MIDDLE_3CHAKU_RUIKEI |   |   | 6.0 |   | 000647 |
| SHIBA_MIDDLE_4CHAKU_RUIKEI |   |   | 6.0 |   | 000541 |
| SHIBA_MIDDLE_5CHAKU_RUIKEI |   |   | 6.0 |   | 000485 |
| SHIBA_MIDDLE_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 002213 |
| SHIBA_LONG_1CHAKU_RUIKEI |   | 芝22超・着回数 | 6.0 | 芝･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000196 |
| SHIBA_LONG_2CHAKU_RUIKEI |   |   | 6.0 |   | 000156 |
| SHIBA_LONG_3CHAKU_RUIKEI |   |   | 6.0 |   | 000121 |
| SHIBA_LONG_4CHAKU_RUIKEI |   |   | 6.0 |   | 000115 |
| SHIBA_LONG_5CHAKU_RUIKEI |   |   | 6.0 |   | 000118 |
| SHIBA_LONG_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000407 |
| DIRT_SHORT_1CHAKU_RUIKEI |   | ダ16下・着回数 | 6.0 | ダート･1600M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 001156 |
| DIRT_SHORT_2CHAKU_RUIKEI |   |   | 6.0 |   | 000880 |
| DIRT_SHORT_3CHAKU_RUIKEI |   |   | 6.0 |   | 000726 |
| DIRT_SHORT_4CHAKU_RUIKEI |   |   | 6.0 |   | 000631 |
| DIRT_SHORT_5CHAKU_RUIKEI |   |   | 6.0 |   | 000553 |
| DIRT_SHORT_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 002489 |
| DIRT_MIDDLE_1CHAKU_RUIKEI |   | ダ22下・着回数 | 6.0 | ダート･1601Ｍ以上2200M以下での1着～5着及び着外(6着以下)の回数（中央のみ) | 000986 |
| DIRT_MIDDLE_2CHAKU_RUIKEI |   |   | 6.0 |   | 000787 |
| DIRT_MIDDLE_3CHAKU_RUIKEI |   |   | 6.0 |   | 000604 |
| DIRT_MIDDLE_4CHAKU_RUIKEI |   |   | 6.0 |   | 000485 |
| DIRT_MIDDLE_5CHAKU_RUIKEI |   |   | 6.0 |   | 000385 |
| DIRT_MIDDLE_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 001908 |
| DIRT_LONG_1CHAKU_RUIKEI |   | ダ22超・着回数 | 6.0 | ダート･2201M以上での1着～5着及び着外(6着以下)の回数（中央のみ) | 000003 |
| DIRT_LONG_2CHAKU_RUIKEI |   |   | 6.0 |   | 000004 |
| DIRT_LONG_3CHAKU_RUIKEI |   |   | 6.0 |   | 000003 |
| DIRT_LONG_4CHAKU_RUIKEI |   |   | 6.0 |   | 000001 |
| DIRT_LONG_5CHAKU_RUIKEI |   |   | 6.0 |   | 000005 |
| DIRT_LONG_CHAKUGAI_RUIKEI |   |   | 6.0 |   | 000009 |

## 追加カラム一覧

`MasterGetter.get_kishu_master()` メソッドではデフォルトで`convert_codes=True`が指定されており、以下のカラムが追加されます。

|名前|項目名|説明|例|
|:----|:----|:----|----|
|kijo_shikaku|騎乗資格|KIJO_SHIKAKU_CODEを名称に変換 <コード表 2302.騎乗資格コード>参照| 騎手 |
|kishu_minarai|騎手見習|KISHU_MINARAI_CODEを略名に変換 <コード表 2303.騎手見習コード>参照|  |
|tozai_shozoku|東西所属|TOZAI_SHOZOKU_CODEを名称に変換 <コード表 2301.東西所属コード>参照| 栗東 |
|hatsukijo1_ijokubun|初騎乗1 異常区分|HATSUKIJO1_IJOKUBUN_CODEを名称に変換 <コード表 2101.異常区分コード>参照|  |
|hatsukijo2_ijokubun|初騎乗2 異常区分|HATSUKIJO2_IJOKUBUN_CODEを名称に変換 <コード表 2101.異常区分コード>参照|  |
|jusho1_grade|重賞1 グレード|JUSHO1_GRADE_CODEを名称に変換 <コード表 2003.グレードコード>参照| GIII |
|jusho2_grade|重賞2 グレード|JUSHO2_GRADE_CODEを名称に変換 <コード表 2003.グレードコード>参照|  |
|jusho3_grade|重賞3 グレード|JUSHO3_GRADE_CODEを名称に変換 <コード表 2003.グレードコード>参照| GII |
