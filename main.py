"""
BrewCha - PyScript Web UI
Faithful mobile reproduction + desktop adaptation of the BrewCha mockup.
"""

from pyscript import document, window
from pyodide.ffi import create_proxy
from js import setTimeout
import html as html_lib


# =====================================================================
# DATA — color_a / color_b are used to color the SVG cup beverage
# =====================================================================

PRODUCTS = [
    # Milk Tea
    {"id": 1,  "cat": "milk_tea", "name": "Brown Sugar Milk Tea",   "desc": "Classic milk tea with brown sugar pearls.",            "price": 120, "color_a": "#D2A878", "color_b": "#6B4423", "kind": "boba",  "best": True},
    {"id": 2,  "cat": "milk_tea", "name": "Matcha Milk Tea",        "desc": "Premium matcha with creamy milk.",                     "price": 130, "color_a": "#C5D89A", "color_b": "#6B8E23", "kind": "boba",  "best": False},
    {"id": 3,  "cat": "milk_tea", "name": "Wintermelon Milk Tea",   "desc": "Smooth wintermelon with milk and pearls.",             "price": 120, "color_a": "#F0E2C2", "color_b": "#B89968", "kind": "boba",  "best": False},
    {"id": 4,  "cat": "milk_tea", "name": "Taro Milk Tea",          "desc": "Creamy taro flavored milk tea with pearls.",           "price": 130, "color_a": "#D8B8DE", "color_b": "#8E6BA8", "kind": "boba",  "best": False},
    {"id": 5,  "cat": "milk_tea", "name": "Okinawa Milk Tea",       "desc": "Roasted Okinawa milk tea with pearls.",                "price": 130, "color_a": "#CDA67E", "color_b": "#5D3A1A", "kind": "boba",  "best": False},
    {"id": 6,  "cat": "milk_tea", "name": "Hokkaido Milk Tea",      "desc": "Smooth Hokkaido-style milk tea.",                      "price": 130, "color_a": "#EDD2A8", "color_b": "#9B7048", "kind": "boba",  "best": False},

    # Coffee
    {"id": 7,  "cat": "coffee",   "name": "Matcha Latte",           "desc": "Smooth matcha latte with creamy milk.",                "price": 130, "color_a": "#B0CD78", "color_b": "#4F7942", "kind": "latte", "best": True},
    {"id": 8,  "cat": "coffee",   "name": "Caramel Macchiato",      "desc": "Rich espresso with caramel.",                          "price": 135, "color_a": "#C9A079", "color_b": "#5D3A1A", "kind": "boba",  "best": True},
    {"id": 9,  "cat": "coffee",   "name": "Brown Sugar Latte",      "desc": "Espresso with brown sugar pearls.",                    "price": 140, "color_a": "#B8956A", "color_b": "#3C2415", "kind": "boba",  "best": False},
    {"id": 10, "cat": "coffee",   "name": "Iced Americano",         "desc": "Bold and refreshing iced americano.",                  "price": 110, "color_a": "#6B4423", "color_b": "#1A0D06", "kind": "ice",   "best": False},

    # Specials
    {"id": 11, "cat": "specials", "name": "BrewCha Signature",      "desc": "House's special blend of premium tea.",                "price": 150, "color_a": "#E8C39E", "color_b": "#8B5A2B", "kind": "boba",  "best": False},
    {"id": 12, "cat": "specials", "name": "Cookies & Cream Frappe", "desc": "Blended frappe with cookies and cream.",               "price": 145, "color_a": "#E8E4DC", "color_b": "#3C2415", "kind": "frappe","best": False},
    {"id": 13, "cat": "specials", "name": "Strawberry Yakult",      "desc": "Refreshing strawberry with yakult and pearls.",        "price": 140, "color_a": "#F5B7B1", "color_b": "#C0392B", "kind": "boba",  "best": False},

    # Add-ons
    {"id": 14, "cat": "add_ons",  "name": "Tapioca Pearls",         "desc": "Extra chewy boba pearls.",                             "price": 20,  "color_a": "#6B4423", "color_b": "#1A0D06", "kind": "topping","best": False},
    {"id": 15, "cat": "add_ons",  "name": "Pudding",                "desc": "Smooth, silky egg pudding topping.",                   "price": 25,  "color_a": "#F4D8A8", "color_b": "#D4A574", "kind": "topping","best": False},
    {"id": 16, "cat": "add_ons",  "name": "Cheese Foam",            "desc": "Sweet-and-salty cheese foam topping.",                 "price": 30,  "color_a": "#FFF4D6", "color_b": "#F0C75E", "kind": "topping","best": False},
    {"id": 17, "cat": "add_ons",  "name": "Crystal Boba",           "desc": "Translucent, jelly-like crystal boba.",                "price": 25,  "color_a": "#E0F2F1", "color_b": "#80CBC4", "kind": "topping","best": False},
]

CATEGORIES = [
    {"key": "milk_tea", "label": "Milk Tea"},
    {"key": "coffee",   "label": "Coffee"},
    {"key": "specials", "label": "Specials"},
    {"key": "add_ons",  "label": "Add-ons"},
]

SIZES = [
    {"key": "S", "label": "S", "delta": -10},
    {"key": "M", "label": "M", "delta": 0},
    {"key": "L", "label": "L", "delta": 15},
]
LEVELS = ["0%", "25%", "50%", "75%", "100%"]


# =====================================================================
# STATE
# =====================================================================

state = {
    "view": "home",        # home | menu | cart | checkout
    "category": "milk_tea",
    "cart": [],
    "modal_open": False,
    "current_product": None,
    "order_placed": False,
    "options": {"size": "M", "ice": "50%", "sweet": "50%", "qty": 1},
    "delivery_method": "delivery",
    "payment_method": "gcash",
}


