---
title: PygameゲームをWeb公開！pygbagとHugoでブログに簡単埋め込み (WebAssembly)
description: Pygameで作ったゲームをWebで動かしたいですか？pygbagでWebAssemblyに変換し、Hugoブログに埋め込む手順を解説。iframe用ショートコードも紹介し、プラグイン不要でゲームを公開できます。
slug: publish-pygame-web-hugo-pygbag
date: '2025-03-30 05:18:12+09:00'
image: publish-pygame-web-hugo-pygbag.webp
categories: [プログラミング, ゲーム]
tags: [Python, Hugo]
---

## はじめに

こんにちは！

Pygameで作った自作ゲーム、せっかくならWebで公開して、たくさんの人に遊んでもらいたいですよね。私もそう思います！

この記事では、Pythonのゲームライブラリ Pygame で作ったゲームを、Webブラウザで誰でも簡単にプレイできるように公開する方法を、一緒に見ていきたいと思います。できるだけ分かりやすく解説してみますね。

この記事で分かること:

1.  `pygbag` というツールで、Pygameゲームを WebAssembly (WASM) を使ってWeb向けに変換（ビルド）する方法。これが結構便利なんです。
2.  Hugo という静的サイトジェネレーターで作ったブログに、変換したゲームを埋め込んで公開する手順。
3.  ゲームを記事に簡単に埋め込むための、Hugoショートコードの作り方。これも作っておくと後が楽ちんですよ。

この手順なら、特別なサーバー設定もいらず、ブラウザだけで遊んでもらえるようになります。嬉しいですね！あなたの作ったゲームを世界中の人に遊んでもらえるようになるかもしれません！

## 出来上がったゲーム

それで、実際にこの方法で作ってみたのが、こちらのゲームです！
（ただ眺めるゲームです。）

{{< game-iframe src="/game/the-labyrinth-of-gaze/build/web/index.html" aspect-ratio="75%" >}}

## PygameゲームをWeb向けにビルドする: `pygbag` という便利なツールを使ってみます

`pygbag` は、PygameゲームをWebブラウザで直接動かせるようにパッケージ化してくれる、本当に便利なツールだと思います。これを使って、まずはゲームをWeb用に変換してみましょう。

### 1. まず、`uv` でプロジェクトの準備をしましょう

ここでは `uv` という、最近注目されているPythonのパッケージ管理ツールを使ってみます。もし `uv` がなければ、まずインストールしましょう。（もし `pip` など他のツールを使っている方は、そちらで大丈夫ですよ）

※ uv のインストール (まだの場合、このコマンドはWindows用ですね)
```batch
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

次に、`uv init` でゲームプロジェクト用のフォルダ作成と初期化をします。
`the-labyrinth-of-gaze` は、今回例として使うゲームの名前なので、ここはご自身のプロジェクト名に置き換えてくださいね。

※ uv でプロジェクトを初期化
```batch
uv init the-labyrinth-of-gaze
cd the-labyrinth-of-gaze
```

次に、必要なライブラリ `pygbag` と `pygame` をインストールします。`uv` だとこんな感じです。

```batch
uv add pygbag pygame
```

*（もし `uv` を使わない場合は、`pip install pygbag pygame` のような感じで、お手元の環境に合わせてインストールしてくださいね）*

### 2. いよいよゲームをビルドします

`uv init` で自動で作られた `main.py` か、ご自身のゲームのメインとなるスクリプトファイルに、Pygameのゲームコードを書きます。

この記事の例で使ったゲームコードは、最後に添付します。

準備ができたら、以下のコマンドでゲームをWeb向けにビルドを実行します。
`main.py` のところは、あなたのゲームのメインスクリプトファイル名に変えてください。

```batch
uv run pygbag --build .\main.py
```

このコマンドが成功すると、今いるフォルダ（カレントディレクトリ）に `build/web` というフォルダができて、その中にWebブラウザでゲームを動かすためのファイル (`index.html` や `the-labyrinth-of-gaze.apk` など) が入っているはずです。

ビルドされたファイルの例はこんな感じですね: [/game/the-labyrinth-of-gaze/build/web/index.html](/game/the-labyrinth-of-gaze/build/web/index.html)

## Hugoブログにゲームを埋め込む

次に、ビルドしたゲームをHugoブログに組み込んでいきましょう。
ここでは `hugo-theme-stack` というテーマを例にしますが、基本的な考え方は他のHugoテーマでも同じだと思います。

### 1. ゲームファイルを置く場所についてです

Hugoには `static` という便利なフォルダがあって、ここに入れたファイルやフォルダは、サイトを作るときにそのままルート（Webサイトの一番上の階層）にコピーしてくれるんです。ここに、さっき `pygbag` で作ったゲームファイルを置いていきます。

配置手順 (例: ゲーム名 `the-labyrinth-of-gaze` の場合):

1.  Hugoプロジェクトのルートにある `static` フォルダの中に `game` というフォルダを作ります（もしなければ作ってくださいね）。
2.  `static/game/` の中に、さらにゲーム用のフォルダを作ります (例: `the-labyrinth-of-gaze`)。
3.  先ほど `pygbag` で生成された `build/web` フォルダの中身を、今作った `static/game/the-labyrinth-of-gaze/` フォルダの中にコピーします。
    *   注意: ここ、大事なポイントです！ `build/web` フォルダごとコピーするのではなく、その中のファイル群 (`index.html`, `the-labyrinth-of-gaze.apk` など) をコピーしてくださいね。

配置後のフォルダ構成は、こんな感じになると思います。

```
(あなたのHugoプロジェクトフォルダ)/
└── static/
    └── game/
        └── the-labyrinth-of-gaze/  <-- このフォルダにビルド結果をコピー
            └── build/
                └── web/
                    ├── index.html
                    ├── the-labyrinth-of-gaze.apk
                    └── (その他必要なファイル) ...
