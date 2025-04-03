import os
from pathlib import Path

from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# .envファイルのパス
ENV_FILE = Path(".env")


def load_config():
    """環境変数から設定を読み込む"""
    config = load_config_from_env()
    return config


def load_config_from_env():
    """環境変数から設定を読み込む"""
    instance_url = os.getenv("MASTODON_INSTANCE_URL")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")

    if not instance_url:
        return None

    config = {"instance_url": instance_url}

    if client_id and client_secret:
        config["client_id"] = client_id
        config["client_secret"] = client_secret

    if access_token:
        config["access_token"] = access_token

    return config


def save_tokens_to_env(client_id, client_secret, access_token=None):
    """トークンを環境変数ファイルに保存する"""
    # .envファイルが存在しない場合は作成
    if not ENV_FILE.exists():
        with open(ENV_FILE, "w") as f:
            f.write(f"MASTODON_INSTANCE_URL={os.getenv('MASTODON_INSTANCE_URL', '')}\n")

    # 既存の.envファイルを読み込む
    with open(ENV_FILE, "r") as f:
        lines = f.readlines()

    # 既存の行を更新または新しい行を追加
    updated_client_id = False
    updated_client_secret = False
    updated_access_token = False

    for i, line in enumerate(lines):
        if line.startswith("CLIENT_ID="):
            lines[i] = f"CLIENT_ID={client_id}\n"
            updated_client_id = True
        elif line.startswith("CLIENT_SECRET="):
            lines[i] = f"CLIENT_SECRET={client_secret}\n"
            updated_client_secret = True
        elif access_token and line.startswith("ACCESS_TOKEN="):
            lines[i] = f"ACCESS_TOKEN={access_token}\n"
            updated_access_token = True

    # 存在しない場合は追加
    if not updated_client_id:
        lines.append(f"CLIENT_ID={client_id}\n")
    if not updated_client_secret:
        lines.append(f"CLIENT_SECRET={client_secret}\n")
    if access_token and not updated_access_token:
        lines.append(f"ACCESS_TOKEN={access_token}\n")

    # 更新した内容を書き込む
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)

    # ファイルのパーミッションを設定（ユーザーのみ読み書き可能）
    os.chmod(ENV_FILE, 0o600)


def create_app_interactive():
    """対話的にアプリケーション情報を設定する"""
    instance_url = input("マストドンインスタンスのURL (例: https://mastodon.social): ")

    # 環境変数に保存
    with open(ENV_FILE, "w") as f:
        f.write(f"MASTODON_INSTANCE_URL={instance_url}\n")

    # ファイルのパーミッションを設定
    os.chmod(ENV_FILE, 0o600)

    print("アクセストークンの取得方法:")
    print(f"1. {instance_url}/settings/applications にアクセス")
    print("2. 「新規アプリ」をクリック")
    print("3. アプリ名（mastodon-cli）とスコープ（read, write）を設定")
    print("4. 作成後、表示されるアクセストークンをコピー")

    return {"instance_url": instance_url}
