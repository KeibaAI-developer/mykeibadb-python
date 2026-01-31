"""TableGettersクラスのテスト用共通fixture."""

from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mykeibadb.getters import TableGetters


@pytest.fixture
def mock_table_accessor() -> MagicMock:
    """モック化されたTableAccessorを生成するfixture."""
    mock_ta = MagicMock()
    mock_ta.get_table_data.return_value = pd.DataFrame()
    return mock_ta


@pytest.fixture
def mock_connection_manager() -> MagicMock:
    """モック化されたConnectionManagerを生成するfixture."""
    mock_cm = MagicMock()
    mock_cm.fetch_dataframe.return_value = pd.DataFrame()
    return mock_cm


@pytest.fixture
def table_getters(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> TableGetters:
    """TableGettersインスタンスを生成するfixture.

    ConfigManager.from_env, ConnectionManager, TableAccessorをモック化する。
    """
    with (
        patch("mykeibadb.getters.ConfigManager") as mock_config_manager,
        patch("mykeibadb.getters.ConnectionManager") as mock_cm_class,
        patch("mykeibadb.getters.TableAccessor") as mock_ta_class,
    ):
        mock_config_manager.from_env.return_value = MagicMock()
        mock_cm_class.return_value = mock_connection_manager
        mock_ta_class.return_value = mock_table_accessor

        getters = TableGetters()
        # モックを直接設定
        getters.connection_manager = mock_connection_manager
        getters.table_accessor = mock_table_accessor

        return getters


# 有効なテストデータ
VALID_RACE_CODE = "2025010306010101"  # 16桁
VALID_RACE_CODES = ["2025010306010101", "2025010306010102"]
VALID_KETTO_TOROKU_BANGO = "2022100001"  # 10桁
VALID_KETTO_TOROKU_BANGOS = ["2022100001", "2022100002"]
VALID_KISHU_CODE = "00001"  # 5桁
VALID_CHOKYOSHI_CODE = "00001"  # 5桁
VALID_SEISANSHA_CODE = "00000001"  # 8桁
VALID_BANUSHI_CODE = "000001"  # 6桁
VALID_KAISAI_CODE = "2025010306010000"  # 16桁
VALID_HANSHOKU_TOROKU_BANGO = "2022100001"  # 10桁
VALID_KEIBAJO_CODE = "06"  # 2桁
VALID_TRACK_CODE = "01"  # 2桁
VALID_TRACEN_KUBUN = "1"  # 1桁
VALID_START_DATE = date(2025, 1, 1)
VALID_END_DATE = date(2025, 1, 31)
