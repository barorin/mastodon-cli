# Mastodon CLI

マストドンを CUI から利用するための Python ツールです。Mastodon.py を使用して、シンプルなコマンドラインインターフェースを提供します。

## 機能

- タイムラインの表示（ホーム、ローカル、パブリック）
- ハッシュタグタイムラインの表示
- トゥートの投稿（メディア添付、CW、公開範囲設定など）
- プロフィール表示
- 安全な認証情報管理（.env ファイル使用）

## インストール

### 必要条件

- Python 3.6 以上
- pip

### インストール手順

1. リポジトリをクローン

```bash
git clone https://github.com/barorin/mastodon-cli.git
cd mastodon-cli
```

2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

## 初期設定

初回実行時には`.env`ファイルの作成が必要です。リポジトリに含まれる`.env.example`ファイルをコピーして`.env`という名前で作成し、必要な情報を設定してください。

```sh
cp .env.example .env
# その後、.envファイルを編集してください
```

`.env`ファイルには以下の情報を設定します。

```sh
# マストドンインスタンスのURL（必須）
MASTODON_INSTANCE_URL=https://mastodon.social

# アプリケーション情報（必須）
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

# アクセストークン（必須）
ACCESS_TOKEN=your_access_token

# アプリケーションのウェブサイトURL（オプション）
MASTODON_APP_WEBSITE=https://github.com/yourusername/mastodon-cli
```

アクセストークンなどは以下の手順で取得できます。

1. Mastodon インスタンスの設定 > アプリケーションにアクセス
2. 「新規アプリ」をクリック
3. アプリ名（例: mastodon-cli）とスコープ（read, write）を設定
4. 作成後、表示されるクライアント ID、クライアントシークレット、アクセストークンをコピー

これらの認証情報は`.env`ファイルに安全に保存され、次回以降の実行では自動的に使用されます。

## 使い方

### トゥートの投稿

```sh
# 基本的な投稿
python main.py post --text "こんにちは、マストドン！"

# 公開範囲を指定して投稿
python main.py post --text "非公開投稿" --visibility private

# メディア付き投稿
python main.py post --text "写真付き投稿" --media photo.jpg

# コンテンツ警告付き投稿
python main.py post --text "長い内容..." --spoiler "長文注意"

# 複数のメディアを添付
python main.py post --text "アルバム" --media photo1.jpg photo2.jpg photo3.jpg
```

### タイムラインの表示

```sh
# ホームタイムラインを表示（デフォルト）
python main.py timeline

# ローカルタイムラインを表示
python main.py timeline --type local

# パブリックタイムラインを表示
python main.py timeline --type public

# 表示件数を指定
python main.py timeline --count 15
```

### ハッシュタグタイムラインの表示

```sh
# 「python」タグのトゥートを表示
python main.py tag python

# 「日本語」タグのトゥートを15件表示
python main.py tag 日本語 --count 15
```

### プロフィール表示

```sh
# 自分のプロフィールを表示
python main.py profile

# 他のユーザーのプロフィールを表示
python main.py profile @username
python main.py profile username@example.com
```

## ファイル構成

```sh
mastodon_cli/
├── main.py               # メインスクリプト（エントリポイント）
├── mastodon_api.py       # Mastodon API関連機能
├── config.py             # 設定管理
├── utils.py              # ユーティリティ関数
├── .env                  # 環境変数（機微情報）
├── .env,example          # 環境変数サンプル
└── requirements.txt      # 依存パッケージ
```

## セキュリティについて

- 認証情報は`.env`ファイルにのみ保存されます
- このファイルのパーミッションは自動的に 600（ユーザーのみ読み書き可能）に設定されます

## カスタマイズ

`utils.py`の`display_toots`関数を編集することで、トゥートの表示形式をカスタマイズできます。

## ライセンス

MIT
