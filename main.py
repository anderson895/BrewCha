"""
BrewCha — a small ordering app written in Python that runs in the browser
through PyScript.

How it works (in plain English):

    1. We keep all app data inside one Python dictionary called `state`.
    2. Every time something changes (a click, a category switch, etc.) we
       call `render()`. That function builds a big HTML string and puts it
       into the page.
    3. We listen for a single "click" event on the whole document. When a
       click happens we look at the `data-action` attribute on the button
       that was clicked, and call the matching handler.

The code is organised into clearly labelled sections so it's easy to find
things. Read top-to-bottom and it should make sense.
"""


from pyscript import document, window
from pyodide.ffi import create_proxy  
from js import setTimeout              
import html                          



PRODUCTS = [
    {"id":  1, "cat": "milk_tea", "name": "Brown Sugar Milk Tea",   "desc": "Classic milk tea with brown sugar pearls.",        "price": 120, "color_a": "#D2A878", "color_b": "#6B4423", "kind": "boba",    "best": True,  "image": "assets/products/brown-sugar-milk-tea.jpg"},
    {"id":  2, "cat": "milk_tea", "name": "Matcha Milk Tea",        "desc": "Premium matcha with creamy milk.",                 "price": 130, "color_a": "#C5D89A", "color_b": "#6B8E23", "kind": "boba",    "best": False, "image": "assets/products/matcha-milk-tea.jpg"},
    {"id":  3, "cat": "milk_tea", "name": "Wintermelon Milk Tea",   "desc": "Smooth wintermelon with milk and pearls.",         "price": 120, "color_a": "#F0E2C2", "color_b": "#B89968", "kind": "boba",    "best": False, "image": "assets/products/wintermelon-milk-tea.jpg"},
    {"id":  4, "cat": "milk_tea", "name": "Taro Milk Tea",          "desc": "Creamy taro flavored milk tea with pearls.",       "price": 130, "color_a": "#D8B8DE", "color_b": "#8E6BA8", "kind": "boba",    "best": False, "image": "assets/products/taro-milk-tea.jpg"},
    {"id":  5, "cat": "milk_tea", "name": "Okinawa Milk Tea",       "desc": "Roasted Okinawa milk tea with pearls.",            "price": 130, "color_a": "#CDA67E", "color_b": "#5D3A1A", "kind": "boba",    "best": False, "image": "assets/products/okinawa-milk-tea.jpg"},
    {"id":  6, "cat": "milk_tea", "name": "Hokkaido Milk Tea",      "desc": "Smooth Hokkaido-style milk tea.",                  "price": 130, "color_a": "#EDD2A8", "color_b": "#9B7048", "kind": "boba",    "best": False, "image": "assets/products/hokkaido-milk-tea.jpg"},

    # ---- Coffee ----
    {"id":  7, "cat": "coffee",   "name": "Matcha Latte",           "desc": "Smooth matcha latte with creamy milk.",            "price": 130, "color_a": "#B0CD78", "color_b": "#4F7942", "kind": "latte",   "best": True,  "image": "assets/products/matcha-latte.jpg"},
    {"id":  8, "cat": "coffee",   "name": "Caramel Macchiato",      "desc": "Rich espresso with caramel.",                      "price": 135, "color_a": "#C9A079", "color_b": "#5D3A1A", "kind": "boba",    "best": True,  "image": "assets/products/caramel-macchiato.jpg"},
    {"id":  9, "cat": "coffee",   "name": "Brown Sugar Latte",      "desc": "Espresso with brown sugar pearls.",                "price": 140, "color_a": "#B8956A", "color_b": "#3C2415", "kind": "boba",    "best": False, "image": "assets/products/brown-sugar-latte.jpg"},
    {"id": 10, "cat": "coffee",   "name": "Iced Americano",         "desc": "Bold and refreshing iced americano.",              "price": 110, "color_a": "#6B4423", "color_b": "#1A0D06", "kind": "ice",     "best": False, "image": "assets/products/iced-americano.jpg"},

    # ---- Specials ----
    {"id": 11, "cat": "specials", "name": "BrewCha Signature",      "desc": "House's special blend of premium tea.",            "price": 150, "color_a": "#E8C39E", "color_b": "#8B5A2B", "kind": "boba",    "best": False, "image": "assets/products/brewcha-signature.jpg"},
    {"id": 12, "cat": "specials", "name": "Cookies & Cream Frappe", "desc": "Blended frappe with cookies and cream.",           "price": 145, "color_a": "#E8E4DC", "color_b": "#3C2415", "kind": "frappe",  "best": False, "image": "assets/products/cookies-and-cream-frappe.jpg"},
    {"id": 13, "cat": "specials", "name": "Strawberry Yakult",      "desc": "Refreshing strawberry with yakult and pearls.",    "price": 140, "color_a": "#F5B7B1", "color_b": "#C0392B", "kind": "boba",    "best": False, "image": "assets/products/strawberry-yakult.jpg"},

    # ---- Add-ons ----
    {"id": 14, "cat": "add_ons",  "name": "Tapioca Pearls",         "desc": "Extra chewy boba pearls.",                         "price":  20, "color_a": "#6B4423", "color_b": "#1A0D06", "kind": "topping", "best": False, "image": "assets/products/tapioca-pearls.jpg"},
    {"id": 15, "cat": "add_ons",  "name": "Pudding",                "desc": "Smooth, silky egg pudding topping.",               "price":  25, "color_a": "#F4D8A8", "color_b": "#D4A574", "kind": "topping", "best": False, "image": "assets/products/pudding.jpg"},
    {"id": 16, "cat": "add_ons",  "name": "Cheese Foam",            "desc": "Sweet-and-salty cheese foam topping.",             "price":  30, "color_a": "#FFF4D6", "color_b": "#F0C75E", "kind": "topping", "best": False, "image": "assets/products/cheese-foam.jpg"},
    {"id": 17, "cat": "add_ons",  "name": "Crystal Boba",           "desc": "Translucent, jelly-like crystal boba.",            "price":  25, "color_a": "#E0F2F1", "color_b": "#80CBC4", "kind": "topping", "best": False, "image": "assets/products/crystal-boba.jpg"},
]

# The 4 category tabs on the Menu screen.
CATEGORIES = [
    {"key": "milk_tea", "label": "Milk Tea"},
    {"key": "coffee",   "label": "Coffee"},
    {"key": "specials", "label": "Specials"},
    {"key": "add_ons",  "label": "Add-ons"},
]

# Size choices. "delta" is added to the base price.
SIZES = [
    {"key": "S", "label": "S", "delta": -10},
    {"key": "M", "label": "M", "delta":   0},
    {"key": "L", "label": "L", "delta":  15},
]

