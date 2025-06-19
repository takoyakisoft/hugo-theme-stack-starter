---
title: 尝试使用最新的免费AI模型 Gemini 2.5 Pro 和 Trae Builder 开发 Three.js 游戏！
description: 使用免费的最新AI Gemini 2.5 Pro 和 Trae Builder 生成 Three.js 游戏！分享追求“多汁感”的开发过程以及单文件生成时的注意事项等。
slug: free-ai-models-create-threejs-game
date: '2025-03-30 23:43:05+09:00'
image: free-ai-models-create-threejs-game.webp
categories: [AI, 编程, 游戏]
tags: [Gemini, Claude, Trae]
---

你好！

这次，我将分享一个尝试使用目前（截至2025年3月30日）可以免费使用的、性能非常强大的AI模型来开发简单Web游戏的故事。

令人惊讶的是，Google 的 Gemini 2.5 Pro 实验模型（`gemini-2.5-pro-exp-03-25`）竟然可以在 [ai.dev](https://ai.dev) 网站上免费使用！据说这是目前性能最顶尖（SOTA）的模型之一，太厉害了！

此外，我还试用了 ByteDance 公司 [Trae](https://trae.ai) 编辑器中的“Builder”功能（测试版）。在这里，可以使用像 Claude 一样的 AI 代理，并且可以选择“Claude 3.7 Sonnet”作为模型。这个也是免费的。

不过，由于两者都是免费计划，输入的数据很可能会被用于服务改进等方面。因此，这不适合用于包含机密信息的开发，但对于要公开的程序或个人实验来说，可能非常合适！

## 让 AI 制作 Three.js 游戏

那么，这次我尝试在这些强大 AI，特别是“Gemini 2.5 Pro”的帮助下，挑战制作一个仅使用单个 HTML 文件、基于 JavaScript 3D 库 Three.js 的游戏。

我不仅仅是让它生成代码，为了让游戏更有趣，我向 AI 传达了“多汁感 (Juiciness)”的概念，并要求它进行了几次修改。“多汁感”指的是改善游戏体验的元素，例如操作时的舒适感和特效的华丽程度。

## 完成的游戏

然后，完成的游戏就是这个！

{{< game-iframe src="/game/polygon-impact/index.html" aspect-ratio="75%" >}}

**操作方法：**

*   移动鼠标光标可以移动相机视角。
*   点击鼠标发射子弹。
*   按 `ESC` 键可以退出操作焦点。

内容相当简单，但您或许能从鼠标操作的响应和效果中感受到一些“多汁感”。

## 生成时间和注意事项

这个游戏实际上仅由一个 `index.html` 文件构成，代码行数达到了约 1500 行。

使用 Gemini 2.5 Pro（`gemini-2.5-pro-exp-03-25` 模型）生成它，输出花费了大约 180 秒。相当耗时呢。

根据这次经验，目前如果让 AI 生成单个文件的完整代码，将代码量控制在1000 行左右似乎是在合理时间内推进工作的较好选择。

当然，这可能会根据模型的性能和拥堵情况而变化，但可以作为一个参考标准。

## 总结

这次，我们介绍了使用免费的最新 AI 模型“Gemini 2.5 Pro”和“Trae Builder (Claude 3.7 Sonnet)”来生成 Three.js 游戏的尝试。

能够免费使用性能如此强大的 AI 真是令人惊讶，根据不同的想法似乎可以创造出各种各样的东西！特别是对于计划公开的项目或学习目的而言，我认为这是非常有用的工具。

虽然在代码生成时间等方面可能还有些不完善之处，但我认为这非常值得一试。

非常感谢您读到这里！也请大家务必尝试一下。