def get_product(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return p
    return None


def products_by_category(cat):
    return [p for p in PRODUCTS if p["cat"] == cat]


def best_sellers():
    return [p for p in PRODUCTS if p["best"]]


def cart_subtotal():
    return sum(item["price"] * item["qty"] for item in state["cart"])


def cart_count():
    return sum(item["qty"] for item in state["cart"])


def delivery_fee():
    if not state["cart"]:
        return 0
    return 30 if state["delivery_method"] == "delivery" else 0


def cart_total():
    return cart_subtotal() + delivery_fee()


def esc(s):
    return html_lib.escape(str(s))


# =====================================================================
# SVG ICONS
# =====================================================================

ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="20" y1="20" x2="16.5" y2="16.5" stroke-linecap="round"/></svg>'
ICON_CART   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 7h14l-1.5 9a2 2 0 0 1-2 1.7H8.5a2 2 0 0 1-2-1.7L5 7Z"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/></svg>'
ICON_USER   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/></svg>'
ICON_HEART  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.5 6c-2.5 4.5-9.5 9-9.5 9z"/></svg>'
ICON_HOME   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V10"/></svg>'
ICON_MENU   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="7"  x2="19" y2="7"/><line x1="5" y1="12" x2="19" y2="12"/><line x1="5" y1="17" x2="19" y2="17"/></svg>'
ICON_BACK   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 6 9 12 15 18"/></svg>'
ICON_TRASH  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>'
ICON_CHEVRON_RIGHT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 6 15 12 9 18"/></svg>'
ICON_CHEVRON_DOWN  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
ICON_PIN    = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-7-7-12a7 7 0 0 1 14 0c0 5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>'
ICON_BIKE   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M12 17.5V14l-3-3 4-3 2 3h3"/></svg>'
ICON_WALLET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/><path d="M3 7l3-3h11"/><circle cx="16" cy="13" r="1.4" fill="currentColor"/></svg>'


# =====================================================================
# SVG CUP IMAGE PLACEHOLDER (BREW & CO style)
# =====================================================================

def cup_svg(p, variant="default"):
    """
    Generates an illustrated cup placeholder image based on product data.
    `variant` controls extra details:
      - 'default' : product card / cart thumbnail
      - 'hero'    : larger, with extra splash & background props (for hero / product detail)
      - 'topping' : for add-on items (no cup, just a bowl)
    """
    pid = p["id"]
    a, b = p["color_a"], p["color_b"]
    kind = p.get("kind", "boba")
    grad = f"bev{pid}"
    pearl_g = f"pearl{pid}"
    glass_g = f"glass{pid}"
    coaster_g = f"coast{pid}"

    if kind == "topping":
        return _topping_svg(p, grad, pearl_g)

    # pearls / boba
    pearls_svg = ""
    if kind in ("boba",):
        pearl_positions = [
            (78, 224, 7), (96, 232, 6), (114, 228, 7), (132, 236, 6),
            (150, 230, 7), (166, 238, 5), (88, 246, 6), (108, 244, 6),
            (128, 250, 6), (148, 246, 6), (164, 252, 5), (78, 240, 5),
            (118, 254, 5), (138, 256, 4), (155, 244, 4),
        ]
        for cx, cy, r in pearl_positions:
            pearls_svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{pearl_g})"/>'

    # ice cubes
    ice_svg = ""
    if kind == "ice":
        ices = [(78, 110, 22), (108, 100, 20), (135, 116, 18), (155, 102, 22)]
        for cx, cy, sz in ices:
            ice_svg += (
                f'<rect x="{cx}" y="{cy}" width="{sz}" height="{sz}" rx="3" '
                f'fill="rgba(255,255,255,0.55)" stroke="rgba(255,255,255,0.85)" stroke-width="1"/>'
            )

    # cream foam (matcha latte / latte styles)
    foam_svg = ""
    if kind == "latte":
        foam_svg = (
            '<ellipse cx="120" cy="98" rx="58" ry="10" fill="#FAF5EC"/>'
            '<ellipse cx="120" cy="95" rx="58" ry="8"  fill="#FFFFFF"/>'
        )

    # cookies for frappe
    cookies_svg = ""
    if kind == "frappe":
        cookies_svg = (
            '<circle cx="90"  cy="118" r="6" fill="#3C2415"/>'
            '<circle cx="115" cy="108" r="7" fill="#3C2415"/>'
            '<circle cx="142" cy="120" r="6" fill="#3C2415"/>'
            '<circle cx="160" cy="110" r="5" fill="#3C2415"/>'
        )

    return f"""
    <svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg" class="cup-svg" aria-label="{esc(p['name'])} illustration">
      <defs>
        <linearGradient id="{grad}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"  stop-color="{a}"/>
          <stop offset="60%" stop-color="{a}"/>
          <stop offset="100%" stop-color="{b}"/>
        </linearGradient>
        <radialGradient id="{pearl_g}" cx="35%" cy="30%" r="65%">
          <stop offset="0%"  stop-color="#5D3A1A"/>
          <stop offset="100%" stop-color="#0F0805"/>
        </radialGradient>
        <linearGradient id="{glass_g}" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%"   stop-color="rgba(255,255,255,0.45)"/>
          <stop offset="50%"  stop-color="rgba(255,255,255,0.0)"/>
          <stop offset="100%" stop-color="rgba(255,255,255,0.20)"/>
        </linearGradient>
        <linearGradient id="{coaster_g}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   stop-color="#A67B5B"/>
          <stop offset="100%" stop-color="#6B4423"/>
        </linearGradient>
      </defs>

      <!-- shadow under cup -->
      <ellipse cx="120" cy="288" rx="78" ry="6" fill="rgba(0,0,0,0.18)"/>

      <!-- wooden coaster -->
      <ellipse cx="120" cy="280" rx="92" ry="11" fill="url(#{coaster_g})"/>
      <ellipse cx="120" cy="276" rx="86" ry="8"  fill="#C9A079" opacity="0.6"/>

      <!-- glass cup back wall -->
      <path d="M 60 80 L 180 80 L 168 272 L 72 272 Z" fill="rgba(255,255,255,0.18)"/>

      <!-- beverage liquid -->
      <path d="M 62 86 L 178 86 L 167 270 L 73 270 Z" fill="url(#{grad})"/>

      {foam_svg}
      {ice_svg}
      {cookies_svg}
      {pearls_svg}

      <!-- glass outline + highlight -->
      <path d="M 60 80 L 180 80 L 168 272 L 72 272 Z" fill="url(#{glass_g})"/>
      <path d="M 60 80 L 180 80 L 168 272 L 72 272 Z" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>
      <path d="M 64 90 L 70 90 L 78 268 L 72 268 Z" fill="rgba(255,255,255,0.4)"/>
      <path d="M 165 92 L 169 92 L 162 265 L 158 265 Z" fill="rgba(255,255,255,0.25)"/>

      <!-- lid -->
      <ellipse cx="120" cy="76" rx="62" ry="7" fill="#3C2415"/>
      <rect x="58" y="70" width="124" height="13" rx="3" fill="#5D3A1A"/>
      <rect x="58" y="68" width="124" height="5"  rx="2" fill="#3C2415"/>
      <ellipse cx="120" cy="71" rx="58" ry="3.5" fill="#7A4F2A"/>

      <!-- straw -->
      <g transform="rotate(10 119 45)">
        <rect x="113" y="14" width="11" height="62" rx="2" fill="#3C2415"/>
        <rect x="115" y="14" width="3"  height="62" rx="1" fill="#5D3A1A"/>
      </g>

      <!-- BREW & CO logo bubble -->
      <circle cx="120" cy="172" r="26" fill="#FAF5EC" opacity="0.96"/>
      <circle cx="120" cy="172" r="26" fill="none" stroke="#3C2415" stroke-width="0.7" opacity="0.5"/>
      <text x="120" y="169" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#3C2415" letter-spacing="0.5">BREW</text>
      <line x1="105" y1="174" x2="135" y2="174" stroke="#3C2415" stroke-width="0.6"/>
      <text x="120" y="184" text-anchor="middle" font-family="Georgia, serif" font-size="7"  font-weight="600" fill="#3C2415" letter-spacing="1.2">&amp; CO</text>
    </svg>
    """


