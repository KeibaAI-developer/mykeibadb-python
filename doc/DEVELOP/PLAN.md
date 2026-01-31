# mykeibadb-python 実装計画書

## 1. 概要

### 1.1 目的

本計画書は、mykeibadb-pythonライブラリの実装を段階的に進めるためのロードマップを定義します。

### 1.2 実装方針

- PR単位で機能を分割し、段階的に実装
- テストファーストで実装（TDD）
- [python-coding-rule](../.github/skills/python-coding-rule/SKILL.md)に準拠
- [pytest-coding-rule](../.github/skills/pytest-coding-rule/SKILL.md)に準拠
- 実装完了後、isort, flake8, mypyのタスクを実行してエラーがないことを確認

## 2. PR詳細計画

### PR#1: プロジェクト初期設定

**目的**: プロジェクトの基本構造を確立

**実装内容**:
- パッケージディレクトリ構造の作成
- pyproject.tomlの作成
- 開発環境設定ファイル
- 依存ライブラリの定義
- README.mdの作成
- .gitignoreの設定
- Docker環境の構築（Dockerfile、docker-compose.yml）

**ファイル構成**:

[DIRECTORY.md](../DIRECTORY.md)を参照。

**Docker構成**:
- `Dockerfile`: Python 3.12.4 ベース
- `docker-compose.yml`:
  - `python` サービス: ライブラリ開発環境
  - Windows側のPostgreSQLに`host.docker.internal`で接続
  - ボリューム: ソースコードのマウント

**注意**:
- PostgreSQLはWindows側のmykeibadbが構築したものを使用
- Dockerコンテナ内からは`host.docker.internal:5432`で接続

**成果物**:
- 実行可能なプロジェクト構造
- CI/CD設定（GitHub Actions）
- リンター・フォーマッター設定

**テスト**:
- パッケージインポートテスト
- 開発環境の動作確認

**レビューポイント**:
- ディレクトリ構造の妥当性
- 依存ライブラリのバージョン指定
- CI/CD設定の適切性

---

### PR#2: 設定管理機能の実装

**目的**: DB接続設定とSSH設定を柔軟に管理

**実装内容**:
- `DBConfig`データクラスの実装
- `SSHConfig`データクラスの実装
- `ConfigManager`クラスの実装
- 環境変数からの設定読み込み
- .envファイルからの設定読み込み
- デフォルト値の管理

**実装ファイル**:
- `mykeibadb/config.py`
- `tests/unit/config/test_config_manager.py`
- `.env.example`（サンプル設定ファイル）

**テスト項目**:

**正常系**:
- デフォルト値での設定生成
- 環境変数からの設定読み込み
- .envファイルからの設定読み込み
- 部分的な設定上書き
- SSH設定の読み込み

**準正常系**:
- 環境変数が一部欠けている場合
- .envファイルが存在しない場合

**異常系**:
- 不正な型の設定値
- ポート番号の範囲外

**成果物**:
- DBConfigクラス
- SSHConfigクラス
- ConfigManagerクラス
- 設定ファイルサンプル

**レビューポイント**:
- 設定の優先順位（環境変数 > .env > デフォルト）
- セキュリティ（パスワード等の扱い）
- 型安全性

---

### PR#3: DB接続機能の実装

**目的**: PostgreSQLへの接続・切断機能を実装

**実装内容**:
- `ConnectionManager`クラスの実装
- 接続プール管理
- クエリ実行機能（execute_query, fetch_dataframe）
- 既存の例外クラスの拡張（exceptions.py）

**実装ファイル**:
- `mykeibadb/connection.py`
- `mykeibadb/exceptions.py`（更新）
- `tests/unit/connection/test_connection_manager.py`
- `tests/integration/test_connection.py`

**テスト項目**:

**正常系**:
- DB接続成功
- シンプルなSELECTクエリの実行
- DataFrame形式でのデータ取得
- 接続のクローズ

**準正常系**:
- 存在しないテーブルへのクエリ
- 不正なSQLクエリ

**異常系**:
- 接続情報の誤り（ホスト名、ポート、DB名、認証情報）
- PostgreSQL未起動時の接続試行
- ネットワーク障害のシミュレーション

