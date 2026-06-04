"""analyze_subject_chakudo の単体テスト."""

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from mykeibadb.analytics import RaceCondition, Subject, analyze_subject_chakudo
from mykeibadb.exceptions import QueryExecutionError


def _make_df(rows: list[dict[str, object]]) -> pd.DataFrame:
    """テスト用DataFrameを生成する."""
    return pd.DataFrame(rows)


def _single_row_df() -> pd.DataFrame:
    """単一行のテスト用DataFrameを生成する."""
    return _make_df([{
        "grp": "武豊", "sort_key": "武豊", "total": 500, "wins": 100,
        "second": 80, "third": 60, "chakugai": 260,
        "win_rate": 20.0, "fukusho_rate": 48.0,
        "tansho_kaishuu": 75.0, "fukusho_kaishuu": 80.0,
    }])


# 正常系
def test_analyze_subject_chakudo_kishu_by_name(mocker: MockerFixture) -> None:
    """Subject.KISHUで名前指定するとChakudoResultが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    result = analyze_subject_chakudo(manager, Subject.KISHU, name="武豊")

    assert result.success is True
    assert len(result.rows) == 1
    assert result.rows[0].group == "武豊"


def test_analyze_subject_chakudo_kishu_by_code(mocker: MockerFixture) -> None:
    """Subject.KISHUでコード指定するとChakudoResultが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    result = analyze_subject_chakudo(manager, Subject.KISHU, code="00666")

    assert result.success is True
    sql_called = manager.fetch_dataframe.call_args[0][0]
    assert "u.kishu_code" in sql_called


def test_analyze_subject_chakudo_kishu_code_takes_priority_over_name(
    mocker: MockerFixture,
) -> None:
    """code指定時はnameより優先してコード完全一致フィルタが使われる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    analyze_subject_chakudo(manager, Subject.KISHU, name="武豊", code="00666")

    sql_called = manager.fetch_dataframe.call_args[0][0]
    assert "u.kishu_code" in sql_called
    assert "LIKE" not in sql_called


def test_analyze_subject_chakudo_uma_by_name(mocker: MockerFixture) -> None:
    """Subject.UMAで名前指定するとChakudoResultが返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    result = analyze_subject_chakudo(manager, Subject.UMA, name="ディープ")

    assert result.success is True
    sql_called = manager.fetch_dataframe.call_args[0][0]
    assert "u.bamei" in sql_called


def test_analyze_subject_chakudo_sire_by_name(mocker: MockerFixture) -> None:
    """Subject.SIREで名前指定するとkyosoba_master2 JOINが含まれる."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    result = analyze_subject_chakudo(manager, Subject.SIRE, name="ディープ")

    assert result.success is True
    sql_called = manager.fetch_dataframe.call_args[0][0]
    assert "kyosoba_master2" in sql_called


def test_analyze_subject_chakudo_no_filter_returns_all(mocker: MockerFixture) -> None:
    """name/code指定なしで全件集計する."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    result = analyze_subject_chakudo(manager, Subject.KISHU)

    assert result.success is True
    sql_called = manager.fetch_dataframe.call_args[0][0]
    assert "LIKE" not in sql_called
    assert "kishu_code = %s" not in sql_called


def test_analyze_subject_chakudo_with_condition(mocker: MockerFixture) -> None:
    """RaceConditionを渡すと絞り込みWHERE句が生成される."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    condition = RaceCondition(keibajo_code="05")
    analyze_subject_chakudo(manager, Subject.KISHU, condition=condition)

    sql_called = manager.fetch_dataframe.call_args[0][0]
    assert "r.keibajo_code" in sql_called


def test_analyze_subject_chakudo_db_error_returns_failure(mocker: MockerFixture) -> None:
    """DBエラー時はsuccess=Falseで返る."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.side_effect = QueryExecutionError("connection failed")

    result = analyze_subject_chakudo(manager, Subject.KISHU, name="武豊")

    assert result.success is False
    assert result.error is not None


@pytest.mark.parametrize("subject", list(Subject))
def test_analyze_subject_chakudo_all_subjects_callable(
    subject: Subject, mocker: MockerFixture
) -> None:
    """全Subjectで呼び出し可能（エラーなし）."""
    manager = mocker.MagicMock()
    manager.fetch_dataframe.return_value = _single_row_df()

    result = analyze_subject_chakudo(manager, subject)

    assert result.success is True


# 準正常系
def test_analyze_subject_chakudo_sire_code_raises() -> None:
    """Subject.SIREにcodeを指定するとValueErrorが発生する."""
    manager = object()
    with pytest.raises(ValueError, match="コード指定に対応していません"):
        analyze_subject_chakudo(manager, Subject.SIRE, code="xxx")  # type: ignore[arg-type]


def test_analyze_subject_chakudo_seisansha_code_raises() -> None:
    """Subject.SEISANSHAにcodeを指定するとValueErrorが発生する."""
    manager = object()
    with pytest.raises(ValueError, match="コード指定に対応していません"):
        analyze_subject_chakudo(manager, Subject.SEISANSHA, code="xxx")  # type: ignore[arg-type]
