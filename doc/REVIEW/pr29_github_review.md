# PR #29 レビューコメント

コメント数: 3

---

## 1. `mykeibadb/analytics/chakudo.py` (L29-L31)

**投稿者**: Copilot | **投稿日時**: 2026-06-04T09:31:35Z

```diff
@@ -0,0 +1,164 @@
+"""グループ別着度数・回収率集計モジュール."""
+
+from typing import Any
+
+import pandas as pd
+
+from mykeibadb.analytics._cte_helpers import build_course_week_cte, build_payout_ctes
+from mykeibadb.analytics._models import ChakudoResult, ChakudoRow
+from mykeibadb.connection import ConnectionManager
+from mykeibadb.exceptions import MykeibaDBError
+
+
+def analyze_chakudo(
+    manager: ConnectionManager,
+    group_expr: str,
+    sort_expr: str,
+    race_name: str | None = None,
+    keibajo: str | None = None,
+    kyori: int | None = None,
+    year_from: str | None = None,
+    year_to: str | None = None,
+    grade: str | None = None,
+    course_kubun: str | None = None,
+    week_in_course: int | None = None,
+) -> ChakudoResult:
+    """グループ別着度数・勝率・回収率を集計する.
+
+    Args:
+        manager (ConnectionManager): DB接続マネージャ
+        group_expr (str): GROUP BY に使用するSQL式
+        sort_expr (str): ORDER BY に使用するSQL式
```

docstringの説明だと sort_expr が「ORDER BY に使用するSQL式」と読めますが、実際には base CTE の SELECT で sort_key を生成する式として埋め込まれており、"... DESC" のような ORDER BY 句の断片を渡すとSQLが壊れます。期待する入力形式（式のみ/ASC・DESCは含めない）に合わせて引数説明を修正してください。

---

## 2. `mykeibadb/analytics/chakudo.py` (L47-L52)

**投稿者**: Copilot | **投稿日時**: 2026-06-04T09:31:36Z

```diff
@@ -0,0 +1,164 @@
+"""グループ別着度数・回収率集計モジュール."""
+
+from typing import Any
+
+import pandas as pd
+
+from mykeibadb.analytics._cte_helpers import build_course_week_cte, build_payout_ctes
+from mykeibadb.analytics._models import ChakudoResult, ChakudoRow
+from mykeibadb.connection import ConnectionManager
+from mykeibadb.exceptions import MykeibaDBError
+
+
+def analyze_chakudo(
+    manager: ConnectionManager,
+    group_expr: str,
+    sort_expr: str,
+    race_name: str | None = None,
+    keibajo: str | None = None,
+    kyori: int | None = None,
+    year_from: str | None = None,
+    year_to: str | None = None,
+    grade: str | None = None,
+    course_kubun: str | None = None,
+    week_in_course: int | None = None,
+) -> ChakudoResult:
+    """グループ別着度数・勝率・回収率を集計する.
+
+    Args:
+        manager (ConnectionManager): DB接続マネージャ
+        group_expr (str): GROUP BY に使用するSQL式
+        sort_expr (str): ORDER BY に使用するSQL式
+        race_name (str | None): レース名フィルタ（部分一致）
+        keibajo (str | None): 競馬場コードフィルタ
+        kyori (int | None): 距離フィルタ
+        year_from (str | None): 集計開始年（YYYY形式）
+        year_to (str | None): 集計終了年（YYYY形式）
+        grade (str | None): グレードコードフィルタ
+        course_kubun (str | None): コース区分（week_in_course と同時指定必須）
+        week_in_course (int | None): コース使用開始からの週番号（course_kubun と同時指定必須）
+
+    Returns:
+        ChakudoResult: グループ別集計結果
+
+    Raises:
+        ValueError: course_kubun と week_in_course のどちらか一方のみ指定した場合
+    """
+    if (course_kubun is None) != (week_in_course is None):
+        raise ValueError(
+            "course_kubun と week_in_course は両方同時に指定するか、両方 None にしてください。"
+        )
+
+    try:
```

group_expr / sort_expr を f-string でSQLに直接埋め込む公開APIになっているため、呼び出し側が外部入力をそのまま渡すとSQLインジェクションの経路になります。少なくとも危険なトークン（`;`, `--`, `/*` 等）を含む場合は即座に ValueError にするなど、最低限のガードを入れてください（完全な防御ではない点もdocstringで明記すると安全です）。

---

## 3. `test/unit/mykeibadb/analytics/test_chakudo.py` (L7-L9)

**投稿者**: Copilot | **投稿日時**: 2026-06-04T09:31:36Z

```diff
@@ -0,0 +1,177 @@
+"""analyze_chakudo の単体テスト."""
+
+import pandas as pd
+import pytest
+from pytest_mock import MockerFixture
+
+from mykeibadb.analytics._models import ChakudoRow
+from mykeibadb.analytics.chakudo import analyze_chakudo
+from mykeibadb.exceptions import QueryExecutionError
```

このPRでは `mykeibadb.analytics` から `analyze_chakudo` / `ChakudoRow` をエクスポートしているため、ユニットテストも公開API経由の import に寄せた方が `__init__.py` の回帰を検知できます（内部モジュール直importだとエクスポート追加の意義がテストされません）。

---
