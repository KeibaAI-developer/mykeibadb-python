"""umagoto_race_joho の出走の行を絞るSQL部品モジュール."""


def ran_entry_condition(alias: str) -> str:
    """umagoto_race_joho の行のうち、出走しなかった馬の行でない行に絞る SQL の条件式を返す.

    出走馬名表に載ったあと出馬表に載らなかった馬の行（行のデータ区分が 1 で、
    同じレースの race_shosai のデータ区分が 1 でない行）を除く。
    出馬表の発表前（race_shosai のデータ区分も 1）の行と、データ区分が NULL の行
    （apply_virtual_race で差し込んだ仮のレースの行）は残す。
    race_shosai は条件式の中のサブクエリで引くため、呼び出し側で結合する必要はない。

    Args:
        alias (str): umagoto_race_joho のSQLエイリアス

    Returns:
        str: WHERE 句に AND でつなげる条件式
    """
    return (
        f"({alias}.data_kubun IS DISTINCT FROM '1' "
        f"OR NOT EXISTS (SELECT 1 FROM race_shosai ran_rs "
        f"WHERE ran_rs.race_code = {alias}.race_code AND ran_rs.data_kubun <> '1'))"
    )
