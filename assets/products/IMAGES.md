# Product Images

Drop product photos into **this folder** and they'll appear in the app
automatically. If a file is missing or fails to load, the drawn SVG cup
takes over — so the app keeps working while you're still gathering images.

## Expected filenames

Save your files with these **exact** names (case matters, all lowercase,
hyphens between words):

| Product               | Filename                              |
|-----------------------|---------------------------------------|
| Brown Sugar Milk Tea  | `brown-sugar-milk-tea.jpg`            |
| Matcha Milk Tea       | `matcha-milk-tea.jpg`                 |
| Wintermelon Milk Tea  | `wintermelon-milk-tea.jpg`            |
| Taro Milk Tea         | `taro-milk-tea.jpg`                   |
| Okinawa Milk Tea      | `okinawa-milk-tea.jpg`                |
| Hokkaido Milk Tea     | `hokkaido-milk-tea.jpg`               |
| Matcha Latte          | `matcha-latte.jpg`                    |
| Caramel Macchiato     | `caramel-macchiato.jpg`               |
| Brown Sugar Latte     | `brown-sugar-latte.jpg`               |
| Iced Americano        | `iced-americano.jpg`                  |
| BrewCha Signature     | `brewcha-signature.jpg`               |
| Cookies & Cream Frappe| `cookies-and-cream-frappe.jpg`        |
| Strawberry Yakult     | `strawberry-yakult.jpg`               |
| Tapioca Pearls        | `tapioca-pearls.jpg`                  |
| Pudding               | `pudding.jpg`                         |
| Cheese Foam           | `cheese-foam.jpg`                     |
| Crystal Boba          | `crystal-boba.jpg`                    |

> Want a different filename or format (`.png`, `.webp`)? Edit the `image`
> field on that product in `main.py`. Example:
> `"image": "assets/products/my-photo.png"`

## Recommended size

- **500 × 500 pixels** minimum, square (1:1) crop works best
- File size under **200 KB** keeps things snappy
- `.jpg` for photos, `.png` if you need transparency

## Where to get free milk tea / coffee photos

All of these allow free commercial use, no attribution required:

| Site       | Browse / Search                                             |
|------------|-------------------------------------------------------------|
| Unsplash   | https://unsplash.com/s/photos/milk-tea                      |
| Unsplash   | https://unsplash.com/s/photos/bubble-tea                    |
| Unsplash   | https://unsplash.com/s/photos/boba                          |
| Pexels     | https://www.pexels.com/search/milk%20tea/                   |
| Pexels     | https://www.pexels.com/search/bubble%20tea/                 |
| Pixabay    | https://pixabay.com/images/search/bubble%20tea/             |
| Freepik    | https://www.freepik.com/search?query=milk+tea (free w/ acct)|

### How to download from Unsplash (fastest)

1. Open one of the URLs above.
2. Click a photo you like.
3. Press the **Download free** button (top-right of the photo).
4. Rename the file to match the table above.
5. Drop it into this folder.
6. Refresh the browser — your photo appears.

## Specific search keywords per product

If you want photos that match each drink closely:

- Brown Sugar Milk Tea → search `brown sugar boba`
- Matcha Milk Tea → search `matcha latte` or `matcha bubble tea`
- Wintermelon Milk Tea → search `wintermelon tea` or `iced tea`
- Taro Milk Tea → search `taro` or `taro latte` (purple drink)
- Okinawa / Hokkaido → search `milk tea` (golden-brown)
- Caramel Macchiato → search `caramel macchiato`
- Iced Americano → search `iced coffee`
- Cookies & Cream Frappe → search `frappe` or `frappuccino`
- Strawberry Yakult → search `strawberry milk` or `pink drink`
- Tapioca Pearls / Crystal Boba → search `tapioca pearls` or `boba pearls`
- Pudding → search `egg pudding` or `flan`
- Cheese Foam → search `cheese tea` or `cheese foam`

## How the fallback works (so you don't worry about broken images)

Each `<img>` tag in the page has an `onerror` handler. If the image file
isn't there, the browser silently hides the `<img>` and shows the drawn
SVG cup behind it instead. You'll never see a broken image icon.