**成果物**:
- ConnectionManagerクラス
- 接続関連の例外クラス
- 単体テスト・結合テスト

**レビューポイント**:
- エラーハンドリングの適切性
- 接続プールの実装方法
- テストカバレッジ（目標80%以上）

---

### PR#4: テーブルアクセス基盤の実装

**目的**: テーブルデータ取得の基本機能を実装

**実装内容**:
- `TableAccessor`クラスの実装
- SQLクエリビルダー（_build_query）
- テーブル名バリデーション
- フィルタ処理機能

**実装ファイル**:
- `mykeibadb/tables.py`
- `tests/unit/tables/test_table_accessor.py`

**テスト項目**:

**正常系**:
- フィルタなしでの全件取得
- 単一値フィルタでの取得
- 複数値フィルタ（IN句）での取得
- 複合フィルタでの取得

**準正常系**:
- 存在しないテーブル名
- 存在しないカラム名でのフィルタ
- 空の結果セット

**異常系**:
- 不正な型のフィルタ値
- SQLインジェクション試行

**成果物**:
- TableAccessorクラス
- クエリビルダー機能
- テーブル定義リスト

**レビューポイント**:
- SQLインジェクション対策
- クエリ生成の効率性
- エラーメッセージの明確さ

---

### PR#5: レース・票数関連テーブル対応

**目的**: レース関連と票数関連テーブルへのアクセスを実装（19テーブル）

**実装内容**:
- レース系・票数系テーブルの定義追加
- テーブル固有のバリデーション
- 使用例の追加

**対象テーブル**:

**レース関連（5テーブル）**:
- TOKUBETSU_TOROKUBA, TOKUBETSU_TOROKUBAGOTO_JOHO
- RACE_SHOSAI（レース詳細）, UMAGOTO_RACE_JOHO（馬毎レース情報）, HARAIMODOSHI（払戻）

**票数関連（10テーブル）**:
- HYOSU1, HYOSU1_TANSHO, HYOSU1_FUKUSHO, HYOSU1_WAKUREN
- HYOSU1_UMAREN, HYOSU1_WIDE, HYOSU1_UMATAN, HYOSU1_SANRENPUKU
- HYOSU6, HYOSU6_SANRENTAN

**開催情報（1テーブル）**:
- KAISAI_SCHEDULE

**コース情報（1テーブル）**:
- COURSE_JOHO

**調教データ（2テーブル）**:
- HANRO_CHOKYO, WOODCHIP_CHOKYO

**実装ファイル**:
- `mykeibadb/tables.py`（更新）
- `tests/integration/test_race_tables.py`
- `tests/integration/test_hyosu_tables.py`
- `tests/integration/test_kaisai_schedule.py`
- `tests/integration/test_course_joho.py`
- `tests/integration/test_chokyo_tables.py`

**テスト項目**:

**正常系**:
- レースコードでのレース詳細取得
- 複数レースの一括取得
- 馬番でのフィルタ
- 票数データの取得
- 調教データの取得
- 開催スケジュールの取得

**準正常系**:
- 存在しないレースコード
- 未来のレース（データなし）

**成果物**:
- レース・票数系テーブル定義
- 結合テスト

**レビューポイント**:
- 実データでの動作確認
- フィルタの妥当性

---

### PR#6: オッズ・マスタテーブル対応

**目的**: オッズ関連とマスタデータテーブルへのアクセスを実装（22テーブル）

**実装内容**:
- オッズ系・マスタ系テーブルの定義追加
- 大量データ取得への対応

**対象テーブル**:

**オッズ関連（14テーブル）**:
- ODDS1, ODDS1_TANSHO, ODDS1_FUKUSHO, ODDS1_WAKUREN
- ODDS1_JIKEIRETSU, ODDS1_TANSHO_JIKEIRETSU, ODDS1_FUKUSHO_JIKEIRETSU, ODDS1_WAKUREN_JIKEIRETSU
- ODDS2_UMAREN, ODDS2_UMAREN_JIKEIRETSU
- ODDS3_WIDE, ODDS4_UMATAN, ODDS5_SANRENPUKU, ODDS6_SANRENTAN

