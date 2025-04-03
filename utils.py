import html
import re
from datetime import datetime

import dateutil.parser  # type: ignore


def clean_html(content):
    """HTMLタグを除去し、エンティティをデコードする"""
    # HTMLタグを除去
    text = re.sub(r"<[^>]+>", "", content)
    # HTMLエンティティをデコード
    text = html.unescape(text)
    return text


def format_datetime(dt_str):
    """日時を読みやすい形式にフォーマットする"""
    try:
        dt = dateutil.parser.parse(dt_str)
        now = datetime.now().astimezone()

        # 今日の場合は時刻のみ
        if dt.date() == now.date():
            return dt.strftime("%H:%M:%S")
        # 今年の場合は月日と時刻
        elif dt.year == now.year:
            return dt.strftime("%m/%d %H:%M")
        # それ以外は年月日と時刻
        else:
            return dt.strftime("%Y/%m/%d %H:%M")
    except Exception:
        return dt_str


def display_toots(toots):
    """トゥートを表示する"""
    if not toots:
        print("表示するトゥートがありません")
        return

    # 最新のトゥートを下に表示するため、リストを逆順にする
    total_toots = len(toots)
    for i, toot in enumerate(reversed(toots), 1):
        # 最新のトゥートが1になるよう番号を逆にする
        display_num = total_toots - i + 1
        # リブーストの場合は元の投稿者情報を取得
        if toot.get("reblog"):
            original_toot = toot["reblog"]
            boosted_by = toot["account"]["display_name"] or toot["account"]["username"]
            account = (
                original_toot["account"]["display_name"]
                or original_toot["account"]["username"]
            )
            username = original_toot["account"]["acct"]
            content = original_toot["content"]
            created_at = original_toot["created_at"]

            print(f"\n[{display_num}] {boosted_by}さんがブースト:")
        else:
            account = toot["account"]["display_name"] or toot["account"]["username"]
            username = toot["account"]["acct"]
            content = toot["content"]
            created_at = toot["created_at"]

        # 内容をクリーンアップして表示
        clean_content = clean_html(content)
        formatted_time = format_datetime(created_at)

        print(f"\n[{display_num}] {account} (@{username}) - {formatted_time}")
        print("-" * 40)
        print(clean_content)

        # CW（コンテンツ警告）があれば表示
        if toot.get("spoiler_text"):
            print(f"\n[CW] {toot['spoiler_text']}")

        # メディア添付があれば表示
        if toot.get("media_attachments"):
            print("\n添付メディア:")
            for media in toot["media_attachments"]:
                media_type = media.get("type", "不明")
                desc = media.get("description") or "説明なし"
                url = media.get("url")
                print(f"- [{media_type}] {desc} ({url})")

        # カスタム絵文字があれば置換して表示
        if toot.get("emojis"):
            print("\n絵文字:")
            for emoji in toot["emojis"]:
                print(f":{emoji['shortcode']}: - {emoji['url']}")

        # 返信数、ブースト数、お気に入り数を表示
        print(
            f"\n💬 {toot.get('replies_count', 0)} "
            f"🔁 {toot.get('reblogs_count', 0)} "
            f"⭐ {toot.get('favourites_count', 0)}"
        )

        # 公開範囲を表示
        visibility = toot.get("visibility", "public")
        visibility_icons = {
            "public": "🌐",
            "unlisted": "🔓",
            "private": "🔒",
            "direct": "✉️",
        }
        print(f"{visibility_icons.get(visibility, '?')} {visibility}")

        print("-" * 60)


def display_account(account):
    """アカウント情報を表示する"""
    print("\n📝 アカウント情報:")
    print(f"名前: {account['display_name']}")
    print(f"ユーザー名: @{account['acct']}")

    if account.get("note"):
        bio = clean_html(account["note"])
        print(f"\n自己紹介:\n{bio}")

    print(
        f"\nフォロー: {account['following_count']} "
        f"フォロワー: {account['followers_count']} "
        f"投稿数: {account['statuses_count']}"
    )

    if account.get("url"):
        print(f"プロフィールURL: {account['url']}")

    if account.get("fields"):
        print("\nプロフィール項目:")
        for field in account["fields"]:
            name = clean_html(field["name"])
            value = clean_html(field["value"])
            print(f"- {name}: {value}")
