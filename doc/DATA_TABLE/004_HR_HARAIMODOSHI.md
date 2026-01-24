# HARAIMODOSHI

- レコード名: 払戻

## カラム一覧

|名前|キー|項目名|バイト|説明|
|:----|:----|:----|:----|:----|
|INSERT_TIMESTAMP| |テーブル作成時間|19||
|UPDATE_TIMESTAMP| |テーブル更新時間|19|(現在未使用)|
|RECORD_SHUBETSU_ID| |レコード種別ID|2|HR” をセットレコードフォーマットを特定する|
|DATA_KUBUN| |データ区分|1|1:速報成績(払戻金確定)　2:成績(月曜)9:レース中止　0:該当レコード削除(提供ミスなどの理由による)|
|DATA_SAKUSEI_NENGAPPI| |データ作成年月日|8|西暦4桁＋月日各2桁 yyyymmdd 形式|
|RACE_CODE|○|レースコード|16|開催年+月日+競馬場コード+回次+日次+レース番号|
|KAISAI_NEN| |開催年|4|該当レース施行年 西暦4桁 yyyy形式|
|KAISAI_GAPPI| |開催月日|4|該当レース施行月日 各2桁 mmdd形式|
|KEIBAJO_CODE| |競馬場コード|2|該当レース施行競馬場 <コード表 2001.競馬場コード>参照|
|KAISAI_KAIJI| |開催回[第N回]|2|該当レース施行回 その競馬場でその年の何回目の開催かを示す|
|KAISAI_NICHIJI| |開催日目[N日目]|2|該当レース施行日目 そのレース施行回で何日目の開催かを示す|
|RACE_BANGO| |レース番号|2|該当レース番号|
|TOROKU_TOSU| |登録頭数|2|出馬表発表時の登録頭数|
|SHUSSO_TOSU| |出走頭数|2|登録頭数から出走取消と競走除外･発走除外を除いた頭数|
|FUSEIRITSU_FLAG_TANSHO| |不成立フラグ　単勝|1|単勝不成立の有無　（0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_FUKUSHO| |不成立フラグ　複勝|1|複勝不成立の有無　（0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_WAKUREN| |不成立フラグ　枠連|1|枠連不成立の有無　（0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_UMAREN| |不成立フラグ　馬連|1|馬連不成立の有無　（0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_WIDE| |不成立フラグ　ワイド|1|ワイド不成立の有無（0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_YOBI| |予備|1||
|FUSEIRITSU_FLAG_UMATAN| |不成立フラグ　馬単|1|馬単不成立の有無　（0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_SANRENPUKU| |不成立フラグ　3連複|1|3連複不成立の有無 （0:不成立なし 1:不成立あり）|
|FUSEIRITSU_FLAG_SANRENTAN| |不成立フラグ　3連単|1|3連単不成立の有無 （0:不成立なし 1:不成立あり）|
|TOKUBARAI_FLAG_TANSHO| |特払フラグ　単勝|1|単勝特払の有無　（0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_FUKUSHO| |特払フラグ　複勝|1|複勝特払の有無　（0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_WAKUREN| |特払フラグ　枠連|1|枠連特払の有無　（0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_UMAREN| |特払フラグ　馬連|1|馬連特払の有無　（0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_WIDE| |特払フラグ　ワイド|1|ワイド特払の有無（0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_YOBI| |予備|1||
|TOKUBARAI_FLAG_UMATAN| |特払フラグ　馬単|1|馬単特払の有無　（0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_SANRENPUKU| |特払フラグ　3連複|1|3連複特払の有無 （0:特払なし 1:特払あり）|
|TOKUBARAI_FLAG_SANRENTAN| |特払フラグ　3連単|1|3連単特払の有無 （0:特払なし 1:特払あり）|
|HENKAN_FLAG_TANSHO| |返還フラグ　単勝|1|単勝返還の有無　（0:返還なし 1:返還あり）|
|HENKAN_FLAG_FUKUSHO| |返還フラグ　複勝|1|複勝返還の有無　（0:返還なし 1:返還あり）|
|HENKAN_FLAG_WAKUREN| |返還フラグ　枠連|1|枠連返還の有無　（0:返還なし 1:返還あり）|
|HENKAN_FLAG_UMAREN| |返還フラグ　馬連|1|馬連返還の有無　（0:返還なし 1:返還あり）|
|HENKAN_FLAG_WIDE| |返還フラグ　ワイド|1|ワイド返還の有無（0:返還なし 1:返還あり）|
|HENKAN_FLAG_YOBI| |予備|1||
|HENKAN_FLAG_UMATAN| |返還フラグ　馬単|1|馬単返還の有無　（0:返還なし 1:返還あり）|
|HENKAN_FLAG_SANRENPUKU| |返還フラグ　3連複|1|3連複返還の有無 （0:返還なし 1:返還あり）|
|HENKAN_FLAG_SANRENTAN| |返還フラグ　3連単|1|3連単返還の有無 （0:返還なし 1:返還あり）|
|HENKAN_UMABAN_JOHO1| |返還馬番情報(馬番01～28)|1|（0:返還なし 1:返還あり）　発売後取消しとなり返還対象となった馬番のエリアに “1” を設定（例）5番取消しの場合 0000100000000000000000000000|
|：| | | | |
|HENKAN_UMABAN_JOHO28| | | | |
|HENKAN_WAKUBAN_JOHO1| |返還枠番情報(枠番1～8)|1|（0:返還なし 1:返還あり）　発売後取消しとなり返還対象となった枠番のエリアに “1” を設定|
| | | | |（例）10頭だての5番取消しの場合、5枠は5番のみのため5枠はなくなる 00001000（0:返還なし 1:返還あり）　発売後取消しとなり返還対象となった枠番のエリアに “1” を設定|
| | | | |（例）10頭だての8番取消しの場合、7枠は7番、8番の登録があるため7枠は取消しにならない　　　ただし7-7は取消しになるので同枠のみ取り消しとなる 00000010|
|：| | | | |
|HENKAN_WAKUBAN_JOHO8| | | | |
|HENKAN_DOWAKU_JOHO1| |返還同枠情報(枠番1～8)|1| |
|HENKAN_DOWAKU_JOHO2| | | | |
|HENKAN_DOWAKU_JOHO3| | | | |
|HENKAN_DOWAKU_JOHO4| | | | |
|HENKAN_DOWAKU_JOHO5| | | | |
|HENKAN_DOWAKU_JOHO6| | | | |
|HENKAN_DOWAKU_JOHO7| | | | |
|HENKAN_DOWAKU_JOHO8| | | | |
| | |<単勝払戻>|13|3同着まで考慮し繰返し3回|
|TANSHO1_UMABAN| |　　馬番|2|単勝的中馬番　（00:発売なし、特払、不成立）|
|TANSHO1_HARAIMODOSHIKIN| |　　払戻金|9|単勝払戻金　（特払、不成立の金額が入る）|
|TANSHO1_NINKIJUN| |　　人気順|2|単勝人気順|
|：| | | | |
|TANSHO3_UMABAN| | | | |
|TANSHO3_HARAIMODOSHIKIN| | | | |
|TANSHO3_NINKIJUN| | | | |
| | |<複勝払戻>|13|3同着まで考慮し繰返し5回|
|FUKUSHO1_UMABAN| |　　馬番|2|複勝的中馬番　（00:発売なし、特払、不成立）|
|FUKUSHO1_HARAIMODOSHIKIN| |　　払戻金|9|複勝払戻金　（特払、不成立の金額が入る）|
|FUKUSHO1_NINKIJUN| |　　人気順|2|複勝人気順|
|：| | | | |
|FUKUSHO5_UMABAN| | | | |
|FUKUSHO5_HARAIMODOSHIKIN| | | | |
|FUKUSHO5_NINKIJUN| | | | |
| | |<枠連払戻>|13|3同着まで考慮し繰返し3回|
|WAKUREN1_KUMIBAN1| |　　組番|2|枠連的中馬番　（00:発売なし、特払、不成立）|
|WAKUREN1_KUMIBAN2| | | | |
|WAKUREN1_HARAIMODOSHIKIN| |　　払戻金|9|枠連払戻金　（特払、不成立の金額が入る）|
|WAKUREN1_NINKIJUN| |　　人気順|2|枠連人気順|
|：| | | | |
|WAKUREN3_KUMIBAN1| | | | |
|WAKUREN3_KUMIBAN2| | | | |
|WAKUREN3_HARAIMODOSHIKIN| | | | |
|WAKUREN3_NINKIJUN| | | | |
| | |<馬連払戻>|16|3同着まで考慮し繰返し3回|
|UMAREN1_KUMIBAN1| |　　組番|4|馬連的中馬番組合　（0000:発売なし、特払、不成立）|
|UMAREN1_KUMIBAN2| | | | |
|UMAREN1_HARAIMODOSHIKIN| |　　払戻金|9|馬連払戻金　（特払、不成立の金額が入る）|
|UMAREN1_NINKIJUN| |　　人気順|3|馬連人気順|
|：| | | | |
|UMAREN3_KUMIBAN1| | | | |
|UMAREN3_KUMIBAN2| | | | |
|UMAREN3_HARAIMODOSHIKIN| | | | |
|UMAREN3_NINKIJUN| | | | |
| | |<ワイド払戻>|16|3同着まで考慮し繰返し7回|
|WIDE1_KUMIBAN1| |　　組番|4|ワイド的中馬番組合　（0000:発売なし、特払、不成立）|
|WIDE1_KUMIBAN2| |　　払戻金|9|ワイド払戻金　（特払、不成立の金額が入る）|
|WIDE1_HARAIMODOSHIKIN| |　　人気順|3|ワイド人気順|
|：| | | | |
|WIDE7_KUMIBAN1| | | | |
|WIDE7_KUMIBAN2| | | | |
|WIDE7_HARAIMODOSHIKIN| | | | |
|WIDE7_NINKIJUN| | | | |
| | |<馬単払戻>|16|3同着まで考慮し繰返し6回|
|UMATAN1_KUMIBAN1| |　　組番|4|馬単的中馬番組合　（0000:発売なし、特払、不成立）|
|UMATAN1_KUMIBAN2| | | | |
|UMATAN1_HARAIMODOSHIKIN| |　　払戻金|9|馬単払戻金　（特払、不成立の金額が入る）|
|UMATAN1_NINKIJUN| |　　人気順|3|馬単人気順|
|：| | | | |
|UMATAN6_KUMIBAN1| | | | |
|UMATAN6_KUMIBAN2| | | | |
|UMATAN6_HARAIMODOSHIKIN| | | | |
|UMATAN6_NINKIJUN| | | | |
| | |<3連複払戻>|18|3同着まで考慮し繰返し3回|
|SANRENPUKU1_KUMIBAN1| |　　組番|6|3連複的中馬番組合　（000000:発売なし、特払、不成立）|
|SANRENPUKU1_KUMIBAN2| | | | |
|SANRENPUKU1_KUMIBAN3| | | | |
|SANRENPUKU1_HARAIMODOSHIKIN| |　　払戻金|9|3連複払戻金　（特払、不成立の金額が入る）|
|SANRENPUKU1_NINKIJUN| |　　人気順|3|3連複人気順|
|：| | | | |
|SANRENPUKU3_KUMIBAN1| | | | |
|SANRENPUKU3_KUMIBAN2| | | | |
|SANRENPUKU3_KUMIBAN3| | | | |
|SANRENPUKU3_HARAIMODOSHIKIN| | | | |
|SANRENPUKU3_NINKIJUN| | | | |
| | |<3連単払戻>|19|3同着まで考慮し繰返し6回|
|SANRENTAN1_KUMIBAN1| |　　組番|6|3連単的中馬番組合　（000000:発売なし、特払、不成立）|
|SANRENTAN1_KUMIBAN2| | | | |
|SANRENTAN1_KUMIBAN3| | | | |
|SANRENTAN1_HARAIMODOSHIKIN| |　　払戻金|9|3連単払戻金　（特払、不成立の金額が入る）|
|SANRENTAN1_NINKIJUN| |　　人気順|4|3連単人気順|
|：| | | | |
|SANRENTAN6_KUMIBAN1| | | | |
|SANRENTAN6_KUMIBAN2| | | | |
|SANRENTAN6_KUMIBAN3| | | | |
|SANRENTAN6_HARAIMODOSHIKIN| | | | |
|SANRENTAN6_NINKIJUN| | | | |
