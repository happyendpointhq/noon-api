"""Search a Noon storefront, then see every seller competing on the top result.

    python quickstart.py laptop          # UAE storefront, prices in AED
    python quickstart.py laptop sa       # Saudi storefront, prices in SAR
"""

import sys

from client import get

query = sys.argv[1] if len(sys.argv) > 1 else "laptop"
region = sys.argv[2] if len(sys.argv) > 2 else "ae"

# 1. Keyword search. Each row is a product card with its current Buy Box price and seller.
results = get("/product-search", region, query=query, page_size=5)
totals = results["totals"]
print(f"About {totals['estimated_matches']:,} matches for {query!r} on noon {region} (an estimate)\n")
# Small page sizes are not always honoured (page_size=5 returned 10 rows in our test), so slice.
for item in results["items"][:5]:
    was = f" (was {item['original_price']:,}, -{item['discount_percent']}%)" if item.get("original_price") else ""
    seller = (item.get("seller") or {}).get("name")
    print(f"{item['currency']} {item['price']:>9,}{was}  {item['brand']}  sku {item['sku']}")
    print(f"    {item['name'][:90]}")
    print(f"    sold by {seller}, rating {(item.get('rating') or {}).get('value')}")

# 2. Every offer on the first product. Index 0 holds the Buy Box.
if results["items"]:
    sku = results["items"][0]["sku"]
    offers = get("/product-offers", region, sku=sku)
    print(f"\n{offers['offer_count']} offers on {sku}:")
    for offer in offers["offers"]:
        flag = "BUY BOX" if offer["is_buy_box"] else "       "
        stock = offer.get("stock")
        print(
            f"  {flag} {offer['price']:>9,}  {offer['seller']['name']:<28} "
            f"stock {stock if stock is not None else '?'}  {(offer.get('delivery') or {}).get('message')}"
        )
