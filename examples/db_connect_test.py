"""PostgreSQL接続テストスクリプト."""

import psycopg2

try:
    conn = psycopg2.connect(
        host="host.docker.internal",
        port=5432,
        database="mykeibadb",
        user="postgres",
        password="postgres",
    )
    print("接続成功！")
    conn.close()
except Exception as e:
    print(f"接続失敗: {e}")
