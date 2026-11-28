"""出走しなかった馬の行を除く条件の結合テスト.

2026110105041109（東京9R）には、出走馬名表に載ったあと出馬表に載らなかった馬
（ジャサルディア）の行が馬番 00 のまま残っている。
"""

from datetime import date

from mykeibadb.analytics import (
    GroupBy,
    VirtualRace,
    apply_virtual_race,
    get_race_entry_groups,
    ran_entry_condition,
)
from mykeibadb.config import DBConfig
from mykeibadb.connection import ConnectionManager
from mykeibadb.getters import RaceGetter

_RACE_CODE = "2026110105041109"
_NON_RUNNING_KETTO = "2022105070"
_VIRTUAL_RACE_CODE = "2099110105041111"


def _fetch_umaban(connection_manager: ConnectionManager, race_code: str, where: str) -> list[str]:
    """umagoto_race_joho の馬番を where で絞って返す."""
    sql = f"SELECT u.umaban FROM umagoto_race_joho u WHERE u.race_code = %s AND {where} ORDER BY 1"  # noqa: S608, E501
    df = connection_manager.fetch_dataframe(sql, params=(race_code,))
    return [str(umaban) for umaban in df["umaban"]]


# 正常系
def test_ran_entry_condition_excludes_non_running_horse(
    connection_manager: ConnectionManager,
) -> None:
    """条件を付けると、出走しなかった馬の行が除かれて14頭になる."""
    without_condition = _fetch_umaban(connection_manager, _RACE_CODE, "TRUE")
    with_condition = _fetch_umaban(connection_manager, _RACE_CODE, ran_entry_condition("u"))

    assert len(without_condition) == 15
    assert without_condition[0] == "00"
    assert with_condition == [f"{i:02d}" for i in range(1, 15)]


def test_ran_entry_condition_keeps_overseas_rows(connection_manager: ConnectionManager) -> None:
    """海外のレース（データ区分 B）の行は、馬番 00 でも除かれない."""
    sql = (
        "SELECT COUNT(*) AS n FROM umagoto_race_joho u "
        "WHERE u.data_kubun = 'B' AND u.umaban = '00'"
    )
    df_all = connection_manager.fetch_dataframe(sql)
    df_kept = connection_manager.fetch_dataframe(f"{sql} AND {ran_entry_condition('u')}")

    assert int(df_all.iloc[0]["n"]) > 0
    assert int(df_kept.iloc[0]["n"]) == int(df_all.iloc[0]["n"])


def test_ran_entry_condition_keeps_rows_without_data_kubun_in_virtual_race(
    connection_manager: ConnectionManager,
) -> None:
    """data_kubun を持たない仮のレースの出走の行は、条件で除かれない."""
    virtual_race = VirtualRace(
        race={"race_code": _VIRTUAL_RACE_CODE},
        entries=[
            {"race_code": _VIRTUAL_RACE_CODE, "ketto_toroku_bango": "2021105898", "umaban": "01"},
            {"race_code": _VIRTUAL_RACE_CODE, "ketto_toroku_bango": "2022105519", "umaban": "02"},
        ],
    )
    sql = (
        "SELECT u.umaban FROM umagoto_race_joho u "
        f"WHERE u.race_code = %s AND {ran_entry_condition('u')} ORDER BY 1"
    )
    sql, params = apply_virtual_race(connection_manager, sql, (_VIRTUAL_RACE_CODE,), virtual_race)

    df = connection_manager.fetch_dataframe(sql, params=params)

    assert [str(umaban) for umaban in df["umaban"]] == ["01", "02"]


def test_get_umagoto_race_joho_excludes_non_running_horse(db_config: DBConfig) -> None:
    """get_umagoto_race_joho が出走しなかった馬の行を返さない."""
    getter = RaceGetter(db_config)
    try:
        df = getter.get_umagoto_race_joho(race_code=_RACE_CODE, convert_codes=False)
    finally:
        getter.connection_manager.close()

    assert len(df) == 14
    assert "00" not in set(df["umaban"].str.strip())
    assert _NON_RUNNING_KETTO not in set(df["ketto_toroku_bango"].str.strip())


def test_get_umagoto_race_joho_with_date_range_excludes_non_running_horse(
    db_config: DBConfig,
) -> None:
    """期間を指定した get_umagoto_race_joho でも、出走しなかった馬の行を返さない."""
    getter = RaceGetter(db_config)
    try:
        df = getter.get_umagoto_race_joho(
            race_code=_RACE_CODE,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 1),
            convert_codes=False,
        )
    finally:
        getter.connection_manager.close()

    assert len(df) == 14
    assert _NON_RUNNING_KETTO not in set(df["ketto_toroku_bango"].str.strip())


def test_get_race_entry_groups_excludes_non_running_horse(
    connection_manager: ConnectionManager,
) -> None:
    """get_race_entry_groups が出走しなかった馬を含めない."""
    result = get_race_entry_groups(
        connection_manager, _RACE_CODE, GroupBy(kind="race_col", column="u.wakuban")
    )

    assert sorted(result) == list(range(1, 15))


# 準正常系
def test_ran_entry_condition_unknown_race_returns_no_rows(
    connection_manager: ConnectionManager,
) -> None:
    """存在しないレースでは、条件を付けても行が返らない."""
    assert _fetch_umaban(connection_manager, "9999999999999999", ran_entry_condition("u")) == []