def _topping_svg(p, grad, pearl_g):
    """Bowl-shape illustration for add-ons."""
    pid = p["id"]
    a, b = p["color_a"], p["color_b"]
    contents = ""
    if "Pearl" in p["name"] or "Boba" in p["name"]:
        positions = [
            (90, 150, 8), (110, 145, 9), (130, 152, 8), (150, 148, 9),
            (95, 168, 9), (118, 165, 8), (138, 170, 9), (158, 167, 8),
            (108, 180, 8), (130, 183, 9), (148, 180, 8),
        ]
        for cx, cy, r in positions:
            contents += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{pearl_g})"/>'
    else:
        contents = (
            f'<ellipse cx="120" cy="160" rx="55" ry="22" fill="{a}"/>'
            f'<ellipse cx="120" cy="156" rx="50" ry="15" fill="{b}" opacity="0.5"/>'
        )

    return f"""
    <svg viewBox="0 0 240 260" xmlns="http://www.w3.org/2000/svg" class="cup-svg" aria-label="{esc(p['name'])} illustration">
      <defs>
        <radialGradient id="{pearl_g}" cx="35%" cy="30%" r="65%">
          <stop offset="0%"  stop-color="#5D3A1A"/>
          <stop offset="100%" stop-color="#0F0805"/>
        </radialGradient>
        <linearGradient id="{grad}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"  stop-color="#FFFFFF"/>
          <stop offset="100%" stop-color="#E8DCC8"/>
        </linearGradient>
      </defs>
      <!-- shadow -->
      <ellipse cx="120" cy="230" rx="85" ry="6" fill="rgba(0,0,0,0.18)"/>
      <!-- bowl -->
      <path d="M 50 150 Q 50 220 120 220 Q 190 220 190 150 Z" fill="url(#{grad})"/>
      <!-- contents -->
      {contents}
      <!-- bowl rim -->
      <ellipse cx="120" cy="150" rx="70" ry="14" fill="#FFFFFF"/>
      <ellipse cx="120" cy="150" rx="70" ry="14" fill="none" stroke="#E8DCC8" stroke-width="1.5"/>
      <ellipse cx="120" cy="146" rx="62" ry="9"  fill="#FAF5EC"/>
    </svg>
    """


# =====================================================================
# HERO ILLUSTRATION (for home hero panel)
# =====================================================================

