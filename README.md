# BrewCha 🧋

A milk tea & coffee ordering web app built with **PyScript** — Python runs directly in the browser via WebAssembly (Pyodide). Faithfully reproduces a 5-screen mobile design (Home, Menu, Product Detail, Cart, Checkout) and adapts gracefully to a desktop layout at wider viewports.

![Built with PyScript](https://img.shields.io/badge/PyScript-2024.11.1-FFD43B?logo=python&logoColor=white) ![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white) ![No backend deps](https://img.shields.io/badge/Backend-stdlib%20only-success)

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start (Windows)](#quick-start-windows)
- [Manual Setup](#manual-setup)
  - [1. Create the virtual environment](#1-create-the-virtual-environment)
  - [2. Run the dev server](#2-run-the-dev-server)
- [Usage Walkthrough](#usage-walkthrough)
- [Customizing the Menu](#customizing-the-menu)
- [Tech Notes](#tech-notes)
- [Troubleshooting](#troubleshooting)
- [Roadmap Ideas](#roadmap-ideas)

---

## Features

- **Mobile-faithful UI** — pixel-close reproduction of the BrewCha mockup screens with a bottom navigation bar (Home / Menu / Cart / Profile).
- **Responsive desktop layout** — top navigation, 4-column product grid, side-by-side product modal, 2-column checkout with a sticky order summary. Switches at the 820px breakpoint.
- **Custom SVG product illustrations** — every product gets a unique "BREW & CO" branded cup illustration generated from Python. Variants for boba, iced, latte, frappe, and add-on items (no emoji placeholders).
- **Live cart state** — quantity steppers, line-item totals, badge count on every cart icon, persistent until the order is placed.
- **Product customization** — Size (S/M/L with price deltas), Ice Level (0–100%), Sweetness Level (0–100%), and quantity.
- **Checkout flow** — Delivery vs. Pickup, payment method (GCash / Maya / Cash on Delivery), animated order-placed confirmation.
- **Zero backend dependencies** — runs on a single Python file using only the standard library.
- **Polished interactions** — toast notifications, smooth modal transitions, hover animations, keyboard support (Esc to close modal).

---

## Project Structure

```
Xyrex/
├── index.html          # PyScript shell + splash screen + Google Fonts
├── main.py             # The Python app — state, views, event handlers, SVG cups
├── style.css           # Design system, desktop styles, mobile media queries
├── serve.py            # Local dev server (Python stdlib only, no-cache headers)
├── run.bat             # One-click launcher for Windows
├── requirements.txt    # Empty — kept for future packages
├── venv/               # Local Python virtual environment (created by setup)
├── UI.png              # Original mobile design mockup (reference)
└── README.md           # You are here
```

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10 or newer | Only needed for the local dev server. The app itself runs in your browser. |
| Modern browser | Chrome / Edge / Firefox / Safari | Needs WebAssembly support (essentially every browser since 2019). |
| Internet (first load only) | — | PyScript and Pyodide are loaded from a CDN on the first visit, then cached. |

> Why a server? PyScript fetches `main.py` via HTTP, so opening `index.html` from the `file://` protocol won't work. Any static HTTP server is fine — `serve.py` is included for convenience.

---

## Quick Start (Windows)

Open the project folder and **double-click `run.bat`**.

It will:

1. Create the venv (`venv/`) if it doesn't exist yet.
2. Launch `serve.py` on `http://localhost:8000`.
3. Open your default browser to the app automatically.

To stop the server, press **Ctrl+C** in the terminal window or just close it.

---

## Manual Setup

If you'd rather see what's happening, run the steps yourself.

### 1. Create the virtual environment

```powershell
# Windows (PowerShell)
cd C:\Users\Desktop\Downloads\projects\Xyrex
python -m venv venv
```

```bash
# macOS / Linux
cd /path/to/Xyrex
python3 -m venv venv
```

The venv keeps any future dependencies isolated from your global Python. The app itself currently has **no Python package dependencies** — the `requirements.txt` file is intentionally empty.

If you later add packages (e.g., `flask`, `fastapi`), install them into the venv:

```powershell
# Windows
.\venv\Scripts\pip install -r requirements.txt
```

```bash
# macOS / Linux
./venv/bin/pip install -r requirements.txt
```

### 2. Run the dev server

```powershell
# Windows (PowerShell)
.\venv\Scripts\python.exe serve.py
```

```bash
# macOS / Linux
./venv/bin/python serve.py
```

You should see:

```
  🧋  BrewCha is brewing at http://localhost:8000
      Serving from: C:\Users\...\Xyrex
      Press Ctrl+C to stop.
```

Your browser will open automatically. If it doesn't, navigate to **http://localhost:8000** manually.

> **Port 8000 in use?** Edit `serve.py` and change `PORT = 8000` to any free port (e.g., 8080, 5500, 3000).

---

## Usage Walkthrough

1. **Splash screen** — a brief animated boba cup loads while PyScript boots Pyodide.
2. **Home** — browse "BEST SELLERS"; tap the hero **ORDER NOW** to jump to the full menu.
3. **Menu** — switch between **Milk Tea / Coffee / Specials / Add-ons** tabs. Tap any card to open the product detail, or hit the `+` button to quick-add with default options (Medium / 50% ice / 50% sugar).
4. **Product Detail** — pick **Size** (Small −₱10, Medium base, Large +₱15), **Ice Level**, **Sweetness Level**, and quantity. The button shows the live total.
5. **Cart** — adjust quantities or remove items. Tap "Add-ons" to jump into the add-ons category. Hit **CHECKOUT** when ready.
6. **Checkout** — choose **Delivery** (₱30, 25–35 min) or **Pickup** (free, 20 min). Pick a payment method. The sticky bottom bar (mobile) or the side summary (desktop) shows the running total. Tap **PLACE ORDER**.
7. **Success** — animated confirmation. Tap "Back to Home" to start a fresh order.

**Try the responsive layout:** resize your browser window — below 820px width, the UI swaps to the mobile mockup with the bottom navigation bar. Above that, you get the desktop layout with the top nav, grid, and modal.

**Keyboard shortcut:** press **Esc** to close the product detail modal.

---

## Customizing the Menu

All products live in the `PRODUCTS` list at the top of `main.py`. To add or modify items:

```python
PRODUCTS = [
    {
        "id": 99,                                # Unique integer
        "cat": "milk_tea",                       # milk_tea | coffee | specials | add_ons
        "name": "Cookie Butter Milk Tea",
        "desc": "Sweet cookie butter blended with creamy milk tea.",
        "price": 145,
        "color_a": "#E8C9A8",                    # SVG cup beverage gradient: top color
        "color_b": "#6B4423",                    # SVG cup beverage gradient: bottom color
        "kind": "boba",                          # boba | latte | ice | frappe | topping
        "best": False,                           # True → shows on Home "BEST SELLERS"
    },
    # ...
]
```

- **`kind`** controls the illustration details (pearls for `boba`, ice cubes for `ice`, cream foam for `latte`, cookie bits for `frappe`, a bowl for `topping`).
- **`color_a` / `color_b`** drive the beverage gradient — top → bottom.
- Save and refresh the browser. PyScript reloads `main.py` on every page load.

To change the size price deltas, edit the `SIZES` list. To change the ice/sweetness options, edit `LEVELS`.

---

## Tech Notes

- **PyScript 2024.11.1** is loaded from `pyscript.net`. The Python interpreter is Pyodide (CPython compiled to WebAssembly), and the runtime is shared across browser tabs via the HTTP cache.
- **No build step.** Edit any of the three source files and refresh — that's the entire dev loop.
- **State management** is a plain Python dict (`state`). The full HTML is re-rendered on every state change via `app.innerHTML = ...`. Event handling uses delegation: a single `click` listener on `document` walks up to find the closest `data-action` element, so re-rendering doesn't break listeners.
- **The `serve.py` helper** is a thin `http.server` wrapper that disables caching (so refreshes pick up edits immediately) and prints logs with a `[BrewCha]` prefix.
- **First load is ~10MB** (Pyodide + standard library). Subsequent loads come from the browser cache and start in well under a second.

---

## Troubleshooting

<details>
<summary><b>The browser shows a blank page or stays on the splash screen</b></summary>

- Open DevTools (F12) → Console tab. PyScript errors and Python tracebacks appear there.
- Make sure you're loading the page from `http://localhost:8000`, **not** from `file:///...`.
- Check your network — first load pulls Pyodide from a CDN.
</details>

<details>
<summary><b><code>UnicodeEncodeError</code> when starting <code>serve.py</code> on Windows</b></summary>

The boba emoji can't be encoded by the legacy `cp1252` console codepage. `serve.py` already calls `sys.stdout.reconfigure(encoding="utf-8")` and falls back to a plain `[BrewCha]` prefix if that fails. If you're on Python < 3.7 (which doesn't have `reconfigure`), upgrade Python or run with:

```powershell
$env:PYTHONIOENCODING = "utf-8"; .\venv\Scripts\python.exe serve.py
```
</details>

<details>
<summary><b>Port 8000 is already in use</b></summary>

Either stop the other process or change the port at the top of `serve.py`:

```python
PORT = 8080
```
</details>

<details>
<summary><b>I edited <code>main.py</code> and nothing changed</b></summary>

Hard-reload your browser tab (**Ctrl+Shift+R** / **Cmd+Shift+R**). The dev server already sends no-cache headers, but the browser may have cached PyScript's own assets.
</details>

<details>
<summary><b>"<code>python</code> is not recognized as a command"</b></summary>

Python isn't on your PATH. Reinstall Python from [python.org](https://python.org) with the **"Add Python to PATH"** checkbox enabled, or use the full path:

```powershell
"C:\Program Files\Python310\python.exe" -m venv venv
```
</details>

---

## Roadmap Ideas

If you'd like to extend the app:

- **Persist the cart** to `localStorage` (via `js.localStorage` in PyScript) so it survives page reloads.
- **Real product images** — swap the SVG cup placeholders for actual product photos (drop them in `assets/` and reference via `<img>` in `render_product_card_*`).
- **Order history** view in the Profile section.
- **Promo code input** on the checkout screen — the `BREWCHA20` banner is currently decorative.
- **Real payment integration** by adding a FastAPI/Flask backend (drop it into the venv via `requirements.txt`) and POSTing the order from PyScript with `pyodide.http`.

---

Made with ☕ and 🧋 — Brewed in Quezon City.
