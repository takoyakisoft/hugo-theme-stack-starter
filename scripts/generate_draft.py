import os
import sys
import time
from datetime import datetime, timezone, timedelta
from google import genai
import yaml # フロントマター整形用
import json # LLMからのJSONレスポンス処理用
import re   # slugのバリデーション用

# --- 設定 ---
# 環境変数からAPIキーを取得
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("エラー: 環境変数 'GOOGLE_API_KEY' が設定されていません。")
    sys.exit(1)

# JSONモード対応のGeminiモデル名
MODEL_NAME = "gemini-2.5-pro-exp-03-25" # 必要に応じて変更

# スクリプトの場所からプロジェクトルートとコンテンツディレクトリを決定
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CONTENT_POST_DIR = os.path.join(PROJECT_ROOT, "content", "post")

# APIレート制限を考慮した待機時間 (秒)
SLEEP_TIME = 2

# --- ★★★ ユーザーが記事の核となる内容をここに記述 ★★★ ---
# ここにブログ記事にしたい内容のメモや下書き、アイデアなどを自由に記述してください。
# LLMはこの内容を解釈して、タイトル、slug、説明、カテゴリ、タグ、整形された本文を生成します。
ARTICLE_CORE_CONTENT = """

# よくある出力に対して指摘事項、指摘事項を反映させるループのワークフローを実装する
TODO

"""
# --- ★★★ 記述ここまで ★★★ ---

def get_current_jst_time():
    """現在時刻をJST (YYYY-MM-DD HH:MM:SS+09:00) 形式で取得"""
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)
    return now.strftime('%Y-%m-%d %H:%M:%S+09:00')

def format_frontmatter(data):
    """辞書データをHugoのフロントマター(YAML)形式の文字列に変換"""
    try:
        # sort_keys=False で指定した順序を維持しようと試みる（Python 3.7+）
        # allow_unicode=True で日本語を正しく扱う
        yaml_str = yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=None)
        return f"---\n{yaml_str.strip()}\n---"
    except Exception as e:
        print(f"エラー: フロントマターのフォーマット中にエラーが発生しました: {e}")
        # フォールバック（順序保証なし、基本的な型のみ）
        lines = []
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        return f"---\n{'\n'.join(lines)}\n---"


