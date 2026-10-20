# CrossPix

**GitHub Actions + Python + Tailwind CSS** をベースに構築された、軽量かつサーバーレスな JAMstack 静的写真アルバムです。絶対パスの自動生成、スマホ表示時 3 列グリッド、マルチタグ検索、および `neighbors.json` を用いた隣接サイト（連合アルバム）のタイムアウト保護付き自動読み込み機能をサポートしています。

---

## ✨ 主な特徴

- **ファイル名＝データ**：厳格なファイル命名規則により、日付、人物、タグ、コメントを自動解析。
- **絶対パス対応**：Python スクリプト内の `SITE_URL` 設定により、原画像およびサムネイルのリンクを絶対パスで自動生成し、クロスサイトでの連合読み込みに完全対応。
- **隣接サイト（連合アルバム）機能**：`neighbors.json` で他サイトのアルバムデータを設定可能。自サイトの読み込み完了後に非同期で取得し、`AbortController` によるタイムアウト保護（3秒超で自動破棄）によりページのフリーズを防ぎます。
- **モバイル最適化**：スマホ表示時のウォーターフォールレイアウトはデフォルトで 1 行 3 列のサムネイル表示に対応。
- **自動化デプロイ**：プッシュのたびに GitHub Actions が古いサムネイルをクリーンアップし、`thumbnails/` と `data.json` を再生成してリポジトリに自動コミット。

---

## 📁 ディレクトリ構造

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions 自動デプロイワークフロー
├── images/                 # 原画像の保存ディレクトリ
├── thumbnails/             # 自動生成されるサムネイルディレクトリ（ビルド時に自動クリーンアップ）
├── generate.py             # Python データ＆サムネイル生成スクリプト
├── index.html              # フロントエンド表示ページ (Tailwind CSS)
├── data.json               # 自動生成される自サイトの画像メタデータ
└── neighbors.json          # 隣接サイト（連合アルバム）の設定ファイル

```

## ファイル命名と設定方法
1. 画像の命名規則
images/ ディレクトリ内の画像は以下の形式に従ってください：
[日付]_[人物]_[タグ]_[コメント].[拡張子]

    - 例：20260930_SaY0_シーサイドフェス.あお_nocomment.jpg

2. generate.py の設定
スクリプトを実行する前に、generate.py 内の SITE_URL をご自身の GitHub Pages の絶対 URL に書き換えてください：

```Python
SITE_URL = "https://example.com"
```

3. neighbors.json の設定（任意）
隣接サイトを追加したい場合は、ルートディレクトリに neighbors.json を作成します：

```JSON
[
  {
    "name": "隣接Aのアルバム",
    "url": "https://example.com/data.json"
  }
]
```

注：隣接サイトの data.json は CORS が許可されており、中の画像 URL が絶対パスである必要があります。