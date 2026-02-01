"""Getterクラスのテスト用共通fixture."""

from datetime import date
from typing import TypeVar
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mykeibadb.getters import (
    BaseGetter,
    ChokyoGetter,
    HyosuGetter,
    KyosobaGetter,
    MasterGetter,
    MiningGetter,
    OddsGetter,
    OthersGetter,
    RaceGetter,
    ShussobetsuGetter,
    SokuhoGetter,
    Win5Getter,
)

T = TypeVar("T", bound=BaseGetter)


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


def _create_getter(
    getter_class: type[T],
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> T:
    """共通のGetterインスタンス生成ロジック."""
    with (
        patch("mykeibadb.getters.base.ConfigManager") as mock_config_manager,
        patch("mykeibadb.getters.base.ConnectionManager") as mock_cm_class,
        patch("mykeibadb.getters.base.TableAccessor") as mock_ta_class,
    ):
        mock_config_manager.from_env.return_value = MagicMock()
        mock_cm_class.return_value = mock_connection_manager
        mock_ta_class.return_value = mock_table_accessor

        getter = getter_class()
        # モックを直接設定
        getter.connection_manager = mock_connection_manager
        getter.table_accessor = mock_table_accessor

        return getter


@pytest.fixture
def table_getters(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> RaceGetter:
    """後方互換性のためのTableGetters(RaceGetter)インスタンス fixture.

    ConfigManager.from_env, ConnectionManager, TableAccessorをモック化する。
    """
    return _create_getter(RaceGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def race_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> RaceGetter:
    """RaceGetterインスタンスを生成するfixture."""
    return _create_getter(RaceGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def hyosu_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> HyosuGetter:
    """HyosuGetterインスタンスを生成するfixture."""
    return _create_getter(HyosuGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def odds_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> OddsGetter:
    """OddsGetterインスタンスを生成するfixture."""
    return _create_getter(OddsGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def master_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> MasterGetter:
    """MasterGetterインスタンスを生成するfixture."""
    return _create_getter(MasterGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def shussobetsu_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> ShussobetsuGetter:
    """ShussobetsuGetterインスタンスを生成するfixture."""
    return _create_getter(ShussobetsuGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def chokyo_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> ChokyoGetter:
    """ChokyoGetterインスタンスを生成するfixture."""
    return _create_getter(ChokyoGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def kyosoba_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> KyosobaGetter:
    """KyosobaGetterインスタンスを生成するfixture."""
    return _create_getter(KyosobaGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def mining_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> MiningGetter:
    """MiningGetterインスタンスを生成するfixture."""
    return _create_getter(MiningGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def win5_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> Win5Getter:
    """Win5Getterインスタンスを生成するfixture."""
    return _create_getter(Win5Getter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def sokuho_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> SokuhoGetter:
    """SokuhoGetterインスタンスを生成するfixture."""
    return _create_getter(SokuhoGetter, mock_table_accessor, mock_connection_manager)


@pytest.fixture
def others_getter(
    mock_table_accessor: MagicMock,
    mock_connection_manager: MagicMock,
) -> OthersGetter:
    """OthersGetterインスタンスを生成するfixture."""
    return _create_getter(OthersGetter, mock_table_accessor, mock_connection_manager)


# 有効なテストデータ
VALID_RACE_CODE = "2025010306010101"  # 16桁
VALID_RACE_CODES = ["2025010306010101", "2025010306010102"]
VALID_KETTO_TOROKU_BANGO = "2022100001"  # 10桁
VALID_KETTO_TOROKU_BANGOS = ["2022100001", "2022100002"]
VALID_KISHU_CODE = "00666"  # 5桁
VALID_CHOKYOSHI_CODE = "01126"  # 5桁
VALID_SEISANSHA_CODE = "39312600"  # 8桁
VALID_BANUSHI_CODE = "232031"  # 6桁
VALID_KAISAI_CODE = "20250103060101"  # 14桁（開催年+月日+競馬場コード+回次+日次）
VALID_KEITO_ID = "0101080201010201"
VALID_HANSHOKU_TOROKU_BANGO = "1220052840"  # 10桁
VALID_KEIBAJO_CODE = "06"  # 2桁
VALID_TRACK_CODE = "01"  # 2桁
VALID_TRACEN_KUBUN = "1"  # 1桁
VALID_START_DATE = date(2025, 1, 1)
VALID_END_DATE = date(2025, 1, 31)
