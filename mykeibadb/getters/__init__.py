"""テーブルデータ取得クラス群.

このモジュールは、各テーブルに対してキーや期間を指定してデータを取得するクラスを提供する。
各クラスはドメインごとにグループ化されており、それぞれのテーブルに対するアクセスメソッドを持つ。

Classes:
    BaseGetter: すべてのGetterクラスの基底クラス
    RaceGetter: レース関連テーブル（7テーブル）
    HyosuGetter: 票数関連テーブル（10テーブル）
    OddsGetter: オッズ関連テーブル（14テーブル）
    MasterGetter: マスタデータテーブル（8テーブル）
    ShussobetsuGetter: 出走別データテーブル（7テーブル）
    ChokyoGetter: 調教データテーブル（2テーブル）
    KyosobaGetter: 競走馬詳細情報テーブル（3テーブル）
    MiningGetter: データマイニング予想テーブル（2テーブル）
    Win5Getter: WIN5テーブル（2テーブル）
    SokuhoGetter: 速報テーブル（7テーブル）
    OthersGetter: その他テーブル（1テーブル）
"""

from mykeibadb.getters.base import BaseGetter
from mykeibadb.getters.chokyo import ChokyoGetter
from mykeibadb.getters.hyosu import HyosuGetter
from mykeibadb.getters.kyosoba import KyosobaGetter
from mykeibadb.getters.master import MasterGetter
from mykeibadb.getters.mining import MiningGetter
from mykeibadb.getters.odds import OddsGetter
from mykeibadb.getters.others import OthersGetter
from mykeibadb.getters.race import RaceGetter
from mykeibadb.getters.shussobetsu import ShussobetsuGetter
from mykeibadb.getters.sokuho import SokuhoGetter
from mykeibadb.getters.win5 import Win5Getter

__all__ = [
    "BaseGetter",
    "RaceGetter",
    "HyosuGetter",
    "OddsGetter",
    "MasterGetter",
    "ShussobetsuGetter",
    "ChokyoGetter",
    "KyosobaGetter",
    "MiningGetter",
    "Win5Getter",
    "SokuhoGetter",
    "OthersGetter",
]
