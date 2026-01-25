# mykeibadb-python

## 目的

mykeibadbを使用してPostgreSQLデータベース「mykeibadb」に格納された競馬データをpythonで取得するためのライブラリを設計・実装したい。  
mykeibadbとは、JRA-VANが提供するJVLinkを使用して競馬データを取得し、ローカルのPostgreSQLデータベースに格納するためのWindows用ソフトウェアです。  
mykeibadbのREADMEは/KeibaAI/src/mykeibadb-python/doc/Readme.txtにあります。

## 要件

### リポジトリ要件

- mykeibadb-pythonはKeibaAIリポジトリのサブモジュールとしてKeibaAI/src/mykeibadb-pythonに配置される。
- ただし、mykeibadb-pythonはKeibaAIには依存せず、単独でも動作する。
- mykeibadb-pythonはPythonパッケージとして構成される。

### 機能要件

- mykeibadbのexeファイル(`C:\mykeibadb_v3.61\mykeibadb.exe`,各自環境による)を実行してDBを更新する機能
- mykeibadbデータベースに接続し、各テーブルをデータフレームで取得する機能
  - テーブルの詳細は`mykeibadb-python/doc/DATA_TABLE.md`を参照
  - 関数の引数は各テーブルのキー（オプション）とすること
  - キーが指定されなかった場合はテーブル全件を取得すること
  - キーが複数ある場合は指定されたキーの組み合わせでフィルタリングすること
  - 使用されているコードに関しては`mykeibadb-python/doc/CODE_TABLE.md`を参照

## 作業内容

以下の手順で最初の作業を行ってください。
実際の実装に関してはPLAN.mdをもとにあとで行うため、ここでは仕様検討と設計に留めてください。

1. `DATA_TABLE.md`,`CODE_TABLE.md`を読んでmykeibadbの仕様を確認する
2. `mykeibadb-python/doc/SPEC.md`に機能仕様書を作成する
3. SPEC.mdをベースに`mykeibadb-python/doc/PLAN.md`に実装計画書を記載する
   - 人がレビュー可能なレベルに分割し、PR単位でタスクを記載する
   - テスト計画も作って実装計画に盛り込む
     - テスト実装は`mykeibadb-python/.github/skills/pytest-coding-rule/SKILL.md`のルールに従うこと