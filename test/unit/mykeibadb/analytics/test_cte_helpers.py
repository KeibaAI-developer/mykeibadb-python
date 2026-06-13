"""_cte_helpers モジュールの単体テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import (
    SUBJECT_MAP,
    build_course_week_cte,
    build_payout_ctes,
    build_race_condition_where,
)
from mykeibadb.analytics._models import RaceCondition, Subject


# 正常系
def test_build_course_week_cte_returns_cte_and_join_sql() -> None:
    """keibajo指定ありでCTE SQLとJOIN句が返る."""
    params: list[object] = []
    cte_sql, join_sql = build_course_week_cte("05", "C", 1, params)
    assert "cw_target" in cte_sql
    assert "week_in_course" in cte_sql
    assert "JOIN cw_target" in join_sql
    assert params == ["05", "C", 1]


def test_build_course_week_cte_without_keibajo() -> None:
    """keibajo=NoneでもCTE SQLが生成され、パラメータにkeibajoが含まれない."""
    params: list[object] = []
    cte_sql, join_sql = build_course_week_cte(None, "B", 2, params)
    assert "cw_target" in cte_sql
    assert "AND keibajo_code = %s" not in cte_sql
    assert params == ["B", 2]


def test_build_course_week_cte_appends_to_existing_params() -> None:
    """既存パラメータリストの末尾にパラメータが追加される."""
    params: list[object] = ["existing"]
    build_course_week_cte("05", "A", 3, params)
    assert params[0] == "existing"
    assert params[-1] == 3


def test_build_course_week_cte_join_sql_has_all_join_columns() -> None:
    """JOIN句が keibajo_code / kaisai_nen / kaisai_kai / kaisai_nichime を含む."""
    params: list[object] = []
    _, join_sql = build_course_week_cte(None, "C", 1, params)
    assert "keibajo_code" in join_sql
    assert "kaisai_nen" in join_sql
    assert "kaisai_kai" in join_sql
    assert "kaisai_nichime" in join_sql


# 準正常系
def test_build_course_week_cte_week_zero_raises() -> None:
    """week_in_course=0でValueErrorが発生する."""
    params: list[object] = []
    with pytest.raises(ValueError, match="week_in_course"):
        build_course_week_cte(None, "C", 0, params)


def test_build_course_week_cte_negative_week_raises() -> None:
    """week_in_course負数でValueErrorが発生する."""
    params: list[object] = []
    with pytest.raises(ValueError, match="week_in_course"):
        build_course_week_cte(None, "C", -1, params)


def test_build_payout_ctes_returns_string() -> None:
    """build_payout_ctesが文字列を返す."""
    result = build_payout_ctes()
    assert isinstance(result, str)
    assert "tansho_payouts" in result
    assert "fukusho_payouts" in result


def test_build_payout_ctes_has_haraimodoshi_reference() -> None:
    """払い戻しCTEがharaimodoshiテーブルを参照する."""
    result = build_payout_ctes()
    assert "haraimodoshi" in result


def test_build_payout_ctes_filters_invalid_values() -> None:
    """払い戻しCTEが正規表現フィルタを含む."""
    result = build_payout_ctes()
    assert "^[0-9]+$" in result


@pytest.mark.parametrize(
    "course_kubun, week_in_course",
    [
        ("C", 1),
        ("B", 3),
        ("A", 5),
    ],
)
def test_build_course_week_cte_various_params(course_kubun: str, week_in_course: int) -> None:
    """様々なコース区分・週番号でCTEが生成できる."""
    params: list[object] = []
    cte_sql, _ = build_course_week_cte(None, course_kubun, week_in_course, params)
    assert "cw_target" in cte_sql
    assert course_kubun in params
    assert week_in_course in params


# SUBJECT_MAP 正常系
def test_subject_map_covers_all_subjects() -> None:
    """全Subjectがマッピングに定義されている."""
    for subject in Subject:
        assert subject in SUBJECT_MAP


@pytest.mark.parametrize(
    "subject",
    [Subject.UMA, Subject.KISHU, Subject.CHOKYOSHI, Subject.BANUSHI],
)
def test_subject_map_no_join_for_umagoto_subjects(subject: Subject) -> None:
    """umagoto_race_joho直接参照の主体はJOIN不要."""
    assert SUBJECT_MAP[subject].join_sql is None


@pytest.mark.parametrize(
    "subject",
    [Subject.SIRE, Subject.SEISANSHA],
)
def test_subject_map_km2_join_for_sire_seisansha(subject: Subject) -> None:
    """種牡馬/生産者はkyosoba_master2 JOINが設定されている."""
    mapping = SUBJECT_MAP[subject]
    assert mapping.join_sql is not None
    assert "kyosoba_master2" in mapping.join_sql


@pytest.mark.parametrize(
    "subject",
    [Subject.UMA, Subject.KISHU, Subject.CHOKYOSHI, Subject.BANUSHI],
)
def test_subject_map_has_code_col_for_umagoto_subjects(subject: Subject) -> None:
    """umagoto_race_joho直接参照の主体はコード列が定義されている."""
    assert SUBJECT_MAP[subject].code_col is not None


@pytest.mark.parametrize(
    "subject",
    [Subject.SIRE, Subject.SEISANSHA],
)
def test_subject_map_no_code_col_for_sire_seisansha(subject: Subject) -> None:
    """種牡馬/生産者はコード指定不可（code_col=None）."""
    assert SUBJECT_MAP[subject].code_col is None


# build_race_condition_where 正常系
def test_build_race_condition_where_race_shubetsu_heichi() -> None:
    """race_shubetsu=平地でtrack_code BETWEEN 10-29のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(race_shubetsu="平地"), params)
    assert any("BETWEEN '10' AND '29'" in p for p in parts)
    assert params == []