**マスタデータ（8テーブル）**:
- KYOSOBA_MASTER2（競走馬マスタ）, KISHU_MASTER（騎手マスタ）, CHOKYOSHI_MASTER（調教師マスタ）
- SEISANSHA_MASTER2（生産者マスタ）, BANUSHI_MASTER（馬主マスタ）, HANSHOKUBA_MASTER2（繁殖馬マスタ）
- SANKU_MASTER2（産駒マスタ）, RECORD_MASTER（レコードマスタ）

**実装ファイル**:
- `mykeibadb/tables.py`（更新）
- `tests/integration/test_odds_tables.py`
- `tests/integration/test_master_tables.py`

**テスト項目**:

**正常系**:
- オッズデータの取得（単勝、複勝、馬連、ワイド、馬単、三連複、三連単）
- 時系列オッズの取得
- マスタ全件取得
- 血統登録番号でのフィルタ
- 名前での検索（部分一致）

**準正常系**:
- 存在しないコード
- オッズ未発売のレース

**成果物**:
- オッズ・マスタテーブル定義
- 結合テスト

**レビューポイント**:
- パフォーマンス（大量データ）
- メモリ使用量

---

### PR#7: 出走別・詳細情報・その他テーブル対応

**目的**: 残りの全テーブルへの対応を完了（22テーブル、合計63テーブル）

**実装内容**:
- 出走別・競走馬詳細・データマイニング・WIN5・速報系テーブルの定義
- 全63テーブルのサポート完了

**対象テーブル**:

**出走別データ（7テーブル）**:
- SHUSSOBETSU_BABA, SHUSSOBETSU_KYORI, SHUSSOBETSU_KEIBAJO
- SHUSSOBETSU_KISHU, SHUSSOBETSU_CHOKYOSHI, SHUSSOBETSU_BANUSHI, SHUSSOBETSU_SEISANSHA2

**競走馬詳細情報（3テーブル）**:
- KYOSOBA_TORIHIKI_KAKAKU2（取引価格）
- BAMEI_IMI_YURAI（馬名意味由来）
- KEITO_JOHO2（系統情報）

**データマイニング予想（2テーブル）**:
- DATA_MINING_TIME, DATA_MINING_TAISEN

**WIN5（2テーブル）**:
- WIN5, WIN5_HARAIMODOSHI

**速報（7テーブル）**:
- KYOSOBA_JOGAI_JOHO（競走馬除外情報）
- BATAIJU（馬体重）, TENKO_BABA_JOTAI（天候馬場状態）
- SHUSSOTORIKESHI_KYOSOJOGAI（出走取消・競走除外）, KISHU_HENKO（騎手変更）
- HASSOJIKOKU_HENKO（発走時刻変更）, COURSE_HENKO（コース変更）

**その他（1テーブル）**:
- SHOBUFUKU（勝負服）

**実装ファイル**:
- `mykeibadb/tables.py`（更新）
- `tests/integration/test_shussobetsu_tables.py`
- `tests/integration/test_kyosoba_detail_tables.py`
- `tests/integration/test_data_mining_tables.py`
- `tests/integration/test_win5_tables.py`
- `tests/integration/test_sokuhou_tables.py`
- `tests/integration/test_other_tables.py`

**テスト項目**:

**正常系**:
- 各テーブルの基本取得
- 代表的なフィルタパターン
- 出走別データの集計
- 速報データの取得
- WIN5データの取得

**成果物**:
- 全テーブル定義（合計63テーブル）
- 結合テスト

**レビューポイント**:
- 全テーブルの動作確認
- ドキュメントとの整合性

---

### PR#8: 結合テストの整備

**目的**: エンドツーエンドのテストを整備

**実装内容**:
- 実DB使用の結合テストシナリオ
- テストデータのセットアップスクリプト
- CI/CD環境でのテスト実行設定

**実装ファイル**:
- `tests/integration/test_end_to_end.py`
- `tests/fixtures/setup_test_db.sql`
- `.github/workflows/mykeibadb-ci.yml`（更新）

**テスト項目**:

**シナリオテスト**:
1. DB接続 → テーブル取得 → 接続クローズ
2. 環境変数からの設定 → テーブル取得
3. フィルタを使った複雑なクエリ
4. エラーからのリカバリ

**パフォーマンステスト**:
- 大量データ取得時の実行時間
- メモリ使用量