# Ice level and sweetness use the same options.
LEVELS = ["0%", "25%", "50%", "75%", "100%"]


# ===========================================================================
# 2. STATE  -- everything the app remembers while running
# ===========================================================================

# One big dictionary that holds the current state of the app.
# When any of these change we call render() to redraw the page.
state = {
    "view":             "home",        # which screen is showing (home / menu / cart / checkout)
    "category":         "milk_tea",    # the active Menu category
    "cart":             [],            # list of items the user has added
    "modal_open":       False,         # is the product detail popup open?
    "current_product":  None,          # the product currently shown in the popup
    "order_placed":     False,         # was the order just submitted?
    "delivery_method":  "delivery",    # "delivery" or "pickup"
    "payment_method":   "gcash",       # "gcash", "maya", or "cod"
    # Options the user picks in the product detail popup:
    "options": {
        "size":  "M",
        "ice":   "50%",
        "sweet": "50%",
        "qty":   1,
    },
}


# ===========================================================================
# 3. SMALL HELPERS
# ===========================================================================

def safe(text):
    """Escape any HTML-special characters in `text` so they can't break the page."""
    return html.escape(str(text))


def find_product(product_id):
    """Return the product dictionary with this id, or None if not found."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def products_in_category(category_key):
    """Return only the products whose category matches."""
    result = []
    for product in PRODUCTS:
        if product["cat"] == category_key:
            result.append(product)
    return result


def best_seller_products():
    """Return only the products marked as best sellers."""
    result = []
    for product in PRODUCTS:
        if product["best"]:
            result.append(product)
    return result


def get_size_delta(size_key):
    """Return how much money to add (or subtract) for a given size."""
    for size in SIZES:
        if size["key"] == size_key:
            return size["delta"]
    return 0


def get_category_label(category_key):
    """Return the human-friendly label for a category key, e.g. 'milk_tea' -> 'Milk Tea'."""
    for category in CATEGORIES:
        if category["key"] == category_key:
            return category["label"]
    return category_key


# ----- Cart math -----

def cart_subtotal():
    """Add up the price of everything in the cart."""
    total = 0
    for item in state["cart"]:
        total = total + item["price"] * item["qty"]
    return total


def cart_count():
    """Count how many items (including duplicates) are in the cart."""
    total = 0
    for item in state["cart"]:
        total = total + item["qty"]
    return total


def delivery_fee():
    """Delivery costs ₱30. Pickup is free. Empty cart pays nothing."""
    if not state["cart"]:
        return 0
    if state["delivery_method"] == "delivery":
        return 30
    return 0


def cart_total():
    """The grand total = subtotal + delivery fee."""
    return cart_subtotal() + delivery_fee()


def product_detail_total():
    """The current total shown on the product detail screen."""
    product = state["current_product"]
    if product is None:
        return 0
    size_delta = get_size_delta(state["options"]["size"])
    unit_price = product["price"] + size_delta
    return unit_price * state["options"]["qty"]


# ===========================================================================
# 4. ICONS  --  small SVG strings reused across the UI
# ===========================================================================
# Storing icons as constants keeps the rendering code short and readable.

ICON_SEARCH        = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="20" y1="20" x2="16.5" y2="16.5" stroke-linecap="round"/></svg>'
ICON_CART          = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 7h14l-1.5 9a2 2 0 0 1-2 1.7H8.5a2 2 0 0 1-2-1.7L5 7Z"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/></svg>'
ICON_USER          = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="3.5"/><path d="M5 21c0-3.5 3.1-6 7-6s7 2.5 7 6"/></svg>'
ICON_HEART         = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.5 6c-2.5 4.5-9.5 9-9.5 9z"/></svg>'
ICON_HOME          = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V10"/></svg>'
ICON_HOME_FILLED   = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.3 2.3a1 1 0 0 1 1.4 0L22 11h-2v9a1 1 0 0 1-1 1h-5v-7h-4v7H5a1 1 0 0 1-1-1v-9H2l9.3-8.7z"/></svg>'
ICON_MENU          = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="6" rx="7.5" ry="2"/><path d="M4.5 6v3c0 1.1 3.4 2 7.5 2s7.5-.9 7.5-2V6"/><path d="M4.5 12v3c0 1.1 3.4 2 7.5 2s7.5-.9 7.5-2v-3"/></svg>'
ICON_BAG           = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 7.5h13l-1 12.5a1 1 0 0 1-1 .9H7.5a1 1 0 0 1-1-.9L5.5 7.5z"/><path d="M9 7.5V6a3 3 0 0 1 6 0v1.5"/></svg>'
ICON_BACK          = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 6 9 12 15 18"/></svg>'
ICON_TRASH         = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>'
ICON_CHEVRON_RIGHT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 6 15 12 9 18"/></svg>'
ICON_CHEVRON_DOWN  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
ICON_PIN           = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-7-7-12a7 7 0 0 1 14 0c0 5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>'
ICON_BIKE          = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M12 17.5V14l-3-3 4-3 2 3h3"/></svg>'
ICON_WALLET        = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/><path d="M3 7l3-3h11"/><circle cx="16" cy="13" r="1.4" fill="currentColor"/></svg>'


# ===========================================================================
# 5. THE BREW & CO CUP ILLUSTRATION
# ===========================================================================
# This function returns an SVG drawing of a cup, colored to match a product.
# It's long because it draws many shapes (cup, beverage, pearls, lid, etc.),
# but each block below is commented so you can follow it.

def cup_svg(product):
    """Return an SVG string that looks like a BREW & CO cup of this drink."""
    product_id = product["id"]
    color_a = product["color_a"]   # top color of the beverage
    color_b = product["color_b"]   # bottom (darker) color
    kind = product.get("kind", "boba")

    # Each <linearGradient> needs a unique id, so we tag it with the product id.
    grad_id      = "bev"   + str(product_id)
    pearl_id     = "pearl" + str(product_id)
    glass_id     = "glass" + str(product_id)
    coaster_id   = "coast" + str(product_id)

    # Add-ons (toppings) get a simple bowl illustration instead of a cup.
    if kind == "topping":
        return topping_svg(product, pearl_id)

    # ---- Pearls (only for "boba" drinks) ----------------------------------
    pearls_html = ""
    if kind == "boba":
        pearl_positions = [
            (78, 224, 7), (96, 232, 6), (114, 228, 7), (132, 236, 6),
            (150, 230, 7), (166, 238, 5), (88, 246, 6), (108, 244, 6),
            (128, 250, 6), (148, 246, 6), (164, 252, 5), (78, 240, 5),
            (118, 254, 5), (138, 256, 4), (155, 244, 4),
        ]
        for cx, cy, r in pearl_positions:
            pearls_html += '<circle cx="{}" cy="{}" r="{}" fill="url(#{})"/>'.format(cx, cy, r, pearl_id)

    # ---- Ice cubes (only for "ice" drinks) -------------------------------
    ice_html = ""
    if kind == "ice":
        ice_positions = [(78, 110, 22), (108, 100, 20), (135, 116, 18), (155, 102, 22)]
        for cx, cy, size in ice_positions:
            ice_html += (
                '<rect x="{}" y="{}" width="{}" height="{}" rx="3" '
                'fill="rgba(255,255,255,0.55)" stroke="rgba(255,255,255,0.85)" stroke-width="1"/>'
                .format(cx, cy, size, size)
            )

    # ---- Cream foam (latte) ----------------------------------------------
    foam_html = ""
    if kind == "latte":
        foam_html = (
            '<ellipse cx="120" cy="98" rx="58" ry="10" fill="#FAF5EC"/>'
            '<ellipse cx="120" cy="95" rx="58" ry="8"  fill="#FFFFFF"/>'
        )

    # ---- Cookie bits (frappe) --------------------------------------------
    cookies_html = ""
    if kind == "frappe":
        cookies_html = (
            '<circle cx="90"  cy="118" r="6" fill="#3C2415"/>'
            '<circle cx="115" cy="108" r="7" fill="#3C2415"/>'
            '<circle cx="142" cy="120" r="6" fill="#3C2415"/>'
            '<circle cx="160" cy="110" r="5" fill="#3C2415"/>'
        )

    # Build the final SVG. Indented blank lines separate each piece.
    return """
    <svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg" class="cup-svg" aria-label="{name} illustration">
      <defs>
        <linearGradient id="{grad}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"  stop-color="{ca}"/>
          <stop offset="60%" stop-color="{ca}"/>
          <stop offset="100%" stop-color="{cb}"/>
        </linearGradient>
        <radialGradient id="{pearl}" cx="35%" cy="30%" r="65%">
          <stop offset="0%"   stop-color="#5D3A1A"/>
          <stop offset="100%" stop-color="#0F0805"/>
        </radialGradient>
        <linearGradient id="{glass}" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%"   stop-color="rgba(255,255,255,0.45)"/>
          <stop offset="50%"  stop-color="rgba(255,255,255,0.0)"/>
          <stop offset="100%" stop-color="rgba(255,255,255,0.20)"/>
        </linearGradient>
        <linearGradient id="{coaster}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   stop-color="#A67B5B"/>
          <stop offset="100%" stop-color="#6B4423"/>
        </linearGradient>
      </defs>

      <!-- shadow under cup -->
      <ellipse cx="120" cy="288" rx="78" ry="6" fill="rgba(0,0,0,0.18)"/>
      <!-- wooden coaster -->
      <ellipse cx="120" cy="280" rx="92" ry="11" fill="url(#{coaster})"/>
      <ellipse cx="120" cy="276" rx="86" ry="8"  fill="#C9A079" opacity="0.6"/>

      <!-- glass cup back wall -->
      <path d="M 60 80 L 180 80 L 168 272 L 72 272 Z" fill="rgba(255,255,255,0.18)"/>
      <!-- the beverage itself -->
      <path d="M 62 86 L 178 86 L 167 270 L 73 270 Z" fill="url(#{grad})"/>

      {foam}
      {ice}
      {cookies}
      {pearls}

      <!-- glass outline and highlights -->
      <path d="M 60 80 L 180 80 L 168 272 L 72 272 Z" fill="url(#{glass})"/>
      <path d="M 60 80 L 180 80 L 168 272 L 72 272 Z" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>
      <path d="M 64 90 L 70 90 L 78 268 L 72 268 Z" fill="rgba(255,255,255,0.4)"/>
      <path d="M 165 92 L 169 92 L 162 265 L 158 265 Z" fill="rgba(255,255,255,0.25)"/>

      <!-- lid -->
      <ellipse cx="120" cy="76" rx="62" ry="7" fill="#3C2415"/>
      <rect x="58" y="70" width="124" height="13" rx="3" fill="#5D3A1A"/>
      <rect x="58" y="68" width="124" height="5"  rx="2" fill="#3C2415"/>
      <ellipse cx="120" cy="71" rx="58" ry="3.5" fill="#7A4F2A"/>

      <!-- straw (slightly tilted) -->
      <g transform="rotate(10 119 45)">
        <rect x="113" y="14" width="11" height="62" rx="2" fill="#3C2415"/>
        <rect x="115" y="14" width="3"  height="62" rx="1" fill="#5D3A1A"/>
      </g>

      <!-- BREW & CO label on the cup -->
      <circle cx="120" cy="172" r="26" fill="#FAF5EC" opacity="0.96"/>
      <circle cx="120" cy="172" r="26" fill="none" stroke="#3C2415" stroke-width="0.7" opacity="0.5"/>
      <text x="120" y="169" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#3C2415" letter-spacing="0.5">BREW</text>
      <line x1="105" y1="174" x2="135" y2="174" stroke="#3C2415" stroke-width="0.6"/>
      <text x="120" y="184" text-anchor="middle" font-family="Georgia, serif" font-size="7"  font-weight="600" fill="#3C2415" letter-spacing="1.2">&amp; CO</text>
    </svg>
    """.format(
        name=safe(product["name"]),
        grad=grad_id, pearl=pearl_id, glass=glass_id, coaster=coaster_id,
        ca=color_a, cb=color_b,
        foam=foam_html, ice=ice_html, cookies=cookies_html, pearls=pearls_html,
    )


def topping_svg(product, pearl_id):
    """A simple bowl illustration used for add-on toppings (pearls, pudding, etc.)."""
    contents_html = ""

    # If it's a pearl-like topping, draw pearls in the bowl.
    if "Pearl" in product["name"] or "Boba" in product["name"]:
        positions = [
            (90, 150, 8), (110, 145, 9), (130, 152, 8), (150, 148, 9),
            (95, 168, 9), (118, 165, 8), (138, 170, 9), (158, 167, 8),
            (108, 180, 8), (130, 183, 9), (148, 180, 8),
        ]
        for cx, cy, r in positions:
            contents_html += '<circle cx="{}" cy="{}" r="{}" fill="url(#{})"/>'.format(cx, cy, r, pearl_id)
    else:
        # Otherwise just draw two coloured ovals to suggest contents.
        contents_html = (
            '<ellipse cx="120" cy="160" rx="55" ry="22" fill="{}"/>'
            '<ellipse cx="120" cy="156" rx="50" ry="15" fill="{}" opacity="0.5"/>'
        ).format(product["color_a"], product["color_b"])

    return """
    <svg viewBox="0 0 240 260" xmlns="http://www.w3.org/2000/svg" class="cup-svg" aria-label="{name} illustration">
      <defs>
        <radialGradient id="{pearl}" cx="35%" cy="30%" r="65%">
          <stop offset="0%"  stop-color="#5D3A1A"/>
          <stop offset="100%" stop-color="#0F0805"/>
        </radialGradient>
      </defs>
      <ellipse cx="120" cy="230" rx="85" ry="6" fill="rgba(0,0,0,0.18)"/>
      <path d="M 50 150 Q 50 220 120 220 Q 190 220 190 150 Z" fill="#FFFFFF"/>
      {contents}
      <ellipse cx="120" cy="150" rx="70" ry="14" fill="#FFFFFF"/>
      <ellipse cx="120" cy="150" rx="70" ry="14" fill="none" stroke="#E8DCC8" stroke-width="1.5"/>
      <ellipse cx="120" cy="146" rx="62" ry="9"  fill="#FAF5EC"/>
    </svg>
    """.format(name=safe(product["name"]), pearl=pearl_id, contents=contents_html)


def product_image(product):
    """
    Return the HTML for a product's image.

    If the product has an `image` path AND the file actually loads in the
    browser, that photo is shown. If the file is missing or fails to load,
    the SVG cup illustration is shown instead (automatic fallback).
    """
    cup_html = cup_svg(product)
    image_path = product.get("image")

    # No image specified — just use the drawn cup.
    if not image_path:
        return cup_html

    # Both the SVG and the <img> are placed in the same spot.
    # The image sits on top (z-index in CSS). If it fails to load, the
    # `onerror` handler hides it and the SVG underneath becomes visible.
    img_html = (
        '<img src="{src}" class="product-photo" alt="{alt}" loading="lazy" '
        'onerror="this.style.display=\'none\'"/>'
        .format(src=image_path, alt=safe(product["name"]))
    )
    return cup_html + img_html


def hero_illustration():
    """A bigger, dressier cup illustration used on the Home hero panel."""
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

      <!-- cream splashes behind the cup -->
      <path d="M 60 130 Q 30 100 60 80 Q 90 60 130 80 L 120 130 Z" fill="#FAF5EC" opacity="0.85"/>
      <path d="M 250 140 Q 290 120 280 80 Q 250 50 220 80 L 240 140 Z" fill="#FAF5EC" opacity="0.85"/>
      <path d="M 100 60 Q 160 30 220 60 L 200 110 L 140 110 Z" fill="#FFFFFF" opacity="0.85"/>

      <!-- floating pearls -->
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

      <!-- shadow + coaster -->
      <ellipse cx="160" cy="345" rx="90" ry="6" fill="rgba(0,0,0,0.15)"/>
      <ellipse cx="160" cy="338" rx="100" ry="11" fill="url(#hero-coaster)"/>
      <ellipse cx="160" cy="335" rx="95"  ry="8"  fill="#C9A079" opacity="0.6"/>

      <!-- cup back + beverage -->
      <path d="M 90 130 L 230 130 L 218 332 L 102 332 Z" fill="rgba(255,255,255,0.18)"/>
      <path d="M 92 136 L 228 136 L 217 330 L 103 330 Z" fill="url(#hero-bev)"/>

      <!-- pearls inside the cup -->
      <g fill="url(#hero-pearl)">
        <circle cx="108" cy="270" r="8"/><circle cx="128" cy="278" r="7"/>
        <circle cx="148" cy="272" r="8"/><circle cx="168" cy="280" r="7"/>
        <circle cx="188" cy="274" r="8"/><circle cx="208" cy="280" r="6"/>
        <circle cx="118" cy="290" r="7"/><circle cx="140" cy="295" r="7"/>
        <circle cx="160" cy="298" r="7"/><circle cx="182" cy="295" r="7"/>
        <circle cx="200" cy="290" r="6"/><circle cx="100" cy="282" r="5"/>
        <circle cx="148" cy="310" r="6"/><circle cx="170" cy="312" r="5"/>
      </g>

      <!-- glass outline -->
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

      <!-- BREW & CO label -->
      <circle cx="160" cy="215" r="32" fill="#FAF5EC" opacity="0.97"/>
      <circle cx="160" cy="215" r="32" fill="none" stroke="#3C2415" stroke-width="0.7" opacity="0.5"/>
      <text x="160" y="212" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700" fill="#3C2415" letter-spacing="0.6">BREW</text>
      <line x1="142" y1="217" x2="178" y2="217" stroke="#3C2415" stroke-width="0.7"/>
      <text x="160" y="230" text-anchor="middle" font-family="Georgia, serif" font-size="9"  font-weight="600" fill="#3C2415" letter-spacing="1.4">&amp; CO</text>
    </svg>
    """


