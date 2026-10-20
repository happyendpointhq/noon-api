# Sample responses

Example `200` responses for four Noon API endpoints, copied from the API's public
documentation. Long arrays are cut to their first few items; field names and values are
otherwise unchanged. The field names were checked against live responses on 20 October
2026 and match.

| File | Request |
|---|---|
| `product-search.json` | `GET /product-search?region=ae&query=laptop` |
| `product-details.json` | `GET /product-details?region=ae&sku=N70211465V` |
| `product-offers.json` | `GET /product-offers?region=ae&sku=N70211465V` |
| `product-prices.json` | `GET /product-prices?region=ae&skus=N70211465V,N53433298A` |

They are useful for writing parsers and tests before you subscribe. Prices, sellers and
stock change constantly, so do not hard-code these values. For example, `N53433298A` has
no seller in the documented example but was on sale live when we tested.
