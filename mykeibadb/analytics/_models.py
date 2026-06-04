"""着度数・回収率集計のデータモデル定義モジュール."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd


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

    @staticmethod
    def from_series(row: "pd.Series[Any]") -> "ChakudoRow":
        """DataFrameの1行からChakudoRowを生成する.

        Args:
            row (pd.Series[Any]): DataFrameの行データ

        Returns:
            ChakudoRow: 生成したChakudoRowインスタンス
        """
        grp_raw = row["grp"]
        if isinstance(grp_raw, (int, float)) and not isinstance(grp_raw, bool):
            group_str = str(int(grp_raw))
        else:
            group_str = str(grp_raw)
        return ChakudoRow(
            group=group_str,
            total=int(row["total"]),
            wins=int(row["wins"]),
            second=int(row["second"]),
            third=int(row["third"]),
            chakugai=int(row["chakugai"]),
            win_rate=float(row["win_rate"]) if pd.notna(row["win_rate"]) else 0.0,
            fukusho_rate=float(row["fukusho_rate"]) if pd.notna(row["fukusho_rate"]) else 0.0,
            tansho_kaishuu=(
                float(row["tansho_kaishuu"]) if pd.notna(row["tansho_kaishuu"]) else 0.0
            ),
            fukusho_kaishuu=(
                float(row["fukusho_kaishuu"]) if pd.notna(row["fukusho_kaishuu"]) else 0.0
            ),
        )


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
class RaceCondition:
    """レースの絞り込み条件.

    Attributes:
        keibajo_code (str | None): 競馬場コードフィルタ
        kyori (int | None): 距離フィルタ
        year_from (str | None): 集計開始年（YYYY形式）
        year_to (str | None): 集計終了年（YYYY形式）
        grade_code (str | None): グレードコードフィルタ
        kyoso_joken_codes (list[str] | None): 競走条件コードフィルタ（複数指定可）
            年齢別条件コード5カラムの最大値と比較する。
        race_shubetsu (str | None): レース種別フィルタ。「平地」または「障害」。
            track_code から導出する。
        shiba_da (str | None): 芝ダフィルタ。「芝」または「ダ」。
            track_code から導出する。
        babajotai_code (str | None): 馬場状態コードフィルタ。「1」=良、「2」=稍重、「3」=重、「4」=不良。
            shiba_babajotai_code / dirt_babajotai_code のうち有効な方と比較する。
        sayuu (str | None): 回り方向フィルタ。「左」「右」「直」。
            track_code から導出する。
        course_kubun (str | None): コース区分フィルタ。「A」〜「E」。
            week_in_course と同時指定時は build_course_week_cte でCTE処理する。
        week_in_course (int | None): コース区分使用開始からの週番号フィルタ。
            course_kubun と必ず同時に指定すること。
    """

    keibajo_code: str | None = None
    kyori: int | None = None
    year_from: str | None = None
    year_to: str | None = None
    grade_code: str | None = None
    kyoso_joken_codes: list[str] | None = None
    race_shubetsu: str | None = None
    shiba_da: str | None = None
    babajotai_code: str | None = None
    sayuu: str | None = None
    course_kubun: str | None = None
    week_in_course: int | None = None

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "RaceCondition":
        """辞書からRaceConditionを生成する.

        kyori / week_in_course は int に変換する。

        Args:
            d (dict[str, Any]): 条件辞書

        Returns:
            RaceCondition: 生成したRaceConditionインスタンス
        """
        raw_kyori = d.get("kyori")
        raw_week = d.get("week_in_course")
        return RaceCondition(
            keibajo_code=d.get("keibajo_code"),
            kyori=int(raw_kyori) if raw_kyori is not None else None,
            year_from=d.get("year_from"),
            year_to=d.get("year_to"),
            grade_code=d.get("grade_code"),
            kyoso_joken_codes=d.get("kyoso_joken_codes"),
            race_shubetsu=d.get("race_shubetsu"),
            shiba_da=d.get("shiba_da"),
            babajotai_code=d.get("babajotai_code"),
            sayuu=d.get("sayuu"),
            course_kubun=d.get("course_kubun"),
            week_in_course=int(raw_week) if raw_week is not None else None,
        )


class Subject(Enum):
    """着度数集計の主体."""

    UMA = "uma"
    KISHU = "kishu"
    CHOKYOSHI = "chokyoshi"
    BANUSHI = "banushi"
    SIRE = "sire"
    SEISANSHA = "seisansha"


@dataclass
class ChokyoThreshold:
    """調教タイムの1閾値条件.

    Attributes:
        course (str): "wood"（ウッドチップ）または "hanro"（坂路）
        metric (str): "gokei"（合計タイム）または "lap"（指定ハロン目のラップ）
        furlong (int): 対象ハロン数（gokei=合計対象, lap=何ハロン目）
        max_value (int | None): 上限（0.1秒単位、以下）
        min_value (int | None): 下限（0.1秒単位、以上）
        tracen_kubun (str | None): トレセン区分（'0'=美浦, '1'=栗東）
    """

    course: str
    metric: str
    furlong: int
    max_value: int | None = None
    min_value: int | None = None
    tracen_kubun: str | None = None


ChokyoCondition = list[ChokyoThreshold]


@dataclass
class AttrSource:
    """出走馬属性の算出方法を定義するデータクラス.

    Attributes:
        type (str): 属性算出種別。以下のいずれか:
            "past_finish_count": 過去N着以内の回数（grade_codes/keibajo_code/kyoriでフィルタ可）
            "career_count": キャリア戦数
            "prev_race_name": 前走レース名
            "debut_venue": デビュー競馬場コード
            "jockey_continuity": 騎手継続性（継続/乗り戻り/テン乗り）
            "sire_condition_finisher": 父馬の条件戦好走有無（condition/top_nでフィルタ）
        top_n (int): 何着以内を入着とみなすか（"past_finish_count"/"sire_condition_finisher"用）
        grade_codes (list[str] | None): 対象グレードコードリスト
        keibajo_code (str | None): 対象競馬場コード
        kyori (int | None): 対象距離
        condition (RaceCondition | None): レース絞り込み条件
    """

    type: str
    top_n: int = 1
    grade_codes: list[str] | None = None
    keibajo_code: str | None = None
    kyori: int | None = None
    condition: RaceCondition | None = None

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "AttrSource":
        """辞書からAttrSourceを生成する.

        Args:
            d (dict[str, Any]): 属性辞書

        Returns:
            AttrSource: 生成したAttrSourceインスタンス
        """
        raw_kyori = d.get("kyori")
        raw_condition = d.get("condition")
        condition: RaceCondition | None = None
        if raw_condition is not None:
            condition = RaceCondition.from_dict(raw_condition)
        return AttrSource(
            type=d["type"],
            top_n=int(d.get("top_n", 1)),
            grade_codes=d.get("grade_codes"),
            keibajo_code=d.get("keibajo_code"),
            kyori=int(raw_kyori) if raw_kyori is not None else None,
            condition=condition,
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

        Raises:
            ValueError: rows の値が (min, max) タプル・int・str 以外の場合
        """
        source = AttrSource.from_dict(d["source"])
        rows: RowsDef = {}
        for key, val in d["rows"].items():
            if isinstance(val, list) and len(val) == 2:
                rows[key] = (int(val[0]), int(val[1]))
            elif isinstance(val, (int, str)):
                rows[key] = val
            else:
                raise ValueError(
                    f"rows['{key}'] の値が無効です: {val!r}。"
                    "(min, max) タプル・int・str のいずれかを指定してください。"
                )
        return EntryAttrDef(source=source, rows=rows)
