"""_cte_helpers モジュールの単体テスト."""

import pytest

from mykeibadb.analytics._cte_helpers import (
    SUBJECT_MAP,
    build_course_week_cte,
    build_payout_ctes,
    build_race_condition_where,
    hinba_gentei_expr,
    mawari_expr,
    sedai_gentei_expr,
    shiba_da_expr,
    stand_mae_hasso_expr,
)
from mykeibadb.analytics._models import RaceCondition, Subject


# 正常系
def test_build_course_week_cte_returns_cte_and_join_sql() -> None:
    """keibajo指定ありでCTE SQLとJOIN句が返る."""
    params: list[object] = []
    cte_sql, join_sql = build_course_week_cte(["05"], "C", 1, params)
    assert "cw_target" in cte_sql
    assert "week_in_course" in cte_sql
    assert "JOIN cw_target" in join_sql
    assert params == [["05"], "C", 1]


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
    build_course_week_cte(["05"], "A", 3, params)
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


def test_build_race_condition_where_babajotai_codes() -> None:
    """babajotai_codes指定でCOALESCEのANY(...)が生成される.

    COALESCE(shiba_babajotai_code, dirt_babajotai_code) を対象とする。
    """
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(babajotai_codes=["1"]), params)
    combined = " ".join(parts)
    assert "shiba_babajotai_code" in combined
    assert "dirt_babajotai_code" in combined
    assert params == [["1"]]


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


# build_race_condition_where keibajo_codes/kaisai_nichime/babajotai_code 正常系
def test_build_race_condition_where_keibajo_codes() -> None:
    """keibajo_codes指定でkeibajo_code = ANY(...)のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(keibajo_codes=["09", "08"]), params)
    assert any("keibajo_code = ANY(%s::TEXT[])" in p for p in parts)
    assert params == [["09", "08"]]


def test_build_race_condition_where_kaisai_nichime() -> None:
    """kaisai_nichime指定でkaisai_nichime = ANY(...)のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(kaisai_nichime=[4]), params)
    assert any("kaisai_nichime::INTEGER = ANY(%s::INTEGER[])" in p for p in parts)
    assert params == [[4]]


def test_build_race_condition_where_babajotai_codes_multiple() -> None:
    """babajotai_codes複数指定でANY(...)のWHERE句が生成される."""
    params: list[object] = []
    parts = build_race_condition_where(RaceCondition(babajotai_codes=["1", "2"]), params)
    combined = " ".join(parts)
    assert "shiba_babajotai_code" in combined
    assert "dirt_babajotai_code" in combined
    assert params == [["1", "2"]]


def test_build_race_condition_where_invalid_babajotai_codes() -> None:
    """未対応のbabajotai_codesでValueErrorが発生する."""
    with pytest.raises(ValueError, match="babajotai_codes"):
        build_race_condition_where(RaceCondition(babajotai_codes=["晴れ"]), [])


# shiba_da_expr
def test_shiba_da_expr_maps_flat_track_codes() -> None:
    """平地の芝・ダートのトラックコード範囲をそれぞれ'芝'・'ダ'に変換する式を返す."""
    expr = shiba_da_expr("r2")
    assert "TRIM(r2.track_code) BETWEEN '10' AND '22' THEN '芝'" in expr
    assert "TRIM(r2.track_code) BETWEEN '23' AND '29' THEN 'ダ'" in expr
    assert "ELSE" not in expr


# mawari_expr
def test_mawari_expr_maps_track_codes_to_direction() -> None:
    """トラックコードを右回り・左回りに変換し、中央競馬以外はNULLにする式を返す."""
    expr = mawari_expr("r2")
    assert "r2.keibajo_code BETWEEN '01' AND '10'" in expr
    assert (
        "TRIM(r2.track_code) IN ('17', '18', '19', '20', '21', '22', '24', '26', '28') THEN '右'"
        in expr
    )
    assert (
        "TRIM(r2.track_code) IN ('11', '12', '13', '14', '15', '16', '23', '25', '27') THEN '左'"
        in expr
    )
    assert "ELSE" not in expr


# hinba_gentei_expr
def test_hinba_gentei_expr_checks_second_char_of_kyoso_kigo_code() -> None:
    """競走記号コードの2文字目が'2'なら'あり'、それ以外は'なし'とする式を返す."""
    expr = hinba_gentei_expr("r2")
    assert "r2.keibajo_code BETWEEN '01' AND '10'" in expr
    assert "SUBSTRING(TRIM(r2.kyoso_kigo_code) FROM 2 FOR 1) = '2' THEN 'あり' ELSE 'なし'" in expr


# sedai_gentei_expr
def test_sedai_gentei_expr_maps_kyoso_shubetsu_code() -> None:
    """競走種別コードを世代限定の有無に変換し、それ以外はNULLにする式を返す."""
    expr = sedai_gentei_expr("r2")
    assert "r2.keibajo_code BETWEEN '01' AND '10'" in expr
    assert "TRIM(r2.kyoso_shubetsu_code) IN ('11', '12') THEN 'あり'" in expr
    assert "TRIM(r2.kyoso_shubetsu_code) IN ('13', '14', '18', '19') THEN 'なし'" in expr
    assert "ELSE" not in expr


# stand_mae_hasso_expr
def test_stand_mae_hasso_expr_checks_corner1_and_shukaisu_equality() -> None:
    """平地で1コーナー通過かつ全コーナーの周回数が等しいとき'あり'とする式を返す."""
    expr = stand_mae_hasso_expr("r2")
    assert "r2.keibajo_code BETWEEN '01' AND '10'" in expr
    assert "TRIM(r2.track_code) BETWEEN '10' AND '29'" in expr
    assert "TRIM(r2.corner1) = '1'" in expr
    assert "TRIM(r2.shukaisu1) = TRIM(r2.shukaisu2)" in expr
    assert "TRIM(r2.shukaisu2) = TRIM(r2.shukaisu3)" in expr
    assert "TRIM(r2.shukaisu3) = TRIM(r2.shukaisu4)" in expr
    assert "THEN 'あり' ELSE 'なし' END END) END" in expr