# ===========================================================================
# 6. NAVIGATION BARS (top + bottom)
# ===========================================================================

def render_desktop_navbar():
    """The top navigation bar used on wide screens."""
    nav_items = [
        ("home", "Home"),
        ("menu", "Menu"),
    ]

    # Build the list of nav links by looping (instead of a generator).
    links_html = ""
    for key, label in nav_items:
        active_class = ""
        if state["view"] == key:
            active_class = "active"
        links_html += (
            '<li class="nav-link {active}" data-action="navigate" data-view="{key}">{label}</li>'
            .format(active=active_class, key=key, label=label)
        )

    # Cart badge with item count.
    count = cart_count()
    badge_html = ""
    if count > 0:
        badge_html = '<span class="cart-badge">{}</span>'.format(count)

    return """
    <nav class="navbar navbar-desktop">
      <div class="nav-inner">
        <div class="nav-brand" data-action="navigate" data-view="home">BrewCha</div>
        <ul class="nav-links">{links}</ul>
        <div class="nav-actions">
          <button class="icon-btn" title="Search">{search}</button>
          <button class="icon-btn" title="Cart" data-action="navigate" data-view="cart">
            {cart}{badge}
          </button>
          <button class="icon-btn" title="Profile">{user}</button>
        </div>
      </div>
    </nav>
    """.format(links=links_html, search=ICON_SEARCH, cart=ICON_CART, badge=badge_html, user=ICON_USER)


