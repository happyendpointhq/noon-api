"""Price the same SKUs on several Noon storefronts, each in its own currency.

    python compare_markets.py N70211465V --regions ae,sa

`ae`, `sa` and `eg` are separate catalogues: a product can have a different price, a
different Buy Box seller, or not exist at all. `kw`, `qa`, `om` and `bh` sell the `ae`
assortment in their own currency. One /product-prices call per storefront (20 SKUs each).
Prices are shown in local currency; convert with your own FX rates before comparing.
"""

import argparse

from client import CURRENCIES, get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skus", help="comma-separated, up to 20")
    parser.add_argument("--regions", default="ae,sa")
    args = parser.parse_args()

    regions = args.regions.split(",")
    table = {}
    for region in regions:
        for row in get("/product-prices", region, skus=args.skus):
            table.setdefault(row["sku"], {"name": row.get("name")})[region] = row

    for sku, by_region in table.items():
        print(f"{sku}  {(by_region['name'] or '')[:70]}")
        for region in regions:
            row = by_region.get(region) or {}
            if row.get("found"):
                print(f"  {region}  {CURRENCIES[region]} {row['price']:>10,}  Buy Box: {row['seller_name']}")
            elif row.get("in_catalogue"):
                print(f"  {region}  listed, no seller right now")
            else:
                print(f"  {region}  not sold on this storefront")


if __name__ == "__main__":
    main()