```

ポイント: こうしておくと、後でWebサイトから `/game/the-labyrinth-of-gaze/build/web/index.html` みたいなURLでゲームの `index.html` にアクセスできるようになります。

### 2. 毎回 `<iframe>` を書くのは大変なので、Hugoのショートコードを作りましょう

Hugoには ショートコード という便利な機能があるので、これを使って楽にゲームを埋め込めるようにしてみます。これを作っておくと、後々すごく楽ですよ。

Hugoプロジェクトの `layouts/shortcodes/` フォルダの中に `game-iframe.html` という名前で新しいファイルを作って、以下のコードを貼り付けてみてください。

```html
{{/* layouts/shortcodes/game-iframe.html */}}
{{/* ゲームのURLを 'src' で受け取る */}}
{{ $src := .Get "src" }}
{{/* アスペクト比を 'aspect-ratio' で受け取る (指定なければ 75% = 4:3) */}}
{{ $aspectRatio := .Get "aspect-ratio" | default "75%" }}

{{/* レスポンシブ対応のiframe埋め込みスタイル */}}
<div style="position: relative; padding-bottom: {{ $aspectRatio }}; height: 0; overflow: hidden; max-width: 100%; height: auto;">
  <iframe
    src="{{ $src }}"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 1px solid #ccc;"
    title="Embedded Game"
    sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-fullscreen"
    loading="lazy"></iframe>
</div>
```

このショートコードが何をしているかというと…:

*   `src` パラメータで、埋め込みたいゲームのURLを受け取ります。
*   `aspect-ratio` パラメータで、ゲーム画面の見た目の比率（アスペクト比）を指定できるようにします (例: `75%` は 4:3、`56.25%` は 16:9)。もし指定しなかったら、デフォルトで `75%` (4:3っぽい感じ) になるようにしています。
*   指定されたURLのコンテンツを `<iframe>` で埋め込むんですが、
*   CSSを使って、画面サイズが変わっても形が崩れないように（レスポンシブ対応ってやつですね）調整しています。
*   `sandbox` 属性で、iframeの中身がちょっと安全に動くように制限をかけています。
*   `loading="lazy"` を付けて、iframeが表示される近くに来るまで読み込みを遅らせることで、ページの表示が少し速くなるように、ちょっとした工夫をしています。

### 3. さあ、準備ができました！記事で使ってみましょう

これで準備完了です！ゲームを紹介したい記事のMarkdownファイルを開いて、さっき作ったショートコードを使ってみましょう。

例えば、`content/posts/my-pygame-game.md` のような記事ファイルを作って、本文中にこんなふうに書きます。

```markdown
---
title: "自作Pygameゲーム「眺める迷路」を公開！" # 記事のタイトル
date: 2025-03-28T00:00:00+09:00
description: "Pygameとpygbagで作った迷路ゲームを公開しました。ブラウザで気軽に遊べます！" # 記事の説明
slug: the-labyrinth-of-gaze-game # 記事のスラッグ（URLの一部）
image: the-labyrinth-of-gaze.webp # アイキャッチ画像
categories: ["ゲーム"] # カテゴリ
tags: ["Pygame", "自作ゲーム", "パズル"] # タグ
draft: false
---

Pygameで作った「眺める迷路」ゲームをWebで公開してみました！
`pygbag` を使うと、こんな風にブログに埋め込めるんですね。便利！

ぜひブラウザで気軽に遊んでみてください。

{{</* game-iframe src="/game/the-labyrinth-of-gaze/build/web/index.html" aspect-ratio="75%" */>}}

操作方法:

*   （ここにゲームの操作方法などを具体的に書いてくださいね）
*   例: 矢印キーで移動、スペースキーでジャンプ など

ゲームの説明:

（ここにゲームのルールや目的、見どころなどを書くと良いと思います）

