"""着度数・回収率集計のデータモデル定義モジュール."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChakudoRow:
    """1グループ分の着度数・回収率集計結果.

    Attributes:
        group (str): グループ名
        total (int): 出走総数
        wins (int): 1着数
        second (int): 2着数
        third (int): 3着数
        chakugai (int): 着外数
        win_rate (float): 勝率（%）
        fukusho_rate (float): 複勝率（%）
        tansho_kaishuu (float): 単勝回収率（%）
        fukusho_kaishuu (float): 複勝回収率（%）
    """

    group: str
    total: int
    wins: int
    second: int
    third: int
    chakugai: int
    win_rate: float
    fukusho_rate: float
    tansho_kaishuu: float
    fukusho_kaishuu: float


@dataclass
class ChakudoResult:
    """着度数集計の結果コンテナ.

    Attributes:
        success (bool): 処理成功フラグ
        rows (list[ChakudoRow]): グループ別集計行のリスト
        error (str | None): エラーメッセージ（success=Falseの場合のみ）
    """

    success: bool
    rows: list[ChakudoRow] = field(default_factory=list)
    error: str | None = None


# グループ名 → 行フィルタ条件の辞書
# 値は (min, max) のタプルまたは単一の int / str
RowsDef = dict[str, tuple[int, int] | int | str]


@dataclass
class AttrSource:
    """出走馬属性の算出方法を定義するデータクラス.

    Attributes:
        type (str): 属性算出種別。以下のいずれか:
            "past_finish_count": 過去N着以内の回数（grade_codes/keibajo_code/kyoriでフィルタ可）
            "career_count": キャリア戦数
            "prev_race_name": 前走レース名
            "debut_venue": デビュー競馬場コード
        top_n (int): 何着以内を入着とみなすか（"past_finish_count"用）
        grade_codes (list[str] | None): 対象グレードコードリスト
        keibajo_code (str | None): 対象競馬場コード
        kyori (int | None): 対象距離
    """

    type: str
    top_n: int = 1
    grade_codes: list[str] | None = None
    keibajo_code: str | None = None
    kyori: int | None = None

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "AttrSource":
        """辞書からAttrSourceを生成する.

        Args:
            d (dict[str, Any]): 属性辞書

        Returns:
            AttrSource: 生成したAttrSourceインスタンス
        """
        return AttrSource(
            type=d["type"],
            top_n=d.get("top_n", 1),
            grade_codes=d.get("grade_codes"),
            keibajo_code=d.get("keibajo_code"),
            kyori=d.get("kyori"),
        )


@dataclass
class EntryAttrDef:
    """出走馬属性集計の条件定義.

    Attributes:
        source (AttrSource): 属性算出方法
        rows (RowsDef): グループ名→行フィルタ条件の辞書
    """

    source: AttrSource
    rows: RowsDef

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "EntryAttrDef":
        """辞書からEntryAttrDefを生成する.

        Args:
            d (dict[str, Any]): 条件定義辞書。"source"キーと"rows"キーを持つ。

        Returns:
            EntryAttrDef: 生成したEntryAttrDefインスタンス
        """
        source = AttrSource.from_dict(d["source"])
        rows: RowsDef = {}
        for key, val in d["rows"].items():
            if isinstance(val, list) and len(val) == 2:
                rows[key] = (int(val[0]), int(val[1]))
            elif isinstance(val, (int, str)):
                rows[key] = val
            else:
                rows[key] = val
        return EntryAttrDef(source=source, rows=rows)
