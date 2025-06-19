---
title: 【Steam Link】Minecraftをリモートプレイ！ノートPCでも快適プレイ
description: ゲーミングPCなしでも大丈夫！Steam Linkを使えば、WindowsノートPCで快適にMinecraftが遊べます。リビングのソファでリラックスしながら、サクサク動くMinecraftを体験しよう！この動画では、Steam Linkの簡単設定方法を分かりやすく解説。低スペックPCでも楽しめるので、ぜひお試しください。
slug: steam-link-play-minecraft-remotely-smooth-gameplay-on-your-laptop
date: 2024-11-20 17:00:00+09:00
image: steam-link-play-minecraft-remotely-smooth-gameplay-on-your-laptop.webp
categories:
    - YouTube
    - ゲーム
tags:
    - Steam
    - Windows
---

## YouTube動画

【Steam Link】Minecraftをリモートプレイ！ノートPCでも快適プレイ
{{< youtube bOvMbOhWdVI >}}

## ノートPCでの作業（Steam Linkを入れるクライアント側）

次のURLからSteam Linkをダウンロードします。
https://store.steampowered.com/remoteplay

![Steam LinkのURLの場所](vlcsnap-2024-11-20-11h19m59s894.webp)
この画像の位置からお手持ちのOSに合ったSteam Linkをダウンロードします。

Steam Linkの対応OSは以下のとおりです。
- iPhone、iPad、Apple TV（11.0以降）
- Android（5.0以降）スマホ、タブレット、テレビ
- Google PlayへのアクセスがないAndroidユーザー
- Raspberry Pi 3、3+、4
- Windows
- Linux
- macOS
- Meta Quest 2、3、Pro

![Steam Linkのインストールはsetup.exe](vlcsnap-2024-11-20-11h20m21s160.webp)
Windowsの場合のインストールは、msiではなくsetup.exeが良いようです。お手持ちのPC環境に足りないソフトのチェックもしてくれるとのことです。

インストールはすべて「Next」にしました。

## ゲーミングPCでの作業（Steamを入れるホスト側）

![Steam LinkのRemote Playを有効にする](vlcsnap-2024-11-20-11h21m01s028.webp)
「Steam」→「設定」→「Remote Play」→「Remote Playを有効にする」のトグルボタンをオンにします。

![Minecraftを非Steamゲームをマイライブラリに追加](vlcsnap-2024-11-20-11h21m12s511.webp)
「ゲーム」→「非Steamゲームをマイライブラリに追加」→「参照」からMinecraftのランチャーを追加します。
私の環境ではDドライブのため「D:\XboxGames\Minecraft Launcher\Content\gamelaunchhelper.exe」にありました。
開いたあと、「gamelaunchhelper」にチェックが入っていることを確認して「選択したプログラムを追加」します。

## ノートPCからリモートプレイ（Steam Linkが入ったクライアント側）

※ノートPC側ではSteamは終了させてください。つながらなくなります。

![Steam Linkの起動](vlcsnap-2024-11-20-11h21m32s090.webp)
Steam Linkを起動します。
ファイアウォールの設定が出たら許可をします。
初回はゲーミングPC側でもOKボタンを押す必要があった思います。

マウスカーソルが表示されないことがありました。
ゲーミングPC側に余ったマウスを接続すると表示されます。
また、Windows 11 Proならば、リモートデスクトップのログイン・ログオフをするとマウスカーソルが表示されました。

![MinecraftのマウスのRaw入力をオフ](vlcsnap-2024-11-20-12h03m53s138.webp)
Minecraftの設定で、マウスのRaw入力をオフにしたほうが良いです。
なぜかチェストを開いてマウスカーソルを動かしチェストを閉じたとき、その方向に視点移動することがありました。マウスのRaw入力のオフでなくなる思います。