def hero_illustration():
    """A bigger, dressier composition with the BREW cup, cream splash, and floating pearls."""
    return """
    <svg viewBox="0 0 320 360" xmlns="http://www.w3.org/2000/svg" class="hero-art" aria-label="Brown sugar milk tea hero">
      <defs>
        <linearGradient id="hero-bev" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"  stop-color="#D2A878"/>
          <stop offset="60%" stop-color="#A77845"/>
          <stop offset="100%" stop-color="#5D3A1A"/>
        </linearGradient>
        <radialGradient id="hero-pearl" cx="35%" cy="30%" r="65%">
          <stop offset="0%"  stop-color="#5D3A1A"/>
          <stop offset="100%" stop-color="#0F0805"/>
        </radialGradient>
        <linearGradient id="hero-coaster" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#A67B5B"/><stop offset="100%" stop-color="#6B4423"/>
        </linearGradient>
      </defs>

      <!-- cream splash behind cup -->
      <path d="M 60 130 Q 30 100 60 80 Q 90 60 130 80 L 120 130 Z" fill="#FAF5EC" opacity="0.85"/>
      <path d="M 250 140 Q 290 120 280 80 Q 250 50 220 80 L 240 140 Z" fill="#FAF5EC" opacity="0.85"/>
      <path d="M 100 60 Q 160 30 220 60 L 200 110 L 140 110 Z" fill="#FFFFFF" opacity="0.85"/>

      <!-- floating pearls (splashed) -->
      <circle cx="40"  cy="120" r="8" fill="url(#hero-pearl)"/>
      <circle cx="280" cy="130" r="9" fill="url(#hero-pearl)"/>
      <circle cx="50"  cy="170" r="6" fill="url(#hero-pearl)"/>
      <circle cx="270" cy="180" r="7" fill="url(#hero-pearl)"/>
      <circle cx="30"  cy="220" r="7" fill="url(#hero-pearl)"/>
      <circle cx="290" cy="230" r="6" fill="url(#hero-pearl)"/>
      <circle cx="60"  cy="270" r="5" fill="url(#hero-pearl)"/>
      <circle cx="280" cy="280" r="8" fill="url(#hero-pearl)"/>
      <circle cx="80"  cy="60"  r="6" fill="url(#hero-pearl)"/>
      <circle cx="200" cy="50"  r="7" fill="url(#hero-pearl)"/>

      <!-- shadow -->
      <ellipse cx="160" cy="345" rx="90" ry="6" fill="rgba(0,0,0,0.15)"/>
      <!-- coaster -->
      <ellipse cx="160" cy="338" rx="100" ry="11" fill="url(#hero-coaster)"/>
      <ellipse cx="160" cy="335" rx="95"  ry="8"  fill="#C9A079" opacity="0.6"/>

      <!-- cup back -->
      <path d="M 90 130 L 230 130 L 218 332 L 102 332 Z" fill="rgba(255,255,255,0.18)"/>
      <!-- beverage -->
      <path d="M 92 136 L 228 136 L 217 330 L 103 330 Z" fill="url(#hero-bev)"/>

      <!-- pearls in cup -->
      <g fill="url(#hero-pearl)">
        <circle cx="108" cy="270" r="8"/><circle cx="128" cy="278" r="7"/>
        <circle cx="148" cy="272" r="8"/><circle cx="168" cy="280" r="7"/>
        <circle cx="188" cy="274" r="8"/><circle cx="208" cy="280" r="6"/>
        <circle cx="118" cy="290" r="7"/><circle cx="140" cy="295" r="7"/>
        <circle cx="160" cy="298" r="7"/><circle cx="182" cy="295" r="7"/>
        <circle cx="200" cy="290" r="6"/><circle cx="100" cy="282" r="5"/>
        <circle cx="148" cy="310" r="6"/><circle cx="170" cy="312" r="5"/>
      </g>

      <!-- glass overlay -->
      <path d="M 90 130 L 230 130 L 218 332 L 102 332 Z" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.8"/>
      <path d="M 96 140 L 104 140 L 112 326 L 104 326 Z" fill="rgba(255,255,255,0.4)"/>

      <!-- lid -->
      <ellipse cx="160" cy="126" rx="72" ry="8" fill="#3C2415"/>
      <rect x="88" y="118" width="144" height="15" rx="3" fill="#5D3A1A"/>
      <rect x="88" y="116" width="144" height="6"  rx="2" fill="#3C2415"/>
      <ellipse cx="160" cy="121" rx="68" ry="4" fill="#7A4F2A"/>

      <!-- straw -->
      <g transform="rotate(10 158 80)">
        <rect x="152" y="40" width="13" height="80" rx="2.5" fill="#3C2415"/>
        <rect x="155" y="40" width="3.5" height="80" rx="1" fill="#5D3A1A"/>
      </g>

      <!-- label -->
      <circle cx="160" cy="215" r="32" fill="#FAF5EC" opacity="0.97"/>
      <circle cx="160" cy="215" r="32" fill="none" stroke="#3C2415" stroke-width="0.7" opacity="0.5"/>
      <text x="160" y="212" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700" fill="#3C2415" letter-spacing="0.6">BREW</text>
      <line x1="142" y1="217" x2="178" y2="217" stroke="#3C2415" stroke-width="0.7"/>
      <text x="160" y="230" text-anchor="middle" font-family="Georgia, serif" font-size="9"  font-weight="600" fill="#3C2415" letter-spacing="1.4">&amp; CO</text>
    </svg>
    """


# =====================================================================
# HEADERS (mobile + desktop)
# =====================================================================

def render_desktop_nav():
    count = cart_count()
    badge_html = f'<span class="cart-badge">{count}</span>' if count > 0 else ""
    nav_items = [
        ("home", "Home"),
        ("menu", "Menu"),
        ("about", "About"),
        ("contact", "Contact"),
    ]
    links = "".join(
        f'<li class="nav-link {"active" if state["view"] == k else ""}" data-action="navigate" data-view="{k}">{label}</li>'
        for k, label in nav_items
    )
    return f"""
    <nav class="navbar navbar-desktop">
      <div class="nav-inner">
        <div class="nav-brand" data-action="navigate" data-view="home">BrewCha</div>
        <ul class="nav-links">{links}</ul>
        <div class="nav-actions">
          <button class="icon-btn" title="Search">{ICON_SEARCH}</button>
          <button class="icon-btn" title="Cart" data-action="navigate" data-view="cart">
            {ICON_CART}{badge_html}
          </button>
          <button class="icon-btn" title="Profile">{ICON_USER}</button>
        </div>
      </div>
    </nav>
    """


