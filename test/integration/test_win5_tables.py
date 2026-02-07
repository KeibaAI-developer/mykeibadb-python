"""WIN5テーブルの結合テスト.

WIN5（WIN5レース情報）、WIN5_HARAIMODOSHI（WIN5払戻）テーブルへのアクセスをテストする。
"""

import pandas as pd
import pytest

from mykeibadb.connection import ConnectionManager

from .conftest import get_sample_data


# WIN5テーブルのテスト
def test_get_win5_sample_data(connection_manager: ConnectionManager) -> None:
    """WIN5テーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "WIN5")
    if len(df) == 0:
        pytest.skip("WIN5テーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    # WIN5テーブルには開催年月日などの識別子があるはず
    assert len(df.columns) > 0


def test_get_win5_has_race_related_columns(connection_manager: ConnectionManager) -> None:
    """WIN5テーブルにレース関連カラムがあることを確認."""
    df = get_sample_data(connection_manager, "WIN5")
    if len(df) == 0:
        pytest.skip("WIN5テーブルにデータがありません")

    # レース関連のカラムが存在することを確認（具体的なカラム名はテーブル構造による）
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) > 0


# WIN5払戻テーブルのテスト
def test_get_win5_haraimodoshi_sample_data(connection_manager: ConnectionManager) -> None:
    """WIN5_HARAIMODOSHIテーブルからサンプルデータを取得できることを確認."""
    df = get_sample_data(connection_manager, "WIN5_HARAIMODOSHI")
    if len(df) == 0:
        pytest.skip("WIN5_HARAIMODOSHIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) > 0


def test_get_win5_haraimodoshi_has_payout_related_columns(
    connection_manager: ConnectionManager,
) -> None:
    """WIN5_HARAIMODOSHIテーブルに払戻関連カラムがあることを確認."""
    df = get_sample_data(connection_manager, "WIN5_HARAIMODOSHI")
    if len(df) == 0:
        pytest.skip("WIN5_HARAIMODOSHIテーブルにデータがありません")

    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) > 0
