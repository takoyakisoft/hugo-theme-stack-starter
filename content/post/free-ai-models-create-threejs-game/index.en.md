---
title: Trying to Develop a Three.js Game Using the Latest Free AI Models Gemini 2.5 Pro and Trae Builder!
description: Generating a Three.js game using the free latest AI, Gemini 2.5 Pro and Trae Builder! Sharing the development process focusing on 'juiciness' and points to note when generating a single file.
slug: free-ai-models-create-threejs-game
date: '2025-03-30 23:43:05+09:00'
image: free-ai-models-create-threejs-game.webp
categories: [AI, Programming, Game]
tags: [Gemini, Claude, Trae]
---

Hello!

Today, I'd like to share my experience trying to develop a simple web game using some incredibly powerful AI models that are currently available for free (as of March 30, 2025).

Amazingly, Google's experimental model of 'Gemini 2.5 Pro' (`gemini-2.5-pro-exp-03-25`) is available for free on the website [ai.dev](https://ai.dev)! It's said to be one of the state-of-the-art (SOTA) models currently available, which is quite impressive!

Furthermore, I also tried the 'Builder' feature (beta version) in the editor called '[Trae](https://trae.ai)' by ByteDance. Here, you can use an AI agent similar to Claude, and you can even select 'Claude 3.7 Sonnet' as the model. This is also available for free.

However, since both are free plans, it's likely that the data you input might be used for service improvements. Therefore, they might not be suitable for development involving confidential information, but they could be perfect for programs intended for public release or personal experiments!

## Having AI Create a Game with Three.js

So, this time, I challenged myself to have these powerful AIs, especially 'Gemini 2.5 Pro', assist in creating a game using the JavaScript 3D library Three.js, contained within just a single HTML file.

Instead of just generating the code, I communicated the concept of 'juiciness' to the AI and requested several revisions to make the game more engaging. 'Juiciness' refers to elements that enhance the feel of gameplay, such as satisfying controls and flashy effects.

## The Resulting Game

And this is the game that was created!

{{< game-iframe src="/game/polygon-impact/index.html" aspect-ratio="75%" >}}

**Controls:**

*   Move the mouse cursor to change the camera's viewpoint.
*   Click the mouse to fire projectiles.
*   Press the `ESC` key to release mouse focus.

It's quite simple, but you might feel a bit of 'juiciness' in the responsiveness to mouse movements and the effects.

## Generation Time and Points to Note

This game is actually self-contained within a single `index.html` file, and the code amounts to approximately 1500 lines.

When generating this with Gemini 2.5 Pro (the `gemini-2.5-pro-exp-03-25` model), it took about 180 seconds to output. That's quite a bit of time.

Based on this experience, it seems that aiming for around 1000 lines might be a good guideline when asking AI to generate code contained within a single file, in order to proceed with work within a realistic timeframe.

Of course, this can vary depending on the model's performance and server load, but please consider it as a general reference point.

## Summary

In this article, I introduced my attempt to generate a Three.js game using the latest free AI models like 'Gemini 2.5 Pro' and 'Trae Builder (Claude 3.7 Sonnet)'.

It's truly surprising that AI with such capabilities is available for free, and it seems like various things can be created depending on the ideas! I believe these are very useful tools, especially for projects intended for public release or for learning purposes.

While there might still be some quirks, such as the code generation time, I felt it was definitely worth trying.

Thank you for reading this far! I encourage you all to give it a try.