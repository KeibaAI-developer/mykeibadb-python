"""mykeibadb-python パッケージ初期化テスト."""


def test_package_import() -> None:
    """パッケージのインポートが正常に動作することを確認."""
    import mykeibadb

    assert mykeibadb is not None


def test_package_has_version() -> None:
    """パッケージにバージョン情報が含まれることを確認."""
    import mykeibadb

    assert hasattr(mykeibadb, "__version__")
