# mykeibadb-python 機能仕様書

## 1. 概要

### 1.1 目的

mykeibadb-pythonは、JRA-VANのJVLinkを使用して競馬データをPostgreSQLに格納するWindowsソフトウェア「mykeibadb」から、Pythonでデータを取得するためのライブラリです。

### 1.2 スコープ

- PostgreSQLに格納された競馬データへのアクセス機能
- pandas DataFrameとしてのデータ取得機能
- mykeibadb.exeの実行によるデータベース更新機能（Windows環境のみ）
- 63種類のテーブルに対する統一的なインターフェース

### 1.3 非スコープ

- JV-Linkとの直接的な連携（mykeibadb経由で行う）
- PostgreSQL以外のデータベースへの対応
- データの加工・分析機能（KeibaAI本体で実装）

## 2. システムアーキテクチャ

### 2.1 全体構成

ディレクトリ構成は[DIRECTORY.md](/doc/DIRECTORY.md)を参照。

### 2.2 コンテナ構成図

```
┌─────────────────────────────────────────┐
│     mykeibadb container (Debian)        │
│  ┌────────────────────────────────────┐ │
│  │  mykeibadb-python                  │ │
│  │  - データ取得ライブラリ             │ │
│  │  - PostgreSQL接続                  │ │
│  └────────────────────────────────────┘ │
│         │                               │
│         │ psycopg2                      │
│         ▼                               │
│  Docker Network (bridge)                │
└─────────────────────────────────────────┘
         │
         │ host.docker.internal
         ▼
┌─────────────────────────────────────────┐
│   Windows Host                           │
│  ┌────────────────────────────────────┐ │
│  │  PostgreSQL 16                     │ │
│  │  - mykeibadb データベース          │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  mykeibadb.exe                     │ │
│  │  - データ更新                      │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 2.2 主要コンポーネント

#### 2.3.1 MykeibaDBClient（client.py）

ライブラリの主要インターフェース。

**責務**:
- データベース接続の初期化
- テーブルデータの取得
- mykeibadbの実行制御

**主要メソッド**:
```python
class MykeibaDBClient:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "mykeibadb",
        user: str = "postgres",
        password: str = "postgres",
        config: DBConfig | None = None
    ) -> None:
        """クライアントを初期化

        Args:
            host: PostgreSQLホスト名
            port: PostgreSQLポート番号
            database: データベース名
            user: ユーザー名
            password: パスワード
            config: DBConfig設定（指定時は他のパラメータを上書き）
        """

    def get_table(
        self,
        table_name: str,
        filters: dict[str, str | int | list[str | int]] | None = None
    ) -> pd.DataFrame:
        """テーブルデータを取得

        Args:
            table_name: テーブル名（例: "RACE_SHOSAI"）
            filters: フィルタ条件（例: {"RACE_CODE": "202509030411"}）

        Returns:
            取得したデータのDataFrame
        """

    def update_database(
        self,
        mykeibadb_path: str | None = None,
        ssh_config: SSHConfig | None = None,
        timeout: int = 300
    ) -> bool:
        """mykeibadb.exeを実行してデータベースを更新

        プラットフォームを自動検知し、適切な方法で実行：
        - Windows上: subprocessでローカル実行
        - Linux/macOS上: SSH経由でリモート実行

        Args:
            mykeibadb_path: mykeibadb.exeのパス（Noneの場合は環境変数MYKEIBADB_EXE_PATHから取得）
            ssh_config: SSH接続設定（Linux/macOSからのリモート実行時のみ必要、Noneの場合は環境変数から取得）
            timeout: タイムアウト秒数（デフォルト300秒）

        Returns:
            更新成功の場合True

        Raises:
            UpdateError: 更新失敗時
            MykeibaDBConnectionError: SSH接続失敗時（リモート実行時）
            PlatformNotSupportedError: SSH設定が必要なのに未設定時
        """

    def close(self) -> None:
        """DB接続をクローズ"""

    def __enter__(self) -> "MykeibaDBClient":
        """コンテキストマネージャーのエントリーポイント

        Returns:
            自身のインスタンス
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None
    ) -> None:
        """コンテキストマネージャーの終了処理

        例外の有無に関わらず、DB接続を確実にクローズします。

        Args:
            exc_type: 例外の型
            exc_val: 例外のインスタンス
            exc_tb: トレースバック
        """
        self.close()
```

#### 2.3.2 ConnectionManager（connection.py）

PostgreSQL接続の管理。

**責務**:
- 接続プールの管理
- クエリ実行
- トランザクション管理

**主要メソッド**:
```python
class ConnectionManager:
    def __init__(self, config: DBConfig) -> None:
        """接続マネージャーを初期化"""

    def execute_query(
        self,
        query: str,
        params: tuple | None = None
    ) -> list[tuple]:
        """SQLクエリを実行"""

    def fetch_dataframe(
        self,
        query: str,
        params: tuple | None = None
    ) -> pd.DataFrame:
        """クエリ結果をDataFrameとして取得"""

    def close(self) -> None:
        """接続をクローズ"""
```

#### 2.3.3 TableAccessor（tables.py）

テーブルアクセスの抽象化。

**責務**:
- テーブル定義の管理
- SQLクエリの生成
- フィルタ条件の処理

**主要メソッド**:
```python
class TableAccessor:
    def __init__(self, connection_manager: ConnectionManager) -> None:
        """テーブルアクセサーを初期化"""

    def get_table_data(
        self,
        table_name: str,
        filters: dict[str, str | int | list[str | int]] | None = None
    ) -> pd.DataFrame:
        """テーブルデータを取得"""

    def _build_query(
        self,
        table_name: str,
        filters: dict[str, str | int | list[str | int]] | None = None
    ) -> tuple[str, tuple]:
        """SQLクエリを構築"""

    def _validate_table_name(self, table_name: str) -> bool:
        """テーブル名の妥当性を検証"""
```

#### 2.3.4 DatabaseUpdater（updater.py）

mykeibadb.exeの実行管理（ローカル/SSH経由）。

**責務**:
- プラットフォーム検知（Windows/Linux/macOS）
- Windows上：subprocessによるローカル実行
- Linux/macOS上：SSH経由のリモート実行
- 実行状態の監視
- エラーハンドリング

**主要メソッド**:
```python
class DatabaseUpdater:
    def __init__(
        self,
        mykeibadb_path: str = r"C:\mykeibadb_v3.61\mykeibadb.exe",
        ssh_config: SSHConfig | None = None
    ) -> None:
        """アップデーターを初期化

        Args:
            mykeibadb_path: mykeibadb.exeのパス（Windows側のパス）
            ssh_config: SSH接続設定（Linux/macOSからのリモート実行時のみ必要）
        """

    def update(self, timeout: int = 300) -> bool:
        """データベースを更新

        プラットフォームを自動検知し、適切な方法で実行。
        - Windows: subprocessでローカル実行
        - Linux/macOS: SSH経由でリモート実行

        Args:
            timeout: タイムアウト秒数（デフォルト300秒）

        Returns:
            更新成功の場合True

        Raises:
            UpdateError: 更新失敗時
            MykeibaDBConnectionError: SSH接続失敗時（リモート実行時）
        """

    def _execute_local(self, timeout: int) -> bool:
        """Windows上でローカル実行（subprocess）"""

    def _execute_remote(self, timeout: int) -> bool:
        """SSH経由でリモート実行（paramiko）"""

    def _connect_ssh(self) -> paramiko.SSHClient:
        """SSH接続を確立"""
```

#### 2.3.5 ConfigManager（config.py）

設定の管理。

**責務**:
- 設定ファイルの読み込み
- 環境変数の処理
- デフォルト値の管理

**主要クラス**:

```python
@dataclass
class DBConfig:
    """データベース接続設定"""
    host: str = "localhost"
    port: int = 5432
    database: str = "mykeibadb"
    user: str = "postgres"
    password: str = "postgres"

@dataclass
class SSHConfig:
    """SSH接続設定（DB更新用、Linux/macOSからのリモート実行時のみ使用）"""
    host: str = "host.docker.internal"
    port: int = 22
    username: str | None = None
    password: str | None = None
    key_path: str | None = None

class ConfigManager:
    def __init__(self, config_path: str | None = None) -> None:
        """設定マネージャーを初期化"""

    def load_config(self) -> DBConfig:
        """設定を読み込み"""

    @staticmethod
    def from_env() -> DBConfig:
        """環境変数から設定を生成"""

    @staticmethod
    def ssh_from_env() -> SSHConfig:
        """環境変数からSSH設定を生成"""
```

#### 2.3.6 例外クラス（exceptions.py）

```python
class MykeibaDBError(Exception):
    """mykeibadb-python基底例外"""

class MykeibaDBConnectionError(MykeibaDBError):
    """DB接続エラー"""

class TableNotFoundError(MykeibaDBError):
    """テーブルが存在しない"""

class InvalidFilterError(MykeibaDBError):
    """無効なフィルタ条件"""

class UpdateError(MykeibaDBError):
    """DB更新エラー"""

class PlatformNotSupportedError(MykeibaDBError):
    """サポートされていないプラットフォーム"""
```

## 3. データアクセス仕様

### 3.1 サポートするテーブル

[DATA_TABLE.md](./DATA_TABLE.md)に記載された全63種類のテーブルをサポート。

#### テーブル分類

**レース関連（5テーブル）**:
- `TOKUBETSU_TOROKUBA`, `TOKUBETSU_TOROKUBAGOTO_JOHO`
- `RACE_SHOSAI`, `UMAGOTO_RACE_JOHO`, `HARAIMODOSHI`

**票数関連（10テーブル）**:
- `HYOSU1`, `HYOSU1_TANSHO`, `HYOSU1_FUKUSHO`, `HYOSU1_WAKUREN`, `HYOSU1_UMAREN`, `HYOSU1_WIDE`, `HYOSU1_UMATAN`, `HYOSU1_SANRENPUKU`
- `HYOSU6`, `HYOSU6_SANRENTAN`

**オッズ関連（14テーブル）**:
- `ODDS1`, `ODDS1_TANSHO`, `ODDS1_FUKUSHO`, `ODDS1_WAKUREN`
- `ODDS1_JIKEIRETSU`, `ODDS1_TANSHO_JIKEIRETSU`, `ODDS1_FUKUSHO_JIKEIRETSU`, `ODDS1_WAKUREN_JIKEIRETSU`
- `ODDS2_UMAREN`, `ODDS2_UMAREN_JIKEIRETSU`
- `ODDS3_WIDE`, `ODDS4_UMATAN`, `ODDS5_SANRENPUKU`, `ODDS6_SANRENTAN`

**マスタデータ（8テーブル）**:
- `KYOSOBA_MASTER2`, `KISHU_MASTER`, `CHOKYOSHI_MASTER`
- `SEISANSHA_MASTER2`, `BANUSHI_MASTER`, `HANSHOKUBA_MASTER2`, `SANKU_MASTER2`
- `RECORD_MASTER`

**出走別データ（7テーブル）**:
- `SHUSSOBETSU_BABA`, `SHUSSOBETSU_KYORI`, `SHUSSOBETSU_KEIBAJO`
- `SHUSSOBETSU_KISHU`, `SHUSSOBETSU_CHOKYOSHI`, `SHUSSOBETSU_BANUSHI`, `SHUSSOBETSU_SEISANSHA2`

**調教データ（2テーブル）**:
- `HANRO_CHOKYO`, `WOODCHIP_CHOKYO`

**開催情報（1テーブル）**:
- `KAISAI_SCHEDULE`

**コース情報（1テーブル）**:
- `COURSE_JOHO`

**競走馬詳細情報（3テーブル）**:
- `KYOSOBA_TORIHIKI_KAKAKU2`
- `BAMEI_IMI_YURAI`
- `KEITO_JOHO2`

**データマイニング予想（2テーブル）**:
- `DATA_MINING_TIME`, `DATA_MINING_TAISEN`

**WIN5（2テーブル）**:
- `WIN5`, `WIN5_HARAIMODOSHI`

**速報（7テーブル）**:
- `KYOSOBA_JOGAI_JOHO`
- `BATAIJU`, `TENKO_BABA_JOTAI`
- `SHUSSOTORIKESHI_KYOSOJOGAI`, `KISHU_HENKO`, `HASSOJIKOKU_HENKO`, `COURSE_HENKO`

**その他（1テーブル）**:
- `SHOBUFUKU`

### 3.2 フィルタ仕様

#### 3.2.1 単一値フィルタ

```python
# 単一のレースコードで絞り込み
client.get_table("RACE_SHOSAI", filters={"RACE_CODE": "202509030411"})
```

#### 3.2.2 複数値フィルタ（IN句）

```python
# 複数のレースコードで絞り込み
client.get_table(
    "RACE_SHOSAI",
    filters={"RACE_CODE": ["202509030411", "202509030412"]}
)
```

#### 3.2.3 複合フィルタ

```python
# 複数のカラムで絞り込み
client.get_table(
    "UMAGOTO_RACE_JOHO",
    filters={
        "RACE_CODE": "202509030411",
        "UMABAN": 1
    }
)
```

#### 3.2.4 フィルタなし（全件取得）

```python
# 全件取得
client.get_table("KISHU_MASTER")
```

### 3.3 データ型マッピング

PostgreSQL型からPandas型へのマッピング:

| PostgreSQL型 | Pandas型 | 備考 |
|-------------|---------|------|
| VARCHAR, TEXT | object | 文字列 |
| INTEGER | int64 | 整数 |
| NUMERIC, DECIMAL | float64 | 小数 |
| DATE | datetime64 | 日付 |
| TIMESTAMP | datetime64 | 日時 |
| BOOLEAN | bool | 真偽値 |

## 4. エラーハンドリング

### 4.1 例外の種類と対応

| 例外クラス | 発生条件 | 対応方法 |
|----------|---------|---------|
| `MykeibaDBConnectionError` | DB接続失敗 | 接続情報を確認、PostgreSQLの起動確認 |
| `TableNotFoundError` | 存在しないテーブル名 | テーブル名を確認、[DATA_TABLE.md](./DATA_TABLE.md)参照 |
| `InvalidFilterError` | 無効なフィルタ条件 | フィルタのキー・値を確認 |
| `UpdateError` | DB更新失敗 | mykeibadb.exeのパス確認、実行権限確認 |
| `PlatformNotSupportedError` | SSH設定が必要なのに未設定時 | Windows環境で実行 |

### 4.2 エラーメッセージ

```python
# 接続エラーの例
raise MykeibaDBConnectionError(
    f"Failed to connect to PostgreSQL: host={host}, port={port}, database={database}"
)

# テーブル存在エラーの例
raise TableNotFoundError(
    f"Table '{table_name}' does not exist. "
    f"See doc/DATA_TABLE.md for supported tables."
)

# フィルタエラーの例
raise InvalidFilterError(
    f"Invalid filter key '{key}' for table '{table_name}'. "
    f"Valid keys: {valid_keys}"
)
```

## 5. パフォーマンス仕様

### 5.1 クエリ最適化

- **接続プール**: psycopg2の接続プールを使用（最大10接続）
- **インデックス活用**: 主キー・外部キーでのフィルタは自動的にインデックスを利用
- **ページネーション**: 大量データ取得時は将来的にLIMIT/OFFSETをサポート予定

### 5.2 メモリ管理

- **チャンクサイズ**: 1クエリあたり最大100,000レコードを推奨
- **DataFrame変換**: psycopg2のカーソルから直接pandas DataFrameに変換

## 6. セキュリティ仕様

### 6.1 認証情報の管理

**データベース接続**:
- `MYKEIBADB_HOST`: PostgreSQLホスト（デフォルト: localhost）
- `MYKEIBADB_PORT`: PostgreSQLポート（デフォルト: 5432）
- `MYKEIBADB_DATABASE`: データベース名（デフォルト: mykeibadb）
- `MYKEIBADB_USER`: PostgreSQLユーザー名（デフォルト: postgres）
- `MYKEIBADB_PASSWORD`: PostgreSQLパスワード（デフォルト: postgres）

**mykeibadb.exe実行パス**:
- `MYKEIBADB_EXE_PATH`: mykeibadb.exeのWindowsパス（デフォルト: C:\mykeibadb_v3.61\mykeibadb.exe）

**SSH接続（Linux/macOSからのDB更新用）**:
- `MYKEIBADB_SSH_HOST`: WindowsホストのSSH接続先（デフォルト: host.docker.internal）
- `MYKEIBADB_SSH_PORT`: SSHポート番号（デフォルト: 22）
- `MYKEIBADB_SSH_USER`: Windowsユーザー名
- `MYKEIBADB_SSH_PASSWORD`: SSHパスワード（鍵認証を使わない場合）
- `MYKEIBADB_SSH_KEY`: SSH秘密鍵のパス（パスワード認証を使わない場合、推奨）

- 設定ファイル（`.env`）からの読み込みをサポート

### 6.2 SQLインジェクション対策

- プリペアドステートメントを使用
- パラメータバインディングによる安全なクエリ実行

```python
# 安全なクエリ例
query = "SELECT * FROM race_shosai WHERE race_code = %s"
params = (race_code,)
```

## 7. 互換性

### 7.1 プラットフォーム

| 機能 | Windows | Linux | macOS |
|-----|---------|-------|-------|
| データ取得 | ○ | ○ | ○ |
| DB更新（ローカル実行） | ○ | × | × |
| DB更新（SSH経由） | ○※ | ○ | ○ |

※ Windows上でもSSH経由でリモート実行可能（OpenSSH Serverが必要）  

**実行方法の選択**:
- Windows上でPythonスクリプトを実行：自動的にローカル実行（SSH不要）
- Docker/Linux/macOS上でPythonスクリプトを実行：SSH経由でWindowsホストのmykeibadb.exeを実行

### 7.2 Pythonバージョン

- Python 3.12以上をサポート

### 7.3 依存ライブラリ

```toml
dependencies = [
    "pandas>=2.0.0",
    "psycopg2-binary>=2.9.0",
    "python-dotenv>=1.0.0",
    "paramiko>=3.0.0",  # SSH接続用（DB更新機能）
]
```

## 8. セットアップ

### 8.1 Windows側のSSH設定（DB更新機能を使用する場合）

DB更新機能を使用するには、Windows側でOpenSSH Serverを有効化する必要があります。

#### 8.1.1 OpenSSH Serverのインストール

**PowerShell（管理者権限）で実行**:
```powershell
# OpenSSH Serverをインストール
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# SSHサービスを開始
Start-Service sshd

# 自動起動設定
Set-Service -Name sshd -StartupType 'Automatic'

# ファイアウォール設定（通常は自動設定される）
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' `
    -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

#### 8.1.2 SSH鍵認証の設定（推奨）

**Linux/Docker側で鍵ペアを生成**:
```bash
# SSH鍵ペアを生成
ssh-keygen -t ed25519 -C "mykeibadb-updater" -f ~/.ssh/mykeibadb_key

# 公開鍵を表示（これをWindows側にコピー）
cat ~/.ssh/mykeibadb_key.pub
```

**Windows側で公開鍵を設定**:
```powershell
# .sshディレクトリが存在しない場合は作成
$sshDir = "$env:USERPROFILE\.ssh"
if (!(Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir
}

# authorized_keysファイルに公開鍵を追加
# （上記で表示された公開鍵をコピー&ペースト）
Add-Content -Path "$sshDir\authorized_keys" -Value "ssh-ed25519 AAAA...（公開鍵）"

# ファイルのアクセス権を設定
icacls "$sshDir\authorized_keys" /inheritance:r
icacls "$sshDir\authorized_keys" /grant:r "$env:USERNAME`:F"
```

#### 8.1.3 接続テスト

**Linux/Docker側からテスト**:
```bash
# SSH接続テスト
ssh -i ~/.ssh/mykeibadb_key your_windows_user@host.docker.internal

# mykeibadb.exeのパスを確認
ls "C:\mykeibadb_v3.61\mykeibadb.exe"
```

### 8.2 環境変数の設定

`.env`ファイルを作成:
```bash
# PostgreSQL接続設定
MYKEIBADB_HOST=host.docker.internal
MYKEIBADB_PORT=5432
MYKEIBADB_DATABASE=mykeibadb
MYKEIBADB_USER=postgres
MYKEIBADB_PASSWORD=postgres

# mykeibadb.exe実行パス
MYKEIBADB_EXE_PATH=C:\mykeibadb_v3.61\mykeibadb.exe

# SSH接続設定（Linux/macOSからのDB更新用）
MYKEIBADB_SSH_HOST=host.docker.internal
MYKEIBADB_SSH_PORT=22
MYKEIBADB_SSH_USER=your_windows_user
MYKEIBADB_SSH_KEY=/root/.ssh/mykeibadb_key
```

## 9. 使用例

### 9.1 基本的な使用例

```python
from mykeibadb import MykeibaDBClient

# クライアント初期化
client = MykeibaDBClient(
    host="localhost",
    port=5432,
    database="mykeibadb",
    user="postgres",
    password="postgres"
)

# レース詳細を取得
race_df = client.get_table(
    "RACE_SHOSAI",
    filters={"RACE_CODE": "202509030411"}
)

# 馬毎レース情報を取得
horse_df = client.get_table(
    "UMAGOTO_RACE_JOHO",
    filters={"RACE_CODE": "202509030411"}
)

# 騎手マスタ全件取得
jockey_df = client.get_table("KISHU_MASTER")

# 接続クローズ
client.close()
```

### 9.2 環境変数を使用した接続

```python
import dataclasses
from mykeibadb import MykeibaDBClient, ConfigManager

# 環境変数から設定を読み込み
config = ConfigManager.from_env()

# 方法1: DBConfigオブジェクトを直接渡す（推奨）
client = MykeibaDBClient(config=config)

# 方法2: dataclasses.asdict()でアンパック
# client = MykeibaDBClient(**dataclasses.asdict(config))

race_df = client.get_table("RACE_SHOSAI")
client.close()
```

### 9.3 データベース更新（Windowsローカル実行）

```python
from mykeibadb import MykeibaDBClient

# Windows上で実行する場合は自動的にローカル実行（ssh_configは不要）
client = MykeibaDBClient()

try:
    # プラットフォームを自動検知して実行
    # ssh_config=Noneの場合、Windowsではローカル実行される
    success = client.update_database(
        mykeibadb_path=r"C:\mykeibadb_v3.61\mykeibadb.exe"
    )

    if success:
        print("データベース更新成功")
        # 更新後のデータを取得
        race_df = client.get_table("RACE_SHOSAI")
finally:
    client.close()
```

### 9.4 データベース更新（SSH経由）

```python
from mykeibadb import MykeibaDBClient, SSHConfig

client = MykeibaDBClient()

# SSH設定（環境変数から取得する場合はNoneでOK）
ssh_config = SSHConfig(
    host="host.docker.internal",
    port=22,
    username="your_windows_user",
    key_path="/path/to/ssh_key",  # または password="your_password"
)

try:
    # データベースを更新（タイムアウト5分）
    # mykeibadb_pathは別パラメータで指定
    success = client.update_database(
        mykeibadb_path=r"C:\mykeibadb_v3.61\mykeibadb.exe",
        ssh_config=ssh_config,
        timeout=300
    )

    if success:
        print("データベース更新成功")
        # 更新後のデータを取得
        race_df = client.get_table("RACE_SHOSAI")
finally:
    client.close()
```

### 9.5 環境変数を使用したDB更新

```python
from mykeibadb import MykeibaDBClient

# 環境変数から設定を自動取得
client = MykeibaDBClient()

try:
    # パラメータを省略すると環境変数から設定を読み込み
    # - mykeibadb_path: MYKEIBADB_EXE_PATHから取得
    # - ssh_config: MYKEIBADB_SSH_*から取得（Linux/macOSの場合のみ）
    success = client.update_database()

    if success:
        print("データベース更新成功")
except UpdateError as e:
    print(f"更新失敗: {e}")
finally:
    client.close()
```

### 9.6 コンテキストマネージャー

```python
from mykeibadb import MykeibaDBClient

with MykeibaDBClient() as client:
    race_df = client.get_table("RACE_SHOSAI")
    # 自動的にcloseされる
```