def render_mobile_header():
    """Different headers per view, matching the mobile mockup screens."""
    v = state["view"]
    count = cart_count()
    badge_html = f'<span class="m-badge">{count}</span>' if count > 0 else ""

    if v == "home":
        return f"""
        <header class="m-header m-header-home">
          <div class="m-brand">BrewCha</div>
          <button class="m-icon-btn" title="Search">{ICON_SEARCH}</button>
        </header>
        """
    if v == "menu":
        return f"""
        <header class="m-header">
          <button class="m-icon-btn" data-action="navigate" data-view="home" title="Back">{ICON_BACK}</button>
          <div class="m-title">MENU</div>
          <button class="m-icon-btn m-icon-btn--cart" data-action="navigate" data-view="cart" title="Cart">
            {ICON_CART}{badge_html}
          </button>
        </header>
        """
    if v == "cart":
        return f"""
        <header class="m-header">
          <button class="m-icon-btn" data-action="back" title="Back">{ICON_BACK}</button>
          <div class="m-title">CART</div>
          <span class="m-icon-spacer"></span>
        </header>
        """
    if v == "checkout":
        return f"""
        <header class="m-header">
          <button class="m-icon-btn" data-action="navigate" data-view="cart" title="Back">{ICON_BACK}</button>
          <div class="m-title">CHECKOUT</div>
          <span class="m-icon-spacer"></span>
        </header>
        """
    return ""


def render_bottom_nav():
    items = [
        ("home", "Home", ICON_HOME),
        ("menu", "Menu", ICON_MENU),
        ("cart", "Cart", ICON_CART),
        ("profile", "Profile", ICON_USER),
    ]
    count = cart_count()
    parts = []
    for key, label, icon in items:
        active = "active" if state["view"] == key else ""
        badge = ""
        if key == "cart" and count > 0:
            badge = f'<span class="bnav-badge">{count}</span>'
        parts.append(f"""
            <button class="bnav-item {active}" data-action="navigate" data-view="{key}">
              <span class="bnav-icon">{icon}{badge}</span>
              <span class="bnav-label">{label}</span>
            </button>
        """)
    return f'<nav class="bottom-nav">{"".join(parts)}</nav>'


# =====================================================================
# PRODUCT CARDS
# =====================================================================

def render_product_card_grid(p, tag=None):
    """Desktop grid card."""
    tag_html = f'<span class="product-tag">{esc(tag)}</span>' if tag else ""
    return f"""
    <div class="product-card" data-action="open_product" data-product-id="{p['id']}">
      <div class="product-img">
        {tag_html}
        {cup_svg(p)}
      </div>
      <div class="product-info">
        <div class="product-name">{esc(p['name'])}</div>
        <div class="product-desc">{esc(p['desc'])}</div>
        <div class="product-footer">
          <div class="product-price">{p['price']}</div>
          <button class="product-add" data-action="quick_add" data-product-id="{p['id']}" title="Add">+</button>
        </div>
      </div>
    </div>
    """


def render_product_card_list(p):
    """Mobile list card — image left, info middle, + button right (matches mockup)."""
    return f"""
    <div class="product-row" data-action="open_product" data-product-id="{p['id']}">
      <div class="product-row-img">{cup_svg(p)}</div>
      <div class="product-row-info">
        <div class="product-row-name">{esc(p['name'])}</div>
        <div class="product-row-desc">{esc(p['desc'])}</div>
        <div class="product-row-price">₱{p['price']}</div>
      </div>
      <button class="product-row-add" data-action="quick_add" data-product-id="{p['id']}" title="Add">+</button>
    </div>
    """


def render_product_card(p, tag=None):
    """Renders both the grid version and the list version — CSS shows the right one."""
    grid = render_product_card_grid(p, tag=tag)
    row  = render_product_card_list(p)
    return f'<div class="product-wrap">{grid}{row}</div>'


# =====================================================================
# HOME VIEW
# =====================================================================

def render_hero():
    return f"""
    <section class="hero">
      <div class="hero-panel">
        <div class="hero-art-wrap">{hero_illustration()}</div>
        <div class="hero-content">
          <span class="hero-eyebrow">Premium Boba Experience</span>
          <h1 class="hero-title">Your Daily<br><em>cup of</em><br>Happiness</h1>
          <p class="hero-sub">Hand-crafted milk tea, signature brews, and decadent toppings.</p>
          <button class="btn btn-primary btn-lg" data-action="navigate" data-view="menu">ORDER NOW</button>
        </div>
      </div>
    </section>
    """


def render_best_sellers():
    cards = "".join(render_product_card(p, tag="Best Seller") for p in best_sellers())
    return f"""
    <section class="section" id="best-sellers">
      <div class="section-head">
        <h2 class="section-title">BEST SELLERS</h2>
        <span class="section-link" data-action="navigate" data-view="menu">View all →</span>
      </div>
      <div class="product-grid">{cards}</div>
    </section>
    """


def render_promo():
    return """
    <section class="promo">
      <div>
        <h2>First Order? Get 20% Off</h2>
        <p>Use code <strong>BREWCHA20</strong> on your first delivery. Limited time only.</p>
        <button class="btn" data-action="navigate" data-view="menu">Order Now</button>
      </div>
      <div class="promo-emoji">🎉</div>
    </section>
    """


