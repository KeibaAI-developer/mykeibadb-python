"""is_valid_identifier関数のテスト."""

import pytest

from mykeibadb.utils import is_valid_identifier

# 正常系


@pytest.mark.parametrize(
    "valid_identifier",
    [
        "table_name",  # 英字とアンダースコア
        "TableName",  # 大文字を含む
        "table123",  # 数字を含む
        "table_name_123",  # 英字、数字、アンダースコアの組み合わせ
        "_private",  # アンダースコア始まり
        "_",  # アンダースコアのみ
        "a",  # 1文字
        "RACE_CODE",  # 大文字とアンダースコア
        "Column1",  # 英字と数字
        "a1b2c3",  # 英数字混合
    ],
)
def test_is_valid_identifier_with_valid_identifiers(valid_identifier: str) -> None:
    """is_valid_identifier: 有効な識別子でTrueを返すことを確認."""
    assert is_valid_identifier(valid_identifier) is True


# 準正常系


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        "",  # 空文字列
        "1table",  # 数字始まり
        "123",  # 数字のみ
        "table-name",  # ハイフン含む
        "table name",  # スペース含む
        "table.name",  # ドット含む
        "table;name",  # セミコロン含む
        "table'name",  # シングルクォート含む
        'table"name',  # ダブルクォート含む
        "table*name",  # アスタリスク含む
        "table(name)",  # 括弧含む
        "table[name]",  # 角括弧含む
        "table{name}",  # 波括弧含む
        "table,name",  # カンマ含む
        "table@name",  # アットマーク含む
        "table#name",  # ハッシュ含む
        "table$name",  # ドル記号含む
        "table%name",  # パーセント含む
        "table&name",  # アンパサンド含む
        "table+name",  # プラス含む
        "table=name",  # イコール含む
        "table\\name",  # バックスラッシュ含む
        "table/name",  # スラッシュ含む
        "table|name",  # パイプ含む
        "table<name>",  # 不等号含む
        "table!name",  # 感嘆符含む
        "table?name",  # 疑問符含む
        "table~name",  # チルダ含む
        "table`name",  # バッククォート含む
    ],
)
def test_is_valid_identifier_with_invalid_identifiers(invalid_identifier: str) -> None:
    """is_valid_identifier: 無効な識別子でFalseを返すことを確認."""
    assert is_valid_identifier(invalid_identifier) is False
