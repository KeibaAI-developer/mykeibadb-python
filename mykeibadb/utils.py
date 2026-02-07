"""ユーティリティ関数群.

このモジュールは、引数の検証などの共通処理を提供する。
"""

from datetime import date

from mykeibadb.exceptions import ValidationError


def is_valid_identifier(name: str) -> bool:
    """識別子（カラム名、テーブル名）の妥当性を確認.

    SQLインジェクション対策として、識別子が安全な形式かを検証する。

    Args:
        name (str): 検証する識別子

    Returns:
        bool: 識別子が妥当な場合True
    """
    if not name:
        return False

    # 英数字とアンダースコアのみを許可
    # 先頭は英字またはアンダースコア
    if not (name[0].isalpha() or name[0] == "_"):
        return False

    return all(char.isalnum() or char == "_" for char in name)


def validate_race_code(race_code: str | list[str] | None) -> None:
    """レースコードの形式を検証.

    開催年+月日+競馬場コード+回次+日次+レース番号

    Args:
        race_code (str | list[str] | None): レースコード（16桁）

    Raises:
        TypeError: race_codeの型が不正な場合
        ValidationError: レースコードの形式が不正な場合
    """
    if race_code is None:
        return

    if not isinstance(race_code, (str, list)):
        raise TypeError(
            f"race_codeはstr, list[str], またはNoneである必要があります: {type(race_code).__name__}"
        )

    codes = [race_code] if isinstance(race_code, str) else race_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"レースコードは文字列である必要があります: {code}")
        if len(code) != 16:
            raise ValidationError(
                f"レースコードは16桁である必要があります: {code} (長さ: {len(code)})"
            )
        year_str = code[0:4]
        if not year_str.isdigit():
            raise ValidationError(
                f"レースコードの年部分は数字である必要があります: {code} (年: {year_str})"
            )
        month_str = code[4:6]
        if not month_str.isdigit():
            raise ValidationError(
                f"レースコードの月部分は数字である必要があります: {code} (月: {month_str})"
            )
        day_str = code[6:8]
        if not day_str.isdigit():
            raise ValidationError(
                f"レースコードの日部分は数字である必要があります: {code} (日: {day_str})"
            )
        kai_str = code[10:12]
        if not kai_str.isdigit():
            raise ValidationError(
                f"レースコードの回次部分は数字である必要があります: {code} (回次: {kai_str})"
            )
        nichi_str = code[12:14]
        if not nichi_str.isdigit():
            raise ValidationError(
                f"レースコードの日次部分は数字である必要があります: {code} (日次: {nichi_str})"
            )
        race_str = code[14:16]
        if not race_str.isdigit():
            raise ValidationError(
                f"レースコードのレース番号部分は数字である必要があります: {code} (レース番号: {race_str})"
            )
        month = int(month_str)
        if not (1 <= month <= 12):
            raise ValidationError(f"レースコードの月部分が不正です: {code} (月: {month})")
        day = int(day_str)
        if not (1 <= day <= 31):
            raise ValidationError(f"レースコードの日部分が不正です: {code} (日: {day})")
        race = int(race_str)
        if not (1 <= race <= 12):
            raise ValidationError(
                f"レースコードのレース番号部分が不正です: {code} (レース番号: {race})"
            )