def test_build_race_condition_where_race_shubetsu_shogai() -> None:
    """race_shubetsu=障害でtrack_code BETWEEN 51-59のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(race_shubetsu="障害"), params)
    assert any("BETWEEN '51' AND '59'" in p for p in parts)


def test_build_race_condition_where_shiba_da_shiba() -> None:
    """shiba_da=芝でtrack_code 10-22 OR 51-59のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(shiba_da="芝"), params)
    combined = " ".join(parts)
    assert "BETWEEN '10' AND '22'" in combined
    assert "BETWEEN '51' AND '59'" in combined


def test_build_race_condition_where_shiba_da_da() -> None:
    """shiba_da=ダでtrack_code BETWEEN 23-29のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(shiba_da="ダ"), params)
    assert any("BETWEEN '23' AND '29'" in p for p in parts)


def test_build_race_condition_where_babajotai_code() -> None:
    """babajotai_code指定でCOALESCE(shiba_babajotai_code, dirt_babajotai_code)=?が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(babajotai_code="1"), params)
    combined = " ".join(parts)
    assert "shiba_babajotai_code" in combined
    assert "dirt_babajotai_code" in combined
    assert "1" in params


@pytest.mark.parametrize(
    "sayuu, expected_code",
    [
        ("左", "11"),
        ("右", "17"),
        ("直", "10"),
    ],
)
def test_build_race_condition_where_sayuu(sayuu: str, expected_code: str) -> None:
    """sayuu指定でtrack_code IN (...)のWHERE句とパラメータが生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(sayuu=sayuu), params)
    assert any("TRIM(r.track_code) IN" in p for p in parts)
    assert expected_code in params


def test_build_race_condition_where_course_kubun_only() -> None:
    """course_kubunのみ指定(week_in_course=None)でr.course_kubun=?が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(course_kubun="A"), params)
    assert any("r.course_kubun = %s" in p for p in parts)
    assert "A" in params


def test_build_race_condition_where_course_kubun_with_week_skipped() -> None:
    """course_kubun+week_in_course同時指定時はcourse_kubunのWHERE句が生成されない."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(course_kubun="A", week_in_course=1), params)
    assert not any("r.course_kubun = %s" in p for p in parts)


def test_build_race_condition_where_empty_condition() -> None:
    """全属性Noneで空リストが返る."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(), params)
    assert parts == []
    assert params == []


# build_race_condition_where 準正常系
def test_build_race_condition_where_invalid_race_shubetsu() -> None:
    """未対応のrace_shubetsuでValueErrorが発生する."""
    with pytest.raises(ValueError, match="race_shubetsu"):
        build_race_condition_where(RaceCondition(race_shubetsu="未知"), [])


def test_build_race_condition_where_invalid_shiba_da() -> None:
    """未対応のshiba_daでValueErrorが発生する."""
    with pytest.raises(ValueError, match="shiba_da"):
        build_race_condition_where(RaceCondition(shiba_da="X"), [])


def test_build_race_condition_where_invalid_sayuu() -> None:
    """未対応のsayuuでValueErrorが発生する."""
    with pytest.raises(ValueError, match="sayuu"):
        build_race_condition_where(RaceCondition(sayuu="斜め"), [])


# build_race_condition_where keibajo_codes/kaisai_nichime/baba 正常系
def test_build_race_condition_where_keibajo_codes() -> None:
    """keibajo_codes指定でkeibajo_code = ANY(...)のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(keibajo_codes=["09", "08"]), params)
    assert any("keibajo_code = ANY(%s::TEXT[])" in p for p in parts)
    assert params == [["09", "08"]]


def test_build_race_condition_where_keibajo_codes_kept_when_include_false() -> None:
    """include_keibajo_code=Falseでもkeibajo_codesのWHERE句は生成される.

    course_kubun + week_in_course のCTE処理では単数のkeibajo_codeのみCTEに
    渡されるため、複数指定のkeibajo_codesはWHERE句側で維持する必要がある。
    """
    params: list[object] = []
    parts = build_race_condition_where(
        RaceCondition(keibajo_codes=["09"]), params, include_keibajo_code=False
    )
    assert any("keibajo_code = ANY(%s::TEXT[])" in p for p in parts)
    assert params == [["09"]]


def test_build_race_condition_where_kaisai_nichime() -> None:
    """kaisai_nichime指定でkaisai_nichime = ANY(...)のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(kaisai_nichime=[4]), params)
    assert any("kaisai_nichime::INTEGER = ANY(%s::INTEGER[])" in p for p in parts)
    assert params == [[4]]


def test_build_race_condition_where_baba() -> None:
    """baba指定で馬場状態コードへ変換しANY(...)のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(baba=["良", "稍重"]), params)
    combined = " ".join(parts)
    assert "shiba_babajotai_code" in combined
    assert "dirt_babajotai_code" in combined
    assert params == [["1", "2"]]


def test_build_race_condition_where_invalid_baba() -> None:
    """未対応のbabaでValueErrorが発生する."""
    with pytest.raises(ValueError, match="baba"):
        build_race_condition_where(RaceCondition(baba=["晴れ"]), [])
