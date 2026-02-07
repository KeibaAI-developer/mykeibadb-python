"""コード変換モジュール.

mykeibadbのコードテーブルに基づいてコード値を人間が読める形式に変換する関数を提供する。
"""

import os
from functools import lru_cache
from pathlib import Path

import yaml


def convert_keibajo_code(code: str) -> str:
    """競馬場コードを場略名(3文字)に変換する.

    Args:
        code: 競馬場コード（例: "01", "05", "A4"）

    Returns:
        場略名(3文字)。該当するコードがない場合は空文字列を返す。
    """
    # 競馬場コード -> 場略名(3文字) のマッピング
    keibajo_code_to_name: dict[str, str] = _load_yaml("keibajo_code.yml")
    return keibajo_code_to_name.get(code, "")


def convert_yobi_code(code: str) -> str:
    """曜日コードを略名(1文字)に変換する.

    Args:
        code: 曜日コード（例: "1", "2", "3"）

    Returns:
        略名(1文字)。該当するコードがない場合は空文字列を返す。
    """
    yobi_code_to_name: dict[str, str] = _load_yaml("yobi_code.yml")
    return yobi_code_to_name.get(code, "")


def convert_grade_code(code: str) -> str:
    """グレードコードを名称に変換する.

    Args:
        code: グレードコード（例: "A", "B", "C"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    grade_code_to_name: dict[str, str] = _load_yaml("grade_code.yml")
    return grade_code_to_name.get(code, "")


def convert_kyoso_shubetsu_code(code: str) -> str:
    """競走種別コードを略名(8文字)に変換する.

    Args:
        code: 競走種別コード（例: "11", "12", "13"）

    Returns:
        略名(8文字)。該当するコードがない場合は空文字列を返す。
    """
    kyoso_shubetsu_code_to_name: dict[str, str] = _load_yaml("kyoso_shubetsu_code.yml")
    return kyoso_shubetsu_code_to_name.get(code, "")


def convert_kyoso_kigo_code(code: str) -> str:
    """競走記号コードを名称に変換する.

    Args:
        code: 競走記号コード（例: "000", "001", "020"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    kyoso_kigo_code_to_name: dict[str, str] = _load_yaml("kyoso_kigo_code.yml")
    return kyoso_kigo_code_to_name.get(code, "")


def convert_kyoso_joken_code(code: str) -> str:
    """競走条件コードを名称に変換する.

    Args:
        code: 競走条件コード（例: "005", "010", "701"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    kyoso_joken_code_to_name: dict[str, str] = _load_yaml("kyoso_joken_code.yml")
    return kyoso_joken_code_to_name.get(code, "")


def convert_juryo_shubetsu_code(code: str) -> str:
    """重量種別コードを内容に変換する.

    Args:
        code: 重量種別コード（例: "1", "2", "3"）

    Returns:
        内容。該当するコードがない場合は空文字列を返す。
    """
    juryo_shubetsu_code_to_name: dict[str, str] = _load_yaml("juryo_shubetsu_code.yml")
    return juryo_shubetsu_code_to_name.get(code, "")


def convert_track_code(code: str) -> str:
    """トラックコードを略名(6文字)に変換する.

    Args:
        code: トラックコード（例: "11", "23", "24"）

    Returns:
        略名(6文字)。該当するコードがない場合は空文字列を返す。
    """
    track_code_to_name: dict[str, str] = _load_yaml("track_code.yml")
    return track_code_to_name.get(code, "")


def convert_babajotai_code(code: str) -> str:
    """馬場状態コードを名称に変換する.

    Args:
        code: 馬場状態コード（例: "1", "2", "3"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    babajotai_code_to_name: dict[str, str] = _load_yaml("babajotai_code.yml")
    return babajotai_code_to_name.get(code, "")


