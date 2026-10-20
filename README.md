# Noon API and Scraper

The Noon API returns product data from noon.com storefronts in the UAE, Saudi Arabia,
Egypt, Kuwait, Qatar, Oman and Bahrain as JSON: keyword and category search, prices and
discounts, every seller competing for the Buy Box, stock, delivery promises, reviews,
seller profiles, deals and sponsored listings. It reads the public storefront, so you get
competitor prices and offers without building or maintaining a noon scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/noon-api?utm_source=github&utm_medium=readme&utm_campaign=noon-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/noon7
- Product page: https://happyendpoint.com/library/noon-api?utm_source=github&utm_medium=readme&utm_campaign=noon-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://noon7.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 27, all `GET` |
| Storefronts | `ae`, `sa`, `eg`, `kw`, `qa`, `om`, `bh`, each priced in its own currency |
| Languages | English and Arabic (`language=en` or `ar`) |
| Page size | Up to 200 products, 10,000 per query |
| Format | JSON, every response wrapped in `{"success": true, "data": ...}` |

---

## What data you get

**Search and browse**
- Keyword search, category listings, a seller's catalogue, deal campaign listings and sponsored placements, with price, rating, brand, seller and attribute filters
- Paste any noon search or category URL and get the same listing as data
- Autocomplete, the category tree, brands, live deal campaigns

**Products**
- Current price, crossed-out price and discount, stock flags, badges, promotions, specifications, variants
- Full product record: description, feature bullets, media, breadcrumbs, best seller rank, the Buy Box summary
- Prices for up to 20 SKUs in one call

**Sellers and offers**
- Every offer on a product, with the Buy Box winner first: price, stock, delivery promise, warranty, return policy, seller rating and metrics
- Seller profiles and seller reviews

**Reviews**
- Product reviews with rating, language, photo and verified filters, a review summary and review images

**Logistics and food**
- Parcel lockers and pickup points, area lookup by coordinates
- noon Food zones, restaurants near a point and full menus

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/noon7). Copy `.env.example`
to `.env` and paste your key.

### 2. Make a request

```bash
curl "https://noon7.p.rapidapi.com/product-search?region=ae&query=laptop&page_size=20" \
  -H "x-rapidapi-host: noon7.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://noon7.p.rapidapi.com/product-offers?region=ae&sku=N70211465V" \
  -H "x-rapidapi-host: noon7.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py laptop        # UAE storefront
python quickstart.py laptop sa     # Saudi storefront
```

```python
from client import get

results = get("/product-search", "ae", query="laptop", page_size=20)
for item in results["items"]:
    print(item["currency"], item["price"], item["sku"], item["name"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs laptop ae
```

---

## Example response

One row from `GET /product-prices?region=ae&skus=N70211465V`. Values are the example in the
API's public documentation. Full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": [
    {
      "sku": "N70211465V",
      "found": true,
      "in_catalogue": true,
      "error": null,
      "price": 4496,
      "original_price": 5099,
      "discount_percent": 12,
      "name": "iPhone 17 Pro Max 256 GB (eSIM only) Cosmic Orange 5G With FaceTime - International Version",
      "brand": "Apple",
      "offer_code": "f3c5559785715d9e",
      "in_stock": true,
      "seller_name": "callmate",
      "market": "ae",
      "currency": "AED"
    }
  ]
}
```

---

## Endpoints

Base URL: `https://noon7.p.rapidapi.com`. Every catalogue endpoint takes `region` and
`language`.

### Discovery

| Endpoint | Returns |
|---|---|
| `GET /marketplace` | Which catalogue, country and currency a storefront resolves to |
| `GET /autocomplete` | Query, brand, category and product suggestions |
| `GET /categories` | The category tree, or one branch |
| `GET /brands` | Brands, searchable and paged |
| `GET /deal-campaigns` | Live deal campaigns and their codes |

### Listings

| Endpoint | Returns |
|---|---|
| `GET /product-search` | Products for a keyword, with filters and sorts |
| `GET /category-products` | Products in a category |
| `GET /seller-products` | One seller's catalogue |
| `GET /deal-products` | Products in a deal campaign |
| `GET /sponsored-products` | Sponsored placements for a query or category |
| `GET /products-by-url` | The listing behind a pasted noon search or category URL |

### Products and offers

| Endpoint | Returns |
|---|---|
| `GET /product-details` | The full product record with a Buy Box summary |
| `GET /product-by-url` | The same, from a noon product URL |
| `GET /product-offers` | Every seller's offer, Buy Box winner first |
| `GET /product-prices` | Price, discount and stock for up to 20 SKUs |
| `GET /related-products` | Related products for one or more SKUs |

### Reviews and sellers

| Endpoint | Returns |
|---|---|
| `GET /product-reviews` | Product reviews with filters and sorts |
| `GET /review-summary` | Rating distribution and summary for a product |
| `GET /review-images` | Customer photos for a product |
| `GET /seller-profile` | A seller's ratings, metrics and badges |
| `GET /seller-reviews` | Reviews of a seller |

### Logistics and noon Food