def render_mobile_header():
    """The small header at the top of the screen on mobile. Changes per view."""
    current_view = state["view"]
    count = cart_count()
    badge_html = ""
    if count > 0:
        badge_html = '<span class="m-badge">{}</span>'.format(count)

    if current_view == "home":
        return """
        <header class="m-header m-header-home">
          <div class="m-brand">BrewCha</div>
          <button class="m-icon-btn" title="Search">{search}</button>
        </header>
        """.format(search=ICON_SEARCH)

    if current_view == "menu":
        return """
        <header class="m-header">
          <button class="m-icon-btn" data-action="navigate" data-view="home" title="Back">{back}</button>
          <div class="m-title">MENU</div>
          <button class="m-icon-btn m-icon-btn--cart" data-action="navigate" data-view="cart" title="Cart">
            {cart}{badge}
          </button>
        </header>
        """.format(back=ICON_BACK, cart=ICON_CART, badge=badge_html)

    if current_view == "cart":
        return """
        <header class="m-header">
          <button class="m-icon-btn" data-action="back" title="Back">{back}</button>
          <div class="m-title">CART</div>
          <span class="m-icon-spacer"></span>
        </header>
        """.format(back=ICON_BACK)

    if current_view == "checkout":
        return """
        <header class="m-header">
          <button class="m-icon-btn" data-action="navigate" data-view="cart" title="Back">{back}</button>
          <div class="m-title">CHECKOUT</div>
          <span class="m-icon-spacer"></span>
        </header>
        """.format(back=ICON_BACK)

    return ""


