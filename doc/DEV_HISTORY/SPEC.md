# mykeibadb.analytics モジュール仕様書

## 概要

`mykeibadb-mcp-server` の `high_level_api.py` と `g1_predict` の `_trend_stats.py` で重複している着度数・回収率集計ロジックを `mykeibadb-python` に汎用化して移植する。

解決する課題:
- 同一のSQL集計ロジックが複数リポジトリに散在
- グループ別集計条件の追加が各リポジトリに波及する
- 調教解析関数も同様に重複

`mykeibadb.analytics` として実装することで、`mykeibadb-mcp-server` および `g1_predict` の両方から共用できる。

## 作業対象リポジトリ

`src/libs/data/mykeibadb-python`

## 既存コードとの関係

### 移植元

| 関数 | 移植元 |
|------|--------|
| `analyze_chakudo` | `mykeibadb-mcp-server/src/mykeibadb_mcp_server/high_level_api.py` の `analyze_race_chakudo` |
| `analyze_entry_attr_chakudo` | `g1_predict/src/g1_predict/_trend_stats.py` の `columns` セクション対応ロジック（現在は個別実装）|
| `get_uma_chokyo` | `mykeibadb-mcp-server/src/mykeibadb_mcp_server/high_level_api.py` の `get_uma_chokyo` |
| `analyze_chokyo_debut_seiseki` | `mykeibadb-mcp-server/src/mykeibadb_mcp_server/high_level_api.py` の `analyze_chokyo_debut_seiseki` |

### 移行後の方針

- `mykeibadb-mcp-server` の `high_level_api.py` は `mykeibadb.analytics` を呼び出すように差し替え（別PR）
- `g1_predict` の `_trend_stats.py` も `mykeibadb.analytics` を使用するように差し替え（別PR）

## ディレクトリ構成（変更分のみ）

```
mykeibadb-python/
├── mykeibadb/
│   └── analytics/
│       ├── __init__.py           # 公開APIのエクスポート
│       ├── _models.py            # データクラス定義
│       ├── _cte_helpers.py       # CTE生成ヘルパー（privateモジュール）
│       ├── chakudo.py            # analyze_chakudo
│       ├── entry_attr.py         # analyze_entry_attr_chakudo
│       └── chokyo.py             # get_uma_chokyo, analyze_chokyo_debut_seiseki
└── test/unit/mykeibadb/analytics/
    ├── test_chakudo.py
    ├── test_entry_attr.py
    └── test_chokyo.py
```

## データモデル（`_models.py`）

### ChakudoRow

1グループ分の着度数・回収率集計結果。

```python
@dataclass
class ChakudoRow:
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
```

### ChakudoResult

`analyze_chakudo` / `analyze_entry_attr_chakudo` の戻り値。

```python
@dataclass
class ChakudoResult:
    success: bool
    rows: list[ChakudoRow]
    error: str | None = None
```

### AttrSource

出走馬属性の算出方法を定義する。

```python
@dataclass
class AttrSource:
    type: str
    # type の値:
    #   "past_finish_count"  — 過去N着以内の回数（grade_codes / keibajo_code / kyori でフィルタ可）
    #   "career_count"       — キャリア戦数
    #   "prev_race_name"     — 前走レース名
    #   "debut_venue"        — デビュー競馬場コード
    top_n: int = 1                        # 何着以内を「入着」とみなすか（"past_finish_count" 用）
    grade_codes: list[str] | None = None  # 対象グレードコード
    keibajo_code: str | None = None       # 対象競馬場コード
    kyori: int | None = None              # 対象距離
```

### RowsDef

グループ名 → 行フィルタ条件の辞書。値は `(min, max)` または単一値 `int | str`。

```python
# type alias
RowsDef = dict[str, tuple[int, int] | int | str]
```

例:
```python
{
    "0勝": (0, 0),
    "1勝": (1, 1),
    "2勝以上": (2, 999),
}
```

### EntryAttrDef

出走馬属性集計の条件定義。辞書または本クラスで受け取る。

```python
@dataclass
class EntryAttrDef:
    source: AttrSource
    rows: RowsDef

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "EntryAttrDef":
        """辞書からEntryAttrDefを生成する"""
```

g1_predict の YAML 例との対応:
```yaml
# 東京優駿.yml の columns セクション
- label: "過去の東京優駿勝利数"
  source:
    type: past_finish_count
    top_n: 1
    grade_codes: ["A"]
    keibajo_code: "05"
    kyori: 2400
  rows:
    "0勝": [0, 0]
    "1勝以上": [1, 999]
```

## 関数仕様

### 1. `analyze_chakudo`（`chakudo.py`）

レース着度数・勝率・回収率を任意のグループ化条件で集計する。

```python
def analyze_chakudo(
    manager: ConnectionManager,
    group_expr: str,
    sort_expr: str,
    race_name: str | None = None,
    keibajo: str | None = None,
    kyori: int | None = None,
    year_from: str | None = None,
    year_to: str | None = None,
    grade: str | None = None,
    course_kubun: str | None = None,
    week_in_course: int | None = None,
) -> ChakudoResult:
    """グループ別着度数・勝率・回収率を集計する

    Args:
        manager (ConnectionManager): DB接続マネージャ
        group_expr (str): GROUP BY に使用するSQL式
        sort_expr (str): ORDER BY に使用するSQL式
        race_name (str | None): レース名フィルタ（部分一致）
        keibajo (str | None): 競馬場コードフィルタ
        kyori (int | None): 距離フィルタ
        year_from (str | None): 集計開始年（YYYY形式）
        year_to (str | None): 集計終了年（YYYY形式）
        grade (str | None): グレードコードフィルタ
        course_kubun (str | None): コース区分（course_kubun + week_in_course で絞り込み）
        week_in_course (int | None): コース内週番号（course_kubun と同時指定必須）

    Returns:
        ChakudoResult: 集計結果

    Raises:
        ValueError: course_kubun と week_in_course のどちらか一方のみ指定した場合
    """
```

