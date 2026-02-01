"""HyosuGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import HyosuGetter

from .conftest import VALID_END_DATE, VALID_RACE_CODE, VALID_RACE_CODES, VALID_START_DATE

# 正常系

# get_hyosu1


def test_get_hyosu1_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_tansho


def test_get_hyosu1_tansho_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_tansho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_tansho()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_TANSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_tansho_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_tansho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_tansho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_TANSHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_tansho_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_tansho: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_tansho(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_TANSHO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_fukusho


def test_get_hyosu1_fukusho_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_fukusho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_fukusho()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_FUKUSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_fukusho_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_fukusho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_fukusho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_FUKUSHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_fukusho_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_fukusho: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_fukusho(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_FUKUSHO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_wakuren


def test_get_hyosu1_wakuren_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wakuren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_wakuren()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_WAKUREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_wakuren_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wakuren: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_wakuren(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_WAKUREN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_wakuren_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wakuren: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_wakuren(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_WAKUREN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_umaren


def test_get_hyosu1_umaren_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umaren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_umaren()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_UMAREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_umaren_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umaren: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_umaren(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_UMAREN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_umaren_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umaren: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_umaren(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_UMAREN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_wide


def test_get_hyosu1_wide_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wide: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_wide()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_WIDE", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_wide_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wide: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_wide(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_WIDE",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_wide_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_wide: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_wide(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_WIDE",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_umatan


def test_get_hyosu1_umatan_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umatan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_umatan()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_UMATAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_umatan_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umatan: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_umatan(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_UMATAN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_umatan_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_umatan: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_umatan(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_UMATAN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu1_sanrenpuku


def test_get_hyosu1_sanrenpuku_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_sanrenpuku: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_sanrenpuku()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU1_SANRENPUKU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_sanrenpuku_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_sanrenpuku: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu1_sanrenpuku(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU1_SANRENPUKU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu1_sanrenpuku_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu1_sanrenpuku: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu1_sanrenpuku(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU1_SANRENPUKU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu6


def test_get_hyosu6_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu6()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU6", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu6_with_race_code(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu6(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU6",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu6_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu6(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU6",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_hyosu6_sanrentan


def test_get_hyosu6_sanrentan_without_filters(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6_sanrentan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu6_sanrentan()

    mock_table_accessor.get_table_data.assert_called_once_with("HYOSU6_SANRENTAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu6_sanrentan_with_race_codes_list(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6_sanrentan: 複数race_codeでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": VALID_RACE_CODES})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = hyosu_getter.get_hyosu6_sanrentan(race_code=VALID_RACE_CODES)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "HYOSU6_SANRENTAN",
        {"RACE_CODE": VALID_RACE_CODES},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_hyosu6_sanrentan_with_date_range(
    hyosu_getter: HyosuGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_hyosu6_sanrentan: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = hyosu_getter.get_hyosu6_sanrentan(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "HYOSU6_SANRENTAN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)
