import getpass
import os
import sys

from mastodon import Mastodon

import config


def create_app(instance_url):
    """インスタンスにアプリケーションを登録する"""
    try:
        # ウェブサイトURLを環境変数から取得
        website_url = os.getenv("MASTODON_APP_WEBSITE")

        client_id, client_secret = Mastodon.create_app(
            "mastodon-cli",
            api_base_url=instance_url,
            scopes=["read", "write"],
            website=website_url,
        )

        # 環境変数ファイルに保存
        app_config = {
            "instance_url": instance_url,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        config.save_tokens_to_env(client_id, client_secret)

        return app_config
    except Exception as e:
        print(f"アプリケーション登録エラー: {e}")
        sys.exit(1)


def authenticate(app_config):
    """ユーザー認証を行う"""
    # アクセストークンがない場合は取得
    if "access_token" not in app_config:
        # アクセストークンの入力を促す
        print("アクセストークンを取得する手順：")
        print(f"1. {app_config['instance_url']}/settings/applications にアクセス")
        print("2. 「新規アプリ」をクリック")
        print("3. アプリ名（例: mastodon-cli）とスコープ（read, write）を設定")
        print("4. 作成後、表示されるアクセストークンをコピー")

        access_token = getpass.getpass("アクセストークン: ")

        try:
            # トークンの有効性をテスト
            test_mastodon = Mastodon(
                access_token=access_token, api_base_url=app_config["instance_url"]
            )
            # 自分のアカウント情報を取得できれば認証成功
            test_mastodon.me()

            app_config["access_token"] = access_token
            config.save_tokens_to_env(
                app_config["client_id"], app_config["client_secret"], access_token
            )
        except Exception as e:
            print(f"認証エラー: {e}")
            sys.exit(1)

    return Mastodon(
        access_token=app_config["access_token"], api_base_url=app_config["instance_url"]
    )


def post_toot(
    mastodon,
    text,
    visibility="public",
    media_files=None,
    sensitive=False,
    spoiler_text=None,
):
    """トゥートを投稿する"""
    media_ids = []

    # メディアファイルがある場合はアップロード
    if media_files:
        for media_file in media_files:
            try:
                media = mastodon.media_post(media_file)
                media_ids.append(media["id"])
            except Exception as e:
                print(f"メディアアップロードエラー ({media_file}): {e}")

    # トゥートを投稿
    try:
        toot = mastodon.status_post(
            text,
            media_ids=media_ids if media_ids else None,
            visibility=visibility,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
        )
        return toot
    except Exception as e:
        print(f"投稿エラー: {e}")
        return None


def get_toots(mastodon, timeline_type="home", count=20):
    """指定したタイムラインから最新のトゥートを取得する"""
    try:
        if timeline_type == "home":
            toots = mastodon.timeline_home(limit=count)
        elif timeline_type == "local":
            toots = mastodon.timeline_local(limit=count)
        elif timeline_type == "public":
            toots = mastodon.timeline_public(limit=count)
        elif timeline_type.startswith("tag:"):
            # ハッシュタグタイムライン
            tag = timeline_type.split(":", 1)[1]
            toots = mastodon.timeline_hashtag(tag, limit=count)
        elif timeline_type.startswith("list:"):
            # リストタイムライン
            list_id = timeline_type.split(":", 1)[1]
            toots = mastodon.timeline_list(list_id, limit=count)
        else:
            print(f"不明なタイムラインタイプ: {timeline_type}")
            return None

        return toots
    except Exception as e:
        print(f"タイムライン取得エラー: {e}")
        return None


def setup():
    """初期セットアップを行う（.envファイルの作成）"""
    print(".env ファイルを作成してください。")
    print(
        "サンプルの .env.example をコピーして .env を作成し、必要な情報を設定してください。"
    )
    print("必要な情報:")
    print("1. MASTODON_INSTANCE_URL - マストドンインスタンスのURL")
    print("2. CLIENT_ID - アプリケーションのクライアントID")
    print("3. CLIENT_SECRET - アプリケーションのクライアントシークレット")
    print("4. ACCESS_TOKEN - アクセストークン")
    print("5. MASTODON_APP_WEBSITE - (オプション)アプリケーションのウェブサイト")

    sys.exit(1)
