---
title: 发布你的Pygame游戏到Web！使用pygbag和Hugo轻松嵌入博客 (WebAssembly)
description: 想让你用Pygame制作的游戏在Web上运行吗？本文将解说如何使用pygbag将其转换为WebAssembly，并嵌入到Hugo博客中。同时介绍iframe的短代码，无需插件即可发布游戏。
slug: publish-pygame-web-hugo-pygbag
date: '2025-03-30 05:18:12+09:00'
image: publish-pygame-web-hugo-pygbag.webp
categories: [编程, 游戏]
tags: [Python, Hugo]
---

## 前言

你好！

用Pygame制作的原创游戏，当然希望发布到Web上，让更多人玩到，对吧？我也是这么想的！

在本文中，我们将一起探讨如何将使用Python游戏库 Pygame 制作的游戏发布到Web浏览器上，让任何人都能轻松玩到。我会尽量以简单易懂的方式进行解说。

通过本文可以了解到：

1.  如何使用名为 `pygbag` 的工具，通过 WebAssembly (WASM) 将Pygame游戏转换（构建）为Web版本。这个工具相当方便。
2.  将转换后的游戏嵌入到使用静态网站生成器 Hugo 创建的博客中并发布的步骤。
3.  如何创建用于轻松将游戏嵌入文章的 Hugo 短代码 (Shortcode)。提前创建好这个会让后续工作轻松很多。

按照这个步骤，无需特殊的服务器设置，只需浏览器就能玩游戏了。很棒吧！你制作的游戏或许能让全世界的人玩到！

## 完成的游戏

那么，实际用这种方法制作出来的就是这款游戏！
（这是一个只能观看的游戏。）

{{< game-iframe src="/game/the-labyrinth-of-gaze/build/web/index.html" aspect-ratio="75%" >}}

## 将Pygame游戏构建为Web版本：尝试使用 `pygbag` 这个便捷工具

我认为 `pygbag` 是一个非常方便的工具，它可以将Pygame游戏打包，使其能直接在Web浏览器中运行。让我们先用它来将游戏转换为Web版本吧。

### 1. 首先，使用 `uv` 准备项目

这里我们尝试使用 `uv`，一个最近备受关注的Python包管理工具。如果还没有安装 `uv`，请先安装。（如果你正在使用 `pip` 等其他工具，用你熟悉的工具也没问题）

※ 安装 uv（如果尚未安装，此命令适用于Windows）
```batch
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

接下来，使用 `uv init` 创建并初始化游戏项目的文件夹。
`the-labyrinth-of-gaze` 是本次示例中使用的游戏名称，请替换为您自己的项目名称。

※ 使用 uv 初始化项目
```batch
uv init the-labyrinth-of-gaze
cd the-labyrinth-of-gaze
```

接下来，安装所需的库 `pygbag` 和 `pygame`。使用 `uv` 的命令如下：

```batch
uv add pygbag pygame
```

*（如果不使用 `uv`，可以像 `pip install pygbag pygame` 这样，根据你的环境进行安装）*

### 2. 开始构建游戏

在通过 `uv init` 自动创建的 `main.py` 文件，或者你自己的游戏主脚本文件中，编写Pygame的游戏代码。

本文示例中使用的游戏代码将在文末附上。

准备就绪后，执行以下命令来构建Web版本的游戏。
请将 `main.py` 替换为你的游戏主脚本文件名。

```batch
uv run pygbag --build .\main.py
```

如果该命令成功执行，当前目录下应该会创建一个名为 `build/web` 的文件夹，其中包含用于在Web浏览器中运行游戏的文件（如 `index.html`、`the-labyrinth-of-gaze.apk` 等）。

构建生成的文件示例如下: [/game/the-labyrinth-of-gaze/build/web/index.html](/game/the-labyrinth-of-gaze/build/web/index.html)

## 将游戏嵌入Hugo博客

接下来，让我们将构建好的游戏集成到Hugo博客中。
这里以 `hugo-theme-stack` 主题为例，但基本思路对于其他Hugo主题应该也是通用的。

### 1. 关于游戏文件的存放位置

Hugo 有一个名为 `static` 的便捷文件夹，放入其中的文件和文件夹在构建网站时会被直接复制到网站的根目录（顶层）。我们将把刚才用 `pygbag` 生成的游戏文件放在这里。

部署步骤（以游戏名 `the-labyrinth-of-gaze` 为例）：

1.  在Hugo项目根目录下的 `static` 文件夹中创建一个名为 `game` 的文件夹（如果不存在的话）。
2.  在 `static/game/` 文件夹内，再创建一个用于存放该游戏的文件夹（例如：`the-labyrinth-of-gaze`）。
3.  将刚才由 `pygbag` 生成的 `build/web` 文件夹内部的所有文件复制到刚刚创建的 `static/game/the-labyrinth-of-gaze/` 文件夹中。
    *   注意： 这是关键点！请不要复制整个 `build/web` 文件夹，而是复制其内部的文件（如 `index.html`, `the-labyrinth-of-gaze.apk` 等）。

部署后的文件夹结构大致如下：

```
(你的Hugo项目文件夹)/
└── static/
    └── game/
        └── the-labyrinth-of-gaze/  <-- 将构建结果复制到此文件夹
            └── build/
                └── web/
                    ├── index.html
                    ├── the-labyrinth-of-gaze.apk
                    └── (其他必要文件) ...