def render_bottom_nav():
    """The dark bottom nav (only shows on mobile). Active item gets a filled icon."""
    # Each tuple: (view_key, label, normal_icon, active_icon)
    items = [
        ("home",    "Home",    ICON_HOME, ICON_HOME_FILLED),
        ("menu",    "Menu",    ICON_MENU, ICON_MENU),
        ("cart",    "Cart",    ICON_BAG,  ICON_BAG),
        ("profile", "Profile", ICON_USER, ICON_USER),
    ]

    count = cart_count()
    parts_html = ""

    for key, label, normal_icon, active_icon in items:
        is_active = (state["view"] == key)

        # Pick the right icon and class for the active tab.
        if is_active:
            active_class = "active"
            chosen_icon = active_icon
        else:
            active_class = ""
            chosen_icon = normal_icon

        # Show the cart badge only on the Cart tab and only if cart isn't empty.
        badge_html = ""
        if key == "cart" and count > 0:
            badge_html = '<span class="bnav-badge">{}</span>'.format(count)

        parts_html += """
        <button class="bnav-item {active}" data-action="navigate" data-view="{key}">
          <span class="bnav-indicator"></span>
          <span class="bnav-icon">{icon}{badge}</span>
          <span class="bnav-label">{label}</span>
        </button>
        """.format(active=active_class, key=key, icon=chosen_icon, badge=badge_html, label=label)

    return '<nav class="bottom-nav">{}</nav>'.format(parts_html)


# ===========================================================================
# 7. PRODUCT CARDS (used by Home, Menu, and Best Sellers)
# ===========================================================================

def render_product_card_grid(product, tag=None):
    """Big square card used in the desktop grid + mobile best-sellers row."""
    tag_html = ""
    if tag is not None:
        tag_html = '<span class="product-tag">{}</span>'.format(safe(tag))

    return """
    <div class="product-card" data-action="open_product" data-product-id="{pid}">
      <div class="product-img">
        {tag}
        {cup}
      </div>
      <div class="product-info">
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <div class="product-footer">
          <div class="product-price">{price}</div>
          <button class="product-add" data-action="quick_add" data-product-id="{pid}" title="Add">+</button>
        </div>
      </div>
    </div>
    """.format(
        pid=product["id"],
        tag=tag_html,
        cup=product_image(product),
        name=safe(product["name"]),
        desc=safe(product["desc"]),
        price=product["price"],
    )


def render_product_card_list(product):
    """Horizontal row used in the mobile Menu screen."""
    return """
    <div class="product-row" data-action="open_product" data-product-id="{pid}">
      <div class="product-row-img">{cup}</div>
      <div class="product-row-info">
        <div class="product-row-name">{name}</div>
        <div class="product-row-desc">{desc}</div>
        <div class="product-row-price">₱{price}</div>
      </div>
      <button class="product-row-add" data-action="quick_add" data-product-id="{pid}" title="Add">+</button>
    </div>
    """.format(
        pid=product["id"],
        cup=product_image(product),
        name=safe(product["name"]),
        desc=safe(product["desc"]),
        price=product["price"],
    )


def render_product_card(product, tag=None):
    """Render BOTH the grid card and the list row. CSS shows the right one per screen size."""
    grid_html = render_product_card_grid(product, tag)
    list_html = render_product_card_list(product)
    return '<div class="product-wrap">{}{}</div>'.format(grid_html, list_html)


# ===========================================================================
# 8. HOME VIEW
# ===========================================================================

def render_hero():
    """Hero panel with the banner image as background and text overlaid."""
    return """
    <section class="hero">
      <div class="hero-panel">
        <img src="assets/banner/banner.png" class="hero-banner-bg"
             alt=""
             onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'"/>
        <div class="hero-banner-fallback" style="display:none">{hero_art}</div>
        <div class="hero-content">
          <span class="hero-eyebrow">Premium Boba Experience</span>
          <h1 class="hero-title">Your Daily<br><em>cup of</em><br>Happiness</h1>
          <p class="hero-sub">Hand-crafted milk tea, signature brews, and decadent toppings.</p>
          <button class="btn btn-primary btn-lg" data-action="navigate" data-view="menu">ORDER NOW</button>
        </div>
      </div>
    </section>
    """.format(hero_art=hero_illustration())


def render_best_sellers():
    """The 'BEST SELLERS' section on the Home screen."""
    cards_html = ""
    for product in best_seller_products():
        cards_html += render_product_card(product, tag="Best Seller")

    return """
    <section class="section" id="best-sellers">
      <div class="section-head">
        <h2 class="section-title">BEST SELLERS</h2>
        <span class="section-link" data-action="navigate" data-view="menu">View all →</span>
      </div>
      <div class="product-grid">{cards}</div>
    </section>
    """.format(cards=cards_html)


def render_promo():
    """A decorative promo banner shown only on desktop."""
    return """
    <section class="promo">
      <div>
        <h2>First Order? Get 20% Off</h2>
        <p>Use code <strong>BREWCHA20</strong> on your first delivery. Limited time only.</p>
        <button class="btn" data-action="navigate" data-view="menu">Order Now</button>
      </div>
      
    </section>
    """


def render_footer():
    """Simple footer with company links, shown only on desktop."""
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


def render_home_view():
    """Glue everything together for the Home screen."""
    return render_hero() + render_best_sellers() + render_promo() + render_footer()


# ===========================================================================
# 9. MENU VIEW
# ===========================================================================

