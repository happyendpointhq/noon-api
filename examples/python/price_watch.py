"""Track Noon prices for a list of SKUs and report changes since the last run.

    python price_watch.py N70211465V N53433298A     # add SKUs and check them
    python price_watch.py                            # check the saved list again later
    python price_watch.py --region sa                # check the Saudi storefront

Uses /product-prices: up to 20 SKUs per call, rows returned in the order sent. A SKU with
no price does not fail the call; `found`, `in_catalogue` and `error` say why.
"""

import argparse
import json
from datetime import date
from pathlib import Path

from client import get


def status(row):
    if row.get("error"):
        return f"lookup failed: {row['error']}"
    if row["found"]:
        return None
    if row["in_catalogue"]:
        return "listed, but nobody is selling it right now"
    return "not on this storefront"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skus", nargs="*")
    parser.add_argument("--region", default="ae")
    args = parser.parse_args()

    state_file = Path(f"noon-prices-{args.region}.json")
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    for sku in args.skus:
        state.setdefault(sku, {})
    if not state:
        raise SystemExit("Pass at least one SKU, for example N70211465V")

    skus = list(state)
    for start in range(0, len(skus), 20):
        for row in get("/product-prices", args.region, skus=",".join(skus[start:start + 20])):
            before = state[row["sku"]].get("price")
            problem = status(row)
            if problem:
                print(f"{row['sku']}  {problem}  ({row.get('name') or ''})")
            else:
                change = "new" if before is None else (
                    "unchanged" if row["price"] == before else f"{before:,} -> {row['price']:,}"
                )
                print(f"{row['sku']}  {row['currency']} {row['price']:>9,}  {change:<20} {row['seller_name']}")
            state[row["sku"]] = {
                "name": row.get("name"),
                "price": row.get("price"),
                "seller": row.get("seller_name"),
                "checked": str(date.today()),
            }

    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