```

要点： 这样做之后，就可以通过类似 `/game/the-labyrinth-of-gaze/build/web/index.html` 这样的URL从网站访问游戏的 `index.html` 文件了。

### 2. 每次都写 `<iframe>` 太麻烦了，让我们来创建Hugo短代码吧

Hugo 有一个名为 短代码 (Shortcode) 的便捷功能，我们可以利用它来轻松嵌入游戏。创建好这个之后，以后会非常方便。

在Hugo项目的 `layouts/shortcodes/` 文件夹中创建一个名为 `game-iframe.html` 的新文件，并将以下代码粘贴进去。

```html
{{/* layouts/shortcodes/game-iframe.html */}}
{{/* 通过 'src' 参数接收游戏URL */}}
{{ $src := .Get "src" }}
{{/* 通过 'aspect-ratio' 参数接收宽高比 (未指定则默认为 75% ≈ 4:3) */}}
{{ $aspectRatio := .Get "aspect-ratio" | default "75%" }}

{{/* 响应式 iframe 嵌入样式 */}}
<div style="position: relative; padding-bottom: {{ $aspectRatio }}; height: 0; overflow: hidden; max-width: 100%; height: auto;">
  <iframe
    src="{{ $src }}"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 1px solid #ccc;"
    title="Embedded Game"
    sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-fullscreen"
    loading="lazy"></iframe>
</div>
```

这个短代码的作用是：

*   通过 `src` 参数接收想要嵌入的游戏的URL。
*   通过 `aspect-ratio` 参数可以指定游戏画面的显示比例（宽高比）（例如：`75%` 对应 4:3，`56.25%` 对应 16:9）。如果未指定，则默认设置为 `75%`（接近 4:3）。
*   它会使用 `<iframe>` 嵌入指定URL的内容，并且：
*   使用CSS进行调整，以确保在屏幕尺寸变化时布局不会混乱（即响应式设计）。
*   使用 `sandbox` 属性施加限制，使iframe中的内容运行更安全。
*   添加了 `loading="lazy"` 属性，延迟加载iframe直到其接近可视区域，这是一个小优化，可以略微加快页面加载速度。

### 3. 好了，准备就绪！让我们在文章中使用它吧

至此准备工作完成！打开你想介绍游戏的那篇文章的Markdown文件，尝试使用刚才创建的短代码吧。

例如，创建一个类似 `content/posts/my-pygame-game.md` 的文章文件，在正文中像这样写入：

```markdown
---
title: "公开自制Pygame游戏“凝视迷宫”！" # 文章标题
date: 2025-03-28T00:00:00+09:00
description: "发布了用Pygame和pygbag制作的迷宫游戏。可以在浏览器中轻松游玩！" # 文章描述
slug: the-labyrinth-of-gaze-game # 文章slug（URL的一部分）
image: the-labyrinth-of-gaze.webp # 封面图片
categories: ["游戏"] # 分类
tags: ["Pygame", "自制游戏", "解谜"] # 标签
draft: false
---

我尝试将用Pygame制作的“凝视迷宫”游戏发布到Web上了！
使用 `pygbag` 就能像这样嵌入到博客中，真方便！

请一定在浏览器中轻松体验一下。

{{</* game-iframe src="/game/the-labyrinth-of-gaze/build/web/index.html" aspect-ratio="75%" */>}}

操作方法：

*   （请在这里具体写上游戏的操作方法等）
*   例如：方向键移动，空格键跳跃 等

游戏说明：

（建议在这里写上游戏的规则、目标、看点等）

