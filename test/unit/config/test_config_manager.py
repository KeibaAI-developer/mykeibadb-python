"""ConfigManagerクラスの単体テスト."""

import os
from unittest.mock import patch

import pytest

from mykeibadb.config import ConfigManager, DBConfig


# 正常系
def test_dbconfig_default_values() -> None:
    """DBConfigのデフォルト値が正しいことを確認する."""
    config = DBConfig()
    assert config.host == "localhost"
    assert config.port == 5432
    assert config.database == "mykeibadb"
    assert config.user == "postgres"
    assert config.password == "postgres"


def test_config_manager_from_env() -> None:
    """環境変数からDB設定を読み込むことができることを確認する."""
    env_vars = {
        "MYKEIBADB_HOST": "testhost",
        "MYKEIBADB_PORT": "5433",
        "MYKEIBADB_DATABASE": "testdb",
        "MYKEIBADB_USER": "testuser",
        "MYKEIBADB_PASSWORD": "testpass",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        config = ConfigManager.from_env()
        assert config.host == "testhost"
        assert config.port == 5433
        assert config.database == "testdb"
        assert config.user == "testuser"
        assert config.password == "testpass"


def test_config_manager_load_config() -> None:
    """ConfigManager経由でDB設定を読み込むことができることを確認する."""
    env_vars = {
        "MYKEIBADB_HOST": "managerhost",
        "MYKEIBADB_PORT": "5434",
        "MYKEIBADB_DATABASE": "managerdb",
        "MYKEIBADB_USER": "manageruser",
        "MYKEIBADB_PASSWORD": "managerpass",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        manager = ConfigManager()
        config = manager.load_config()
        assert config.host == "managerhost"
        assert config.port == 5434
        assert config.database == "managerdb"
        assert config.user == "manageruser"
        assert config.password == "managerpass"


def test_config_manager_partial_env() -> None:
    """一部の環境変数だけ設定されている場合、残りはデフォルト値を使用することを確認する."""
    env_vars = {
        "MYKEIBADB_HOST": "partialhost",
        "MYKEIBADB_DATABASE": "partialdb",
    }
    with patch.dict(os.environ, env_vars, clear=True):
        with patch("mykeibadb.config.load_dotenv"):
            config = ConfigManager.from_env()
            assert config.host == "partialhost"
            assert config.port == 5432  # デフォルト値
            assert config.database == "partialdb"
            assert config.user == "postgres"  # デフォルト値
            assert config.password == "postgres"  # デフォルト値


def test_config_manager_from_env_no_env_vars() -> None:
    """環境変数が設定されていない場合、デフォルト値を使用することを確認する."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("mykeibadb.config.load_dotenv"):
            config = ConfigManager.from_env()
            assert config.host == "localhost"
            assert config.port == 5432
            assert config.database == "mykeibadb"
            assert config.user == "postgres"
            assert config.password == "postgres"


# 準正常系
def test_config_manager_from_env_invalid_port_too_low() -> None:
    """ポート番号が範囲外（下限未満）の場合、ValueErrorが発生することを確認する."""
    env_vars = {
        "MYKEIBADB_PORT": "0",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError, match="ポート番号は1～65535の範囲で指定してください"):
            ConfigManager.from_env()


def test_config_manager_from_env_invalid_port_too_high() -> None:
    """ポート番号が範囲外（上限超過）の場合、ValueErrorが発生することを確認する."""
    env_vars = {
        "MYKEIBADB_PORT": "65536",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError, match="ポート番号は1～65535の範囲で指定してください"):
            ConfigManager.from_env()


def test_config_manager_from_env_invalid_port_non_numeric() -> None:
    """ポート番号が数値でない場合、ValueErrorが発生することを確認する."""
    env_vars = {
        "MYKEIBADB_PORT": "invalid",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError):
            ConfigManager.from_env()


def test_config_manager_load_config_invalid_port() -> None:
    """ConfigManagerのload_configでポート番号が範囲外の場合、ValueErrorが発生することを確認する."""
    env_vars = {
        "MYKEIBADB_PORT": "99999",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        manager = ConfigManager()
        with pytest.raises(ValueError, match="ポート番号は1～65535の範囲で指定してください"):
            manager.load_config()
