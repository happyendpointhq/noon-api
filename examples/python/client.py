"""Minimal client for the Noon API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "noon7.p.rapidapi.com"

# Storefronts and the currency each one prices in.
CURRENCIES = {"ae": "AED", "sa": "SAR", "eg": "EGP", "kw": "KWD", "qa": "QAR", "om": "OMR", "bh": "BHD"}


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, region="ae", **params):
    """GET an endpoint on one storefront and return the `data` part of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={"region": region, **{k: v for k, v in params.items() if v is not None}},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    # A SKU the storefront does not hold is a 404, not an empty record.
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]
