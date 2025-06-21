はい、承知いたしました。世界最高のマークダウン翻訳家として、与えられた日本語のマークダウンファイルを簡体中国語に翻訳します。元の構造、コード、技術用語を維持しつつ、自然で正確な翻訳を心がけます。

---
title: 使用 Roblox (Luau) 和 VSCode 的现代开发环境模板
description: 一个使用 Roblox Studio (Luau) 和 VSCode 的 GitHub 模板，集成了 Selene Linter、StyLua Formatter、Wally 包管理器和 Rokit 工具管理器。
slug: roblox-luau-template-for-modern-development
date: 2025-06-21 00:00:00+09:00
image: roblox-luau-template-for-modern-development.webp
categories:
    - 游戏
    - 编程
tags:
    - Roblox
    - VSCode
    - Luau
---

# GitHub 模板

[roblox-rojo-wally-template](https://github.com/takoyakisoft/roblox-rojo-wally-template)

# 这是什么？

这是一个使用 VSCode 进行 Roblox (Luau) 现代开发的模板。

- 从 VSCode 同步到 Roblox Studio: [Rojo](https://github.com/rojo-rbx/rojo)
- Linter: [Selene](https://github.com/Kampfkarren/selene)
- Formatter: [StyLua](https://github.com/JohnnyMorganz/StyLua)
- 包管理器: [Wally](https://github.com/UpliftGames/wally)
- Rojo 和 Wally 的管理器: [Rokit](https://github.com/rojo-rbx/rokit)

{{< notice warning >}}
不包含 CI/CD: [CI/CD](https://github.com/Roblox/place-ci-cd-demo)
{{< /notice >}}

# 安装

{{< notice tip >}}
可以通过 [roblox-rojo-wally-template](https://github.com/takoyakisoft/roblox-rojo-wally-template) 仓库的 “Use this template” 按钮来使用。
{{< /notice >}}

## 安装 Rokit

Windows (PowerShell)

```powershell
Invoke-RestMethod https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.ps1 | Invoke-Expression
```

macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | sh
```

## 安装 Rojo、Wally 等工具

```bash
rokit add rojo
rokit add wally
rokit add wally-package-types
```

## 安装包

```bash
wally install
rojo sourcemap default.project.json --output sourcemap.json
wally-package-types -s sourcemap.json Packages/
wally-package-types -s sourcemap.json ServerPackages/
wally-package-types -s sourcemap.json DevPackages/
```

## 安装 VSCode 扩展

当你在 VSCode 中打开此项目时，会提示安装以下扩展，请进行安装。

- [Rojo](https://marketplace.visualstudio.com/items?itemName=evaera.vscode-rojo)
- [Luau Language Server](https://marketplace.visualstudio.com/items?itemName=JohnnyMorganz.luau-lsp)
- [Selene](https://marketplace.visualstudio.com/items?itemName=Kampfkarren.selene-vscode)
- [StyLua](https://marketplace.visualstudio.com/items?itemName=JohnnyMorganz.stylua)

# 使用方法

## 从 VSCode 连接到 Rojo

按下 “Ctrl + Shift + P”

选择 “Rojo: Open Menu”

{{< notice note >}}
如果是第一次使用，请先启动 Roblox Studio，然后点击 Install Roblox Studio Plugin。
{{< /notice >}}

点击 “▶ default.project.json”

![从VSCode启动Rojo的方法](Code_m5RjRhSECe.webp)

## 从 Roblox Studio 连接到 Rojo

点击 “插件” (Plugins) 选项卡

在 “Rojo” 功能区

点击 “Connect” 按钮

![从Roblox Studio连接Rojo的方法](roblox-luau-template-for-modern-development.webp)

## 使用 Wally 添加包

在 VSCode 中编辑 wally.toml 文件。

在 [wally.run](https://wally.run/) 网站上查找你需要的包，然后复制 “Install” 部分的包名。

各个部分的分类如下：

[dependencies] 用于客户端和服务器

[server-dependencies] 仅用于服务器

[dev-dependencies] 仅用于开发和测试

编辑完成后，再次执行[安装包](#安装包)的步骤。

# 参考资料

{{< youtube IJDg6tRJmHo >}}