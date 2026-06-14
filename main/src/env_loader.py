# encoding utf-8
"""prod/dev で読み込む .env を切り替える共通ローダ。

褒めbot・歓迎bot の両方から使う。実行環境（docker-compose / Cloud Run Job）
で渡す環境変数 `APP_ENV` を見て、読み込む .env ファイルを選ぶ:

    APP_ENV=dev  → .env.dev （devコミュニティ用）
    それ以外     → .env     （本番用）

コンテナでは `/env/` を、ローカル直実行では `env/` を探す。APP_ENV 自体は
.env の中ではなく実行環境側で渡すこと（どのファイルを読むかを決める値のため）。
"""

import os

from dotenv import load_dotenv


def load_env():
    """APP_ENV に応じた .env を読み込み、読んだパスを返す（無ければ None）。"""
    app_env = os.environ.get("APP_ENV", "").strip().lower()
    filename = ".env.dev" if app_env == "dev" else ".env"
    for base in ("/env", "env"):
        path = os.path.join(base, filename)
        if os.path.exists(path):
            load_dotenv(path)
            return path
    print("error doesn't exist .env path: {}".format(filename))
    return None