def render_footer():
    return """
    <footer class="footer">
      <div class="footer-inner">
        <div>
          <div class="footer-brand">BrewCha</div>
          <div class="footer-text">Your daily cup of happiness.<br>
            Hand-crafted milk tea & coffee, brewed fresh every day.</div>
        </div>
        <div>
          <h4>Shop</h4>
          <ul><li>Milk Tea</li><li>Coffee</li><li>Specials</li><li>Add-ons</li></ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul><li>About Us</li><li>Locations</li><li>Careers</li><li>Press</li></ul>
        </div>
        <div>
          <h4>Support</h4>
          <ul><li>Help Center</li><li>Order Status</li><li>Contact</li><li>FAQ</li></ul>
        </div>
      </div>
      <div class="footer-bottom">© 2026 BrewCha. Brewed with care in Quezon City.</div>
    </footer>
    """


def render_home():
    return render_hero() + render_best_sellers() + render_promo() + render_footer()


# =====================================================================
# MENU VIEW
# =====================================================================

def render_menu():
    tabs = "".join(
        f'<button class="category-tab {"active" if state["category"] == c["key"] else ""}" '
        f'data-action="select_category" data-category="{c["key"]}">{c["label"]}</button>'
        for c in CATEGORIES
    )
    items = products_by_category(state["category"])
    cards = "".join(render_product_card(p) for p in items)
    cat_label = next(c["label"] for c in CATEGORIES if c["key"] == state["category"])
    return f"""
    <section class="section">
      <div class="section-head section-head-desktop">
        <div>
          <h2 class="section-title">Menu</h2>
          <div class="section-sub">Browse our full {esc(cat_label.lower())} selection</div>
        </div>
      </div>
      <div class="category-tabs">{tabs}</div>
      <div class="product-grid product-grid-menu">{cards}</div>
    </section>
    {render_footer()}
    """


# =====================================================================
# PRODUCT MODAL / DETAIL VIEW
# =====================================================================

def option_price():
    p = state["current_product"]
    if not p:
        return 0
    delta = next((s["delta"] for s in SIZES if s["key"] == state["options"]["size"]), 0)
    return (p["price"] + delta) * state["options"]["qty"]


def render_size_chip(s, current):
    active = "active" if s["key"] == current else ""
    sub = f'<span class="chip-sub">₱{s["delta"]:+d}</span>' if s["delta"] != 0 else '<span class="chip-sub">base</span>'
    return f"""
      <button class="chip chip-size {active}" data-action="set_option" data-option="size" data-value="{s["key"]}">
        <span class="chip-main">{s["label"]}</span>
        {sub}
      </button>
    """


def render_chips(group_key, values, current):
    chips = []
    for v in values:
        active = "active" if v == current else ""
        chips.append(
            f'<button class="chip {active}" data-action="set_option" '
            f'data-option="{group_key}" data-value="{v}">{v}</button>'
        )
    return "".join(chips)


def render_product_detail_panel():
    """Inner contents — used by both the modal (desktop) and the full-page mobile view."""
    if not state["current_product"]:
        return ""
    p = state["current_product"]
    opts = state["options"]
    size_chips = "".join(render_size_chip(s, opts["size"]) for s in SIZES)
    ice_chips = render_chips("ice", LEVELS, opts["ice"])
    sweet_chips = render_chips("sweet", LEVELS, opts["sweet"])
    total = option_price()

    return f"""
      <div class="detail-image-wrap">
        <button class="detail-back" data-action="close_modal" title="Back">{ICON_BACK}</button>
        <button class="detail-fav" title="Favorite">{ICON_HEART}</button>
        {cup_svg(p, variant='hero')}
        <div class="detail-dots"><span class="active"></span><span></span><span></span></div>
      </div>
      <div class="detail-body">
        <div class="detail-title-row">
          <h2 class="detail-name">{esc(p['name'])}</h2>
          <div class="detail-price">₱{p['price']}</div>
        </div>
        <p class="detail-desc">{esc(p['desc'])}</p>

        <div class="option-group">
          <div class="option-label">Size</div>
          <div class="option-chips size-chips">{size_chips}</div>
        </div>
        <div class="option-group">
          <div class="option-label">Ice Level</div>
          <div class="option-chips">{ice_chips}</div>
        </div>
        <div class="option-group">
          <div class="option-label">Sweetness Level</div>
          <div class="option-chips">{sweet_chips}</div>
        </div>

        <div class="detail-actions">
          <div class="quantity">
            <button class="qty-btn" data-action="change_qty" data-dir="-1">−</button>
            <span class="qty-val">{opts['qty']}</span>
            <button class="qty-btn" data-action="change_qty" data-dir="1">+</button>
          </div>
          <button class="btn btn-primary btn-lg btn-add-cart" data-action="add_to_cart">
            ADD TO CART · ₱{total}
          </button>
        </div>
      </div>
    """


def render_product_modal():
    if not state["modal_open"] or not state["current_product"]:
        return ""
    return f"""
    <div class="modal-overlay" data-action="close_modal">
      <div class="modal" data-stop="1">
        {render_product_detail_panel()}
      </div>
    </div>
    """


# =====================================================================
# CART VIEW
# =====================================================================

def render_cart_item(item, idx):
    item_p = get_product(item["pid"]) or item
    return f"""
    <div class="cart-item">
      <div class="cart-item-img">{cup_svg(item_p)}</div>
      <div class="cart-item-info">
        <div class="cart-item-head">
          <div class="cart-item-name">{esc(item['name'])}</div>
          <button class="cart-item-trash" data-action="remove_cart" data-idx="{idx}" title="Remove">{ICON_TRASH}</button>
        </div>
        <div class="cart-item-meta">Size: {item['size']} · {item['sweet']} Sugar · {item['ice']} Ice</div>
        <div class="cart-item-bottom">
          <div class="cart-item-price">₱{item['price'] * item['qty']}</div>
          <div class="quantity quantity-sm">
            <button class="qty-btn" data-action="cart_qty" data-idx="{idx}" data-dir="-1">−</button>
            <span class="qty-val">{item['qty']}</span>
            <button class="qty-btn" data-action="cart_qty" data-idx="{idx}" data-dir="1">+</button>
          </div>
        </div>
      </div>
    </div>
    """


