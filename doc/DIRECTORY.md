# ディレクトリ構成

```
mykeibadb-python/
├── mykeibadb/               # メインパッケージ
│   ├── __init__.py
│   ├── client.py            # メインクライアントクラス
│   ├── connection.py        # DB接続管理
│   ├── config.py            # 設定管理
│   ├── tables.py            # テーブル定義・アクセス
│   ├── updater.py           # mykeibadb.exe実行管理
│   └── exceptions.py        # 例外クラス定義
├── tests/                   # テストコード
│   ├── unit/
│   └── integration/
├── doc/                     # ドキュメント
├── .github/                 # GitHub関連設定
│   └── workflows/           # GitHub Actionsワークフロー
│       └── ci.yml           # CI/CD設定
├── .env.example             # 環境変数サンプル
├── .gitignore               # Git無視ファイル
├── .dockerignore            # Docker除外ファイル
├── Dockerfile               # Python環境
├── docker-compose.yml       # Docker Compose設定
├── pyproject.toml           # プロジェクト設定
└── README.md
```