如果你能乐在其中，我会很高兴！
```

这里的要点是：

*   在 `{{</* ... */>}}` 中间写入刚才创建的短代码名称 `game-iframe`。
*   对于 `src` 参数，需要指定刚才放在 `static` 文件夹中的游戏 `index.html` 文件在网站上的绝对路径（以 `/` 开头的路径）。
    *   例如：如果文件放在 `static/game/the-labyrinth-of-gaze/build/web/index.html`，则应写为 `/game/the-labyrinth-of-gaze/build/web/index.html`。
    *   重要： 这里很容易出错，请注意！请根据你的游戏实际存放位置，正确填写此路径。
*   建议根据你的游戏画面调整 `aspect-ratio` 参数，以获得更好的视觉效果（例如：16:9 对应 `56.25%`）。
*   在短代码下方，当然可以自由地写上操作方法、游戏说明等内容。

完成这些之后，只需使用 `hugo` 命令构建并发布网站，游戏应该就会嵌入并显示在文章中了！

## 总结

本次，我们介绍了使用便捷工具 `pygbag` 将 Pygame 游戏转换为 WebAssembly (WASM)，将其部署到 Hugo 博客的 `static` 文件夹，并创建 用于 iframe 嵌入的 Hugo 短代码 以便在文章中轻松显示游戏的完整步骤。

我个人认为这种方法的优点在于：

*   无需特殊服务器配置！ 仅用静态文件就能发布游戏，非常方便快捷。
*   能够轻松地在博客文章中添加互动游戏，是不是很令人兴奋？
*   为你制作的 Pygame 游戏提供了让更多人玩到的机会！
*   对于访问者来说，无需任何浏览器插件就能立刻开始玩，这也是一个优点。

如果你正在使用 Pygame 制作游戏，并且想“尝试发布到 Web 上”，不妨参考这个步骤挑战一下。

感谢您阅读到最后！

## 源代码

```python
# 使用 Pygame 的 A* 算法迷宫寻路动画（自动进行和效果添加/修正版）
import pygame
import random
import heapq
import math
import time # 为计算 dt 添加（即使没有，clock.tick 也可以）

# --- 常量 ---
# 网格设置
GRID_WIDTH = 31
GRID_HEIGHT = 25
CELL_SIZE = 15
MARGIN = 1

# 窗口大小
WINDOW_WIDTH = GRID_WIDTH * (CELL_SIZE + MARGIN) + MARGIN
WINDOW_HEIGHT = GRID_HEIGHT * (CELL_SIZE + MARGIN) + MARGIN

# 颜色 (RGB) - 更新为现代配色方案
WHITE = (245, 245, 245)
BLACK = (20, 20, 30)
GREY = (180, 180, 180)
GREEN = (76, 187, 23)
RED = (235, 64, 52)
BLUE = (66, 135, 245)
YELLOW = (250, 204, 21)
CYAN = (28, 186, 210)
ORANGE = (255, 126, 28)
LIGHT_ORANGE = (255, 183, 77)  # 用于闪烁
PATH_HIGHLIGHT = (130, 210, 240)  # 浅蓝色（路径显示动画用）
PATH_HIGHLIGHT_PULSE = (180, 230, 250)  # 用于脉冲效果
GOAL_FLASH = (255, 255, 255)  # 目标到达时效果用
HOVER_COLOR = (220, 220, 220)  # 用于悬停效果
PURPLE = (180, 120, 240)  # 新颜色
PINK = (255, 105, 180)  # 新颜色

# 动画速度 (Frame Per Second)
FPS = 60
# 自动重置前的等待时间（秒）
RESET_DELAY_SECONDS = 2.0
# 路径高亮动画速度（每帧移动的格子数，越小越慢）
PATH_HIGHLIGHT_SPEED = 0.3


# --- 辅助函数（无更改） ---
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

