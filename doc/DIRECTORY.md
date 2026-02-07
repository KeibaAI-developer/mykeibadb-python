# ディレクトリ構成

```
mykeibadb-python/
├── mykeibadb/               # メインパッケージ
│   ├── __init__.py
│   ├── config.py            # 設定管理
│   ├── connection.py        # DB接続管理
│   ├── tables.py            # テーブル定義・アクセス
│   ├── utils.py             # ユーティリティ関数
│   ├── exceptions.py        # 例外クラス定義
│   ├── py.typed             # 型情報ファイル
│   ├── code_converter/      # コード変換モジュール
│   │   ├── __init__.py
│   │   ├── code_converter.py
│   │   └── mapping/         # マッピングデータ
│   └── getters/             # データ取得クラス群
│       ├── __init__.py
│       ├── base.py          # 基底クラス
│       ├── chokyo.py        # 調教データ
│       ├── hyosu.py         # 票数データ
│       ├── kyosoba.py       # 競走馬データ
│       ├── master.py        # マスタデータ
│       ├── mining.py        # データマイニング
│       ├── odds.py          # オッズデータ
│       ├── others.py        # その他データ
│       ├── race.py          # レースデータ
│       ├── shussobetsu.py   # 出走別データ
│       ├── sokuho.py        # 速報データ
│       └── win5.py          # WIN5データ
├── test/                    # テストコード
│   ├── __init__.py
│   ├── unit/                # ユニットテスト
│   │   ├── code_converter/
│   │   ├── config/
│   │   ├── connection/
│   │   ├── getters/
│   │   ├── tables/
│   │   ├── utils/
│   │   └── test_import.py
│   └── integration/         # 統合テスト
│       ├── conftest.py
│       └── test_*.py        # 各種統合テスト
├── example/                 # サンプルコード
│   ├── db_connect_test.py   # DB接続テスト
│   └── getter/              # Getter使用例
├── doc/                     # ドキュメント
│   ├── DIRECTORY.md         # このファイル
│   ├── CODE_TABLE.md        # コードテーブル一覧
│   ├── DATA_TABLE.md        # データテーブル一覧
│   └── DATA_TABLE/          # テーブル詳細ドキュメント
├── .github/                 # GitHub関連設定
│   └── workflows/           # GitHub Actionsワークフロー
│       └── ci.yml           # CI/CD設定
├── .env.example             # 環境変数サンプル
├── .gitignore               # Git無視ファイル
├── pyproject.toml           # プロジェクト設定
└── README.md                # プロジェクト概要
```