def validate_ketto_toroku_bango(ketto_toroku_bango: str | list[str] | None) -> None:
    """血統登録番号の形式を検証.

    生年(西暦)4桁+品種1桁<コード表2201.品種コード>参照+数字5桁|

    Args:
        ketto_toroku_bango (str | list[str] | None): 血統登録番号（10桁）

    Raises:
        TypeError: ketto_toroku_bangoの型が不正な場合
        ValidationError: 血統登録番号の形式が不正な場合
    """
    if ketto_toroku_bango is None:
        return

    if not isinstance(ketto_toroku_bango, (str, list)):
        raise TypeError(
            f"ketto_toroku_bangoはstr, list[str], またはNoneである必要があります: "
            f"{type(ketto_toroku_bango).__name__}"
        )

    codes = [ketto_toroku_bango] if isinstance(ketto_toroku_bango, str) else ketto_toroku_bango
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"血統登録番号は文字列である必要があります: {code}")
        if len(code) != 10:
            raise ValidationError(
                f"血統登録番号は10桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"血統登録番号は数字のみで構成される必要があります: {code}")


def validate_kishu_code(kishu_code: str | list[str] | None) -> None:
    """騎手コードの形式を検証.

    Args:
        kishu_code (str | list[str] | None): 騎手コード（5桁）

    Raises:
        TypeError: kishu_codeの型が不正な場合
        ValidationError: 騎手コードの形式が不正な場合
    """
    if kishu_code is None:
        return

    if not isinstance(kishu_code, (str, list)):
        raise TypeError(
            f"kishu_codeはstr, list[str], またはNoneである必要があります: {type(kishu_code).__name__}"
        )

    codes = [kishu_code] if isinstance(kishu_code, str) else kishu_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"騎手コードは文字列である必要があります: {code}")
        if len(code) != 5:
            raise ValidationError(
                f"騎手コードは5桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"騎手コードは数字のみで構成される必要があります: {code}")


def validate_chokyoshi_code(chokyoshi_code: str | list[str] | None) -> None:
    """調教師コードの形式を検証.

    Args:
        chokyoshi_code (str | list[str] | None): 調教師コード（5桁）

    Raises:
        TypeError: chokyoshi_codeの型が不正な場合
        ValidationError: 調教師コードの形式が不正な場合
    """
    if chokyoshi_code is None:
        return

    if not isinstance(chokyoshi_code, (str, list)):
        raise TypeError(
            f"chokyoshi_codeはstr, list[str], またはNoneである必要があります: {type(chokyoshi_code).__name__}"
        )

    codes = [chokyoshi_code] if isinstance(chokyoshi_code, str) else chokyoshi_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"調教師コードは文字列である必要があります: {code}")
        if len(code) != 5:
            raise ValidationError(
                f"調教師コードは5桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"調教師コードは数字のみで構成される必要があります: {code}")


def validate_seisansha_code(seisansha_code: str | list[str] | None) -> None:
    """生産者コードの形式を検証.

    Args:
        seisansha_code (str | list[str] | None): 生産者コード（8桁）

    Raises:
        TypeError: seisansha_codeの型が不正な場合
        ValidationError: 生産者コードの形式が不正な場合
    """
    if seisansha_code is None:
        return

    if not isinstance(seisansha_code, (str, list)):
        raise TypeError(
            f"seisansha_codeはstr, list[str], またはNoneである必要があります: {type(seisansha_code).__name__}"
        )

    codes = [seisansha_code] if isinstance(seisansha_code, str) else seisansha_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"生産者コードは文字列である必要があります: {code}")
        if len(code) != 8:
            raise ValidationError(
                f"生産者コードは8桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"生産者コードは数字のみで構成される必要があります: {code}")


def validate_banushi_code(banushi_code: str | list[str] | None) -> None:
    """馬主コードの形式を検証.

    Args:
        banushi_code (str | list[str] | None): 馬主コード（6桁）

    Raises:
        TypeError: banushi_codeの型が不正な場合
        ValidationError: 馬主コードの形式が不正な場合
    """
    if banushi_code is None:
        return

    if not isinstance(banushi_code, (str, list)):
        raise TypeError(
            f"banushi_codeはstr, list[str], またはNoneである必要があります: {type(banushi_code).__name__}"
        )

    codes = [banushi_code] if isinstance(banushi_code, str) else banushi_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"馬主コードは文字列である必要があります: {code}")
        if len(code) != 6:
            raise ValidationError(
                f"馬主コードは6桁である必要があります: {code} (長さ: {len(code)})"
            )


