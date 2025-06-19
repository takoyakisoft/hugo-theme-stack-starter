import os
import sys
import time
from google import genai

# --- 設定 ---

# Google AI APIキーを環境変数から取得
# 事前に環境変数 GOOGLE_API_KEY を設定してください
# 例: export GOOGLE_API_KEY='YOUR_API_KEY'
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("エラー: 環境変数 'GOOGLE_API_KEY' が設定されていません。")
    print("APIキーを設定してから再実行してください。")
    sys.exit(1)

# 使用するGeminiモデル名 (例: 'gemini-1.5-flash', 'gemini-pro')
# 利用可能なモデルは `[m.name for m in genai.list_models()]` で確認できます
MODEL_NAME = "gemini-2.5-pro-exp-03-25" # "gemini-2.0-flash-thinking-exp-01-21"

# Hugoプロジェクトのコンテンツディレクトリ (スクリプトからの相対パスを想定)
# scriptフォルダがプロジェクトルート直下にあると仮定
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(PROJECT_ROOT, "content")

# 翻訳対象の言語とファイル拡張子のマッピング
# キー: 言語コード (APIで使用), 値: (ファイル拡張子, プロンプト用言語名)
TARGET_LANGUAGES = {
    "en": (".en.md", "英語"),
    "zh-cn": (".zh-cn.md", "中国語（簡体字）"),
    # 必要であれば他の言語を追加
}

# APIレート制限を考慮したリクエスト間の待機時間 (秒)
# 必要に応じて調整してください (例: 無料枠の場合は長めに設定)
SLEEP_TIME = 2

# --- 翻訳関数 ---

def translate_text(text, target_language_code, target_language_name):
    """Google Generative AI を使用してテキストを翻訳する"""
    print(f"    {target_language_name}への翻訳を開始...")

    # Markdownの構造とフロントマターを維持するように指示するプロンプト
    prompt = f"""以下のMarkdownテキストを{target_language_name}に翻訳してください。
コメントも翻訳し日本語は残さないでください。
翻訳結果はそのままHugoで使用できるMarkdown形式のみを出力してください。

```markdown
{text}
```
"""

    try:
        # Client APIを使用
        client = genai.Client(
            api_key=GOOGLE_API_KEY,
        )
        response = client.models.generate_content(
            model=MODEL_NAME,  # モデル名を直接渡す
            contents=prompt,
        )

        # レスポンスから翻訳テキストを抽出
        translated_text = response.text
        
        #  翻訳結果から ```markdown と ``` を文字列の先頭と末尾で削除する処理を追加
        if translated_text.startswith("```markdown"):
            translated_text = translated_text[len("```markdown"):]
        if translated_text.endswith("```"):
            translated_text = translated_text[:-len("```")]
        translated_text = translated_text.strip()

        print(f"    {target_language_name}への翻訳完了。")
        return translated_text.strip()
    
    except Exception as e:
        print(f"    エラー: 翻訳中にエラーが発生しました: {e}")
        # レート制限のエラー (ResourceExhausted or 429) かどうかを簡易的に判定
        if "Resource has been exhausted" in str(e) or "429" in str(e):
            wait_time = SLEEP_TIME * 5
            print(f"    レート制限の可能性があります。{wait_time}秒待機します...")
            time.sleep(wait_time)
        elif "block" in str(e).lower(): # コンテンツフィルター等によるブロック
             print(f"    リクエストがブロックされました。理由: {e}")
             print(f"    プロンプトまたはコンテンツに問題がある可能性があります。スキップします。")
        else:
             # その他の予期せぬエラー
             print(f"    予期せぬエラーが発生しました。詳細: {e}")
        return None

# --- メイン処理 ---

def main():
    print(f"Hugoコンテンツディレクトリ ({CONTENT_DIR}) の翻訳を開始します...")
    print(f"使用モデル: {MODEL_NAME}")
    print(f"対象言語: {', '.join([lang[1] for lang in TARGET_LANGUAGES.values()])}")
    print("-" * 30)

    if not os.path.isdir(CONTENT_DIR):
        print(f"エラー: コンテンツディレクトリ '{CONTENT_DIR}' が見つかりません。")
        print("スクリプトがHugoプロジェクトの 'script' フォルダ内に正しく配置されているか確認してください。")
        sys.exit(1)

    found_ja_files = 0
    translated_count = 0

    # contentディレクトリ以下を再帰的に探索
    for root, dirs, files in os.walk(CONTENT_DIR):
        # draftsフォルダなどはスキップしたい場合に追加
        # if "drafts" in root:
        #    continue

        for file in files:
            if file.endswith(".ja.md"):
                found_ja_files += 1
                ja_filepath = os.path.join(root, file)
                base_filepath = ja_filepath[:-len(".ja.md")] # ".ja.md" を除いたパス

                print(f"\n[処理ファイル] {os.path.relpath(ja_filepath, PROJECT_ROOT)}")

                # 元ファイルの読み込み
                try:
                    with open(ja_filepath, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    if not original_content.strip():
                        print("  ファイルが空のためスキップします。")
                        continue
                except Exception as e:
                    print(f"  エラー: ファイル '{ja_filepath}' の読み込みに失敗しました: {e}")
                    continue

                # 各ターゲット言語について処理
                for lang_code, (lang_suffix, lang_name) in TARGET_LANGUAGES.items():
                    target_filepath = base_filepath + lang_suffix

                    # 翻訳済みファイルが存在するか確認
                    if not os.path.exists(target_filepath):
                        print(f"  -> {lang_name} ({lang_suffix}) の翻訳ファイルが見つかりません。翻訳を実行します。")

                        # 翻訳実行
                        translated_content = translate_text(original_content, lang_code, lang_name)

                        if translated_content:
                            # 翻訳結果をファイルに書き込み
                            try:
                                with open(target_filepath, 'w', encoding='utf-8') as f:
                                    f.write(translated_content)
                                print(f"    翻訳結果を保存しました: {os.path.relpath(target_filepath, PROJECT_ROOT)}")
                                translated_count += 1
                                # API負荷軽減のため待機
                                print(f"    {SLEEP_TIME}秒待機...")
                                time.sleep(SLEEP_TIME)
                            except Exception as e:
                                print(f"    エラー: ファイル '{target_filepath}' への書き込みに失敗しました: {e}")
                        else:
                            print(f"    {lang_name}への翻訳に失敗したため、ファイルは作成されませんでした。")
                            # 失敗した場合も少し待機（連続エラーを防ぐ）
                            time.sleep(max(1, SLEEP_TIME / 2))

                    else:
                        print(f"  -> {lang_name} ({lang_suffix}) の翻訳ファイルは既に存在します。スキップします。")

    print("-" * 30)
    print("翻訳処理が完了しました。")
    print(f"処理対象の日本語ファイル (.ja.md): {found_ja_files} 件")
    print(f"新規に翻訳・保存したファイル数: {translated_count} 件")

if __name__ == "__main__":
    main()