def render_cart_view():
    if not state["cart"]:
        body = f"""
        <div class="cart-empty">
          <div class="cart-empty-emoji">🛒</div>
          <h3>Your cart is empty</h3>
          <p>Add a delicious brew to get started.</p>
          <button class="btn btn-primary" data-action="navigate" data-view="menu">Browse Menu</button>
        </div>
        """
    else:
        items = "".join(render_cart_item(it, i) for i, it in enumerate(state["cart"]))
        body = f"""
        <div class="cart-items">{items}</div>

        <div class="cart-add-more-label">Add more items</div>
        <div class="cart-add-more" data-action="select_category" data-category="add_ons">
          <div>
            <strong>Add-ons</strong>
            <small>Toppings, Pearls, Milk, etc.</small>
          </div>
          <span class="cart-add-arrow">{ICON_CHEVRON_RIGHT}</span>
        </div>

        <div class="cart-summary">
          <div class="summary-row"><span>Subtotal</span><span class="val">₱{cart_subtotal()}</span></div>
          <div class="summary-row"><span>Delivery Fee</span><span class="val">₱{delivery_fee()}</span></div>
          <div class="summary-row total"><span>Total</span><span class="val">₱{cart_total()}</span></div>
        </div>

        <div class="cart-checkout-wrap">
          <button class="btn btn-primary btn-block btn-lg" data-action="navigate" data-view="checkout">CHECKOUT</button>
        </div>
        """
    return f"""
    <section class="page page-cart">
      <div class="page-inner">
        <h1 class="page-title page-title-desktop">Your Cart</h1>
        {body}
      </div>
    </section>
    """


# =====================================================================
# CHECKOUT VIEW
# =====================================================================

def render_checkout_view():
    if not state["cart"]:
        return f"""
        <section class="page page-cart">
          <div class="page-inner">
            <div class="cart-empty">
              <div class="cart-empty-emoji">🛒</div>
              <h3>No items to checkout</h3>
              <button class="btn btn-primary" data-action="navigate" data-view="menu">Browse Menu</button>
            </div>
          </div>
        </section>
        """

    delivery_active = "active" if state["delivery_method"] == "delivery" else ""
    pickup_active = "active" if state["delivery_method"] == "pickup" else ""

    payments = [
        ("gcash", "GCash",            "Pay via GCash e-wallet",       ICON_WALLET, "#0085FF"),
        ("maya",  "Maya",             "Pay via Maya e-wallet",        ICON_WALLET, "#00C97F"),
        ("cod",   "Cash on Delivery", "Pay when your order arrives",  ICON_WALLET, "#8B5A2B"),
    ]
    payment_rows = "".join(
        f"""
        <div class="option-row {'active' if state['payment_method'] == k else ''}"
             data-action="set_payment" data-method="{k}">
          <div class="option-radio"></div>
          <div class="option-icon" style="color: {color};">{icon}</div>
          <div class="option-content">
            <strong>{label}</strong>
            <small>{sub}</small>
          </div>
        </div>
        """
        for k, label, sub, icon, color in payments
    )

    cart_items = "".join(render_cart_item(it, i) for i, it in enumerate(state["cart"]))

    return f"""
    <section class="page page-checkout">
      <div class="page-inner">
        <h1 class="page-title page-title-desktop">Checkout</h1>
        <div class="checkout-grid">
          <div class="checkout-main">
            <div class="checkout-section">
              <h3>Delivery Method</h3>
              <div class="option-row option-row-tall {delivery_active}" data-action="set_delivery" data-method="delivery">
                <div class="option-radio"></div>
                <div class="option-icon">{ICON_BIKE}</div>
                <div class="option-content">
                  <strong>Delivery</strong>
                  <small>(₱30, 25–35 min)</small>
                </div>
                <span class="option-chevron">{ICON_CHEVRON_DOWN}</span>
              </div>
              <div class="option-row option-row-tall {pickup_active}" data-action="set_delivery" data-method="pickup">
                <div class="option-radio"></div>
                <div class="option-icon">{ICON_PIN}</div>
                <div class="option-content">
                  <strong>Pick up</strong>
                  <small>(123 Coffee St, Barangay 12, Quezon City)</small>
                </div>
                <span class="option-time">20 min</span>
              </div>
            </div>

            <div class="checkout-section">
              <h3>Payment Method</h3>
              {payment_rows}
            </div>
          </div>

          <aside class="checkout-summary">
            <div class="checkout-section summary-card">
              <h3>Order Summary</h3>
              <div class="summary-items">{cart_items}</div>
              <div class="cart-summary">
                <div class="summary-row"><span>Subtotal</span><span class="val">₱{cart_subtotal()}</span></div>
                <div class="summary-row"><span>Delivery Fee</span><span class="val">₱{delivery_fee()}</span></div>
                <div class="summary-row total"><span>Total</span><span class="val">₱{cart_total()}</span></div>
              </div>
            </div>
          </aside>
        </div>

        <div class="checkout-total-bar">
          <div>
            <small>Total</small>
            <strong>₱{cart_total()}</strong>
          </div>
          <button class="btn btn-primary btn-lg" data-action="place_order">PLACE ORDER</button>
        </div>
      </div>
    </section>
    """


# =====================================================================
# SUCCESS
# =====================================================================

