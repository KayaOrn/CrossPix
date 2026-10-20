import os
import re
import json
import shutil
from PIL import Image

# ==================== 設定項目 ====================
# ご自身の GitHub Pages の絶対 URL に書き換えてください
# 例： "https://example.com"
SITE_URL = ""

IMAGE_DIR = "images"       # 元画像の保存ディレクトリ
THUMB_DIR = "thumbnails"   # サムネイルの保存ディレクトリ
OUTPUT_JSON = "data.json"  # 生成されるメタデータの出力ファイル

# サポートする画像形式
VALID_EXTS = (".jpg", ".jpeg", ".png", ".webp")

# 正規表現：[日付(8桁)] - [人物(ドット区切り)] - [タグ(ドット区切り)] - [コメント] にマッチ
FILENAME_PATTERN = re.compile(
    r"^(\d{8})[-_](.*?)[-_](.*?)[-_](?:\.?)(.*?)\.(?:" + "|".join([e.lstrip('.') for e in VALID_EXTS]) + ")$",
    re.IGNORECASE
)

def generate_thumbnail(img_path, thumb_path, max_size=(400, 400)):
    """フロントエンドで大きすぎる原画像を読み込むのを防ぐため、サムネイルを生成する"""
    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
    try:
        with Image.open(img_path) as img:
            img.thumbnail(max_size)
            img.save(thumb_path, optimize=True, quality=85)
    except Exception as e:
        print(f"警告: {img_path} のサムネイル生成に失敗しました: {e}")

def main():
    if not os.path.exists(IMAGE_DIR):
        print(f"エラー: ディレクトリ '{IMAGE_DIR}' が存在しません。")
        return

    # 処理実行前に thumbnails ディレクトリを完全にクリーンアップ（削除＆再作成）
    if os.path.exists(THUMB_DIR):
        shutil.rmtree(THUMB_DIR)
    os.makedirs(THUMB_DIR, exist_ok=True)

    image_items = []
    base_url = SITE_URL.rstrip('/')

    # 画像ディレクトリを走査
    for filename in sorted(os.listdir(IMAGE_DIR), reverse=True):
        if not filename.lower().endswith(VALID_EXTS):
            continue

        match = FILENAME_PATTERN.match(filename)
        if not match:
            print(f"スキップ: 命名規則に一致しません -> {filename}")
            continue

        date_str, people_str, tags_str, comment = match.groups()[:4]

        # 人物とタグを解析
        people = [p.strip() for p in people_str.split(".") if p.strip()]
        custom_tags = [t.strip() for t in tags_str.split(".") if t.strip()]

        # # 付きの統一タグリストを生成
        all_tags = [f"#{p}" for p in people] + [f"#{t}" for t in custom_tags]

        img_path = os.path.join(IMAGE_DIR, filename)
        thumb_name = f"thumb_{filename}"
        thumb_path = os.path.join(THUMB_DIR, thumb_name)

        # サムネイルを生成
        generate_thumbnail(img_path, thumb_path)

        # データ構造を組み立て（URLを絶対パスに設定）
        item = {
            "filename": filename,
            "url": f"{base_url}/{IMAGE_DIR}/{filename}",
            "thumbnail_url": f"{base_url}/{THUMB_DIR}/{thumb_name}",
            "date": date_str,
            "people": people,
            "custom_tags": custom_tags,
            "tags": all_tags,
            "comment": comment if comment != "nocomment" else ""
        }
        image_items.append(item)

    # JSON ファイルに書き込み
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(image_items, f, ensure_ascii=False, indent=2)

    print(f"正常に {len(image_items)} 件の画像を処理しました。データは '{OUTPUT_JSON}' に保存されました。")

if __name__ == "__main__":
    main()