# 粒子类定义 - 改进以支持更多样化的效果
class Particle:
    def __init__(self, x, y, color, particle_type="normal"):
        self.x = x
        self.y = y
        self.base_color = color # 保留原始颜色
        self.color = color
        self.particle_type = particle_type
        self.size = (
            random.randint(2, 6)
            if particle_type == "normal"
            else random.randint(3, 8)
        )
        self.speed = (
            random.uniform(1, 5) * 50 # 速度调整（基于 dt）
            if particle_type == "normal"
            else random.uniform(0.5, 3) * 50 # 速度调整（基于 dt）
        )
        self.angle = random.uniform(0, math.pi * 2)
        self.lifespan = (
            random.uniform(0.5, 1.5)
            if particle_type == "normal"
            else random.uniform(1.0, 2.5)
        )
        self.age = 0
        self.pulse_rate = random.uniform(3.0, 6.0)  # 用于脉冲效果
        self.original_size = self.size  # 用于尺寸变化
        self.fade_in_duration = 0.3 # 淡入时间
        self.fade_out_start_ratio = 0.7 # 从寿命的百分之多少开始淡出

        # 星形粒子的顶点数
        self.vertices = random.randint(4, 6) if particle_type == "star" else 0

        # 用于轨迹粒子
        self.trail = []
        self.trail_length = 5 if particle_type == "trail" else 0

        # 用于波纹效果
        if particle_type == "ripple":
            self.size = 1
            self.max_size = random.randint(15, 25)
            self.expand_speed = random.uniform(0.8, 1.2) * 30 # 速度调整（基于 dt）
            self.lifespan = random.uniform(1.0, 1.5)
            self.speed = 0 # 波纹不移动

    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        self.age += dt

        # 根据粒子类型进行更新处理
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
                self.size = self.original_size # 淡入后、淡出前为最大尺寸
        elif self.particle_type == "trail":
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)
            if self.age >= self.lifespan * self.fade_out_start_ratio:
                self.size = max(0, self.size - size_decay_rate * dt * 0.5) # Trail 消失得稍慢一些
        elif self.particle_type == "ripple":
            self.size = min(self.size + self.expand_speed * dt, self.max_size)
        elif self.particle_type == "star":
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                 self.size = max(0, self.size - size_decay_rate * dt)
        else: # default or rainbow etc.
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                 self.size = max(0, self.size - size_decay_rate * dt)

        # 颜色变化（色相随时间变化 - rainbow 类型）
        if self.particle_type == "rainbow":
            hue_shift = (self.age * 100) % 360
            # HSV -> RGB 转换（简化版）
            r_val, g_val, b_val = 0, 0, 0
            i = int(hue_shift / 60) % 6
            f = hue_shift / 60 - i
            v = 1.0 # 亮度
            s = 1.0 # 饱和度
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
        if self.size <= 0: # 如果尺寸小于等于 0 则不绘制
            return

        # 淡入/淡出效果的透明度计算
        alpha = 255
        if self.particle_type == "ripple":
            # 波纹效果的透明度计算（逐渐变淡）
            progress = self.age / self.lifespan if self.lifespan > 0 else 1
            alpha = max(0, min(255, int(255 * (1 - progress) * 0.8))) # 结尾时更加透明
        elif self.particle_type == "fade_in":
            if self.age < self.fade_in_duration:
                alpha = int(255 * (self.age / self.fade_in_duration))
            elif self.age >= self.lifespan * self.fade_out_start_ratio:
                fade_out_duration = self.lifespan * (1.0 - self.fade_out_start_ratio)
                if fade_out_duration > 0:
                    alpha = max(0, min(255, int(255 * (1 - (self.age - self.lifespan * self.fade_out_start_ratio) / fade_out_duration))))
                else:
                    alpha = 0 # 以防万一
            else:
                alpha = 255
        else: # Normal, Pulse, Star, Trail, Rainbow etc.
            # 通用的淡出处理
             if self.age >= self.lifespan * self.fade_out_start_ratio:
                fade_out_duration = self.lifespan * (1.0 - self.fade_out_start_ratio)
                if fade_out_duration > 0:
                    alpha = max(0, min(255, int(255 * (1 - (self.age - self.lifespan * self.fade_out_start_ratio) / fade_out_duration))))
                else:
                    alpha = 0
             else:
                alpha = 255

        # 颜色验证和设置
        try:
            current_color = self.color if self.particle_type == "rainbow" else self.base_color
            if isinstance(current_color, tuple) and len(current_color) == 3:
                r = max(0, min(255, int(current_color[0])))
                g = max(0, min(255, int(current_color[1])))
                b = max(0, min(255, int(current_color[2])))
                final_color = (r, g, b, alpha)
            else:
                final_color = (255, 255, 255, alpha)  # 默认颜色

            # 根据粒子类型绘制
            if self.particle_type == "ripple":
                # 波纹效果（绘制轮廓）
                line_width = max(1, int(self.max_size / 15 * (1 - self.age / self.lifespan))) # 逐渐变细的轮廓
                if self.size >= 1: # 最小半径大于等于 1
                    pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size), width=line_width)
            elif self.particle_type == "star" and self.vertices > 0:
                # 星形粒子
                points = []
                outer_radius = self.size
                inner_radius = self.size * 0.4
                for i in range(self.vertices * 2):
                    angle = math.pi / self.vertices * i - math.pi / 2 # 调整使顶点朝上
                    radius = outer_radius if i % 2 == 0 else inner_radius
                    x_p = self.x + math.cos(angle) * radius
                    y_p = self.y + math.sin(angle) * radius
                    points.append((x_p, y_p))
                if len(points) >= 3:  # 至少需要 3 个点
                    pygame.draw.polygon(surface, final_color, points)
            elif self.particle_type == "trail" and len(self.trail) > 1:
                # 轨迹粒子
                for i in range(len(self.trail) - 1):
                    start_pos = self.trail[i]
                    end_pos = self.trail[i + 1]
                    # 调整轨迹的 alpha 和宽度
                    trail_alpha = alpha * ((i + 1) / len(self.trail))**2 # 越往后越淡
                    trail_width = max(1, int(self.size * ((i + 1) / len(self.trail))))
                    trail_color_tuple = (final_color[0], final_color[1], final_color[2], int(trail_alpha))
                    pygame.draw.line(surface, trail_color_tuple, start_pos, end_pos, trail_width)
                # 也绘制前端的圆
                pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size))
            else:
                # 普通圆形粒子 (Normal, Pulse, Fade_in, Rainbow)
                pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size))

        except (ValueError, TypeError) as e:
            # 如果发生错误，则使用默认颜色
            print(f"Error drawing particle: {e}, color={self.color}, alpha={alpha}, size={self.size}")
            try:
                safe_color = (255, 255, 255, alpha)
                if self.size >= 1:
                    pygame.draw.circle(surface, safe_color, (int(self.x), int(self.y)), int(max(1, self.size))) # 保证最小尺寸为 1
            except Exception as final_e:
                 print(f"Final fallback drawing failed: {final_e}")


