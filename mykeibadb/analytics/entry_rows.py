"""umagoto_race_joho の出走の行を絞るSQL部品モジュール."""


def ran_entry_condition(alias: str) -> str:
    """umagoto_race_joho の行のうち、出走しなかった馬の行でない行に絞る SQL の条件式を返す.

    出走馬名表に載ったあと出馬表に載らなかった馬の行（行のデータ区分が 1 で、
    同じレースの race_shosai のデータ区分が 1 でない行）を除く。
    出馬表の発表前（race_shosai のデータ区分も 1）の行と、データ区分が NULL の行
    （apply_virtual_race で差し込んだ仮のレースの行）は残す。
    race_shosai は条件式の中のサブクエリで引くため、呼び出し側で結合する必要はない。
    行のデータ区分の比較をサブクエリの中に置き、NOT EXISTS だけの条件にしている。
    OR でつなぐと、反結合にならず大きな集計の実行計画が遅くなるため。

    Args:
        alias (str): umagoto_race_joho のSQLエイリアス

    Returns:
        str: WHERE 句に AND でつなげる条件式
    """
    # サブクエリの別名を引数の別名から作り、外側の別名を隠さないようにする
    rs = f"{alias}_ran_rs"
    return (
        f"NOT EXISTS (SELECT 1 FROM race_shosai {rs} "
        f"WHERE {rs}.race_code = {alias}.race_code "
        f"AND {alias}.data_kubun = '1' AND {rs}.data_kubun <> '1')"
    )
