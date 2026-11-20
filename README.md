# Airplane Game

A three-level airplane game written in Python with Pygame. The same Python files run on your computer and in a web browser. The browser copy is packaged with Pygbag 0.9.3. There is no login, database, or game server.

## Project files

These are the files you edit:

| File | What it does |
| --- | --- |
| `main.py` | The game loop, platforms, hazards, lives, and level changes |
| `player.py` | The airplane you control |
| `settings.py` | Window size, colors, and the three levels |
| `requirements.txt` | The two libraries the game needs |
| `pygbag.ini` | Tells Pygbag to skip the virtual environment when it builds the browser copy |

`build/web-cache/` is created by Pygbag and is listed in `.gitignore`. `build/web/`, including the hardened `index.html`, is not ignored, so it can be committed. Do not edit it by hand, except to add the integrity hash back to index.html after a rebuild.

## What you need

- Python 3.12
- The libraries in `requirements.txt`: Pygame and Pygbag

Install them once, from this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run it on your computer

```bash
source .venv/bin/activate
python main.py
```

Controls: arrow keys or A and D to move, Space to jump, R to retry a failed level.

## How the levels work

The game has three levels. Each one starts with 3 lives. The names are Above the Clouds, Sunset Flight, and The Storm. The layouts are in `settings.py`.

You stand on white platforms and jump toward the red HOME flag on the last platform. Touching that flag moves you to the next level and fills your lives back to 3. Falling off the bottom of the screen, touching a cloud, or touching another plane costs one life. The airplane is placed back at that level's start. When the lives reach 0, the level stops and the page says to press R. R starts only the current level again, with 3 lives.

Level 1 is a bright daytime sky with one cloud and one other plane. Level 2 is a sunset sky with more platforms, clouds, and planes. Level 3 is a dark storm with rain, fog, and faster planes. The rain is only a picture. It does not take a life.

The HOME flag on Level 3 shows "You Win!" for about two seconds. The game then starts again at Level 1 with 3 lives. Nothing is saved between runs.

## Build the browser copy

Pygbag packs `main.py`, `player.py`, and `settings.py` into a small archive and writes an HTML page that knows how to start that archive.

```bash
source .venv/bin/activate
python -m pygbag --build --app_name airplane-game --width 960 --height 540 --title "Airplane Game" main.py
```

`--width` and `--height` match the game window, 960 by 540, so the page is not a different size from the desktop game. `--app_name airplane-game` keeps the archive name free of spaces. The project folder itself can still be called `Airplane game`.

### Files the build creates

| File | What it is |
| --- | --- |
| `build/web/index.html` | The browser page. It contains the generated HTML and JavaScript shell. |
| `build/web/airplane.game.apk` | Your Python game, packed for the browser. This is not a phone app. |
| `build/web/airplane.game.tar.gz` | The same package in a second archive format. |
| `build/web/favicon.png` | The small icon copied from the Pygbag template. |
| `build/version.txt` | The Pygbag version that produced this build. |
| `build/web-cache/` | Files Pygbag downloaded while building. The game does not need this folder to run. |

Running the build again replaces these files.

## Open it in a browser

The page cannot be opened by double-clicking `index.html`. Browsers block parts of the game when the address starts with `file://`. Use a small local web server instead.

```bash
source .venv/bin/activate
python -m http.server 8001 --bind 127.0.0.1 --directory build/web
```

Then open [http://127.0.0.1:8001/](http://127.0.0.1:8001/).

Keep `--bind 127.0.0.1`. That limits the server to this computer. Do not remove it, and do not use `python -m http.server` as a public website. The server also sends its Python version in a response header. That is acceptable only because the server stays on this computer.

The first visit needs an internet connection. The page loads the Python interpreter, which is a WebAssembly program, from `https://pygame-web.github.io`. Your game code is the local `airplane.game.apk` file. After the interpreter is cached by the browser, later visits can be faster, but a new browser may need to download it again.

Click the game once so the keyboard goes to the game, then use the same keys as on the desktop.

The gray bars around the picture are the page background. The game itself stays 960 by 540 and is centered in the window.

## How the browser runs the game

Nothing in this project accepts accounts, passwords, or saved scores.

1. The browser asks the local server for `index.html`.
2. That page's JavaScript loads the Python WebAssembly runtime from the Pygbag site, `pygame-web.github.io`.
3. The same page downloads `airplane.game.apk` from the local server and runs your Python inside the WebAssembly interpreter.
4. Pygame draws into a canvas element on the page. The canvas is the game window.
5. When you press a key, the browser delivers that key to the canvas. Pygame reads it with the same event loop the desktop game uses. The key is not sent to another computer.
6. Lives, the current level, and the airplane position exist only in the page's memory. Closing the tab clears them.

So the parts that execute in the browser are:

- `index.html` and the JavaScript inside it, generated by Pygbag
- the Python WebAssembly runtime, downloaded from the Pygbag site
- your game, from `airplane.game.apk`

A database, login system, API, or other backend is not required. Adding one would not make this game more secure. The local `http.server` command only hands files to your own browser. It is not a public website.

For a security review, the third-party piece is the runtime from `pygame-web.github.io`. The integrity hash checks `pythons.js`. The rest of the runtime is still trusted from that site. The game's own rules stay in the Python files in this folder.

## Security note

The hardened `build/web/index.html` loads `pythons.js` with a Subresource Integrity hash. Rebuilding with Pygbag replaces `index.html`, so the hash must be added again after every build.

## AI tools used

This project was built in Cursor with help from its AI coding assistant. The assistant wrote and revised the Python game, the browser package, the security tests, and this README from directions in the chat. Danielle chose the game, the look, and the security changes, and played all three levels in the browser.