def render_success():
    if not state["order_placed"]:
        return ""
    return """
    <div class="success-screen">
      <div class="success-card">
        <div class="success-icon">✓</div>
        <h2>Order Placed!</h2>
        <p>Thank you for choosing BrewCha. Your order is being brewed and will arrive soon.</p>
        <button class="btn btn-primary btn-block btn-lg" data-action="finish_order">Back to Home</button>
      </div>
    </div>
    """


# =====================================================================
# MAIN RENDER
# =====================================================================

def render():
    v = state["view"]
    if v == "home":
        main_view = render_home()
    elif v == "menu":
        main_view = render_menu()
    elif v == "cart":
        main_view = render_cart_view()
    elif v == "checkout":
        main_view = render_checkout_view()
    else:
        main_view = render_home()

    html_str = (
        '<div class="app-root">'
        + render_desktop_nav()
        + render_mobile_header()
        + main_view
        + render_bottom_nav()
        + "</div>"
        + render_product_modal()
        + render_success()
    )
    app = document.getElementById("app")
    app.innerHTML = html_str


# =====================================================================
# TOAST
# =====================================================================

def toast(message):
    host = document.getElementById("toast-host")
    el = document.createElement("div")
    el.className = "toast"
    el.innerHTML = f'<span style="font-size:1rem;">✓</span><span>{esc(message)}</span>'
    host.appendChild(el)

    def remove(*_):
        try:
            host.removeChild(el)
        except Exception:
            pass

    setTimeout(create_proxy(remove), 2600)


# =====================================================================
# EVENT HANDLING
# =====================================================================

def find_action(target):
    el = target
    while el and getattr(el, "nodeType", None) == 1:
        if el.hasAttribute and el.hasAttribute("data-action"):
            return el
        el = el.parentElement
    return None


def handle_click(event):
    el = find_action(event.target)
    if not el:
        return
    action = el.getAttribute("data-action")

    if action == "navigate":
        view = el.getAttribute("data-view")
        if view in ("home", "menu", "cart", "checkout"):
            state["view"] = view
            state["modal_open"] = False
            window.scrollTo(0, 0)
            render()
        else:
            toast(f"{view.title()} page coming soon!")

    elif action == "back":
        prev = "menu" if state["view"] == "cart" else "home"
        state["view"] = prev
        window.scrollTo(0, 0)
        render()

    elif action == "select_category":
        state["category"] = el.getAttribute("data-category")
        if state["view"] != "menu":
            state["view"] = "menu"
            window.scrollTo(0, 0)
        render()

    elif action == "open_product":
        pid = int(el.getAttribute("data-product-id"))
        p = get_product(pid)
        if p:
            state["current_product"] = p
            state["options"] = {"size": "M", "ice": "50%", "sweet": "50%", "qty": 1}
            state["modal_open"] = True
            render()

    elif action == "close_modal":
        state["modal_open"] = False
        state["current_product"] = None
        render()

    elif action == "set_option":
        opt = el.getAttribute("data-option")
        val = el.getAttribute("data-value")
        state["options"][opt] = val
        render()

    elif action == "change_qty":
        d = int(el.getAttribute("data-dir"))
        new_q = max(1, min(20, state["options"]["qty"] + d))
        state["options"]["qty"] = new_q
        render()

    elif action == "add_to_cart":
        if state["current_product"]:
            add_current_to_cart()

    elif action == "quick_add":
        pid = int(el.getAttribute("data-product-id"))
        p = get_product(pid)
        if p:
            state["cart"].append({
                "pid": p["id"],
                "name": p["name"],
                "color_a": p["color_a"],
                "color_b": p["color_b"],
                "price": p["price"],
                "size": "M",
                "ice": "50%",
                "sweet": "50%",
                "qty": 1,
            })
            toast(f"{p['name']} added to cart")
            render()

    elif action == "cart_qty":
        idx = int(el.getAttribute("data-idx"))
        d = int(el.getAttribute("data-dir"))
        if 0 <= idx < len(state["cart"]):
            state["cart"][idx]["qty"] = max(1, min(20, state["cart"][idx]["qty"] + d))
            render()

    elif action == "remove_cart":
        idx = int(el.getAttribute("data-idx"))
        if 0 <= idx < len(state["cart"]):
            removed = state["cart"].pop(idx)
            toast(f"{removed['name']} removed")
            render()

    elif action == "set_delivery":
        state["delivery_method"] = el.getAttribute("data-method")
        render()

    elif action == "set_payment":
        state["payment_method"] = el.getAttribute("data-method")
        render()

    elif action == "place_order":
        state["order_placed"] = True
        render()

    elif action == "finish_order":
        state["cart"] = []
        state["order_placed"] = False
        state["view"] = "home"
        window.scrollTo(0, 0)
        render()


def add_current_to_cart():
    p = state["current_product"]
    opts = state["options"]
    delta = next((s["delta"] for s in SIZES if s["key"] == opts["size"]), 0)
    state["cart"].append({
        "pid": p["id"],
        "name": p["name"],
        "color_a": p["color_a"],
        "color_b": p["color_b"],
        "price": p["price"] + delta,
        "size": opts["size"],
        "ice": opts["ice"],
        "sweet": opts["sweet"],
        "qty": opts["qty"],
    })
    name = p["name"]
    state["modal_open"] = False
    state["current_product"] = None
    state["view"] = "cart"
    render()
    toast(f"{name} added to cart")


def handle_keydown(event):
    if event.key == "Escape":
        if state["order_placed"]:
            return
        if state["modal_open"]:
            state["modal_open"] = False
            state["current_product"] = None
            render()


# =====================================================================
# BOOT
# =====================================================================

document.addEventListener("click", create_proxy(handle_click))
document.addEventListener("keydown", create_proxy(handle_keydown))
render()