def convert_tenko_code(code: str) -> str:
    """天候コードを名称に変換する.

    Args:
        code: 天候コード（例: "1", "2", "3"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    tenko_code_to_name: dict[str, str] = _load_yaml("tenko_code.yml")
    return tenko_code_to_name.get(code, "")


def convert_ijo_kubun_code(code: str) -> str:
    """異常区分コードを名称に変換する.

    Args:
        code: 異常区分コード（例: "1", "2", "5"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    ijo_kubun_code_to_name: dict[str, str] = _load_yaml("ijo_kubun_code.yml")
    return ijo_kubun_code_to_name.get(code, "")


def convert_chakusa_code(code: str) -> str:
    """着差コードを名称に変換する.

    Args:
        code: 着差コード（例: "1__", "A__", "K__"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    chakusa_code_to_name: dict[str, str] = _load_yaml("chakusa_code.yml")
    return chakusa_code_to_name.get(code, "")


def convert_hinshu_code(code: str) -> str:
    """品種コードを名称に変換する.

    Args:
        code: 品種コード（例: "01", "05", "07"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    hinshu_code_to_name: dict[str, str] = _load_yaml("hinshu_code.yml")
    return hinshu_code_to_name.get(code, "")


def convert_seibetsu_code(code: str) -> str:
    """性別コードを略に変換する.

    Args:
        code: 性別コード（例: "1", "2", "3"）

    Returns:
        略。該当するコードがない場合は空文字列を返す。
    """
    seibetsu_code_to_name: dict[str, str] = _load_yaml("seibetsu_code.yml")
    return seibetsu_code_to_name.get(code, "")


def convert_moshoku_code(code: str) -> str:
    """毛色コードを名称に変換する.

    Args:
        code: 毛色コード（例: "1", "3", "7"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    moshoku_code_to_name: dict[str, str] = _load_yaml("moshoku_code.yml")
    return moshoku_code_to_name.get(code, "")


def convert_uma_kigo_code(code: str) -> str:
    """馬記号コードを名称に変換する.

    Args:
        code: 馬記号コード（例: "01", "03", "15"）

    Returns:
        名称。該当するコードがない場合は空文字列を返す。
    """
    uma_kigo_code_to_name: dict[str, str] = _load_yaml("uma_kigo_code.yml")
    return uma_kigo_code_to_name.get(code, "")


def convert_tozai_shozoku_code(code: str) -> str:
    """東西所属コードを名称１に変換する.

    Args:
        code: 東西所属コード（例: "1", "2", "3"）

    Returns:
        名称１。該当するコードがない場合は空文字列を返す。
    """
    tozai_shozoku_code_to_name: dict[str, str] = _load_yaml("tozai_shozoku_code.yml")
    return tozai_shozoku_code_to_name.get(code, "")


def convert_kijo_shikaku_code(code: str) -> str:
    """騎乗資格コードを内容に変換する.

    Args:
        code: 騎乗資格コード（例: "1", "2", "3"）

    Returns:
        内容。該当するコードがない場合は空文字列を返す。
    """
    kijo_shikaku_code_to_name: dict[str, str] = _load_yaml("kijo_shikaku_code.yml")
    return kijo_shikaku_code_to_name.get(code, "")


def convert_kishu_minarai_code(code: str) -> str:
    """騎手見習コードを略名に変換する.

    Args:
        code: 騎手見習コード（例: "1", "2", "3"）

    Returns:
        略名。該当するコードがない場合は空文字列を返す。
    """
    kishu_minarai_code_to_name: dict[str, str] = _load_yaml("kishu_minarai_code.yml")
    return kishu_minarai_code_to_name.get(code, "")


@lru_cache(maxsize=None)
def _load_yaml(filename: str) -> dict[str, str]:
    """YAMLファイルを読み込んで辞書として返す.

    同じファイル名に対する結果はキャッシュされ、ファイルI/Oは初回のみ実行される。

    Args:
        filename: 読み込むYAMLファイル名

    Returns:
        YAMLファイルの内容を表す辞書
    """
    yaml_path = os.path.join(Path(__file__).parent, "mapping", filename)
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