実装要件:
- `kakutei_chakujun ~ '^[0-9]{2}$'` で取消（'00'）除外
- `haraimodoshi` テーブルと JOIN して払い戻し金額から回収率を計算
- `course_kubun` と `week_in_course` を両方指定した場合は `_build_course_week_cte` で CTE を生成
- 片方のみ指定時は `ValueError` を raise

### 2. `analyze_entry_attr_chakudo`（`entry_attr.py`）

出走馬の属性（過去実績・前走情報等）でグループ分けした着度数・回収率を集計する。

```python
def analyze_entry_attr_chakudo(
    manager: ConnectionManager,
    attr_def: EntryAttrDef | dict[str, Any],
    race_name: str | None = None,
    keibajo: str | None = None,
    kyori: int | None = None,
    year_from: str | None = None,
    year_to: str | None = None,
    grade: str | None = None,
) -> ChakudoResult:
    """出走馬属性別の着度数・勝率・回収率を集計する

    Args:
        manager (ConnectionManager): DB接続マネージャ
        attr_def (EntryAttrDef | dict[str, Any]): 属性集計条件定義
        race_name (str | None): レース名フィルタ（部分一致）
        keibajo (str | None): 競馬場コードフィルタ
        kyori (int | None): 距離フィルタ
        year_from (str | None): 集計開始年（YYYY形式）
        year_to (str | None): 集計終了年（YYYY形式）
        grade (str | None): グレードコードフィルタ

    Returns:
        ChakudoResult: グループ別集計結果

    Raises:
        ValueError: attr_def の type が未対応の場合
    """
```

実装要件:
- `attr_def` が `dict` の場合は `EntryAttrDef.from_dict` で変換
- `source.type` に応じて属性値を計算するサブクエリを生成
  - `"past_finish_count"`: `chakujun <= top_n` の出走回数を集計、grade_codes / keibajo_code / kyori でフィルタ
  - `"career_count"`: 全キャリア戦数
  - `"prev_race_name"`: サブクエリで直前レース名を取得
  - `"debut_venue"`: サブクエリで初出走の競馬場コードを取得
- `rows` の各エントリで CASE WHEN 式を組み立ててグループ名を割り当て

### 3. `get_uma_chokyo`（`chokyo.py`）

指定した馬の調教データを取得する。

```python
def get_uma_chokyo(
    manager: ConnectionManager,
    race_id: str,
    horse_num: int,
) -> dict[str, Any]:
    """馬の調教データを取得する

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_id (str): レースID
        horse_num (int): 馬番

    Returns:
        dict[str, Any]: success フラグと調教データのリスト
    """
```

### 4. `analyze_chokyo_debut_seiseki`（`chokyo.py`）

新馬・未勝利戦における調教タイプ別の成績を集計する。

```python
def analyze_chokyo_debut_seiseki(
    manager: ConnectionManager,
    race_name: str | None = None,
    keibajo: str | None = None,
    kyori: int | None = None,
    year_from: str | None = None,
    year_to: str | None = None,
) -> dict[str, Any]:
    """調教タイプ別の新馬・未勝利戦成績を集計する

    Args:
        manager (ConnectionManager): DB接続マネージャ
        race_name (str | None): レース名フィルタ（部分一致）
        keibajo (str | None): 競馬場コードフィルタ
        kyori (int | None): 距離フィルタ
        year_from (str | None): 集計開始年（YYYY形式）
        year_to (str | None): 集計終了年（YYYY形式）

    Returns:
        dict[str, Any]: success フラグと集計結果
    """
```

## 公開API（`__init__.py`）

```python
from mykeibadb.analytics.chakudo import analyze_chakudo
from mykeibadb.analytics.chokyo import analyze_chokyo_debut_seiseki, get_uma_chokyo
from mykeibadb.analytics.entry_attr import analyze_entry_attr_chakudo
from mykeibadb.analytics._models import (
    AttrSource,
    ChakudoResult,
    ChakudoRow,
    EntryAttrDef,
)

__all__ = [
    "analyze_chakudo",
    "analyze_entry_attr_chakudo",
    "get_uma_chokyo",
    "analyze_chokyo_debut_seiseki",
    "ChakudoRow",
    "ChakudoResult",
    "AttrSource",
    "EntryAttrDef",
]
```

## CTE ヘルパー（`_cte_helpers.py`）

```python
def build_course_week_cte(course_kubun: str, week_in_course: int) -> tuple[str, list[Any]]:
    """コース区分・週番号フィルタ用CTEを生成する

    Returns:
        tuple[str, list[Any]]: (CTE SQL文字列, バインドパラメータリスト)
    """

def build_payout_ctes() -> str:
    """単勝・複勝払い戻しJOIN用のCTE SQLを返す"""
```

## テスト方針

- 外部DBは `pytest-mock` でモック化
- 各関数の正常系・準正常系（`ValueError` 等）をカバー
- `analyze_entry_attr_chakudo` は `source.type` の全バリエーションをテスト

## 実装順序

1. `_models.py` — データクラス定義
2. `_cte_helpers.py` — CTE生成ヘルパー
3. `chakudo.py` — `analyze_chakudo`
4. `entry_attr.py` — `analyze_entry_attr_chakudo`
5. `chokyo.py` — `get_uma_chokyo`, `analyze_chokyo_debut_seiseki`
6. `__init__.py` — 公開API定義
7. テストコード（各実装と並行）