def validate_kaisai_code(kaisai_code: str | list[str] | None) -> None:
    """開催コードの形式を検証.

    Args:
        kaisai_code (str | list[str] | None): 開催コード（14桁）
            開催年+月日+競馬場コード+回次+日次

    Raises:
        TypeError: kaisai_codeの型が不正な場合
        ValidationError: 開催コードの形式が不正な場合
    """
    if kaisai_code is None:
        return

    if not isinstance(kaisai_code, (str, list)):
        raise TypeError(
            f"kaisai_codeはstr, list[str], またはNoneである必要があります: {type(kaisai_code).__name__}"
        )

    codes = [kaisai_code] if isinstance(kaisai_code, str) else kaisai_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"開催コードは文字列である必要があります: {code}")
        if len(code) != 14:
            raise ValidationError(
                f"開催コードは14桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"開催コードは数字のみで構成される必要があります: {code}")


def validate_hanshoku_toroku_bango(hanshoku_toroku_bango: str | list[str] | None) -> None:
    """繁殖登録番号の形式を検証.

    Args:
        hanshoku_toroku_bango (str | list[str] | None): 繁殖登録番号（10桁）

    Raises:
        TypeError: hanshoku_toroku_bangoの型が不正な場合
        ValidationError: 繁殖登録番号の形式が不正な場合
    """
    if hanshoku_toroku_bango is None:
        return

    if not isinstance(hanshoku_toroku_bango, (str, list)):
        raise TypeError(
            f"hanshoku_toroku_bangoはstr, list[str], またはNoneである必要があります: "
            f"{type(hanshoku_toroku_bango).__name__}"
        )

    codes = (
        [hanshoku_toroku_bango] if isinstance(hanshoku_toroku_bango, str) else hanshoku_toroku_bango
    )
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"繁殖登録番号は文字列である必要があります: {code}")
        if len(code) != 10:
            raise ValidationError(
                f"繁殖登録番号は10桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"繁殖登録番号は数字のみで構成される必要があります: {code}")


def validate_keibajo_code(keibajo_code: str | list[str] | None) -> None:
    """競馬場コードの形式を検証.

    Args:
        keibajo_code (str | list[str] | None): 競馬場コード（2桁）

    Raises:
        TypeError: keibajo_codeの型が不正な場合
        ValidationError: 競馬場コードの形式が不正な場合
    """
    if keibajo_code is None:
        return

    if not isinstance(keibajo_code, (str, list)):
        raise TypeError(
            f"keibajo_codeはstr, list[str], またはNoneである必要があります: {type(keibajo_code).__name__}"
        )

    codes = [keibajo_code] if isinstance(keibajo_code, str) else keibajo_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"競馬場コードは文字列である必要があります: {code}")
        if len(code) != 2:
            raise ValidationError(
                f"競馬場コードは2桁である必要があります: {code} (長さ: {len(code)})"
            )


def validate_track_code(track_code: str | list[str] | None) -> None:
    """トラックコードの形式を検証.

    Args:
        track_code (str | list[str] | None): トラックコード（2桁）

    Raises:
        TypeError: track_codeの型が不正な場合
        ValidationError: トラックコードの形式が不正な場合
    """
    if track_code is None:
        return

    if not isinstance(track_code, (str, list)):
        raise TypeError(
            f"track_codeはstr, list[str], またはNoneである必要があります: {type(track_code).__name__}"
        )

    codes = [track_code] if isinstance(track_code, str) else track_code
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"トラックコードは文字列である必要があります: {code}")
        if len(code) != 2:
            raise ValidationError(
                f"トラックコードは2桁である必要があります: {code} (長さ: {len(code)})"
            )
        if not code.isdigit():
            raise ValidationError(f"トラックコードは数字のみで構成される必要があります: {code}")


def validate_tracen_kubun(tracen_kubun: str | list[str] | None) -> None:
    """トレセン区分の形式を検証.

    Args:
        tracen_kubun (str | list[str] | None): トレセン区分

    Raises:
        TypeError: tracen_kubunの型が不正な場合
        ValidationError: トレセン区分の形式が不正な場合
    """
    if tracen_kubun is None:
        return

    if not isinstance(tracen_kubun, (str, list)):
        raise TypeError(
            f"tracen_kubunはstr, list[str], またはNoneである必要があります: {type(tracen_kubun).__name__}"
        )

    codes = [tracen_kubun] if isinstance(tracen_kubun, str) else tracen_kubun
    for code in codes:
        if not isinstance(code, str):
            raise ValidationError(f"トレセン区分は文字列である必要があります: {code}")


def validate_date_range(start_date: date | None, end_date: date | None) -> None:
    """日付範囲の妥当性を検証.

    両方の日付が指定されている場合、start_dateがend_date以前であることを確認する。

    Args:
        start_date (date | None): 開始日
        end_date (date | None): 終了日

    Raises:
        ValidationError: start_dateがend_dateより後の場合
    """
    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise ValidationError(
                f"start_date ({start_date}) はend_date ({end_date}) 以前である必要があります"
            )