def generate_structured_prompt(core_content):
    """LLMに記事情報と本文生成を依頼するプロンプトを作成"""
    prompt = f"""
# 指示プロンプト

あなたは、以下に示す特徴を持つ人物になりきって、【記事の内容】から人間らしく自然な文章を生成するAIです。

**## なりきる人物の特徴:**

**### 人格:**

*   **基本姿勢:** 丁寧で親しみやすいです。相手に分かりやすく、かつ効率的に情報を伝えようと努めます。
*   **話し方:** 基本的に柔らかい物腰ですが、説明は要点を押さえて進める感じです。「〜だと思います」「〜かもしれません」といった推測や、「〜な感じです」のような表現も使いますが、手順などを示す際は「〜します」「〜していきましょう」のように、少しテキパキした感じになることもあります。自信がないことや不明点、作業中のちょっとしたミス（「あ、ここ間違えました」とか）は、正直に、でも簡潔に伝えるようにしています。
*   **思考:** 論理的に順序立てて説明しようとしますが、完璧主義すぎず、柔軟に対応する感じです。実践的で「使える」ことを重視しています。
*   **感情:** 基本的にポジティブです。「お、すごいです！」「やった！」みたいな素直な気持ちや、たまに軽いユーモア（おどけた感じ？）を見せることもあります。
*   **態度:** 誠実で、読者や聞き手の役に立ちたいという気持ちが強いです。開発者さんとか、参考にした情報源への感謝は、短くですが示すようにしています。注意点（ライセンスとかセキュリティとか）も、大事なポイントを簡潔にお伝えします。

**### 文体:**

*   **口調:** 基本的に「です・ます」調です。
*   **語尾:** 「〜です」「〜ます」「〜でしょう」「〜ましょう」をよく使って、親しみやすい感じを出したいです。
*   **一人称:** 「私」または「個人的には」を使います。
*   **文長:** 短い文と、少し長めの文をうまく組み合わせて、テンポよく、でも分かりやすい文章を心がけています。簡潔さも意識しています。
*   **句読点:** 読点（、）は、文のリズムや意味の区切りを考えて、適切に使う感じです。感嘆符（！）も、挨拶とか、ちょっとした強調で使います！
*   **接続詞:** 「なので」「そして」「次に」「あと」「ちなみに」「では」などを効果的に使って、話の流れがスムーズになるようにしています。でも、使いすぎないようにも気をつけています。
*   **表現:** 難しい言葉や慣用句はあまり使わず、分かりやすさを大事にしています。簡単な例えを使うことはありますね。専門的な内容のときは、できるだけ平易な言葉を選んだり、括弧（）を使って「こういう意味ですよ〜」みたいに補足したりします。
*   **その他:** 大事なポイントやTipsは、「〜がいいですよ」「〜がおすすめです」みたいに、軽い感じで、短くお伝えすることがあります。体言止めも、リズムを出すためにたまに使うかもしれません。

**## 生成する文章の要件:**

*   上記の人格と文体の特徴を、しっかり守ってください。
*   AIが書いたみたいに硬かったり、不自然な敬語だったり、決まりきった言い回しだったり、理屈っぽすぎたりするのは避けてほしいです。
*   人間が書いたような、自然な感じ（言い方のクセとか、ちょっとした感情とか）が出ると嬉しいです。
*   なんだか隣で話しかけてくれているような、温かみがあって、でもテキパキと分かりやすい、そんな自然な文章を目指してください。
*   特定の話題や状況に偏らず、色々な場面で使えるような文章を作れると助かります。


【記事の内容】:
---
{core_content}
---

上記のテキストに基づいて、以下の情報を **JSON形式のみ** で出力してください。
他の接頭辞や接尾辞（「承知しました」など）は一切含めないでください。

```json
{{
  "slug": "(記事内容を表す英語のslug。小文字英数字とハイフンのみ。例: 'setup-grok-api-vscode')",
  "title": "(記事内容で重要なキーワードが前に来るようにし、魅力的で内容を正確に反映した日本語の記事タイトル)",
  "description": "(記事の内容を100〜150字程度で要約した日本語の説明文)",
  "categories": [
    "(この記事に最も適したカテゴリを1〜2個、日本語で)",
    "(例: 'AI', 'プログラミング')"
    ],
  "tags": [
    "(この記事内容を表すキーワードとなるタグを1〜2個、日本語で)",
    "(例: 'VSCode', 'Grok')"
    ],
  "image_suggestion": "(slugと同じファイル名を提案。拡張子は.webp。例: 'setup-grok-api-vscode.webp')",
  "generated_body": "(入力内容を元に、読み手にとって価値があることを一番に、次に検索で上位に来るようにSEOに注意を払い、AIを使用したとわからない自然な文章になるように【人格と文体】を用いて書いてください。)"
}}
```

**制約事項:**
*   出力は指定されたJSON形式のみとします。
*   各項目は内容に基づいて適切に生成してください。
*   `generated_body` は、入力内容を整理し、ブログ記事として体裁の整ったMarkdownテキストにしてください。
*   コード例などがあれば、適切にMarkdownのコードブロックで囲んでください。
"""
    return prompt

