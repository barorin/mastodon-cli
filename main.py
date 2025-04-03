import argparse
import sys

import config
import mastodon_api
import utils


def main():
    parser = argparse.ArgumentParser(description="マストドンCUIクライアント")

    # サブコマンドを作成
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # 投稿コマンド
    post_parser = subparsers.add_parser("post", help="トゥートを投稿する")
    post_parser.add_argument("--text", "-t", required=True, help="投稿するテキスト")
    post_parser.add_argument(
        "--visibility",
        "-v",
        choices=["public", "unlisted", "private", "direct"],
        default="public",
        help="投稿の公開範囲 (デフォルト: public)",
    )
    post_parser.add_argument(
        "--media", "-m", nargs="+", help="添付するメディアファイル (最大4つ)"
    )
    post_parser.add_argument(
        "--sensitive", "-s", action="store_true", help="センシティブな内容としてマーク"
    )
    post_parser.add_argument("--spoiler", "-w", help="内容の警告/概要 (CW)")

    # タイムライン取得コマンド
    timeline_parser = subparsers.add_parser("timeline", help="タイムラインを表示する")
    timeline_parser.add_argument(
        "--type",
        "-t",
        choices=["home", "local", "public"],
        default="home",
        help="タイムラインのタイプ (デフォルト: home)",
    )
    timeline_parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=10,
        help="取得するトゥートの数 (デフォルト: 10)",
    )

    # タグタイムライン取得コマンド
    tag_parser = subparsers.add_parser("tag", help="ハッシュタグタイムラインを表示する")
    tag_parser.add_argument("hashtag", help="ハッシュタグ (先頭の#は省略可)")
    tag_parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=10,
        help="取得するトゥートの数 (デフォルト: 10)",
    )

    # プロフィール表示コマンド
    profile_parser = subparsers.add_parser("profile", help="プロフィールを表示する")
    profile_parser.add_argument("username", nargs="?", help="ユーザー名 (@は省略可)")

    args = parser.parse_args()

    # コマンドがない場合はヘルプを表示
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 設定ファイルを読み込む
    app_config = config.load_config()

    # 設定ファイルがない場合
    if app_config is None:
        print(".env ファイルが見つからないか、必要な設定が不足しています")
        print(
            "サンプルの .env.example をコピーして .env を作成し、必要な情報を設定してください"
        )
        sys.exit(1)

    # ユーザー認証
    mastodon = mastodon_api.authenticate(app_config)

    # コマンドに応じた処理を実行
    if args.command == "post":
        # トゥート投稿
        toot = mastodon_api.post_toot(
            mastodon,
            args.text,
            visibility=args.visibility,
            media_files=args.media,
            sensitive=args.sensitive,
            spoiler_text=args.spoiler,
        )

        if toot:
            print(f"トゥート投稿成功: {toot['url']}")

    elif args.command == "timeline":
        # タイムライン表示
        toots = mastodon_api.get_toots(
            mastodon, timeline_type=args.type, count=args.count
        )

        if toots:
            print(f"{args.type}タイムラインの最新{len(toots)}件:")
            utils.display_toots(toots)

    elif args.command == "tag":
        # ハッシュタグタイムライン表示
        hashtag = args.hashtag.lstrip("#")  # #が先頭についていたら削除
        toots = mastodon_api.get_toots(
            mastodon, timeline_type=f"tag:{hashtag}", count=args.count
        )

        if toots:
            print(f"#{hashtag}タグの最新{len(toots)}件:")
            utils.display_toots(toots)

    elif args.command == "profile":
        # プロフィール表示
        username = args.username

        try:
            if username:
                # @が先頭についていたら削除
                username = username.lstrip("@")
                account = mastodon.account_lookup(username)
            else:
                # 自分のアカウント情報を取得
                account = mastodon.me()

            utils.display_account(account)
        except Exception as e:
            print(f"プロフィール取得エラー: {e}")


if __name__ == "__main__":
    main()