楽しんでいただけたら嬉しいです！
```

ここでのポイントは…:

*   `{{</* ... */>}}` の中に、先ほど作成したショートコード名 `game-iframe` を書きます。
*   `src` パラメータには、さっき `static` フォルダに置いたゲームの `index.html` への Webサイト上での絶対パス (`/` から始まるパス) を指定します。
    *   例: `static/game/the-labyrinth-of-gaze/build/web/index.html` に置いた場合は、`/game/the-labyrinth-of-gaze/build/web/index.html` と書きます。
    *   重要: ここ、間違えやすいので注意です！ あなたのゲームの配置場所に合わせて、このパスを正しく書いてくださいね。
*   `aspect-ratio` は、あなたのゲーム画面に合わせて調整すると、見た目がいい感じになると思います (例: 16:9 なら `56.25%` とか)。
*   ショートコードの下には、もちろん操作方法とかゲームの説明とか、自由に書けますよ。

ここまでできたら、あとは `hugo` コマンドでサイトをビルドして公開すれば、記事の中にゲームが埋め込まれて表示されるはずです！

## まとめ

今回は、`pygbag` という便利なツールを使って Pygame ゲームを WebAssembly (WASM) に変換し、それを Hugo ブログの `static` フォルダに配置して、さらに iframe 埋め込み用の Hugo ショートコード を作って記事内に簡単に表示する、という手順を見てきました。

この方法のいいところは、個人的にはこんな点かなと思います:

*   特別なサーバー設定がいらない！ 静的なファイルだけでゲームを公開できるのは手軽でいいですよね。
*   ブログ記事の中にインタラクティブなゲームを簡単に追加できるって、なんだかワクワクしませんか？
*   あなたの作った Pygame ゲームをより多くの人に遊んでもらえるチャンスが広がります！
*   見てくれる人も、ブラウザのプラグインとか何もなしで、すぐに遊べるのが嬉しいですね。

もしあなたがPygameでゲームを作っていて、「Webで公開してみたいな」と思っていたら、ぜひこの手順を参考にして、チャレンジしてみてはいかがでしょうか。

最後まで読んでくださって、ありがとうございました！

## ソースコード

```python
# Pygameを使ったA*アルゴリズムによる迷路探索アニメーション (自動進行＆エフェクト追加・修正版)
import pygame
import random
import heapq
import math
import time # dt計算のために追加 (なくてもclock.tickでOK)

# --- 定数 ---
# グリッド設定
GRID_WIDTH = 31
GRID_HEIGHT = 25
CELL_SIZE = 15
MARGIN = 1

# ウィンドウサイズ
WINDOW_WIDTH = GRID_WIDTH * (CELL_SIZE + MARGIN) + MARGIN
WINDOW_HEIGHT = GRID_HEIGHT * (CELL_SIZE + MARGIN) + MARGIN

# 色 (RGB) - モダンな配色に更新
WHITE = (245, 245, 245)
BLACK = (20, 20, 30)
GREY = (180, 180, 180)
GREEN = (76, 187, 23)
RED = (235, 64, 52)
BLUE = (66, 135, 245)
YELLOW = (250, 204, 21)
CYAN = (28, 186, 210)
ORANGE = (255, 126, 28)
LIGHT_ORANGE = (255, 183, 77)  # 点滅用
PATH_HIGHLIGHT = (130, 210, 240)  # ライトブルー (経路表示アニメ用)
PATH_HIGHLIGHT_PULSE = (180, 230, 250)  # パルスエフェクト用
GOAL_FLASH = (255, 255, 255)  # ゴール到達時エフェクト用
HOVER_COLOR = (220, 220, 220)  # ホバーエフェクト用
PURPLE = (180, 120, 240)  # 新しい色
PINK = (255, 105, 180)  # 新しい色

# アニメーション速度 (Frame Per Second)
FPS = 60
# 自動リセットまでの待機時間 (秒)
RESET_DELAY_SECONDS = 2.0
# 経路ハイライトアニメーションの速度 (1フレームあたりに進むマス数、小さいほど遅い)
PATH_HIGHLIGHT_SPEED = 0.3


# --- ヘルパー関数 (変更なし) ---
def heuristic(a, b):
    (r1, c1) = a
    (r2, c2) = b
    return abs(r1 - r2) + abs(c1 - c2)


