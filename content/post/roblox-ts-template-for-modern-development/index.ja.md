---
title: Roblox（TypeScript）とVSCodeでモダンな開発環境のテンプレート
description: Roblox Studio（TypeScript）とVSCodeを使用した、ESLintリンター、Prettierフォーマッター、pnpmパッケージマネージャーのGitHubテンプレートを作成しました
slug: roblox-ts-template-for-modern-development
date: 2025-06-22 00:00:00+09:00
image: roblox-ts-template-for-modern-development.webp
categories:
    - ゲーム
    - プログラミング
tags:
    - Roblox
    - VSCode
    - TypeScript
---

# GitHubテンプレート

[roblox-ts-rojo-template](https://github.com/takoyakisoft/roblox-ts-rojo-template)

# これは何？

Roblox（TypeScript）でVSCodeを使ったモダンな開発環境のテンプレートです。

- VSCode 👉 Roblox Studioへの同期: [Rojo](https://github.com/rojo-rbx/rojo)
- リンター: [ESlint](https://github.com/eslint/eslint)
- フォーマッター: [Prettier](https://github.com/prettier/prettier)
- パッケージマネージャー: [pnpm](https://github.com/pnpm/pnpm)

> [!CAUTION]
> 動作未確認ですが、有名なパッケージを入れてあります。

- "@rbxts/janitor"
- "@rbxts/knit"
- "@rbxts/profileservice"
- "@rbxts/replicaservice"
- "@rbxts/roact"
- "@rbxts/testez"

> [!WARNING]
> CI/CDは入ってないです

# インストール

> [!TIP]
> "Use this template"ボタンから使えます。

## パッケージのインストール

```bash
pnpm install
```

## VSCode拡張機能のインストール

このプロジェクトを開くとVSCodeで以下の拡張機能が表示されるのでインストールします。

- [roblox-ts](https://marketplace.visualstudio.com/items?itemName=Roblox-TS.vscode-roblox-ts)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Rojo](https://marketplace.visualstudio.com/items?itemName=evaera.vscode-rojo)


# 使い方

## VSCodeからRojo

```bash
pnpm run watch
```

「Ctrl + Shift + P」

「Rojo: Open Menu」

> [!NOTE]
> 初めてならRoblox Studioを起動して、Install Roblox Studio Plugin

「▶ default.project.json」

![VSCodeからRojoの起動方法](Code_m5RjRhSECe.webp)

## Roblox StudioからRojo

「プラグイン」タブ

「Rojo」リボン

「Connect」ボタン

![Roblox StudioからRojoの接続方法](roblox-ts-template-for-modern-development.webp)
