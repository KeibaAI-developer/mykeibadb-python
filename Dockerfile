# ベースイメージ
FROM python:3.12.4

# 作業ディレクトリを設定
WORKDIR /mykeibadb-python

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# ソースコードをコピー
COPY . /mykeibadb-python

# 依存ライブラリをインストール
RUN pip install --no-cache-dir -e .[dev]

# デフォルトで実行するコマンド
CMD ["/bin/bash"]