def get_valid_neighbors(node, grid):
    neighbors = []
    row, col = node
    rows = len(grid)
    cols = len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def generate_maze(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]
    start_r, start_c = random.randrange(1, height, 2), random.randrange(1, width, 2)
    grid[start_r][start_c] = 0
    stack = [(start_r, start_c)]
    visited = {(start_r, start_c)}

    while stack:
        cr, cc = stack[-1]
        neighbors = []
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = cr + dr, cc + dc
            if 0 < nr < height - 1 and 0 < nc < width - 1 and (nr, nc) not in visited:
                neighbors.append((nr, nc))

        if neighbors:
            nr, nc = random.choice(neighbors)
            grid[(cr + nr) // 2][(cc + nc) // 2] = 0
            grid[nr][nc] = 0
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()

    passages = [(r, c) for r in range(height) for c in range(width) if grid[r][c] == 0]
    if len(passages) < 2:
        start_node = (1, 1) if height > 1 and width > 1 else (0, 0)
        end_node = (height - 2, width - 2) if height > 2 and width > 2 else start_node
        if grid[start_node[0]][start_node[1]] == 1:
            grid[start_node[0]][start_node[1]] = 0
        if grid[end_node[0]][end_node[1]] == 1:
            grid[end_node[0]][end_node[1]] = 0
    else:
        start_node = random.choice(passages)
        end_node = random.choice(passages)
        while end_node == start_node:
            end_node = random.choice(passages)

    return grid, start_node, end_node

# パーティクルクラス定義 - より多様なエフェクト対応に改良
class Particle:
    def __init__(self, x, y, color, particle_type="normal"):
        self.x = x
        self.y = y
        self.base_color = color # 元の色を保持
        self.color = color
        self.particle_type = particle_type
        self.size = (
            random.randint(2, 6)
            if particle_type == "normal"
            else random.randint(3, 8)
        )
        self.speed = (
            random.uniform(1, 5) * 50 # スピード調整 (dtベース)
            if particle_type == "normal"
            else random.uniform(0.5, 3) * 50 # スピード調整 (dtベース)
        )
        self.angle = random.uniform(0, math.pi * 2)
        self.lifespan = (
            random.uniform(0.5, 1.5)
            if particle_type == "normal"
            else random.uniform(1.0, 2.5)
        )
        self.age = 0
        self.pulse_rate = random.uniform(3.0, 6.0)  # パルスエフェクト用
        self.original_size = self.size  # サイズ変動用
        self.fade_in_duration = 0.3 # フェードイン時間
        self.fade_out_start_ratio = 0.7 # 寿命の何割からフェードアウト開始か

        # 星型パーティクル用の頂点数
        self.vertices = random.randint(4, 6) if particle_type == "star" else 0

        # 軌跡パーティクル用
        self.trail = []
        self.trail_length = 5 if particle_type == "trail" else 0

        # 波紋エフェクト用
        if particle_type == "ripple":
            self.size = 1
            self.max_size = random.randint(15, 25)
            self.expand_speed = random.uniform(0.8, 1.2) * 30 # スピード調整 (dtベース)
            self.lifespan = random.uniform(1.0, 1.5)
            self.speed = 0 # 波紋は移動しない

    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        self.age += dt

        # パーティクルタイプに応じた更新処理
        size_decay_rate = self.original_size / (self.lifespan * (1.0 - self.fade_out_start_ratio)) if self.lifespan > 0 else 1

        if self.particle_type == "normal":
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                 self.size = max(0, self.size - size_decay_rate * dt)
        elif self.particle_type == "pulse":
            pulse = math.sin(self.age * self.pulse_rate) * 0.5 + 0.5
            current_size_factor = 1.0
            if self.age >= self.lifespan * self.fade_out_start_ratio:
                current_size_factor = max(0, 1 - (self.age - self.lifespan * self.fade_out_start_ratio) / (self.lifespan * (1.0 - self.fade_out_start_ratio)))
            self.size = self.original_size * (0.5 + pulse * 0.5) * current_size_factor
        elif self.particle_type == "fade_in":
            if self.age < self.fade_in_duration:
                self.size = self.original_size * (self.age / self.fade_in_duration)
            elif self.age >= self.lifespan * self.fade_out_start_ratio:
                 fade_out_duration = self.lifespan * (1.0 - self.fade_out_start_ratio)
                 self.size = max(0, self.original_size * (1 - (self.age - self.lifespan * self.fade_out_start_ratio) / fade_out_duration))
            else:
                self.size = self.original_size # フェードイン後、フェードアウト前は最大サイズ
        elif self.particle_type == "trail":
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)
            if self.age >= self.lifespan * self.fade_out_start_ratio:
                self.size = max(0, self.size - size_decay_rate * dt * 0.5) # Trailは少しゆっくり消える
        elif self.particle_type == "ripple":
            self.size = min(self.size + self.expand_speed * dt, self.max_size)
        elif self.particle_type == "star":
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                 self.size = max(0, self.size - size_decay_rate * dt)
        else: # default or rainbow etc.
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                 self.size = max(0, self.size - size_decay_rate * dt)

        # 色の変化（時間経過で色相が変化 - rainbowタイプ）
        if self.particle_type == "rainbow":
            hue_shift = (self.age * 100) % 360
            # HSV -> RGB変換 (簡易版)
            r_val, g_val, b_val = 0, 0, 0
            i = int(hue_shift / 60) % 6
            f = hue_shift / 60 - i
            v = 1.0 # 明度
            s = 1.0 # 彩度
            p = v * (1 - s)
            q = v * (1 - f * s)
            t = v * (1 - (1 - f) * s)
            if i == 0: r_val, g_val, b_val = v, t, p
            elif i == 1: r_val, g_val, b_val = q, v, p
            elif i == 2: r_val, g_val, b_val = p, v, t
            elif i == 3: r_val, g_val, b_val = p, q, v
            elif i == 4: r_val, g_val, b_val = t, p, v
            elif i == 5: r_val, g_val, b_val = v, p, q
            self.color = (int(r_val*255), int(g_val*255), int(b_val*255))


    def draw(self, surface):
        if self.size <= 0: # サイズが0以下なら描画しない
            return

        # フェードイン/アウト効果の透明度計算
        alpha = 255
        if self.particle_type == "ripple":
            # 波紋エフェクトの透明度計算 (徐々に薄くなる)
            progress = self.age / self.lifespan if self.lifespan > 0 else 1
            alpha = max(0, min(255, int(255 * (1 - progress) * 0.8))) # 終盤はより透明に
        elif self.particle_type == "fade_in":
            if self.age < self.fade_in_duration:
                alpha = int(255 * (self.age / self.fade_in_duration))
            elif self.age >= self.lifespan * self.fade_out_start_ratio:
                fade_out_duration = self.lifespan * (1.0 - self.fade_out_start_ratio)
                if fade_out_duration > 0:
                    alpha = max(0, min(255, int(255 * (1 - (self.age - self.lifespan * self.fade_out_start_ratio) / fade_out_duration))))
                else:
                    alpha = 0 # 念のため
            else:
                alpha = 255
        else: # Normal, Pulse, Star, Trail, Rainbow etc.
            # 共通のフェードアウト処理
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                fade_out_duration = self.lifespan * (1.0 - self.fade_out_start_ratio)
                if fade_out_duration > 0:
                    alpha = max(0, min(255, int(255 * (1 - (self.age - self.lifespan * self.fade_out_start_ratio) / fade_out_duration))))
                else:
                    alpha = 0
             else:
                alpha = 255

        # 色の検証と設定
        try:
            current_color = self.color if self.particle_type == "rainbow" else self.base_color
            if isinstance(current_color, tuple) and len(current_color) == 3:
                r = max(0, min(255, int(current_color[0])))
                g = max(0, min(255, int(current_color[1])))
                b = max(0, min(255, int(current_color[2])))
                final_color = (r, g, b, alpha)
            else:
                final_color = (255, 255, 255, alpha)  # デフォルト色

            # パーティクルタイプに応じた描画
            if self.particle_type == "ripple":
                # 波紋エフェクト (輪郭を描画)
                line_width = max(1, int(self.max_size / 15 * (1 - self.age / self.lifespan))) # 徐々に細くなる輪郭
                if self.size >= 1: # 最小半径1以上
                    pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size), width=line_width)
            elif self.particle_type == "star" and self.vertices > 0:
                # 星型パーティクル
                points = []
                outer_radius = self.size
                inner_radius = self.size * 0.4
                for i in range(self.vertices * 2):
                    angle = math.pi / self.vertices * i - math.pi / 2 # 頂点が上に来るように調整
                    radius = outer_radius if i % 2 == 0 else inner_radius
                    x_p = self.x + math.cos(angle) * radius
                    y_p = self.y + math.sin(angle) * radius
                    points.append((x_p, y_p))
                if len(points) >= 3:  # 少なくとも3点必要
                    pygame.draw.polygon(surface, final_color, points)
            elif self.particle_type == "trail" and len(self.trail) > 1:
                # 軌跡パーティクル
                for i in range(len(self.trail) - 1):
                    start_pos = self.trail[i]
                    end_pos = self.trail[i + 1]
                    # 軌跡のアルファと太さを調整
                    trail_alpha = alpha * ((i + 1) / len(self.trail))**2 # 後ろほど薄く
                    trail_width = max(1, int(self.size * ((i + 1) / len(self.trail))))
                    trail_color_tuple = (final_color[0], final_color[1], final_color[2], int(trail_alpha))
                    pygame.draw.line(surface, trail_color_tuple, start_pos, end_pos, trail_width)
                # 先端の円も描画
                pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size))
            else:
                # 通常の円形パーティクル (Normal, Pulse, Fade_in, Rainbow)
                pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size))

        except (ValueError, TypeError) as e:
            # エラーが発生した場合はデフォルト色を使用
            print(f"Error drawing particle: {e}, color={self.color}, alpha={alpha}, size={self.size}")
            try:
                safe_color = (255, 255, 255, alpha)
                if self.size >= 1:
                    pygame.draw.circle(surface, safe_color, (int(self.x), int(self.y)), int(max(1, self.size))) # 最小サイズ1を保証
            except Exception as final_e:
                 print(f"Final fallback drawing failed: {final_e}")


