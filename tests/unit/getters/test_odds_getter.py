"""OddsGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import OddsGetter

from .conftest import VALID_END_DATE, VALID_RACE_CODE, VALID_RACE_CODES, VALID_START_DATE

# 正常系

# get_odds1


def test_get_odds1_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_tansho


def test_get_odds1_tansho_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_tansho()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_TANSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_tansho_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_tansho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_TANSHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_tansho_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_tansho(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_TANSHO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_fukusho


def test_get_odds1_fukusho_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_fukusho()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_FUKUSHO", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_fukusho_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_fukusho(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_FUKUSHO",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_fukusho_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_fukusho(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_FUKUSHO",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_wakuren


def test_get_odds1_wakuren_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_wakuren()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_WAKUREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_wakuren_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_wakuren(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_WAKUREN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_wakuren_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_wakuren(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_WAKUREN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_jikeiretsu


def test_get_odds1_jikeiretsu_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_jikeiretsu_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_jikeiretsu: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_jikeiretsu(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_JIKEIRETSU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_jikeiretsu_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_jikeiretsu: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_jikeiretsu(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_JIKEIRETSU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_tansho_jikeiretsu


def test_get_odds1_tansho_jikeiretsu_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_tansho_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_TANSHO_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_tansho_jikeiretsu_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho_jikeiretsu: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_tansho_jikeiretsu(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_TANSHO_JIKEIRETSU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_tansho_jikeiretsu_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_tansho_jikeiretsu: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_tansho_jikeiretsu(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_TANSHO_JIKEIRETSU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_fukusho_jikeiretsu


def test_get_odds1_fukusho_jikeiretsu_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_fukusho_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_FUKUSHO_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_fukusho_jikeiretsu_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho_jikeiretsu: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_fukusho_jikeiretsu(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_FUKUSHO_JIKEIRETSU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_fukusho_jikeiretsu_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_fukusho_jikeiretsu: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_fukusho_jikeiretsu(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_FUKUSHO_JIKEIRETSU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds1_wakuren_jikeiretsu


def test_get_odds1_wakuren_jikeiretsu_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_wakuren_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS1_WAKUREN_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_wakuren_jikeiretsu_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren_jikeiretsu: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds1_wakuren_jikeiretsu(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS1_WAKUREN_JIKEIRETSU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds1_wakuren_jikeiretsu_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds1_wakuren_jikeiretsu: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds1_wakuren_jikeiretsu(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS1_WAKUREN_JIKEIRETSU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds2_umaren


def test_get_odds2_umaren_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds2_umaren()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS2_UMAREN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds2_umaren_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds2_umaren(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS2_UMAREN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds2_umaren_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds2_umaren(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS2_UMAREN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds2_umaren_jikeiretsu


def test_get_odds2_umaren_jikeiretsu_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren_jikeiretsu: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds2_umaren_jikeiretsu()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS2_UMAREN_JIKEIRETSU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds2_umaren_jikeiretsu_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren_jikeiretsu: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds2_umaren_jikeiretsu(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS2_UMAREN_JIKEIRETSU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds2_umaren_jikeiretsu_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds2_umaren_jikeiretsu: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds2_umaren_jikeiretsu(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS2_UMAREN_JIKEIRETSU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds3_wide


def test_get_odds3_wide_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds3_wide: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds3_wide()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS3_WIDE", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds3_wide_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds3_wide: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds3_wide(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS3_WIDE",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds3_wide_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds3_wide: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds3_wide(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS3_WIDE",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds4_umatan


def test_get_odds4_umatan_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds4_umatan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds4_umatan()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS4_UMATAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds4_umatan_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds4_umatan: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds4_umatan(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS4_UMATAN",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds4_umatan_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds4_umatan: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds4_umatan(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS4_UMATAN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds5_sanrenpuku


def test_get_odds5_sanrenpuku_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds5_sanrenpuku: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds5_sanrenpuku()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS5_SANRENPUKU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds5_sanrenpuku_with_race_code(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds5_sanrenpuku: race_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds5_sanrenpuku(race_code=VALID_RACE_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS5_SANRENPUKU",
        {"RACE_CODE": VALID_RACE_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds5_sanrenpuku_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds5_sanrenpuku: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds5_sanrenpuku(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS5_SANRENPUKU",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)


# get_odds6_sanrentan


def test_get_odds6_sanrentan_without_filters(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds6_sanrentan: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds6_sanrentan()

    mock_table_accessor.get_table_data.assert_called_once_with("ODDS6_SANRENTAN", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds6_sanrentan_with_race_codes_list(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds6_sanrentan: 複数race_codeでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": VALID_RACE_CODES})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = odds_getter.get_odds6_sanrentan(race_code=VALID_RACE_CODES)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "ODDS6_SANRENTAN",
        {"RACE_CODE": VALID_RACE_CODES},
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_odds6_sanrentan_with_date_range(
    odds_getter: OddsGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_odds6_sanrentan: 期間フィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"RACE_CODE": [VALID_RACE_CODE]})
    mock_table_accessor.get_table_data_with_composite_date_period.return_value = expected_df

    result = odds_getter.get_odds6_sanrentan(
        start_date=VALID_START_DATE,
        end_date=VALID_END_DATE,
    )

    mock_table_accessor.get_table_data_with_composite_date_period.assert_called_once_with(
        "ODDS6_SANRENTAN",
        None,
        VALID_START_DATE,
        VALID_END_DATE,
        "KAISAI_NEN",
        "KAISAI_GAPPI",
    )
    pd.testing.assert_frame_equal(result, expected_df)