def render_menu_view():
    """The Menu screen — category tabs at the top, product cards below."""
    # Build the category tabs.
    tabs_html = ""
    for category in CATEGORIES:
        active_class = ""
        if state["category"] == category["key"]:
            active_class = "active"
        tabs_html += (
            '<button class="category-tab {active}" data-action="select_category" '
            'data-category="{key}">{label}</button>'
            .format(active=active_class, key=category["key"], label=category["label"])
        )

    # Build the product cards for the currently-selected category.
    cards_html = ""
    for product in products_in_category(state["category"]):
        cards_html += render_product_card(product)

    return """
    <section class="section">
      <div class="section-head section-head-desktop">
        <div>
          <h2 class="section-title">Menu</h2>
          <div class="section-sub">Browse our full {label} selection</div>
        </div>
      </div>
      <div class="category-tabs">{tabs}</div>
      <div class="product-grid product-grid-menu">{cards}</div>
    </section>
    {footer}
    """.format(
        label=safe(get_category_label(state["category"]).lower()),
        tabs=tabs_html,
        cards=cards_html,
        footer=render_footer(),
    )


# ===========================================================================
# 10. PRODUCT DETAIL (Modal on desktop / fullscreen on mobile)
# ===========================================================================

def render_size_chips():
    """The three size chips (S/M/L) on the product detail screen."""
    current_size = state["options"]["size"]
    chips_html = ""
    for size in SIZES:
        active_class = ""
        if size["key"] == current_size:
            active_class = "active"

        if size["delta"] == 0:
            sub_label = '<span class="chip-sub">base</span>'
        else:
            sub_label = '<span class="chip-sub">{:+d}</span>'.format(size["delta"])

        chips_html += (
            '<button class="chip chip-size {active}" data-action="set_option" '
            'data-option="size" data-value="{key}">'
            '<span class="chip-main">{label}</span>{sub}</button>'
            .format(active=active_class, key=size["key"], label=size["label"], sub=sub_label)
        )
    return chips_html


def render_level_chips(option_name):
    """Chips for ice level / sweetness level (0% through 100%)."""
    current_value = state["options"][option_name]
    chips_html = ""
    for value in LEVELS:
        active_class = ""
        if value == current_value:
            active_class = "active"
        chips_html += (
            '<button class="chip {active}" data-action="set_option" '
            'data-option="{opt}" data-value="{val}">{val}</button>'
            .format(active=active_class, opt=option_name, val=value)
        )
    return chips_html


def render_product_detail():
    """The big product detail panel shared by desktop modal and mobile fullscreen."""
    product = state["current_product"]
    if product is None:
        return ""

    options = state["options"]
    total = product_detail_total()

    return """
    <div class="detail-image-wrap">
      <button class="detail-back" data-action="close_modal" title="Back">{back}</button>
      <button class="detail-fav" title="Favorite">{heart}</button>
      {cup}
      <div class="detail-dots"><span class="active"></span><span></span><span></span></div>
    </div>
    <div class="detail-body">
      <div class="detail-title-row">
        <h2 class="detail-name">{name}</h2>
        <div class="detail-price">₱{price}</div>
      </div>
      <p class="detail-desc">{desc}</p>

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
          <span class="qty-val">{qty}</span>
          <button class="qty-btn" data-action="change_qty" data-dir="1">+</button>
        </div>
        <button class="btn btn-primary btn-lg btn-add-cart" data-action="add_to_cart">
          ADD TO CART · ₱{total}
        </button>
      </div>
    </div>
    """.format(
        back=ICON_BACK, heart=ICON_HEART,
        cup=product_image(product),
        name=safe(product["name"]),
        price=product["price"],
        desc=safe(product["desc"]),
        size_chips=render_size_chips(),
        ice_chips=render_level_chips("ice"),
        sweet_chips=render_level_chips("sweet"),
        qty=options["qty"],
        total=total,
    )


def render_product_modal():
    """Wrap the product detail in a centered modal overlay (for desktop)."""
    if not state["modal_open"]:
        return ""
    if state["current_product"] is None:
        return ""
    return """
    <div class="modal-overlay" data-action="close_modal">
      <div class="modal" data-stop="1">
        {detail}
      </div>
    </div>
    """.format(detail=render_product_detail())


# ===========================================================================
# 11. CART VIEW
# ===========================================================================

def render_cart_item(item, index):
    """One row in the cart list."""
    # We look up the original product to get the right colors for the SVG cup.
    product_for_cup = find_product(item["pid"])
    if product_for_cup is None:
        product_for_cup = item

    line_total = item["price"] * item["qty"]

    return """
    <div class="cart-item">
      <div class="cart-item-img">{cup}</div>
      <div class="cart-item-info">
        <div class="cart-item-head">
          <div class="cart-item-name">{name}</div>
          <button class="cart-item-trash" data-action="remove_cart" data-idx="{idx}" title="Remove">{trash}</button>
        </div>
        <div class="cart-item-meta">Size: {size} · {sweet} Sugar · {ice} Ice</div>
        <div class="cart-item-bottom">
          <div class="cart-item-price">₱{total}</div>
          <div class="quantity quantity-sm">
            <button class="qty-btn" data-action="cart_qty" data-idx="{idx}" data-dir="-1">−</button>
            <span class="qty-val">{qty}</span>
            <button class="qty-btn" data-action="cart_qty" data-idx="{idx}" data-dir="1">+</button>
          </div>
        </div>
      </div>
    </div>
    """.format(
        cup=product_image(product_for_cup),
        name=safe(item["name"]),
        idx=index, trash=ICON_TRASH,
        size=item["size"], sweet=item["sweet"], ice=item["ice"],
        total=line_total, qty=item["qty"],
    )


def render_cart_empty():
    """What we show when the cart has no items."""
    return """
    <div class="cart-empty">
      <div class="cart-empty-emoji">🛒</div>
      <h3>Your cart is empty</h3>
      <p>Add a delicious brew to get started.</p>
      <button class="btn btn-primary" data-action="navigate" data-view="menu">Browse Menu</button>
    </div>
    """


def render_cart_view():
    """The Cart screen."""
    # If the cart is empty, show a placeholder.
    if not state["cart"]:
        return """
        <section class="page page-cart">
          <div class="page-inner">
            <h1 class="page-title page-title-desktop">Your Cart</h1>
            {empty}
          </div>
        </section>
        """.format(empty=render_cart_empty())

    # Otherwise build the list of items.
    items_html = ""
    for index, item in enumerate(state["cart"]):
        items_html += render_cart_item(item, index)

    return """
    <section class="page page-cart">
      <div class="page-inner">
        <h1 class="page-title page-title-desktop">Your Cart</h1>

        <div class="cart-items">{items}</div>

        <div class="cart-add-more-label">Add more items</div>
        <div class="cart-add-more" data-action="select_category" data-category="add_ons">
          <div>
            <strong>Add-ons</strong>
            <small>Toppings, Pearls, Milk, etc.</small>
          </div>
          <span class="cart-add-arrow">{arrow}</span>
        </div>

        <div class="cart-summary">
          <div class="summary-row"><span>Subtotal</span><span class="val">₱{subtotal}</span></div>
          <div class="summary-row"><span>Delivery Fee</span><span class="val">₱{fee}</span></div>
          <div class="summary-row total"><span>Total</span><span class="val">₱{total}</span></div>
        </div>

        <div class="cart-checkout-wrap">
          <button class="btn btn-primary btn-block btn-lg" data-action="navigate" data-view="checkout">CHECKOUT</button>
        </div>
      </div>
    </section>
    """.format(
        items=items_html, arrow=ICON_CHEVRON_RIGHT,
        subtotal=cart_subtotal(), fee=delivery_fee(), total=cart_total(),
    )