# --- Pygame 初始化 ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("A* Maze Solver Animation (Auto-Repeat, ESC: Quit)")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# --- 状态变量 ---
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
particles = []  # 粒子列表（ripples 也合并到这里）
# ripples = [] # 因为不再需要而删除
node_pulses = []  # 用于节点搜索时的脉冲效果（目前可能未使用？）

# --- 自动重置用变量 ---
reset_timer = 0  # 等待帧计数器
RESET_DELAY_FRAMES = int(RESET_DELAY_SECONDS * FPS)  # 将秒转换为帧数
start_reset_timer_after_highlight = False  # 高亮完成后启动计时器的标志

# --- 路径高亮动画用变量 ---
path_highlight_index = 0.0  # 使用 float 缓慢前进
highlighting_path = False

# --- 目标到达效果用 ---
goal_reached_flash = False  # 是否是到达目标后的那一帧

# --- 主循环 ---
running = True
frame_count = 0  # 用于闪烁动画
hover_cell = None  # 悬停中的单元格

while running:
    # --- Delta Time 计算 ---
    dt = clock.tick(FPS) / 1000.0 # 以秒为单位的 delta time（避免除以 0）
    if dt == 0: dt = 1 / FPS # 保证最小时间步长

    # --- 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 从鼠标坐标获取悬停中的单元格
    mouse_pos = pygame.mouse.get_pos()
    mouse_col = mouse_pos[0] // (CELL_SIZE + MARGIN)
    mouse_row = mouse_pos[1] // (CELL_SIZE + MARGIN)
    if 0 <= mouse_row < GRID_HEIGHT and 0 <= mouse_col < GRID_WIDTH:
        hover_cell = (mouse_row, mouse_col)
    else:
        hover_cell = None

    # --- 状态更新 ---
    if not maze_generated:
        # 重置等待计时器
        reset_timer = 0
        start_reset_timer_after_highlight = False
        highlighting_path = False
        path_highlight_index = 0.0
        goal_reached_flash = False
        hover_cell = None
        particles = [] # 清除现有粒子

        message = "正在生成新迷宫..."
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
        if start_node: # 确认 start_node 不为 None
            g_score[start_node] = 0
            h_start = heuristic(start_node, end_node) if end_node else 0
            f_start = g_score[start_node] + h_start
            heapq.heappush(open_set_heap, (f_start, h_start, start_node))
            open_set_map[start_node] = (f_start, h_start)

        maze_generated = True
        solving = True if start_node and end_node else False # 如果没有开始/结束节点则不求解
        message = "正在求解..." if solving else "迷宫已生成（没有起点/终点？）"


    # --- A* 算法的步进执行 ---
    if solving and open_set_heap:
        current_f, current_h, current_node_popped = heapq.heappop(open_set_heap)

        # 如果已从 open_set_map 中删除，或者之后找到了更好的路径，则跳过
        if current_node_popped not in open_set_map or open_set_map[current_node_popped] > (current_f, current_h):
             pass # 忽略并进入下一个循环
        else:
            # 因为要处理，所以从 open_set_map 中删除（可能再次添加）
            # 因为在从 heapq 弹出时就作为处理对象，所以 del 可能不需要。重复检查在上面的 if 中进行。
            # del open_set_map[current_node_popped] # 此处的删除可能不需要
            current_node = current_node_popped

            if current_node == end_node:
                path = reconstruct_path(came_from, current_node)
                solving = False
                message = "已到达目标！正在高亮路径..."
                current_node = None
                highlighting_path = True
                path_highlight_index = 0.0
                goal_reached_flash = True # 打开效果生成标志
                start_reset_timer_after_highlight = True
            else:
                closed_set.add(current_node)
                # 确认从 open_set_map 中删除（因为它已进入 closed）
                if current_node in open_set_map:
                    del open_set_map[current_node]


                # 为正在搜索的节点添加波纹效果
                node_x = (current_node[1] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
                node_y = (current_node[0] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2

                # 生成波纹效果（使用 Particle 类）
                particles.append(Particle(node_x, node_y, YELLOW, "ripple")) # 将颜色更改为 YELLOW

                # 少量生成小粒子（搜索时）
                if random.random() < 0.1: # 稍微降低概率
                    for _ in range(1): # 减少数量
                        color = random.choice([YELLOW, ORANGE]) # 使颜色与搜索颜色匹配
                        particles.append(Particle(node_x, node_y, color, "fade_in"))

                for neighbor in get_valid_neighbors(current_node, grid):
                    if neighbor in closed_set:
                        continue

                    tentative_g_score = g_score[current_node] + 1

                    # 如果此路径不如现有路径，或者 open set 中已有更好的路径，则忽略
                    # 注意：open_set_map 中存储的是 (f, h)
                    neighbor_in_open = open_set_map.get(neighbor)
                    if neighbor_in_open and tentative_g_score >= g_score.get(neighbor, float('inf')):
                         continue

                    # 如果找到更好的路径，或者首次访问
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    h_neighbor = heuristic(neighbor, end_node)
                    f_neighbor = tentative_g_score + h_neighbor

                    # 如果不在 open_set 中则添加，如果存在则更新（heapq 不直接支持更新，因此添加新元素）
                    heapq.heappush(open_set_heap, (f_neighbor, h_neighbor, neighbor))
                    open_set_map[neighbor] = (f_neighbor, h_neighbor) # 保存 f, h


    elif solving and not open_set_heap:
        solving = False
        message = f"未找到路径！将在 {RESET_DELAY_SECONDS:.1f} 秒后重置..."
        current_node = None
        reset_timer = RESET_DELAY_FRAMES  # 搜索失败时立即启动计时器

    # --- 路径高亮处理 ---
    if highlighting_path and path:
        if path_highlight_index < len(path):
            path_highlight_index += PATH_HIGHLIGHT_SPEED * FPS * dt # 使用 dt 调整速度
            # 完成瞬间的处理
            if path_highlight_index >= len(path):
                path_highlight_index = len(path)
                if start_reset_timer_after_highlight:
                    reset_timer = RESET_DELAY_FRAMES
                    message = f"路径完成！将在 {RESET_DELAY_SECONDS:.1f} 秒后重置..."
                    start_reset_timer_after_highlight = False

    # --- 自动重置计时器处理 ---
    if reset_timer > 0:
        reset_timer -= 1 # 基于帧进行倒计时
        remaining_time = reset_timer / FPS # 转换为秒并显示
        if not solving and not path:
            message = f"未找到路径！将在 {remaining_time:.1f} 秒后重置..."
        elif not solving and path and path_highlight_index >= len(path):
            message = f"路径完成！将在 {remaining_time:.1f} 秒后重置..."

        if reset_timer <= 0:
            maze_generated = False

    # --- 绘制处理 ---
    # 渐变背景
    for y in range(WINDOW_HEIGHT):
        time_factor = math.sin(frame_count * 0.005) * 0.2
        r_base = 30 + int(10 * time_factor)
        g_base = 40 + int(15 * time_factor)
        b_base = 60 + int(20 * time_factor)
        gradient_factor = math.sin(math.pi * y / WINDOW_HEIGHT)
        r = int(r_base + (50 - r_base) * gradient_factor) # 稍微调暗
        g = int(g_base + (70 - g_base) * gradient_factor) # 稍微调暗
        b = int(b_base + (90 - b_base) * gradient_factor) # 稍微调暗
        pygame.draw.line(screen, (max(0,r), max(0,g), max(0,b)), (0, y), (WINDOW_WIDTH, y))

    # 提升单元格质感（阴影和光泽）- 这部分保持原样也可以
    shadow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(
                (MARGIN + CELL_SIZE) * col + MARGIN,
                (MARGIN + CELL_SIZE) * row + MARGIN,
                CELL_SIZE,
                CELL_SIZE,
            )
            if grid[row][col] == 0: # 通道
                pygame.draw.rect(shadow_surface, (0, 0, 0, 30), rect.inflate(1, 1), border_radius=3) # 稍微浅一点的阴影
                light_rect = rect.inflate(-3, -3).move(-1, -1)
                pygame.draw.rect(shadow_surface, (255, 255, 255, 50), light_rect, border_radius=2) # 光泽也稍微低调一点
            else: # 墙壁
                pygame.draw.rect(shadow_surface, (0, 0, 0, 20), rect.inflate(1, 1), border_radius=2)
                pygame.draw.rect(shadow_surface, (0, 0, 0, 30), rect.inflate(-2, -2), border_radius=1, width=1) # 内部阴影

    screen.blit(shadow_surface, (0, 0))


    # 到达目标时的粒子生成
    if goal_reached_flash:
        goal_x = (end_node[1] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
        goal_y = (end_node[0] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2

        # 生成多种粒子类型
        for _ in range(40): # 增加普通粒子数量
            color = random.choice([RED, YELLOW, ORANGE, BLUE, GREEN, PURPLE, PINK, WHITE])
            particles.append(Particle(goal_x, goal_y, color, "normal"))
        for _ in range(15): # 增加星形粒子数量
            color = random.choice([YELLOW, WHITE, ORANGE, CYAN])
            particles.append(Particle(goal_x, goal_y, color, "star"))
        for _ in range(10): # 脉冲效果
            color = random.choice([CYAN, PURPLE, PINK, BLUE])
            particles.append(Particle(goal_x, goal_y, color, "pulse"))
        for _ in range(8): # 轨迹粒子
            color = random.choice([BLUE, CYAN, WHITE, GREEN])
            particles.append(Particle(goal_x, goal_y, color, "trail"))
        for _ in range(10): # 彩虹粒子
            particles.append(Particle(goal_x, goal_y, WHITE, "rainbow")) # 初始颜色为白色即可
        for _ in range(6): # 波纹效果也作为 Particle 生成
            color = random.choice([WHITE, CYAN, BLUE, YELLOW]) # 波纹颜色
            particles.append(Particle(goal_x, goal_y, color, "ripple")) # 以 ripple 类型生成

        goal_reached_flash = False # ★★★ 粒子生成后立即重置标志 ★★★

    # 单元格绘制循环
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = WHITE
            if grid[row][col] == 1:
                color = BLACK

            node = (row, col)
            is_path_node = False # 是否为路径高亮对象的标志

            # --- 根据单元格状态设置颜色 ---
            if node in closed_set:
                # closed 列表的颜色（已搜索）- 稍暗的 CYAN
                 color = (20, 140, 160)
            # 存在于 open_set_map 中的节点（搜索候选）- 稍暗的 YELLOW
            # 即使 heapq 中有多个相同节点，open_set_map 中也应该包含最新的 (f, h)
            if node in open_set_map:
                 color = (200, 160, 10) # 稍暗的 YELLOW

            # --- 路径高亮 ---
            if highlighting_path and path:
                current_path_segment_index = int(path_highlight_index)
                if node in path[:current_path_segment_index]:
                    is_path_node = True
                    pulse_factor = math.sin(frame_count * 0.15 + path.index(node) * 0.1) * 0.5 + 0.5 # 根据节点位置进行相位偏移
                    r = int(PATH_HIGHLIGHT[0] + (PATH_HIGHLIGHT_PULSE[0] - PATH_HIGHLIGHT[0]) * pulse_factor)
                    g = int(PATH_HIGHLIGHT[1] + (PATH_HIGHLIGHT_PULSE[1] - PATH_HIGHLIGHT[1]) * pulse_factor)
                    b = int(PATH_HIGHLIGHT[2] + (PATH_HIGHLIGHT_PULSE[2] - PATH_HIGHLIGHT[2]) * pulse_factor)
                    color = (r, g, b)

                    # 前端节点的效果
                    if current_path_segment_index < len(path) and node == path[current_path_segment_index - 1]:
                        if (frame_count // 4) % 2 == 0: # 调整闪烁速度
                            color = PATH_HIGHLIGHT_PULSE
                        # 在前端生成粒子（低概率）
                        if random.random() < 0.15: # 稍微提高概率
                            x = (node[1] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
                            y = (node[0] * (CELL_SIZE + MARGIN)) + MARGIN + CELL_SIZE // 2
                            particles.append(Particle(x, y, PATH_HIGHLIGHT_PULSE, "fade_in")) # 匹配颜色

            # --- 当前搜索中的节点 ---
            if solving and node == current_node:
                # 闪烁效果
                if (frame_count // 8) % 2 == 0: # 调整闪烁速度
                    color = LIGHT_ORANGE
                else:
                    color = ORANGE

            # --- 开始和目标 ---
            if node == start_node:
                color = GREEN
            elif node == end_node:
                # 到达目标后的闪光不由 goal_reached_flash 标志管理，
                # 也可以考虑其他方法，例如仅在 highlighting_path 变为 True 的最初几帧调亮
                # 目前保持简单的 RED
                color = RED

            # --- 单元格绘制 ---
            rect = pygame.Rect(
                (MARGIN + CELL_SIZE) * col + MARGIN,
                (MARGIN + CELL_SIZE) * row + MARGIN,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, color, rect, border_radius=3)

            # --- 光泽和悬停效果 ---
            is_floor_like = (grid[row][col] == 0 or node == start_node or node == end_node or node in open_set_map or node in closed_set or is_path_node)
            if is_floor_like:
                # 光泽
                highlight_rect = rect.copy()
                highlight_rect.height = max(1, CELL_SIZE // 4) # 稍微小一点
                highlight_color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
                pygame.draw.rect(screen, highlight_color, highlight_rect, border_top_left_radius=3, border_top_right_radius=3)

                # 悬停
                if hover_cell == node:
                    hover_rect = rect.inflate(-1, -1) # 避免与边框重叠
                    hover_color = HOVER_COLOR # 固定颜色可能更容易理解
                    # pygame.draw.rect(screen, hover_color, hover_rect, border_radius=2) # 填充
                    pygame.draw.rect(screen, hover_color, hover_rect, width=1, border_radius=2) # 用边框显示


            # --- 边界线 ---
            border_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)) # 更暗
            pygame.draw.rect(screen, border_color, rect, 1, border_radius=3)

    frame_count += 1 # 在这里递增 frame_count

    # --- 粒子更新和绘制 ---
    active_particles = []
    for p in particles:
        p.update(dt) # 传递 dt 进行更新
        # 根据寿命和尺寸（或波纹达到最大尺寸）判断生存
        is_alive = p.age < p.lifespan
        if p.particle_type == "ripple":
            # 波纹寿命结束后消失（即使达到 max_size 也会继续移动）
            pass
        else:
             # 普通粒子尺寸变为 0 后消失
             is_alive = is_alive and p.size > 0

        if is_alive:
            active_particles.append(p)

    particles = active_particles # 只保留有效的粒子

    # 创建用于粒子绘制的透明 Surface
    # 使用 SRCALPHA 可以正确处理每个粒子的 alpha 值（透明度）
    particle_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for p in particles:
        p.draw(particle_surface) # 在透明 Surface 上绘制

    # 在 screen（已绘制背景和单元格）上叠加绘制 particle_surface
    screen.blit(particle_surface, (0, 0))

    # --- 消息显示 ---
    if message:
        text_color = WHITE
        stroke_color = BLACK
        msg_render = font.render(message, True, text_color)
        # 描边绘制
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]:
            stroke_render = font.render(message, True, stroke_color)
            screen.blit(stroke_render, (10 + dx, WINDOW_HEIGHT - 25 + dy))
        # 主体文本绘制
        screen.blit(msg_render, (10, WINDOW_HEIGHT - 25))

    # --- 画面更新 ---
    pygame.display.flip()

    # goal_reached_flash 的重置移至粒子生成后立即进行


# --- 结束处理 ---
pygame.quit()
```