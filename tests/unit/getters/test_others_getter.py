"""OthersGetterクラスのテスト."""

from unittest.mock import MagicMock

import pandas as pd

from mykeibadb.getters import OthersGetter

from .conftest import VALID_BANUSHI_CODE

# 正常系 - get_shobufuku


def test_get_shobufuku_without_filters(
    others_getter: OthersGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shobufuku: フィルタなしで呼び出せることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = others_getter.get_shobufuku()

    mock_table_accessor.get_table_data.assert_called_once_with("SHOBUFUKU", None)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_shobufuku_with_banushi_code(
    others_getter: OthersGetter,
    mock_table_accessor: MagicMock,
) -> None:
    """get_shobufuku: banushi_codeフィルタでデータを取得できることを確認."""
    expected_df = pd.DataFrame({"BANUSHI_CODE": [VALID_BANUSHI_CODE]})
    mock_table_accessor.get_table_data.return_value = expected_df

    result = others_getter.get_shobufuku(banushi_code=VALID_BANUSHI_CODE)

    mock_table_accessor.get_table_data.assert_called_once_with(
        "SHOBUFUKU",
        {"BANUSHI_CODE": VALID_BANUSHI_CODE},
    )
    pd.testing.assert_frame_equal(result, expected_df)
