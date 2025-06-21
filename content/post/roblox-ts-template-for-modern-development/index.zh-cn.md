---
title: 使用 Roblox (TypeScript) 和 VSCode 的现代开发环境模板
description: 我创建了一个使用 Roblox Studio (TypeScript) 和 VSCode 的 GitHub 模板，集成了 ESLint Linter、Prettier Formatter 和 pnpm 包管理器。
slug: roblox-ts-template-for-modern-development
date: 2025-06-22 00:00:00+09:00
image: roblox-ts-template-for-modern-development.webp
categories:
    - 游戏
    - 编程
tags:
    - Roblox
    - VSCode
    - TypeScript
---

# GitHub 模板

[roblox-ts-rojo-template](https://github.com/takoyakisoft/roblox-ts-rojo-template)

# 这是什么？

这是一个使用 VSCode 为 Roblox (TypeScript) 开发的现代开发环境模板。

- VSCode 👉 Roblox Studio 同步: [Rojo](https://github.com/rojo-rbx/rojo)
- Linter: [ESlint](https://github.com/eslint/eslint)
- Formatter: [Prettier](https://github.com/prettier/prettier)
- 包管理器: [pnpm](https://github.com/pnpm/pnpm)

> [!CAUTION]
> 虽然尚未确认其功能，但已包含了一些知名的包。

- "@rbxts/janitor"
- "@rbxts/knit"
- "@rbxts/profileservice"
- "@rbxts/replicaservice"
- "@rbxts/roact"
- "@rbxts/testez"

> [!WARNING]
> 不包含 CI/CD。

# 安装

> [!TIP]
> 您可以通过点击 "Use this template" 按钮来使用。

## 安装包

```bash
pnpm install
```

## 安装 VSCode 扩展

当您打开此项目时，VSCode 会提示您安装以下扩展，请进行安装。

- [roblox-ts](https://marketplace.visualstudio.com/items?itemName=Roblox-TS.vscode-roblox-ts)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Rojo](https://marketplace.visualstudio.com/items?itemName=evaera.vscode-rojo)


# 使用方法

## 从 VSCode 启动 Rojo

按下“Ctrl + Shift + P”

选择“Rojo: Open Menu”

> [!NOTE]
> 如果是首次使用，请启动 Roblox Studio 并安装 Roblox Studio 插件（Install Roblox Studio Plugin）。

点击“▶ default.project.json”

![从VSCode启动Rojo的方法](Code_m5RjRhSECe.webp)

## 从 Roblox Studio 连接 Rojo

“插件”选项卡

Rojo 功能区

“Connect”按钮

![从Roblox Studio连接Rojo的方法](roblox-ts-template-for-modern-development.webp)