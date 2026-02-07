# mykeibadb-python

## 概要

`mykeibadb-python`は、[mykeibadb](https://keough.watson.jp/wp/mykeibadb/)で構築されたPostgreSQLデータベースから競馬データを取得するためのPythonライブラリです。[63種類のテーブル](doc/DATA_TABLE.md)に対する統一的なインターフェースを提供し、`pandas.DataFrame`としてデータを取得できます。

mykeibadbは[JRA-VAN Data Lab.](https://jra-van.jp/dlb/)のデータをPostgreSQL/MySQLに蓄積するWindowsアプリケーションです。本ライブラリは、そのPostgreSQLサーバーに接続してデータを取得するためのクライアントライブラリです。


## 動作要件

- Python 3.12以上
- mykeibadbがインストールされたWindows PC上のPostgreSQLサーバーにアクセスできること


## 依存パッケージ

- `pandas>=2.0.0`
- `psycopg2-binary>=2.9.0`
- `python-dotenv>=1.0.0`
- `paramiko>=3.0.0`
- `pyyaml>=6.0.0`


## インストール

```bash
pip install -e /path/to/mykeibadb-python
```


## セットアップ

### 環境変数の設定

`.env.example`を`.env`にコピーし、接続先のPostgreSQLサーバーに合わせて編集します。

`.env`の内容：

```dotenv
# PostgreSQL接続設定
MYKEIBADB_HOST=host.docker.internal   # 接続先ホスト（下記参照）
MYKEIBADB_PORT=5432                   # ポート番号
MYKEIBADB_DATABASE=mykeibadb          # データベース名
MYKEIBADB_USER=postgres               # ユーザー名
MYKEIBADB_PASSWORD=postgres           # パスワード
```

`MYKEIBADB_HOST`の設定値は接続元の環境によって異なります：

| 接続元 | `MYKEIBADB_HOST`の値 |
|---|---|
| WindowsホストPC自体 | `localhost` |
| Dockerコンテナ | `host.docker.internal` |
| 別のPC（LAN内） | WindowsホストPCのIPアドレス |

環境変数を設定しない場合、以下のデフォルト値が使用されます：
`host=localhost`, `port=5432`, `database=mykeibadb`, `user=postgres`, `password=postgres`

### PostgreSQLサーバー側の設定（リモート接続時）

WindowsホストPC**以外**から接続する場合（Dockerコンテナや別のPCなど）、PostgreSQLサーバー側でリモート接続を許可する必要があります。

> **WindowsホストPC上で直接利用する場合はこの手順は不要です。**

#### 1. postgresql.confの編集

`C:\Program Files\PostgreSQL\16\data\postgresql.conf`（バージョンは適宜読み替え）を管理者権限で開き、以下を変更：

```conf
# 全てのIPアドレスからの接続を許可
listen_addresses = '*'
```

#### 2. pg_hba.confの編集

`C:\Program Files\PostgreSQL\16\data\pg_hba.conf`の最後に、接続元に応じた行を追加：

```conf
# Docker からの接続を許可
host    all             all             172.17.0.0/16           md5
host    all             all             host.docker.internal    md5

# LAN内の別PCからの接続を許可（例: 192.168.1.0/24）
# host    all             all             192.168.1.0/24          md5
```

#### 2. pg_hba.confの編集

コマンドプロンプト（管理者権限）で実行：

```cmd
netsh advfirewall firewall add rule name="PostgreSQL" dir=in action=allow protocol=TCP localport=5432
```

#### 3. PostgreSQLサービスの再起動

コマンドプロンプト（管理者権限）で実行：

```cmd
net stop postgresql-x64-16
net start postgresql-x64-16
```

### 接続テスト

```bash
python example/db_connect_test.py
```

成功すると、PostgreSQLバージョンとテーブル数が表示されます。


## 使い方

### 基本的な使い方

各テーブルには対応するGetterクラスが用意されています。Getterクラスをインスタンス化し、メソッドを呼ぶだけでデータを`pandas.DataFrame`として取得できます。

```python
from mykeibadb.getters import RaceGetter

getter = RaceGetter()

# レースコードを指定してレース詳細を取得
df = getter.get_race_shosai(race_code="2025122806050811")
print(df)
```

Getterクラスの初期化時に引数なしで呼ぶと、環境変数（`.env`）から接続設定を自動で読み込みます。明示的に設定を渡す場合は`DBConfig`を使用します：

```python
from mykeibadb.config import DBConfig
from mykeibadb.getters import RaceGetter

config = DBConfig(
    host="192.168.1.100",
    port=5432,
    database="mykeibadb",
    user="postgres",
    password="your_password",
)
getter = RaceGetter(config=config)
df = getter.get_race_shosai(race_code="2025122806050811")
```

### 期間を指定して取得

```python
from datetime import date
from mykeibadb.getters import RaceGetter

getter = RaceGetter()

# 期間を指定してレース詳細を取得
df = getter.get_race_shosai(
    start_date=date(2025, 12, 1),
    end_date=date(2025, 12, 31),
)
```

### コード変換

各Getterメソッドには`convert_codes`引数（デフォルト`True`）があり、コード値（競馬場コード、トラックコードなど）を自動的に人間が読める名称に変換します。変換せずに生のコード値を取得したい場合は`False`を指定します：

```python
# コード変換なし
df = getter.get_race_shosai(race_code="2025122806050811", convert_codes=False)
```

### ConnectionManagerを直接使用する

低レベルのAPIとして`ConnectionManager`を使い、任意のSQLクエリを実行することも可能です：

```python
from mykeibadb.config import ConfigManager
from mykeibadb.connection import ConnectionManager

config = ConfigManager.from_env()

with ConnectionManager(config) as conn:
    # 結果をDataFrameで取得
    df = conn.fetch_dataframe("SELECT * FROM \"RACE_SHOSAI\" LIMIT 10")

    # 結果をタプルのリストで取得
    rows = conn.execute_query("SELECT version()")
```

### TableAccessorを使用する

テーブル名とフィルタ条件を指定してデータを取得できます：

```python
from mykeibadb.config import ConfigManager
from mykeibadb.connection import ConnectionManager
from mykeibadb.tables import TableAccessor

config = ConfigManager.from_env()

with ConnectionManager(config) as conn:
    accessor = TableAccessor(conn)
    df = accessor.get_table_data(
        "RACE_SHOSAI",
        filters={"KEIBAJO_CODE": "05"},  # 東京競馬場のみ
    )
```


## Getterクラス一覧

| Getterクラス | 対象テーブル数 | 説明 |
|---|---|---|
| `RaceGetter` | 7 | レース関連（レース詳細、馬毎レース情報、払戻、開催スケジュールなど） |
| `HyosuGetter` | 10 | 票数関連（単勝・複勝・枠連・馬連・ワイド・馬単・三連複・三連単） |
| `OddsGetter` | 14 | オッズ関連（単複枠・馬連・ワイド・馬単・三連複・三連単、時系列含む） |
| `MasterGetter` | 8 | マスタデータ（競走馬・騎手・調教師・生産者・馬主・繁殖馬・産駒・レコード） |
| `ShussobetsuGetter` | 7 | 出走別着度数（馬場別・距離別・競馬場別・騎手別・調教師別・馬主別・生産者別） |
| `ChokyoGetter` | 2 | 調教データ（坂路調教・ウッドチップ調教） |
| `KyosobaGetter` | 3 | 競走馬詳細情報（市場取引価格・馬名の意味由来・系統情報） |
| `MiningGetter` | 2 | データマイニング予想（タイム型・対戦型） |
| `Win5Getter` | 2 | WIN5（ベース情報・払戻） |
| `SokuhoGetter` | 7 | 速報（除外情報・馬体重・天候馬場状態・出走取消・騎手変更・発走時刻変更・コース変更） |
| `OthersGetter` | 1 | その他（勝負服） |


## エラーハンドリング

本ライブラリが送出する例外は全て`MykeibaDBError`を基底クラスとしています：

| 例外クラス | 説明 |
|---|---|
| `MykeibaDBError` | 基底例外クラス |
| `MykeibaDBConnectionError` | PostgreSQLへの接続に失敗した場合 |
| `TableNotFoundError` | 指定されたテーブルがサポートされていない場合 |
| `InvalidFilterError` | 無効なフィルタ条件が指定された場合 |
| `QueryExecutionError` | SQLクエリの実行に失敗した場合 |
| `ValidationError` | 引数の検証に失敗した場合（レースコードの桁数不正など） |

```python
from mykeibadb.exceptions import MykeibaDBConnectionError, ValidationError
from mykeibadb.getters import RaceGetter

try:
    getter = RaceGetter()
    df = getter.get_race_shosai(race_code="2025122806050811")
except MykeibaDBConnectionError as e:
    print(f"接続エラー: {e}")
except ValidationError as e:
    print(f"引数エラー: {e}")
```


## ドキュメント

- [テーブル仕様（DATA_TABLE.md）](doc/DATA_TABLE.md): 全63テーブルの詳細（カラム定義など）
- [コード仕様（CODE_TABLE.md）](doc/CODE_TABLE.md): 各種コード値の定義
- [ディレクトリ構造（DIRECTORY.md）](doc/DIRECTORY.md): プロジェクトのディレクトリ構造
- [サンプルコード（example/）](example/getter/): 各Getterの使用例

## リンク

- [mykeibadb公式サイト](https://keough.watson.jp/wp/mykeibadb/)
- [JRA-VAN Data Lab.](https://jra-van.jp/dlb/)
