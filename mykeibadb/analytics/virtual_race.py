"""仮のレースをクエリの中だけで DB にあるものとして扱うモジュール."""

import json
import re
from dataclasses import dataclass, field
from typing import Any

from mykeibadb.connection import ConnectionManager

# 先頭の空白・行コメント・ブロックコメントに続く WITH（RECURSIVE を含む）
_WITH_PATTERN = re.compile(
    r"^(?:\s+|--[^\n]*(?:\n|$)|/\*.*?\*/)*WITH\s+(?:RECURSIVE\s+)?",
    re.IGNORECASE | re.DOTALL,
)
_COLUMNS_QUERY = """
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = %s
"""


@dataclass(frozen=True)
class VirtualRace:
    """DB にまだ入っていないレースを、クエリの中だけで DB にあるものとして扱うための行.

    値は DB の列と同じ書式の文字列で渡す（例: 馬番 "01"、騎手コード "05339"）。

    Attributes:
        race (dict[str, str]): race_shosai の1行。列名 -> 値。書かない列は NULL。
        entries (list[dict[str, str]]): umagoto_race_joho の出走ごとの行。列名 -> 値。
            書かない列は NULL。出走取消などで除外しない出走は ijo_kubun_code に "0" を入れる。
        horses (list[dict[str, str]]): kyosoba_master2 に無い馬の行。列名 -> 値。
            書かない列は NULL。

    Raises:
        ValueError: race_code・ketto_toroku_bango・umaban が無い場合
        ValueError: entries の race_code が race と違う場合
        ValueError: umaban または horses の ketto_toroku_bango が重複する場合
    """

    race: dict[str, str]
    entries: list[dict[str, str]]
    horses: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """必須の列と重複を検証する.

        Raises:
            ValueError: 必須の列が無い、race_code が違う、または重複がある場合
        """
        _require_columns(self.race, ("race_code",), "race")
        race_code = self.race["race_code"]
        umabans: set[str] = set()
        for entry in self.entries:
            _require_columns(entry, ("race_code", "ketto_toroku_bango", "umaban"), "entries")
            if entry["race_code"] != race_code:
                raise ValueError(
                    f"entries の race_code が race と違います: {entry['race_code']!r} != "
                    f"{race_code!r}"
                )
            if entry["umaban"] in umabans:
                raise ValueError(f"entries の umaban が重複しています: {entry['umaban']!r}")
            umabans.add(entry["umaban"])
        horse_ids: set[str] = set()
        for horse in self.horses:
            _require_columns(horse, ("ketto_toroku_bango",), "horses")
            ketto = horse["ketto_toroku_bango"]
            if ketto in horse_ids:
                raise ValueError(f"horses の ketto_toroku_bango が重複しています: {ketto!r}")
            horse_ids.add(ketto)


def apply_virtual_race(
    manager: ConnectionManager, sql: str, params: tuple[Any, ...], virtual_race: VirtualRace
) -> tuple[str, tuple[Any, ...]]:
    """SQL の中で、race_shosai・umagoto_race_joho に仮のレースの行が加わって見えるようにする.

    SQL の先頭に仮の行の CTE と、race_shosai・umagoto_race_joho（horses がある場合は
    kyosoba_master2 も）を上書きする CTE を足す。SQL がすでに WITH で始まる場合は、その
    CTE の並びの先頭に足す。DB には書き込まない。仮のレースと同じレースコードの行が DB に
    ある場合の確認はしない。

    仮のレースの列名が対応する表の列にあることを、DB の列名と照合して確かめる。
    jsonb_populate_recordset は表に無いキーを黙って無視するため。

    Args:
        manager (ConnectionManager): 列名の照合に使う DB接続マネージャ
        sql (str): 書き換え前の SQL
        params (tuple[Any, ...]): 書き換え前の SQL のパラメータ
        virtual_race (VirtualRace): 仮のレース

    Returns:
        tuple[str, tuple[Any, ...]]: 書き換えた SQL
        tuple[str, tuple[Any, ...]]: 書き換えた SQL のパラメータ（足した CTE の分が先頭）

    Raises:
        ValueError: 仮のレースに表に無い列名がある場合
    """
    _validate_columns(manager, virtual_race)
    tables = [
        ("race_shosai", [virtual_race.race]),
        ("umagoto_race_joho", virtual_race.entries),
    ]
    if virtual_race.horses:
        tables.append(("kyosoba_master2", virtual_race.horses))

    row_ctes: list[str] = []
    override_ctes: list[str] = []
    cte_params: list[Any] = []
    for table, rows in tables:
        row_ctes.append(
            f"virtual_{table} AS MATERIALIZED (\n"
            f"        SELECT * FROM jsonb_populate_recordset(NULL::public.{table}, %s::jsonb)\n"
            f"    )"
        )
        override_ctes.append(
            f"{table} AS NOT MATERIALIZED (\n"
            f"        SELECT * FROM public.{table}\n"
            f"        UNION ALL\n"
            f"        SELECT * FROM virtual_{table}\n"
            f"    )"
        )
        cte_params.append(json.dumps(rows, ensure_ascii=False))

    virtual_ctes = ", ".join(row_ctes + override_ctes)
    match = _WITH_PATTERN.match(sql)
    if match:
        new_sql = f"{sql[: match.end()]}{virtual_ctes}, {sql[match.end() :]}"
    else:
        new_sql = f"WITH {virtual_ctes}\n{sql}"
    return new_sql, (*cte_params, *params)


def _validate_columns(manager: ConnectionManager, virtual_race: VirtualRace) -> None:
    """仮のレースの列名が、対応する表の列にあることを確かめる.

    jsonb_populate_recordset は表に無いキーを黙って無視するため、DB の列名と照合して検出する。

    Args:
        manager (ConnectionManager): DB接続マネージャ
        virtual_race (VirtualRace): 仮のレース

    Raises:
        ValueError: 列名が表に無い場合
    """
    tables = [
        ("race_shosai", [virtual_race.race]),
        ("umagoto_race_joho", virtual_race.entries),
        ("kyosoba_master2", virtual_race.horses),
    ]
    for table, rows in tables:
        used = {column for row in rows for column in row}
        if not used:
            continue
        known = {str(row[0]) for row in manager.execute_query(_COLUMNS_QUERY, (table,))}
        unknown = sorted(used - known)
        if unknown:
            raise ValueError(f"{table} に無い列名です: {unknown}")


def _require_columns(row: dict[str, str], columns: tuple[str, ...], label: str) -> None:
    """row に必須の列が揃っていることを確かめる.

    Raises:
        ValueError: 必須の列が無い場合
    """
    missing = [column for column in columns if column not in row]
    if missing:
        raise ValueError(f"{label} に必須の列がありません: {missing}")
