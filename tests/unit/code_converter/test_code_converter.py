"""code_converterモジュールのテスト."""

import pytest

from mykeibadb.code_converter import (
    convert_babajotai_code,
    convert_chakusa_code,
    convert_grade_code,
    convert_hinshu_code,
    convert_ijo_kubun_code,
    convert_juryo_shubetsu_code,
    convert_keibajo_code,
    convert_kijo_shikaku_code,
    convert_kishu_minarai_code,
    convert_kyoso_joken_code,
    convert_kyoso_kigo_code,
    convert_kyoso_shubetsu_code,
    convert_moshoku_code,
    convert_seibetsu_code,
    convert_tenko_code,
    convert_tozai_shozoku_code,
    convert_track_code,
    convert_uma_kigo_code,
    convert_yobi_code,
)


# 正常系
@pytest.mark.parametrize(
    "code, expected",
    [
        ("01", "札幌"),
        ("05", "東京"),
        ("09", "阪神"),
        ("A4", "アメリ"),
        ("G0", "香港"),
        ("00", ""),  # 未設定
        ("99", ""),  # 存在しないコード
    ],
)
def test_convert_keibajo_code(code: str, expected: str) -> None:
    """競馬場コード変換のテスト."""
    assert convert_keibajo_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "土"),
        ("2", "日"),
        ("3", "祝"),
        ("8", "金"),
        ("0", ""),  # 未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_yobi_code(code: str, expected: str) -> None:
    """曜日コード変換のテスト."""
    assert convert_yobi_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("A", "GI"),
        ("B", "GII"),
        ("C", "GIII"),
        ("D", "重賞"),
        ("E", "特別競走"),
        ("L", "L"),
        ("_", ""),  # 一般競走または未設定
        ("Z", ""),  # 存在しないコード
    ],
)
def test_convert_grade_code(code: str, expected: str) -> None:
    """グレードコード変換のテスト."""
    assert convert_grade_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("11", "サラ系２歳"),
        ("13", "サラ系３歳以上"),
        ("19", "サラ障害４歳以上"),
        ("24", "アラブ系４歳以上"),
        ("0", ""),  # 未設定
        ("99", ""),  # 存在しないコード
    ],
)
def test_convert_kyoso_shubetsu_code(code: str, expected: str) -> None:
    """競走種別コード変換のテスト."""
    assert convert_kyoso_shubetsu_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("000", ""),  # 記号なし
        ("001", "(指定)"),
        ("020", "牝"),
        ("030", "牡・ｾﾝ"),
        ("A00", "(混合)"),
        ("N00", "(国際)"),
        ("999", ""),  # 存在しないコード
    ],
)
def test_convert_kyoso_kigo_code(code: str, expected: str) -> None:
    """競走記号コード変換のテスト."""
    assert convert_kyoso_kigo_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("005", "５００万円以下"),
        ("010", "１０００万円以下"),
        ("016", "１６００万円以下"),
        ("701", "新馬"),
        ("703", "未勝利"),
        ("999", "オープン"),
        ("000", ""),  # 未設定
        ("9999", ""),  # 存在しないコード
    ],
)
def test_convert_kyoso_joken_code(code: str, expected: str) -> None:
    """競走条件コード変換のテスト."""
    assert convert_kyoso_joken_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "ハンデ"),
        ("2", "別定"),
        ("3", "馬齢"),
        ("4", "定量"),
        ("0", ""),  # 未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_juryo_shubetsu_code(code: str, expected: str) -> None:
    """重量種別コード変換のテスト."""
    assert convert_juryo_shubetsu_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("11", "芝・左"),
        ("23", "ダート・左"),
        ("24", "ダート・右"),
        ("10", "芝・直"),
        ("51", "芝・襷"),
        ("0", ""),  # 未設定
        ("99", ""),  # 存在しないコード
    ],
)
def test_convert_track_code(code: str, expected: str) -> None:
    """トラックコード変換のテスト."""
    assert convert_track_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "良"),
        ("2", "稍重"),
        ("3", "重"),
        ("4", "不良"),
        ("0", ""),  # 未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_babajotai_code(code: str, expected: str) -> None:
    """馬場状態コード変換のテスト."""
    assert convert_babajotai_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "晴"),
        ("2", "曇"),
        ("3", "雨"),
        ("5", "雪"),
        ("0", ""),  # 未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_tenko_code(code: str, expected: str) -> None:
    """天候コード変換のテスト."""
    assert convert_tenko_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "出走取消"),
        ("2", "発走除外"),
        ("5", "失格"),
        ("7", "降着"),
        ("0", ""),  # 下記以外または未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_ijo_kubun_code(code: str, expected: str) -> None:
    """異常区分コード変換のテスト."""
    assert convert_ijo_kubun_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1__", "１馬身"),
        ("2__", "２馬身"),
        ("A__", "アタマ"),
        ("H__", "ハナ"),
        ("K__", "クビ"),
        ("T__", "大差"),
        ("___", ""),  # 未設定
        ("999", ""),  # 存在しないコード
    ],
)
def test_convert_chakusa_code(code: str, expected: str) -> None:
    """着差コード変換のテスト."""
    assert convert_chakusa_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "サラブレッド"),
        ("2", "サラブレッド系種"),
        ("5", "アングロアラブ"),
        ("7", "アラブ"),
        ("0", ""),  # 未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_hinshu_code(code: str, expected: str) -> None:
    """品種コード変換のテスト."""
    assert convert_hinshu_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "牡"),
        ("2", "牝"),
        ("3", "ｾﾝ"),
        ("0", ""),  # 未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_seibetsu_code(code: str, expected: str) -> None:
    """性別コード変換のテスト."""
    assert convert_seibetsu_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("01", "栗毛"),
        ("03", "鹿毛"),
        ("07", "芦毛"),
        ("11", "白毛"),
        ("00", ""),  # 未設定
        ("99", ""),  # 存在しないコード
    ],
)
def test_convert_moshoku_code(code: str, expected: str) -> None:
    """毛色コード変換のテスト."""
    assert convert_moshoku_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("01", "(抽)"),
        ("03", "(父)"),
        ("06", "(外)"),
        ("15", "(招)"),
        ("26", "[外]"),
        ("00", ""),  # 下記以外または未設定
        ("99", ""),  # 存在しないコード
    ],
)
def test_convert_uma_kigo_code(code: str, expected: str) -> None:
    """馬記号コード変換のテスト."""
    assert convert_uma_kigo_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "関東"),
        ("2", "関西"),
        ("3", "地方招待"),
        ("4", "外国招待"),
        ("0", ""),  # 下記以外または未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_tozai_shozoku_code(code: str, expected: str) -> None:
    """東西所属コード変換のテスト."""
    assert convert_tozai_shozoku_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "平・障"),
        ("2", "平地"),
        ("3", "障害"),
        ("0", "資格なし"),  # または未設定
        ("9", ""),  # 存在しないコード
    ],
)
def test_convert_kijo_shikaku_code(code: str, expected: str) -> None:
    """騎乗資格コード変換のテスト."""
    assert convert_kijo_shikaku_code(code) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1", "☆"),
        ("2", "△"),
        ("3", "▲"),
        ("4", "★"),
        ("9", "◇"),
        ("0", ""),  # 下記以外または未設定
        ("99", ""),  # 存在しないコード
    ],
)
def test_convert_kishu_minarai_code(code: str, expected: str) -> None:
    """騎手見習コード変換のテスト."""
    assert convert_kishu_minarai_code(code) == expected