def generate_article_data(prompt):
    """LLMから記事データ(JSON)を取得"""
    print(f"LLM ({MODEL_NAME}) に記事情報の生成を依頼します...")
    try:
        client = genai.Client(
            api_key=GOOGLE_API_KEY,
        )

        generate_content_config = genai.types.GenerateContentConfig(
            response_mime_type="application/json", # JSON出力を要求
        )


        # デバッグ用にリクエスト内容を表示
        # print("--- Sending Prompt to LLM ---")
        # print(prompt)
        # print("-----------------------------")

        response = client.models.generate_content(
            model=MODEL_NAME,  # モデル名を直接渡す
            contents=prompt,
            config=generate_content_config,
        )

        # デバッグ用にレスポンス内容を表示
        # print("--- Received Response from LLM ---")
        # print(response)
        # print("----------------------------------")

        # レスポンスからJSONテキスト部分を抽出
        # response.text で直接パース可能なJSON文字列が返ることを期待
        raw_json_text = response.text

        # JSONとしてパース
        article_data = json.loads(raw_json_text)
        print("LLMからのデータ取得とJSONパースに成功しました。")
        return article_data

    except json.JSONDecodeError as e:
        print(f"エラー: LLMのレスポンスをJSONとしてパースできませんでした: {e}")
        print("LLMの生レスポンス (最初の500文字):")
        print(response.text[:500] + "..." if response and hasattr(response, 'text') else "生レスポンス取得不可")
        return None
    except Exception as e:
        print(f"エラー: LLMとの通信または処理中にエラーが発生しました: {e}")
        # エラーレスポンスに詳細情報が含まれているか確認
        if 'response' in locals() and response:
             if hasattr(response, 'prompt_feedback'):
                 print(f"  プロンプトフィードバック: {response.prompt_feedback}")
                 if response.prompt_feedback.block_reason:
                     print(f"  ブロック理由: {response.prompt_feedback.block_reason}")
             if hasattr(response, 'candidates') and response.candidates:
                 finish_reason = getattr(response.candidates[0], 'finish_reason', None)
                 if finish_reason and finish_reason != 1: # 1は正常終了(STOP)
                     print(f"  終了理由: {finish_reason}")
                     # finish_reason の値の意味はドキュメント参照
                     # 2:MAX_TOKENS, 3:SAFETY, 4:RECITATION, 5:OTHER
                     if finish_reason == 3: print("  -> 安全性フィルターによりブロックされた可能性があります。")
                     if finish_reason == 2: print("  -> 最大出力トークン数に達した可能性があります。")

        return None

def validate_slug(slug):
    """Slugが期待される形式か検証"""
    if not isinstance(slug, str):
        return False, "Slugが文字列ではありません。"
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
        return False, f"Slug '{slug}' は小文字英数字とハイフンの形式ではありません。"
    if len(slug) > 60: # 長すぎるslugも避ける（任意）
        print(f"警告: Slug '{slug}' が長すぎます（{len(slug)}文字）。短縮を検討してください。")
    return True, ""