| Endpoint | Returns |
|---|---|
| `GET /collection-points` | Parcel lockers and pickup points |
| `GET /area-by-coordinates` | The delivery area for a point |
| `GET /food-zones` | noon Food delivery zones |
| `GET /food-restaurants` | Restaurants near a point, with cuisine and price filters |
| `GET /food-menu` | A restaurant's menu |
| `GET /status` | Service health |

---

## Things to know about the data

These come from building against the API, including live calls in October 2026.

- **Storefronts are separate catalogues.** `ae`, `sa` and `eg` each have their own prices,
  sellers and assortment; `kw`, `qa`, `om` and `bh` sell the `ae` assortment in their own
  currency. In our live test the same Acer laptop was AED 2,285 on `ae` and SAR 3,069 on
  `sa`, and an iPhone had a different Buy Box seller on each. Always store `currency` with
  the price, and convert with your own FX rates before comparing.
- **Prices are not always whole numbers.** Live rows included AED 2,798.95 and 2,301.05,
  and `kw`, `om` and `bh` price in three-decimal currencies. Do not store prices as
  integers.
- **`original_price` is null when there is no discount.** Live, 2 of 10 laptop cards had
  no crossed-out price, and `discount_percent` was null with it.
- **`rating` can be `null` as a whole object**, not `{"value": null}`. Six of ten live
  laptop cards had no rating at all. Guard with `(item.get("rating") or {})`.
- **noon itself is often the seller.** In the live laptop search, 6 of 10 cards had the
  Buy Box held by `noon` (first-party retail), the rest by marketplace sellers. Use
  `/product-offers` to see who else is selling: offers come in noon's own order, index `0`
  is the Buy Box winner, and `offer_count` is the length of `offers`, not proof that no
  other seller exists.
- **Do not trust the row count to equal `page_size`.** A live call with `page_size=5`
  returned 10 products while `pagination.page_size` said 5. Slice locally if you need an
  exact number.
- **`totals.estimated_matches` is an estimate.** Identical calls can differ (1,309 in the
  documented example, 1,263 live for the same query). Page on `pagination.has_more`, at
  most 50 pages of 200, and split by category, brand or price window when
  `totals.exceeds_retrievable_cap` is true.
- **Keyword pages can overlap.** Ranking is recomputed per request, so deduplicate on
  `sku` when you crawl a search.
- **A missing price has three causes.** On `/product-prices`, read `found`, `in_catalogue`
  and `error` together: listed but nobody selling, not on this storefront, or a failed
  lookup. A SKU the storefront does not hold is a 404 on the single-product endpoints.
- **`sort=price` is broad, not strict.** It reaches the cheap or expensive end reliably,
  but a few rows can sit out of order. Re-sort locally.
- **`low_stock_count: null` means not flagged as scarce**, not zero stock. Per-seller stock
  is `stock` on `/product-offers`.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Searches a storefront, then lists every seller's offer on the top product |
| [`examples/python/price_watch.py`](examples/python/price_watch.py) | Tracks prices for a SKU list and reports changes, 20 SKUs per call |
| [`examples/python/compare_markets.py`](examples/python/compare_markets.py) | Prices the same SKUs on several storefronts, each in its own currency |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | Keyword search in Node 18+, no dependencies |
| [`samples/`](samples/) | Documented example responses for four endpoints |

---

## API or your own noon scraper

A homemade noon scraper has to keep up with page changes, bot protection and seven
storefronts that each behave differently. This API returns the same storefront data as
documented JSON, so the work you keep is the pricing analysis, not the parser. If you need
a recurring export of a category or a whole storefront rather than API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=noon-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query noon prices
and offers without code:

```json
{
  "mcpServers": {
    "noon": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: noon7.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a noon API?

noon provides integrations for its own sellers (to manage their listings and orders) and
for noon payments. This API is different: it reads the public storefront, so you can see
any product's price, sellers and reviews, not only your own. It is built and maintained
by Happy Endpoint and is independent of noon.

### Is there a free noon API?

Yes. The RapidAPI listing has a free plan, and every endpoint can be tried on it.

### Where is the noon API documentation?

Every endpoint, parameter and response is documented on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/noon7). The endpoint table above
summarises them, and [`samples/`](samples/) has example responses.

### Can I scrape noon prices for free?

You can try every endpoint on the free plan. For a price list, `/product-prices` returns
up to 20 SKUs per call, which keeps the number of calls low.
[`price_watch.py`](examples/python/price_watch.py) shows the pattern.

### Can I see who holds the Buy Box on a product?

Yes. `/product-offers` lists every seller's offer with the Buy Box winner first and
`is_buy_box: true`, plus each seller's price, stock and delivery promise.

### Does it cover noon Saudi Arabia and Egypt?

Yes. Set `region` to `sa`, `eg`, `kw`, `qa`, `om` or `bh` (default `ae`), and `language`
to `ar` for Arabic names.

### Is there a noon Food API?

The API includes noon Food zones, restaurants near a point and restaurant menus.

---

## Related repos

- [awesome-ecommerce-data-apis](https://github.com/happyendpointhq/awesome-ecommerce-data-apis) - ecommerce and product data APIs, including free and official ones
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources, including web-scraped pricing data
- [sephora-api](https://github.com/happyendpointhq/sephora-api) - beauty product prices, reviews and store stock
- [ikea-api](https://github.com/happyendpointhq/ikea-api) - IKEA products, categories and store data

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
