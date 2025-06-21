---
title: A Modern Development Environment Template for Roblox (TypeScript) and VSCode
description: I created a GitHub template for Roblox Studio (TypeScript) and VSCode that includes the ESLint linter, Prettier formatter, and pnpm package manager.
slug: roblox-ts-template-for-modern-development
date: 2025-06-22 00:00:00+09:00
image: roblox-ts-template-for-modern-development.webp
categories:
    - Game
    - Programming
tags:
    - Roblox
    - VSCode
    - TypeScript
---

# GitHub Template

[roblox-ts-rojo-template](https://github.com/takoyakisoft/roblox-ts-rojo-template)

[English](README.md) [日本語](README.ja.md)

# What is this?

This is a template for a modern development environment using VSCode for Roblox (TypeScript).

- VSCode 👉 Roblox Studio sync: [Rojo](https://github.com/rojo-rbx/rojo)
- Linter: [ESlint](https://github.com/eslint/eslint)
- Formatter: [Prettier](https://github.com/prettier/prettier)
- Package Manager: [pnpm](https://github.com/pnpm/pnpm)

> [!CAUTION]
> Functionality is unconfirmed, but popular packages have been included.

- "@rbxts/janitor"
- "@rbxts/knit"
- "@rbxts/profileservice"
- "@rbxts/replicaservice"
- "@rbxts/react"
- "@rbxts/react-roblox"
- "@rbxts/cmdr"
- "@rbxts/testez"

> [!WARNING]
> CI/CD is not included.

# Installation

> [!TIP]
> You can use this via the "Use this template" button.

## Install Packages

```bash
pnpm install
```

## Install VSCode Extensions

When you open this project, VSCode will recommend the following extensions. Please install them.

- [roblox-ts](https://marketplace.visualstudio.com/items?itemName=Roblox-TS.vscode-roblox-ts)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Rojo](https://marketplace.visualstudio.com/items?itemName=evaera.vscode-rojo)

# Usage

## From VSCode to Rojo

```bash
pnpm run watch
```

`Ctrl + Shift + P`

`Rojo: Open Menu`

> [!NOTE]
> If this is your first time, launch Roblox Studio and install the Roblox Studio Plugin.

`▶ default.project.json`

![How to start Rojo from VSCode](Code_m5RjRhSECe.webp)

## From Roblox Studio to Rojo

"Plugins" tab

"Rojo" ribbon

"Connect" button

![How to connect Rojo from Roblox Studio](roblox-ts-template-for-modern-development.webp)