# --- Pygame初期化 ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("A* Maze Solver Animation (Auto-Repeat, ESC: Quit)")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# --- 状態変数 ---
grid = []
start_node = None
end_node = None
open_set_heap = []
open_set_map = {}
closed_set = set()
came_from = {}
g_score = {}
path = []
current_node = None
solving = False
maze_generated = False
message = ""
particles = []  # パーティクル用リスト (ripplesもここに統合)
# ripples = [] # 不要になったので削除
node_pulses = []  # ノード探索時のパルスエフェクト用 (現状未使用かも？)

# --- 自動リセット用変数 ---
reset_timer = 0  # 待機フレームカウンタ
RESET_DELAY_FRAMES = int(RESET_DELAY_SECONDS * FPS)  # 秒をフレーム数に変換
start_reset_timer_after_highlight = False  # ハイライト完了後にタイマーを開始するフラグ

# --- 経路ハイライトアニメーション用変数 ---
path_highlight_index = 0.0  # floatでゆっくり進める
highlighting_path = False

# --- ゴール到達エフェクト用 ---
goal_reached_flash = False  # ゴール到達直後のフレームか

# --- メインループ ---
running = True
frame_count = 0  # 点滅アニメーション用
hover_cell = None  # ホバー中のセル

while running:
    # --- デルタタイム計算 ---
    dt = clock.tick(FPS) / 1000.0 # 秒単位のデルタタイム (0除算を避ける)
    if dt == 0: dt = 1 / FPS # 最小時間ステップを保証

    # --- イベント処理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # マウス座標からホバー中のセルを取得
    mouse_pos = pygame.mouse.get_pos()
    mouse_col = mouse_pos[0] // (CELL_SIZE + MARGIN)
    mouse_row = mouse_pos[1] // (CELL_SIZE + MARGIN)
    if 0 <= mouse_row < GRID_HEIGHT and 0 <= mouse_col < GRID_WIDTH:
        hover_cell = (mouse_row, mouse_col)
    else:
        hover_cell = None

    # --- 状態更新 ---
    if not maze_generated:
        # 待機タイマーをリセット
        reset_timer = 0
        start_reset_timer_after_highlight = False
        highlighting_path = False
        path_highlight_index = 0.0
        goal_reached_flash = False
        hover_cell = None
        particles = [] # 既存のパーティクルをクリア

        message = "Generating new maze..."
        screen.fill(BLACK)
        msg_render = font.render(message, True, WHITE)
        screen.blit(msg_render, (10, WINDOW_HEIGHT // 2 - 10))
        pygame.display.flip()

        grid, start_node, end_node = generate_maze(GRID_WIDTH, GRID_HEIGHT)

        open_set_heap = []
        open_set_map = {}
        closed_set = set()
        came_from = {}
        path = []
        current_node = None
        g_score = {
            (r, c): float("inf") for r in range(GRID_HEIGHT) for c in range(GRID_WIDTH)
        }
        if start_node: # start_nodeがNoneでないことを確認
            g_score[start_node] = 0
            h_start = heuristic(start_node, end_node) if end_node else 0
            f_start = g_score[start_node] + h_start
            heapq.heappush(open_set_heap, (f_start, h_start, start_node))
            open_set_map[start_node] = (f_start, h_start)

        maze_generated = True
        solving = True if start_node and end_node else False # 開始/終了ノードがない場合は解かない
        message = "Solving..." if solving else "Maze generated (No start/end?)"


    # --- A*アルゴリズムのステップ実行 ---
    if solving and open_set_heap:
        current_f, current_h, current_node_popped = heapq.heappop(open_set_heap)

        # open_set_map から削除されたか、より良い経路が後で見つかった場合はスキップ
        if current_node_popped not in open_set_map or open_set_map[current_node_popped] > (current_f, current_h):
             pass # 無視して次のループへ
        else:
            # 処理するので open_set_map から削除 (再追加される可能性はある)
            # heapqからpopされた時点で処理対象とするため、delは不要かも。重複チェックは上記ifで行う。
            # del open_set_map[current_node_popped] # ここでの削除は不要かも
            current_node = current_node_popped

            if current_node == end_node:
                path = reconstruct_path(came_from, current_node)
                solving = False
                message = "Goal Reached! Highlighting path..."
                current_node = None
                highlighting_path = True
                path_highlight_index = 0.0
                goal_reached_flash = True # エフェクト生成フラグON
                start_reset_timer_after_highlight = True
            else:
                closed_set.add(current_node)
                # open_set_map からは確実に削除（closedに入ったので）
                if current_node in open_set_map:
                    del open_set_map[current_node]


                # 探索中のノードに波紋エフェクトを追加
                node_x = (current_node[1] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
                node_y = (current_node[0] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2

                # 波紋エフェクトを生成 (Particleクラスを使用)
                particles.append(Particle(node_x, node_y, YELLOW, "ripple")) # 色をYELLOWに変更

                # 小さなパーティクルを少量生成 (探索時に)
                if random.random() < 0.1: # 確率を少し下げる
                    for _ in range(1): # 数を減らす
                        color = random.choice([YELLOW, ORANGE]) # 色を探索色に合わせる
                        particles.append(Particle(node_x, node_y, color, "fade_in"))

                for neighbor in get_valid_neighbors(current_node, grid):
                    if neighbor in closed_set:
                        continue

                    tentative_g_score = g_score[current_node] + 1

                    # この経路が既存の経路より良くない、またはopen setに既により良い経路がある場合は無視
                    # 注意: open_set_mapには (f, h) が格納されている
                    neighbor_in_open = open_set_map.get(neighbor)
                    if neighbor_in_open and tentative_g_score >= g_score.get(neighbor, float('inf')):
                         continue

                    # より良い経路が見つかった場合、または初めて訪れる場合
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    h_neighbor = heuristic(neighbor, end_node)
                    f_neighbor = tentative_g_score + h_neighbor

                    # open_setになければ追加、あれば更新(heapqは更新を直接サポートしないので、新しい要素を追加)
                    heapq.heappush(open_set_heap, (f_neighbor, h_neighbor, neighbor))
                    open_set_map[neighbor] = (f_neighbor, h_neighbor) # f, h を保存


    elif solving and not open_set_heap:
        solving = False
        message = f"No path found! Resetting in {RESET_DELAY_SECONDS:.1f}s..."
        current_node = None
        reset_timer = RESET_DELAY_FRAMES  # 探索失敗時はすぐにタイマー開始

    # --- 経路ハイライト処理 ---
    if highlighting_path and path:
        if path_highlight_index < len(path):
            path_highlight_index += PATH_HIGHLIGHT_SPEED * FPS * dt # dtを使って速度を調整
            # 完了した瞬間の処理
            if path_highlight_index >= len(path):
                path_highlight_index = len(path)
                if start_reset_timer_after_highlight:
                    reset_timer = RESET_DELAY_FRAMES
                    message = f"Path complete! Resetting in {RESET_DELAY_SECONDS:.1f}s..."
                    start_reset_timer_after_highlight = False

    # --- 自動リセットタイマー処理 ---
    if reset_timer > 0:
        reset_timer -= 1 # フレームベースでカウントダウン
        remaining_time = reset_timer / FPS # 秒に変換して表示
        if not solving and not path:
            message = f"No path found! Resetting in {remaining_time:.1f}s..."
        elif not solving and path and path_highlight_index >= len(path):
            message = f"Path complete! Resetting in {remaining_time:.1f}s..."

        if reset_timer <= 0:
            maze_generated = False

    # --- 描画処理 ---
    # グラデーション背景
    for y in range(WINDOW_HEIGHT):
        time_factor = math.sin(frame_count * 0.005) * 0.2
        r_base = 30 + int(10 * time_factor)
        g_base = 40 + int(15 * time_factor)
        b_base = 60 + int(20 * time_factor)
        gradient_factor = math.sin(math.pi * y / WINDOW_HEIGHT)
        r = int(r_base + (50 - r_base) * gradient_factor) # 少し暗めに調整
        g = int(g_base + (70 - g_base) * gradient_factor) # 少し暗めに調整
        b = int(b_base + (90 - b_base) * gradient_factor) # 少し暗めに調整
        pygame.draw.line(screen, (max(0,r), max(0,g), max(0,b)), (0, y), (WINDOW_WIDTH, y))

    # セルの質感向上（影と光沢）- この部分は元のままでも良い
    shadow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(
                (MARGIN + CELL_SIZE) * col + MARGIN,
                (MARGIN + CELL_SIZE) * row + MARGIN,
                CELL_SIZE,
                CELL_SIZE,
            )
            if grid[row][col] == 0: # 通路
                pygame.draw.rect(shadow_surface, (0, 0, 0, 30), rect.inflate(1, 1), border_radius=3) # 少し薄い影
                light_rect = rect.inflate(-3, -3).move(-1, -1)
                pygame.draw.rect(shadow_surface, (255, 255, 255, 50), light_rect, border_radius=2) # 光沢も少し控えめ
            else: # 壁
                pygame.draw.rect(shadow_surface, (0, 0, 0, 20), rect.inflate(1, 1), border_radius=2)
                pygame.draw.rect(shadow_surface, (0, 0, 0, 30), rect.inflate(-2, -2), border_radius=1, width=1) # 内側の影

    screen.blit(shadow_surface, (0, 0))


    # ゴール到達時のパーティクル生成
    if goal_reached_flash:
        goal_x = (end_node[1] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
        goal_y = (end_node[0] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2

        # 多様なパーティクルタイプを生成
        for _ in range(40): # 通常パーティクル増量
            color = random.choice([RED, YELLOW, ORANGE, BLUE, GREEN, PURPLE, PINK, WHITE])
            particles.append(Particle(goal_x, goal_y, color, "normal"))
        for _ in range(15): # 星型パーティクル増量
            color = random.choice([YELLOW, WHITE, ORANGE, CYAN])
            particles.append(Particle(goal_x, goal_y, color, "star"))
        for _ in range(10): # パルスエフェクト
            color = random.choice([CYAN, PURPLE, PINK, BLUE])
            particles.append(Particle(goal_x, goal_y, color, "pulse"))
        for _ in range(8): # 軌跡パーティクル
            color = random.choice([BLUE, CYAN, WHITE, GREEN])
            particles.append(Particle(goal_x, goal_y, color, "trail"))
        for _ in range(10): # 虹色パーティクル
            particles.append(Particle(goal_x, goal_y, WHITE, "rainbow")) # 初期色は白でOK
        for _ in range(6): # 波紋エフェクトもParticleとして生成
            color = random.choice([WHITE, CYAN, BLUE, YELLOW]) # 波紋の色
            particles.append(Particle(goal_x, goal_y, color, "ripple")) # rippleタイプで生成

        goal_reached_flash = False # ★★★ パーティクル生成直後にフラグをリセット ★★★

    # セル描画ループ
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = WHITE
            if grid[row][col] == 1:
                color = BLACK

            node = (row, col)
            is_path_node = False # 経路ハイライト対象かどうかのフラグ

            # --- セルの状態に応じた色設定 ---
            if node in closed_set:
                # closedリストの色 (探索済み) - 少し暗めのCYAN
                 color = (20, 140, 160)
            # open_set_mapにあるノード (探索候補) - 少し暗めのYELLOW
            # heapqに同じノードが複数あっても、open_set_mapには最新の(f,h)が入っているはず
            if node in open_set_map:
                 color = (200, 160, 10) # 少し暗めのYELLOW

            # --- 経路ハイライト ---
            if highlighting_path and path:
                current_path_segment_index = int(path_highlight_index)
                if node in path[:current_path_segment_index]:
                    is_path_node = True
                    pulse_factor = math.sin(frame_count * 0.15 + path.index(node) * 0.1) * 0.5 + 0.5 # ノード位置で位相ずらし
                    r = int(PATH_HIGHLIGHT[0] + (PATH_HIGHLIGHT_PULSE[0] - PATH_HIGHLIGHT[0]) * pulse_factor)
                    g = int(PATH_HIGHLIGHT[1] + (PATH_HIGHLIGHT_PULSE[1] - PATH_HIGHLIGHT[1]) * pulse_factor)
                    b = int(PATH_HIGHLIGHT[2] + (PATH_HIGHLIGHT_PULSE[2] - PATH_HIGHLIGHT[2]) * pulse_factor)
                    color = (r, g, b)

                    # 先端ノードのエフェクト
                    if current_path_segment_index < len(path) and node == path[current_path_segment_index - 1]:
                        if (frame_count // 4) % 2 == 0: # 点滅速度調整
                            color = PATH_HIGHLIGHT_PULSE
                        # 先端にパーティクル (低確率)
                        if random.random() < 0.15: # 確率少し上げる
                            x = (node[1] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
                            y = (node[0] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
                            particles.append(Particle(x, y, PATH_HIGHLIGHT_PULSE, "fade_in")) # 色を合わせる

            # --- 現在探索中のノード ---
            if solving and node == current_node:
                # 点滅エフェクト
                if (frame_count // 8) % 2 == 0: # 点滅速度調整
                    color = LIGHT_ORANGE
                else:
                    color = ORANGE

            # --- スタートとゴール ---
            if node == start_node:
                color = GREEN
            elif node == end_node:
                # ゴール到達直後のフラッシュは goal_reached_flash フラグで管理せず、
                # highlighting_path が True になった最初の数フレームだけ明るくするなど別の方法も検討可
                # 現状はシンプルにREDのまま
                color = RED

            # --- セル描画 ---
            rect = pygame.Rect(
                (MARGIN + CELL_SIZE) * col + MARGIN,
                (MARGIN + CELL_SIZE) * row + MARGIN,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, color, rect, border_radius=3)

            # --- 光沢とホバー効果 ---
            is_floor_like = (grid[row][col] == 0 or node == start_node or node == end_node or node in open_set_map or node in closed_set or is_path_node)
            if is_floor_like:
                # 光沢
                highlight_rect = rect.copy()
                highlight_rect.height = max(1, CELL_SIZE // 4) # 少し小さく
                highlight_color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
                pygame.draw.rect(screen, highlight_color, highlight_rect, border_top_left_radius=3, border_top_right_radius=3)

                # ホバー
                if hover_cell == node:
                    hover_rect = rect.inflate(-1, -1) # 枠線にかぶらないように
                    hover_color = HOVER_COLOR # 固定色の方がわかりやすいかも
                    # pygame.draw.rect(screen, hover_color, hover_rect, border_radius=2) # 塗りつぶし
                    pygame.draw.rect(screen, hover_color, hover_rect, width=1, border_radius=2) # 枠線で表示


            # --- 境界線 ---
            border_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)) # より暗く
            pygame.draw.rect(screen, border_color, rect, 1, border_radius=3)

    frame_count += 1 # ここでframe_countをインクリメント

    # --- パーティクル更新と描画 ---
    active_particles = []
    for p in particles:
        p.update(dt) # dt を渡して更新
        # 寿命とサイズ（または波紋の最大サイズ到達）で生存判定
        is_alive = p.age < p.lifespan
        if p.particle_type == "ripple":
            # 波紋は寿命が来たら消える (max_sizeに達しても動き続ける)
            pass
        else:
             # 通常のパーティクルはサイズが0になったら消える
             is_alive = is_alive and p.size > 0

        if is_alive:
            active_particles.append(p)

    particles = active_particles # 有効なパーティクルのみ残す

    # パーティクル描画用の透過Surfaceを作成
    # SRCALPHAを使うことで、各パーティクルのアルファ値（透明度）が正しく扱われる
    particle_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for p in particles:
        p.draw(particle_surface) # 透過Surfaceに描画

    # screen（背景とセルが描画済み）の上にparticle_surfaceを重ねて描画
    screen.blit(particle_surface, (0, 0))

    # --- メッセージ表示 ---
    if message:
        text_color = WHITE
        stroke_color = BLACK
        msg_render = font.render(message, True, text_color)
        # ストローク描画
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]:
            stroke_render = font.render(message, True, stroke_color)
            screen.blit(stroke_render, (10 + dx, WINDOW_HEIGHT - 25 + dy))
        # 本体テキスト描画
        screen.blit(msg_render, (10, WINDOW_HEIGHT - 25))

    # --- 画面更新 ---
    pygame.display.flip()

    # goal_reached_flash のリセットはパーティクル生成直後に移動


# --- 終了処理 ---
pygame.quit()
```