**成果物**:
- 結合テストスイート
- テストデータ
- CI/CD設定

**レビューポイント**:
- テストカバレッジ（全体で80%以上）
- CI/CDの安定性
- テスト実行時間

---

### PR#9: ドキュメント・サンプルコードの整備

**目的**: ユーザー向けドキュメントを完成

**実装内容**:
- README.mdの詳細化
- APIドキュメント（docstring）の充実
- サンプルコードの追加
- インストール手順の整備

**実装ファイル**:
- `README.md`（更新）
- `doc/USAGE.md`（使用例詳細）
- `examples/`（サンプルコード）
- `doc/API.md`（API仕様）

**サンプルコード**:
- `examples/basic_usage.py`: 基本的な使い方
- `examples/filtering.py`: フィルタの使い方
- `examples/with_keibaai.py`: KeibaAIとの連携例

**成果物**:
- 完全なドキュメント
- サンプルコード集

**レビューポイント**:
- ドキュメントの分かりやすさ
- サンプルコードの実行可能性
- 初心者でも理解できるか

---

### PR#10: パフォーマンス最適化

**目的**: クエリ実行速度とメモリ使用量を最適化

**実装内容**:
- クエリキャッシング機能（簡易版）
- 接続プールサイズの最適化
- 大量データ取得時のチャンク処理
- プロファイリングとボトルネック解消

**実装ファイル**:
- `mykeibadb/connection.py`（更新）
- `mykeibadb/cache.py`（新規）
- `tests/performance/test_benchmark.py`

**最適化ポイント**:
- DataFrame変換の高速化
- 不要なカラムの除外オプション
- バッチ処理機能

**成果物**:
- 最適化されたコード
- ベンチマーク結果

**レビューポイント**:
- パフォーマンス改善の定量評価
- メモリ使用量の削減
- 既存機能への影響なし

---

### PR#11: エラーハンドリング強化

**目的**: エラーメッセージとロギングを改善

**実装内容**:
- 詳細なエラーメッセージ
- ロギング機能の追加
- リトライ機能（接続エラー時）
- エラー発生時のデバッグ情報

**実装ファイル**:
- `mykeibadb/logger.py`（新規）
- 各モジュールのエラーハンドリング強化

**成果物**:
- ロギング機能
- 改善されたエラーメッセージ

**レビューポイント**:
- エラーメッセージの有用性
- ログレベルの適切性
- セキュリティ（パスワード等の非出力）

---

### PR#12: v1.0.0リリース準備

**目的**: 初版リリースに向けた最終調整

**実装内容**:
- CHANGELOG.mdの作成
- バージョン番号の設定
- PyPIへの公開準備
- ライセンスファイルの確認
- セキュリティスキャン

**実装ファイル**:
- `CHANGELOG.md`
- `LICENSE`
- `pyproject.toml`（バージョン更新）
- `setup.py`（必要に応じて）

**成果物**:
- リリース可能なパッケージ
- PyPI公開（検討）

**レビューポイント**:
- すべてのテストが通過
- ドキュメントの完全性
- セキュリティ問題なし

---

## 3. テスト計画

### 3.1 テスト戦略

- [pytest-coding-rule](/.github/skills/pytest-coding-rule/SKILL.md)に準拠
- テストファーストで実装（各PR作成前にテストコードを書く）
- カバレッジ目標: 80%以上

### 3.2 テスト環境

#### 単体テスト環境
- モックDBを使用（pytest-mock）
- 外部依存を排除
- 高速実行（全テスト5秒以内）

#### 結合テスト環境
- Windows側のPostgreSQL 16を使用（mykeibadbが構築）
- Dockerコンテナから`host.docker.internal`で接続
- テストデータは`tests/fixtures/setup_test_db.sql`で投入
- CI/CD環境でも実行可能（PostgreSQLサービスを使用）

### 3.3 テストデータ

**最小限のサンプルデータ**:
- RACE_SHOSAI: 10レース分
- UMAGOTO_RACE_JOHO: 100件（10レース × 平均10頭）
- KISHU_MASTER: 100騎手
- その他テーブル: 各10-100件

**注意**:
- ローカル開発環境: Windows側のPostgreSQLを使用
- CI/CD環境: GitHub ActionsのPostgreSQLサービスを使用