# ===========================================================================
# 12. CHECKOUT VIEW
# ===========================================================================

def render_delivery_options():
    """The Delivery / Pick up options card."""
    delivery_active = ""
    pickup_active = ""
    if state["delivery_method"] == "delivery":
        delivery_active = "active"
    else:
        pickup_active = "active"

    return """
    <div class="checkout-section">
      <h3>Delivery Method</h3>
      <div class="option-row option-row-tall {delivery_active}" data-action="set_delivery" data-method="delivery">
        <div class="option-radio"></div>
        <div class="option-icon">{bike}</div>
        <div class="option-content">
          <strong>Delivery</strong>
          <small>(₱30, 25–35 min)</small>
        </div>
        <span class="option-chevron">{chevron}</span>
      </div>
      <div class="option-row option-row-tall {pickup_active}" data-action="set_delivery" data-method="pickup">
        <div class="option-radio"></div>
        <div class="option-icon">{pin}</div>
        <div class="option-content">
          <strong>Pick up</strong>
          <small>(123 Coffee St, Barangay 12, Quezon City)</small>
        </div>
        <span class="option-time">20 min</span>
      </div>
    </div>
    """.format(
        delivery_active=delivery_active, pickup_active=pickup_active,
        bike=ICON_BIKE, pin=ICON_PIN, chevron=ICON_CHEVRON_DOWN,
    )


def render_payment_options():
    """The Payment Method card with GCash / Maya / Cash on Delivery."""
    payments = [
        ("gcash", "GCash",            "Pay via GCash e-wallet",      "#0085FF"),
        ("maya",  "Maya",             "Pay via Maya e-wallet",       "#00C97F"),
        ("cod",   "Cash on Delivery", "Pay when your order arrives", "#8B5A2B"),
    ]

    rows_html = ""
    for key, label, sub_text, color in payments:
        active_class = ""
        if state["payment_method"] == key:
            active_class = "active"
        rows_html += """
        <div class="option-row {active}" data-action="set_payment" data-method="{key}">
          <div class="option-radio"></div>
          <div class="option-icon" style="color: {color};">{wallet}</div>
          <div class="option-content">
            <strong>{label}</strong>
            <small>{sub}</small>
          </div>
        </div>
        """.format(active=active_class, key=key, color=color, wallet=ICON_WALLET, label=label, sub=sub_text)

    return """
    <div class="checkout-section">
      <h3>Payment Method</h3>
      {rows}
    </div>
    """.format(rows=rows_html)


