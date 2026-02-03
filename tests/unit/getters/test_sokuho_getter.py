"""SokuhoGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import SokuhoGetter

from .conftest import VALID_END_DATE, VALID_KAISAI_CODE, VALID_RACE_CODE, VALID_START_DATE

# 正常系

# get_kyosoba_jogai_joho


def test_get_kyosoba_jogai_joho_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_jogai_joho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_kyosoba_jogai_joho()

    mock_table_accessor.get_table_data.assert_called_once_with("KYOSOBA_JOGAI_JOHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_jogai_joho_with_race_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_jogai_joho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_kyosoba_jogai_joho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KYOSOBA_JOGAI_JOHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kyosoba_jogai_joho_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kyosoba_jogai_joho: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_kyosoba_jogai_joho(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "KYOSOBA_JOGAI_JOHO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_bataiju


def test_get_bataiju_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bataiju: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_bataiju()

    mock_table_accessor.get_table_data.assert_called_once_with("BATAIJU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_bataiju_with_race_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bataiju: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_bataiju(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "BATAIJU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_bataiju_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_bataiju: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_bataiju(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "BATAIJU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_tenko_baba_jotai


def test_get_tenko_baba_jotai_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tenko_baba_jotai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_tenko_baba_jotai()

    mock_table_accessor.get_table_data.assert_called_once_with("TENKO_BABA_JOTAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tenko_baba_jotai_with_race_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tenko_baba_jotai: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_tenko_baba_jotai(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "TENKO_BABA_JOTAI",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_tenko_baba_jotai_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_tenko_baba_jotai: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_tenko_baba_jotai(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "TENKO_BABA_JOTAI",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_shussotorikeshi_kyosojogai


def test_get_shussotorikeshi_kyosojogai_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussotorikeshi_kyosojogai: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_shussotorikeshi_kyosojogai()

    mock_table_accessor.get_table_data.assert_called_once_with("SHUSSOTORIKESHI_KYOSOJOGAI", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussotorikeshi_kyosojogai_with_kaisai_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussotorikeshi_kyosojogai: kaisai_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_KAISAI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_shussotorikeshi_kyosojogai(kaisai_code=VALID_KAISAI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHUSSOTORIKESHI_KYOSOJOGAI",
        {"RACE_CODE": VALID_KAISAI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shussotorikeshi_kyosojogai_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shussotorikeshi_kyosojogai: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_shussotorikeshi_kyosojogai(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "SHUSSOTORIKESHI_KYOSOJOGAI",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_kishu_henko


def test_get_kishu_henko_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_henko: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_kishu_henko()

    mock_table_accessor.get_table_data.assert_called_once_with("KISHU_HENKO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kishu_henko_with_race_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_henko: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_kishu_henko(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "KISHU_HENKO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_kishu_henko_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_kishu_henko: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_kishu_henko(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "KISHU_HENKO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hassojikoku_henko


def test_get_hassojikoku_henko_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hassojikoku_henko: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_hassojikoku_henko()

    mock_table_accessor.get_table_data.assert_called_once_with("HASSOJIKOKU_HENKO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hassojikoku_henko_with_race_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hassojikoku_henko: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_hassojikoku_henko(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HASSOJIKOKU_HENKO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hassojikoku_henko_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hassojikoku_henko: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_hassojikoku_henko(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HASSOJIKOKU_HENKO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_course_henko


def test_get_course_henko_without_filters(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_henko: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_course_henko()

    mock_table_accessor.get_table_data.assert_called_once_with("COURSE_HENKO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_course_henko_with_race_code(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_henko: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = sokuho_getter.get_course_henko(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "COURSE_HENKO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_course_henko_with_date_range(
    sokuho_getter: SokuhoGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_course_henko: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = sokuho_getter.get_course_henko(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "COURSE_HENKO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)