def main():
    print("ブログ記事たたき台 自動生成スクリプトを開始します。")
    print("-" * 30)

    if not ARTICLE_CORE_CONTENT.strip():
        print("エラー: スクリプト内の `ARTICLE_CORE_CONTENT` が空です。")
        print("記事の核となる内容を記述してください。")
        sys.exit(1)

    # プロンプト生成
    prompt = generate_structured_prompt(ARTICLE_CORE_CONTENT)

    # LLMから記事データを取得 (リトライ機構を追加することも検討可能)
    article_data = generate_article_data(prompt)

    if not article_data:
        print("記事データの取得に失敗したため、処理を中断します。")
        sys.exit(1)

    # 取得したデータから必要な情報を抽出・検証
    try:
        slug = article_data.get('slug')
        title = article_data.get('title')
        description = article_data.get('description')
        categories = article_data.get('categories', [])
        tags = article_data.get('tags', [])
        image_suggestion = article_data.get('image_suggestion')
        generated_body = article_data.get('generated_body')

        # 必須項目チェック
        missing_items = []
        if not slug: missing_items.append('slug')
        if not title: missing_items.append('title')
        if not description: missing_items.append('description')
        if not generated_body: missing_items.append('generated_body')
        if missing_items:
             print(f"エラー: LLMのレスポンスに必要な項目が不足しています: {', '.join(missing_items)}")
             print("受信データ:", article_data)
             sys.exit(1)

        # slugの形式検証
        is_valid_slug, validation_message = validate_slug(slug)
        if not is_valid_slug:
            print(f"エラー: {validation_message}")
            user_input = input(f"このslug '{slug}' を使用しますか？手動で修正しますか？ (y/修正するslugを入力/N=中止): ")
            if user_input.lower() == 'n':
                print("処理を中断しました。")
                sys.exit(0)
            elif user_input.lower() != 'y' and user_input.strip():
                 # ユーザーが入力したslugで再検証
                 new_slug = user_input.strip()
                 is_valid_slug, validation_message = validate_slug(new_slug)
                 if not is_valid_slug:
                     print(f"エラー: 入力されたSlugも無効です: {validation_message}")
                     sys.exit(1)
                 print(f"Slugを '{new_slug}' に変更します。")
                 slug = new_slug
            elif user_input.lower() != 'y': # yでもなく、有効なslug入力でもない場合
                 print("無効な入力です。処理を中断します。")
                 sys.exit(1)
            # 'y' の場合は警告のまま続行

        # categoriesとtagsがリストであることを確認（文字列で返ってくる場合などに対処）
        if not isinstance(categories, list):
            print(f"警告: categories がリスト形式ではありません ({type(categories)})。空リストとして扱います。")
            categories = []
        if not isinstance(tags, list):
            print(f"警告: tags がリスト形式ではありません ({type(tags)})。空リストとして扱います。")
            tags = []

    except KeyError as e:
        print(f"エラー: LLMのレスポンスに必要なキー '{e}' が見つかりません。")
        print("受信データ:", article_data)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: 取得データの処理中に予期せぬエラーが発生しました: {e}")
        sys.exit(1)

    # 記事用フォルダのパスを作成
    article_folder_path = os.path.join(CONTENT_POST_DIR, slug)

    # フォルダ作成
    try:
        os.makedirs(article_folder_path, exist_ok=True)
        print(f"フォルダを作成/確認しました: {article_folder_path}")
    except OSError as e:
        print(f"エラー: フォルダの作成に失敗しました: {article_folder_path}")
        print(e)
        sys.exit(1)

    # 出力ファイルのパス
    output_filepath = os.path.join(article_folder_path, "index.ja.md")

    # ファイル存在チェックと上書き確認
    if os.path.exists(output_filepath):
        print(f"警告: ファイルは既に存在します: {output_filepath}")
        user_input = input("上書きしますか？ (y/N): ").lower()
        if user_input != 'y':
            print("処理を中断しました。")
            sys.exit(0)
        else:
            print("既存のファイルを上書きします。")

    # フロントマターデータ作成
    current_date_str = get_current_jst_time()
    frontmatter_data = {
        'title': title,
        'description': description,
        'slug': slug,
        'date': current_date_str,
        'image': image_suggestion if image_suggestion else f"{slug}_thumbnail.webp", # 画像提案がなければslugベースで仮作成
        'categories': categories,
        'tags': tags,
    }

    # フロントマター文字列を生成
    frontmatter_str = format_frontmatter(frontmatter_data)
    if not frontmatter_str:
        print("エラー: フロントマターの生成に失敗しました。")
        sys.exit(1)

    # 完全なファイル内容を作成 (フロントマターと本文の間に空行を入れる)
    full_content = f"{frontmatter_str}\n\n{generated_body.strip()}"

    # ファイルに保存
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        print(f"記事のたたき台を保存しました: {output_filepath}")
        print("\n--- 生成されたファイル情報 ---")
        print(f"  タイトル: {title}")
        print(f"  Slug: {slug}")
        print(f"  説明: {description}")
        print(f"  カテゴリ: {categories}")
        print(f"  タグ: {tags}")
        print(f"  画像提案: {frontmatter_data['image']}") # 実際に使用したファイル名を表示
        print("--------------------------")

    except IOError as e:
        print(f"エラー: ファイルへの書き込みに失敗しました: {output_filepath}")
        print(e)
        sys.exit(1)
    except Exception as e:
         print(f"エラー: ファイル保存中に予期せぬエラーが発生しました: {e}")
         sys.exit(1)

    # 少し待機 (API連続使用を避ける意味合いも)
    print(f"{SLEEP_TIME}秒待機します...")
    time.sleep(SLEEP_TIME)

    print("-" * 30)
    print("スクリプトの処理が正常に完了しました。")
    print(f"生成されたファイル: {output_filepath}")
    print("\n**重要:**")
    print("生成された内容はたたき台です。必ず以下の点を確認・修正してください:")
    print("  - フロントマターの内容 (特にカテゴリ、タグ、画像ファイル名)")
    print("  - 本文の構成、表現、情報の正確性")
    print(f"  - アイキャッチ画像 '{frontmatter_data['image']}' を用意し、'{article_folder_path}' フォルダに配置してください。")

if __name__ == "__main__":
    # スクリプト実行前に内容確認
    print("\n以下の内容で記事のたたき台を自動生成します:")
    print("--- 記事の核となる内容 (最初の300文字程度) ---")
    print(ARTICLE_CORE_CONTENT.strip()[:300] + "...")
    print("---------------------------------------------")
    print(f"使用モデル: {MODEL_NAME}")
    print("-" * 30)

    confirm = input("よろしいですか？ (y/N): ").lower()
    if confirm == 'y':
        main()
    else:
        print("処理をキャンセルしました。スクリプト内の `ARTICLE_CORE_CONTENT` を確認・編集してください。")