def render_checkout_view():
    """The Checkout screen."""
    # If somehow we got here with no items, show a placeholder.
    if not state["cart"]:
        return """
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

    # Order summary (used in the right-hand column on desktop).
    summary_items_html = ""
    for index, item in enumerate(state["cart"]):
        summary_items_html += render_cart_item(item, index)

    return """
    <section class="page page-checkout">
      <div class="page-inner">
        <h1 class="page-title page-title-desktop">Checkout</h1>

        <div class="checkout-grid">
          <div class="checkout-main">
            {delivery}
            {payment}
          </div>

          <aside class="checkout-summary">
            <div class="checkout-section summary-card">
              <h3>Order Summary</h3>
              <div class="summary-items">{summary_items}</div>
              <div class="cart-summary">
                <div class="summary-row"><span>Subtotal</span><span class="val">₱{subtotal}</span></div>
                <div class="summary-row"><span>Delivery Fee</span><span class="val">₱{fee}</span></div>
                <div class="summary-row total"><span>Total</span><span class="val">₱{total}</span></div>
              </div>
            </div>
          </aside>
        </div>

        <div class="checkout-total-bar">
          <div>
            <small>Total</small>
            <strong>₱{total}</strong>
          </div>
          <button class="btn btn-primary btn-lg" data-action="place_order">PLACE ORDER</button>
        </div>
      </div>
    </section>
    """.format(
        delivery=render_delivery_options(),
        payment=render_payment_options(),
        summary_items=summary_items_html,
        subtotal=cart_subtotal(), fee=delivery_fee(), total=cart_total(),
    )


# ===========================================================================
# 13. ORDER SUCCESS
# ===========================================================================

def render_success_screen():
    """The 'Order Placed!' overlay shown after submitting."""
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


# ===========================================================================
# 14. THE MAIN RENDER FUNCTION
# ===========================================================================

def render():
    """Rebuild the page from the current state and put it on the screen."""
    # Pick the main view based on what the user is looking at.
    current_view = state["view"]

    if current_view == "home":
        main_view_html = render_home_view()
    elif current_view == "menu":
        main_view_html = render_menu_view()
    elif current_view == "cart":
        main_view_html = render_cart_view()
    elif current_view == "checkout":
        main_view_html = render_checkout_view()
    else:
        # Fallback in case `view` is set to something we don't know about.
        main_view_html = render_home_view()

    # Put it all together.
    full_html = (
        '<div class="app-root">'
        + render_desktop_navbar()
        + render_mobile_header()
        + main_view_html
        + render_bottom_nav()
        + '</div>'
        + render_product_modal()
        + render_success_screen()
    )

    # Find the <div id="app"> and replace its contents.
    app_root = document.getElementById("app")
    app_root.innerHTML = full_html


# ===========================================================================
# 15. TOAST NOTIFICATIONS  (the little message that pops up at the bottom)
# ===========================================================================

def show_toast(message):
    """Show a small message at the bottom of the screen for a few seconds."""
    toast_host = document.getElementById("toast-host")
    toast_element = document.createElement("div")
    toast_element.className = "toast"
    toast_element.innerHTML = (
        '<span style="font-size:1rem;">✓</span><span>{}</span>'.format(safe(message))
    )
    toast_host.appendChild(toast_element)

    # Schedule the toast to be removed after ~2.6 seconds.
    def remove_toast(*ignored_args):
        try:
            toast_host.removeChild(toast_element)
        except Exception:
            pass

    setTimeout(create_proxy(remove_toast), 2600)


# ===========================================================================
# 16. EVENT HANDLERS
# ===========================================================================
# Instead of writing one giant function, we have one small function per
# action. The dispatcher at the bottom (`handle_click`) just decides which
# one to call based on the `data-action` attribute on the clicked element.

def find_action_element(target):
    """Walk up from the clicked element looking for one with `data-action`."""
    element = target
    while element is not None and getattr(element, "nodeType", None) == 1:
        if element.hasAttribute and element.hasAttribute("data-action"):
            return element
        element = element.parentElement
    return None


# ---- Individual handlers ----

def do_navigate(element):
    """Switch to a different top-level screen."""
    view = element.getAttribute("data-view")
    if view in ("home", "menu", "cart", "checkout"):
        state["view"] = view
        state["modal_open"] = False
        window.scrollTo(0, 0)
        render()
    else:
        show_toast("{} page coming soon!".format(view.title()))


def do_back():
    """Mobile back button. From cart go to menu, otherwise go home."""
    if state["view"] == "cart":
        state["view"] = "menu"
    else:
        state["view"] = "home"
    window.scrollTo(0, 0)
    render()


def do_select_category(element):
    """Switch the active Menu category."""
    state["category"] = element.getAttribute("data-category")
    if state["view"] != "menu":
        state["view"] = "menu"
        window.scrollTo(0, 0)
    render()


def do_open_product(element):
    """Open the product detail popup for a product."""
    product_id = int(element.getAttribute("data-product-id"))
    product = find_product(product_id)
    if product is None:
        return
    state["current_product"] = product
    # Reset options to defaults every time we open a new product.
    state["options"] = {"size": "M", "ice": "50%", "sweet": "50%", "qty": 1}
    state["modal_open"] = True
    render()


def do_close_modal():
    """Close the product detail popup."""
    state["modal_open"] = False
    state["current_product"] = None
    render()


def do_set_option(element):
    """Update one of the option chips (size / ice / sweetness)."""
    option_name = element.getAttribute("data-option")
    new_value = element.getAttribute("data-value")
    state["options"][option_name] = new_value
    render()


def do_change_qty(element):
    """Bump the quantity in the product detail popup up or down by 1."""
    direction = int(element.getAttribute("data-dir"))
    new_quantity = state["options"]["qty"] + direction
    # Clamp between 1 and 20.
    if new_quantity < 1:
        new_quantity = 1
    if new_quantity > 20:
        new_quantity = 20
    state["options"]["qty"] = new_quantity
    render()


def do_add_to_cart():
    """Add the currently-configured product to the cart."""
    product = state["current_product"]
    if product is None:
        return

    options = state["options"]
    size_delta = get_size_delta(options["size"])
    final_price = product["price"] + size_delta

    new_item = {
        "pid":   product["id"],
        "name":  product["name"],
        "color_a": product["color_a"],
        "color_b": product["color_b"],
        "price": final_price,
        "size":  options["size"],
        "ice":   options["ice"],
        "sweet": options["sweet"],
        "qty":   options["qty"],
    }
    state["cart"].append(new_item)

    # Close the modal and jump to the cart screen.
    product_name = product["name"]
    state["modal_open"] = False
    state["current_product"] = None
    state["view"] = "cart"

    render()
    show_toast("{} added to cart".format(product_name))


def do_quick_add(element):
    """Add a product with default options (M, 50%, 50%, 1) straight from a card."""
    product_id = int(element.getAttribute("data-product-id"))
    product = find_product(product_id)
    if product is None:
        return

    new_item = {
        "pid":   product["id"],
        "name":  product["name"],
        "color_a": product["color_a"],
        "color_b": product["color_b"],
        "price": product["price"],
        "size":  "M",
        "ice":   "50%",
        "sweet": "50%",
        "qty":   1,
    }
    state["cart"].append(new_item)
    show_toast("{} added to cart".format(product["name"]))
    render()


def do_cart_qty(element):
    """Bump the quantity of an item already in the cart."""
    index = int(element.getAttribute("data-idx"))
    direction = int(element.getAttribute("data-dir"))

    if index < 0 or index >= len(state["cart"]):
        return

    cart_item = state["cart"][index]
    new_quantity = cart_item["qty"] + direction
    if new_quantity < 1:
        new_quantity = 1
    if new_quantity > 20:
        new_quantity = 20
    cart_item["qty"] = new_quantity
    render()


def do_remove_cart(element):
    """Remove an item from the cart by its index."""
    index = int(element.getAttribute("data-idx"))
    if index < 0 or index >= len(state["cart"]):
        return
    removed_item = state["cart"].pop(index)
    show_toast("{} removed".format(removed_item["name"]))
    render()


def do_set_delivery(element):
    state["delivery_method"] = element.getAttribute("data-method")
    render()


def do_set_payment(element):
    state["payment_method"] = element.getAttribute("data-method")
    render()


def do_place_order():
    """User pressed PLACE ORDER — show the success screen."""
    state["order_placed"] = True
    render()


def do_finish_order():
    """After the success screen, reset and go home."""
    state["cart"] = []
    state["order_placed"] = False
    state["view"] = "home"
    window.scrollTo(0, 0)
    render()


# ---- The dispatcher ----

def handle_click(event):
    """Run on every click. Decides which handler to call."""
    element = find_action_element(event.target)
    if element is None:
        return

    action = element.getAttribute("data-action")

    # Big if/elif chain — one line per action.
    if action == "navigate":
        do_navigate(element)
    elif action == "back":
        do_back()
    elif action == "select_category":
        do_select_category(element)
    elif action == "open_product":
        do_open_product(element)
    elif action == "close_modal":
        do_close_modal()
    elif action == "set_option":
        do_set_option(element)
    elif action == "change_qty":
        do_change_qty(element)
    elif action == "add_to_cart":
        do_add_to_cart()
    elif action == "quick_add":
        do_quick_add(element)
    elif action == "cart_qty":
        do_cart_qty(element)
    elif action == "remove_cart":
        do_remove_cart(element)
    elif action == "set_delivery":
        do_set_delivery(element)
    elif action == "set_payment":
        do_set_payment(element)
    elif action == "place_order":
        do_place_order()
    elif action == "finish_order":
        do_finish_order()


def handle_keydown(event):
    """Close the product modal when the user presses Escape."""
    if event.key == "Escape" and state["modal_open"] and not state["order_placed"]:
        do_close_modal()


# ===========================================================================
# 17. BOOT  -- wire up the listeners and draw the first frame
# ===========================================================================

# create_proxy is needed so the JavaScript side can keep calling our Python
# functions without them being garbage-collected.
document.addEventListener("click",   create_proxy(handle_click))
document.addEventListener("keydown", create_proxy(handle_keydown))

# Render the first time so the user sees something.
render()
