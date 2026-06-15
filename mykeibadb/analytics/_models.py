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
        babajotai_codes (list[str] | None): 馬場状態コードフィルタ（複数指定可）。
            「1」=良、「2」=稍重、「3」=重、「4」=不良。
            shiba_babajotai_code / dirt_babajotai_code のうち有効な方と比較する。
        sayuu (str | None): 回り方向フィルタ。「左」「右」「直」。
            track_code から導出する。
        course_kubun (str | None): コース区分フィルタ。「A」〜「E」。
            week_in_course と同時指定時は build_course_week_cte でCTE処理する。
        week_in_course (int | None): コース区分使用開始からの週番号フィルタ。
            course_kubun と必ず同時に指定すること。
        tokubetsu_kyoso_bango (str | None): 特別競走番号フィルタ。race_shosai の
            tokubetsu_kyoso_bango と完全一致で比較する。
        keibajo_codes (list[str] | None): 競馬場コードフィルタ（複数指定可）。
        kaisai_nichime (list[int] | None): 開催日目フィルタ（複数指定可）。
    """

    kyori: int | None = None
    year_from: str | None = None
    year_to: str | None = None
    grade_code: str | None = None
    kyoso_joken_codes: list[str] | None = None
    race_shubetsu: str | None = None
    shiba_da: str | None = None
    babajotai_codes: list[str] | None = None
    sayuu: str | None = None
    course_kubun: str | None = None
    week_in_course: int | None = None
    tokubetsu_kyoso_bango: str | None = None
    keibajo_codes: list[str] | None = None
    kaisai_nichime: list[int] | None = None

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "RaceCondition":
        """辞書からRaceConditionを生成する.

        kyori / week_in_course / kaisai_nichime は int に変換する。

        Args:
            d (dict[str, Any]): 条件辞書

        Returns:
            RaceCondition: 生成したRaceConditionインスタンス
        """
        raw_kyori = d.get("kyori")
        raw_week = d.get("week_in_course")
        raw_kaisai_nichime = d.get("kaisai_nichime")
        return RaceCondition(
            kyori=int(raw_kyori) if raw_kyori is not None else None,
            year_from=d.get("year_from"),
            year_to=d.get("year_to"),
            grade_code=d.get("grade_code"),
            kyoso_joken_codes=d.get("kyoso_joken_codes"),
            race_shubetsu=d.get("race_shubetsu"),
            shiba_da=d.get("shiba_da"),
            babajotai_codes=d.get("babajotai_codes"),
            sayuu=d.get("sayuu"),
            course_kubun=d.get("course_kubun"),
            week_in_course=int(raw_week) if raw_week is not None else None,
            tokubetsu_kyoso_bango=d.get("tokubetsu_kyoso_bango"),
            keibajo_codes=d.get("keibajo_codes"),
            kaisai_nichime=(
                [int(v) for v in raw_kaisai_nichime] if raw_kaisai_nichime is not None else None
            ),
        )


class Subject(Enum):
    """着度数集計の主体.

    Attributes:
        UMA (str): 馬
        KISHU (str): 騎手
        CHOKYOSHI (str): 調教師
        BANUSHI (str): 馬主
        SIRE (str): 父馬
        SEISANSHA (str): 生産者
    """

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

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "ChokyoThreshold":
        """辞書からChokyoThresholdを生成する.

        Args:
            d (dict[str, Any]): 閾値条件辞書。"course"・"metric"・"furlong"
                キーが必須。"max_value"・"min_value"・"tracen_kubun"は任意。

        Returns:
            ChokyoThreshold: 生成したChokyoThresholdインスタンス
        """
        raw_max = d.get("max_value")
        raw_min = d.get("min_value")
        return ChokyoThreshold(
            course=d["course"],
            metric=d["metric"],
            furlong=int(d["furlong"]),
            max_value=int(raw_max) if raw_max is not None else None,
            min_value=int(raw_min) if raw_min is not None else None,
            tracen_kubun=d.get("tracen_kubun"),
        )


ChokyoCondition = list[ChokyoThreshold]


@dataclass
class AttrSource:
    """出走馬属性の算出方法を定義するデータクラス.

    Attributes:
        type (str): 属性算出種別。以下のいずれか:
            "past_race_top_n_count": 過去レースの集計（top_n/grade_codes/keibajo_codes/filtersでフィルタ可）
            "career_count": キャリア戦数
            "prev_race_name": 前走レース名
            "debut_venue": デビュー競馬場コード
            "jockey_continuity": 騎手継続性（継続/乗り戻り/テン乗り）
            "sire_condition_finisher": 父馬の条件戦好走有無（condition/top_nでフィルタ）
            "prev_race_col": 前走の任意列値（column で対象列を指定。filtersで前走の別列を
                条件に絞り込み、条件を満たさない場合はNULL（fixedの全行から除外）にできる）
            "same_race_prev_year_finish": 前年同特別競走番号レースでの確定着順
        top_n (int | None): 何着以内を入着とみなすか（"sire_condition_finisher"用は既定1）。
            "past_race_top_n_count" で None の場合は着順で絞り込まない。
        grade_codes (list[str] | None): 対象グレードコードリスト
        keibajo_codes (list[str] | None): 対象競馬場コードリスト（"past_race_top_n_count"用）
        condition (RaceCondition | None): レース絞り込み条件
        allowed_values (list[str] | None): 表示を許可する属性値リスト（"debut_venue"用）
        column (str | None): 前走列名（"prev_race_col"用）
        overseas_label (str | None): 海外開催集約ラベル（"prev_race_name"用）
        tokubetsu_kyoso_bango (str | None): 対象特別競走番号（"same_race_prev_year_finish"用）
        absent_label (str): 不出走ラベル（"same_race_prev_year_finish"用）
        filters (list[dict[str, Any]] | None): 汎用フィルタ（"past_race_top_n_count"用）。
            各要素は {"column": horse_histの列名, "op": 演算子, "value": 比較値} の形式。
    """

    type: str
    top_n: int | None = 1
    grade_codes: list[str] | None = None
    keibajo_codes: list[str] | None = None
    condition: RaceCondition | None = None
    allowed_values: list[str] | None = None
    column: str | None = None
    overseas_label: str | None = None
    tokubetsu_kyoso_bango: str | None = None
    absent_label: str = "出走無し"
    filters: list[dict[str, Any]] | None = None

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "AttrSource":
        """辞書からAttrSourceを生成する.

        "past_race_top_n_count" で top_n 未指定時は None（着順で絞り込まない）。
        それ以外の type で top_n 未指定時は既定値 1。

        Args:
            d (dict[str, Any]): 属性辞書

        Returns:
            AttrSource: 生成したAttrSourceインスタンス
        """
        raw_condition = d.get("condition")
        raw_top_n = d.get("top_n")
        condition: RaceCondition | None = None
        if raw_condition is not None:
            condition = RaceCondition.from_dict(raw_condition)
        if raw_top_n is None and d["type"] == "past_race_top_n_count":
            top_n: int | None = None
        else:
            top_n = int(raw_top_n) if raw_top_n is not None else 1
        return AttrSource(
            type=d["type"],
            top_n=top_n,
            grade_codes=d.get("grade_codes"),
            keibajo_codes=d.get("keibajo_codes"),
            condition=condition,
            allowed_values=d.get("allowed_values"),
            column=d.get("column"),
            overseas_label=d.get("overseas_label"),
            tokubetsu_kyoso_bango=d.get("tokubetsu_kyoso_bango"),
            absent_label=d.get("absent_label", "出走無し"),
            filters=d.get("filters"),
        )


@dataclass
class RaceColFilter:
    """対象レースにおける馬の列値で絞り込む（枠・人気・脚質等）.

    u.* / r.* の列に対する IN もしくは数値範囲の述語。

    Attributes:
        column (str): 絞り込む列名（例: "u.wakuban"）
        values (list[str] | None): IN 条件（例: ["1","2","3"]）
        min_value (int | None): 範囲下限（以上）
        max_value (int | None): 範囲上限（以下）
    """

    column: str
    values: list[str] | None = None
    min_value: int | None = None
    max_value: int | None = None


@dataclass
class SubjectFilter:
    """主体の一致で絞り込む（種牡馬・騎手・調教師・馬主・生産者）.

    Attributes:
        subject (Subject): 絞り込む主体
        name (str | None): 主体名（部分一致）
        code (str | None): 主体コード（完全一致。code対応主体のみ）
    """

    subject: Subject
    name: str | None = None
    code: str | None = None


@dataclass
class HistoryFilter:
    """馬の過去履歴で絞り込む（旧 AttrSource）.

    source で算出した属性値が cond を満たす馬×レースのみ通す。

    Attributes:
        source (AttrSource): 属性算出方法の定義
        cond (tuple[int, int] | int | str): 絞り込み条件。
            (min, max) の場合は範囲一致、int/str の場合は完全一致。
    """

    source: AttrSource
    cond: tuple[int, int] | int | str


@dataclass
class ChokyoFilter:
    """対象レース直前の調教で絞り込む（旧 ChokyoCondition）.

    対象レース日より前の最新調教窓が全閾値を満たす馬×レースのみ通す。

    Attributes:
        condition (ChokyoCondition): 調教閾値条件リスト
    """

    condition: ChokyoCondition


EntryFilter = RaceColFilter | SubjectFilter | HistoryFilter | ChokyoFilter


@dataclass
class GroupBy:
    """集計のグループ分け軸.

    kind と各種パラメータで「何でグループ化するか」を表す。

    Attributes:
        kind (str): グループ軸の種別。以下のいずれか:
            "race_col": column のDISTINCT値（枠別・人気別）
            "subject": subject の名称（騎手別・種牡馬別）
            "history": source の属性値（デビュー地別・前走名別）
            "fixed": rows 定義に従う固定ビン
        column (str | None): "race_col" 時の列名
        subject (Subject | None): "subject" 時の主体
        source (AttrSource | None): "history" 時の属性算出定義
        rows (RowsDef | None): "fixed" 時のグループ定義
    """

    kind: str
    column: str | None = None
    subject: Subject | None = None
    source: AttrSource | None = None
    rows: RowsDef | None = None

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "GroupBy":
        """辞書からGroupByを生成する.

        Args:
            d (dict[str, Any]): グループ分け軸の辞書。"kind"キーが必須。
                kind に応じて以下のキーが必須:
                "race_col" -> "column"、"subject" -> "subject"、
                "history" -> "source"、"fixed" -> "source"・"rows"

        Returns:
            GroupBy: 生成したGroupByインスタンス

        Raises:
            ValueError: kind が未対応、または kind に必要なキーが欠落した場合
        """
        kind = d["kind"]
        if kind == "race_col":
            if "column" not in d:
                raise ValueError("GroupBy.kind='race_col' には column が必要です。")
            return GroupBy(kind=kind, column=d["column"])
        if kind == "subject":
            if "subject" not in d:
                raise ValueError("GroupBy.kind='subject' には subject が必要です。")
            return GroupBy(kind=kind, subject=Subject(d["subject"]))
        if kind == "history":
            if "source" not in d:
                raise ValueError("GroupBy.kind='history' には source が必要です。")
            return GroupBy(kind=kind, source=AttrSource.from_dict(d["source"]))
        if kind == "fixed":
            if "source" not in d or "rows" not in d:
                raise ValueError("GroupBy.kind='fixed' には source と rows が必要です。")
            return GroupBy(
                kind=kind,
                source=AttrSource.from_dict(d["source"]),
                rows=parse_rows_def(d["rows"]),
            )
        raise ValueError(f"未対応の kind です: {kind!r}")


@dataclass
class Entry:
    """絞り込み後の1エントリ（馬×レース）.

    Attributes:
        ketto_toroku_bango (str): 血統登録番号
        race_code (str): レースコード
        umaban (str): 馬番
        group_label (str): グループラベル（GroupBy未指定時は "全体"）
    """

    ketto_toroku_bango: str
    race_code: str
    umaban: str
    group_label: str


EntrySet = list[Entry]


@dataclass
class GroupTally:
    """グループ別の着順カウント・払戻合計（フェーズ2出力）.

    Attributes:
        group (str): グループラベル
        total (int): 出走総数
        wins (int): 1着数
        second (int): 2着数
        third (int): 3着数
        chakugai (int): 着外数
        tansho_payout_sum (int): 単勝払戻合計
        fukusho_payout_sum (int): 複勝払戻合計
    """

    group: str
    total: int
    wins: int
    second: int
    third: int
    chakugai: int
    tansho_payout_sum: int
    fukusho_payout_sum: int


ChakudoTally = list[GroupTally]


def parse_rows_def(rows: dict[str, Any]) -> RowsDef:
    """辞書を RowsDef（グループ名→行フィルタ条件）に変換する.

    Args:
        rows (dict[str, Any]): グループ名→条件の辞書。条件は長さ2のリスト
            （(min, max) 範囲）、int、str のいずれか。

    Returns:
        RowsDef: 変換済みのグループ名→行フィルタ条件の辞書

    Raises:
        ValueError: 値が (min, max) リスト・int・str 以外の場合
    """
    result: RowsDef = {}
    for key, val in rows.items():
        if isinstance(val, list) and len(val) == 2:
            result[key] = (int(val[0]), int(val[1]))
        elif isinstance(val, (int, str)):
            result[key] = val
        else:
            raise ValueError(
                f"rows['{key}'] の値が無効です: {val!r}。"
                "(min, max) タプル・int・str のいずれかを指定してください。"
            )
    return result


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
        rows = parse_rows_def(d["rows"])
        return EntryAttrDef(source=source, rows=rows)


def build_entry_filter(d: dict[str, Any]) -> EntryFilter:
    """辞書からEntryFilterを生成する.

    "type" キーで RaceColFilter / SubjectFilter / HistoryFilter / ChokyoFilter
    のいずれを生成するかを判定する。

    Args:
        d (dict[str, Any]): エントリフィルタ辞書。"type"キーが必須。
            "race_col": "column"・"values"・"min_value"・"max_value"
            "subject": "subject"・"name"・"code"
            "history": "source"・"cond"
            "chokyo": "condition"（ChokyoThreshold辞書のリスト）

    Returns:
        EntryFilter: 生成したフィルタインスタンス

    Raises:
        ValueError: type が未対応の場合
    """
    filter_type = d["type"]
    if filter_type == "race_col":
        return RaceColFilter(
            column=d["column"],
            values=d.get("values"),
            min_value=d.get("min_value"),
            max_value=d.get("max_value"),
        )
    if filter_type == "subject":
        return SubjectFilter(
            subject=Subject(d["subject"]),
            name=d.get("name"),
            code=d.get("code"),
        )
    if filter_type == "history":
        return HistoryFilter(
            source=AttrSource.from_dict(d["source"]),
            cond=_parse_history_cond(d["cond"]),
        )
    if filter_type == "chokyo":
        return ChokyoFilter(
            condition=[ChokyoThreshold.from_dict(t) for t in d["condition"]],
        )
    raise ValueError(f"未対応の type です: {filter_type!r}")


def _parse_history_cond(cond: Any) -> tuple[int, int] | int | str:
    """HistoryFilter.cond の値を変換する.

    Args:
        cond (Any): 条件値。長さ2のリスト・int・str のいずれか。

    Returns:
        tuple[int, int] | int | str: 変換済みの条件値

    Raises:
        ValueError: 長さ2のリスト・int・str 以外の場合
    """
    if isinstance(cond, list) and len(cond) == 2:
        return (int(cond[0]), int(cond[1]))
    if isinstance(cond, (int, str)):
        return cond
    raise ValueError(
        f"cond の値が無効です: {cond!r}。(min, max) タプル・int・str のいずれかを指定してください。"
    )
