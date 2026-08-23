"""ColumnTypeResolverクラスの単体テスト."""

from unittest.mock import MagicMock

import pytest

from mykeibadb.column_types import ColumnTypeResolver


@pytest.fixture
def mock_connection_manager() -> MagicMock:
    """RACE_SHOSAIの列の型を返すモック化されたConnectionManagerを生成するfixture."""
    mock_cm = MagicMock()
    mock_cm.execute_query.return_value = [
        ("race_code", "character"),
        ("kaisai_nen", "character"),
        ("kyosomei_hondai", "character varying"),
        ("shusso_tosu", "integer"),
    ]
    return mock_cm


@pytest.fixture
def resolver(mock_connection_manager: MagicMock) -> ColumnTypeResolver:
    """ColumnTypeResolverインスタンスを生成するfixture."""
    return ColumnTypeResolver(mock_connection_manager)


# 正常系


def test_blank_padded_char_column_returns_true(resolver: ColumnTypeResolver) -> None:
    """固定長文字列（character）の列に対してTrueを返すことを確認."""
    assert resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE") is True


@pytest.mark.parametrize(
    "column_name",
    ["KYOSOMEI_HONDAI", "SHUSSO_TOSU"],
)
def test_non_blank_padded_char_column_returns_false(
    resolver: ColumnTypeResolver, column_name: str
) -> None:
    """固定長文字列でない列に対してFalseを返すことを確認."""
    assert resolver.is_blank_padded_char("RACE_SHOSAI", column_name) is False


def test_queries_information_schema_once_per_table(
    resolver: ColumnTypeResolver, mock_connection_manager: MagicMock
) -> None:
    """同一テーブルの複数の列を問い合わせてもクエリが1回だけであることを確認.

    列ごとに問い合わせるとテーブルの列数だけクエリが増えるため、テーブル単位で
    まとめて取得してキャッシュする。
    """
    resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE")
    resolver.is_blank_padded_char("RACE_SHOSAI", "KAISAI_NEN")
    resolver.is_blank_padded_char("RACE_SHOSAI", "SHUSSO_TOSU")

    mock_connection_manager.execute_query.assert_called_once()


def test_queries_information_schema_per_table(
    resolver: ColumnTypeResolver, mock_connection_manager: MagicMock
) -> None:
    """テーブルごとにクエリが発行されることを確認."""
    resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE")
    resolver.is_blank_padded_char("UMAGOTO_RACE_JOHO", "RACE_CODE")

    assert mock_connection_manager.execute_query.call_count == 2


@pytest.mark.parametrize(
    "table_name, column_name",
    [
        ("RACE_SHOSAI", "RACE_CODE"),
        ("race_shosai", "race_code"),
        ("Race_Shosai", "Race_Code"),
    ],
)
def test_resolves_regardless_of_case(
    resolver: ColumnTypeResolver, table_name: str, column_name: str
) -> None:
    """テーブル名・カラム名の大文字小文字を問わず解決できることを確認."""
    assert resolver.is_blank_padded_char(table_name, column_name) is True


def test_queries_with_lowercase_table_name(
    resolver: ColumnTypeResolver, mock_connection_manager: MagicMock
) -> None:
    """information_schemaへは小文字のテーブル名で問い合わせることを確認.

    PostgreSQLのinformation_schemaはテーブル名を小文字で保持する。
    """
    resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE")

    _, params = mock_connection_manager.execute_query.call_args[0]
    assert params == ("race_shosai", "race_shosai")


def test_resolves_table_through_search_path(
    resolver: ColumnTypeResolver, mock_connection_manager: MagicMock
) -> None:
    """テーブルをsearch_pathで解決することを確認.

    データ取得クエリはスキーマ非修飾で発行されsearch_pathで解決されるため、
    列の型も同じテーブルを見る必要がある。テーブル名だけでinformation_schemaを
    絞り込むと、同名テーブルが複数のスキーマにある場合に別のテーブルの型を拾う。
    """
    resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE")

    query, _ = mock_connection_manager.execute_query.call_args[0]
    assert "to_regclass" in query
    assert "table_schema" in query


# 準正常系


def test_unknown_column_returns_false(resolver: ColumnTypeResolver) -> None:
    """存在しないカラムに対してFalseを返すことを確認."""
    assert resolver.is_blank_padded_char("RACE_SHOSAI", "NOT_EXIST") is False


def test_unknown_table_returns_false(mock_connection_manager: MagicMock) -> None:
    """存在しないテーブルに対してFalseを返すことを確認."""
    mock_connection_manager.execute_query.return_value = []
    resolver = ColumnTypeResolver(mock_connection_manager)

    assert resolver.is_blank_padded_char("NOT_EXIST", "RACE_CODE") is False


def test_query_failure_returns_false(mock_connection_manager: MagicMock) -> None:
    """問い合わせが失敗した場合にFalseを返すことを確認.

    Falseを返すことで呼び出し側はTRIMを付ける側（従来の振る舞い）へ倒せる。
    速度は落ちるが結果は正しくなる。
    """
    mock_connection_manager.execute_query.side_effect = RuntimeError("接続に失敗しました")
    resolver = ColumnTypeResolver(mock_connection_manager)

    assert resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE") is False


def test_query_failure_is_not_retried(mock_connection_manager: MagicMock) -> None:
    """問い合わせが失敗したテーブルへ繰り返し問い合わせないことを確認."""
    mock_connection_manager.execute_query.side_effect = RuntimeError("接続に失敗しました")
    resolver = ColumnTypeResolver(mock_connection_manager)

    resolver.is_blank_padded_char("RACE_SHOSAI", "RACE_CODE")
    resolver.is_blank_padded_char("RACE_SHOSAI", "KAISAI_NEN")

    mock_connection_manager.execute_query.assert_called_once()
