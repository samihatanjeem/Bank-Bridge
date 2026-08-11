"""
Data loading utilities for Bank Bridge.

Loads the financial products and account-opening process datasets from /data.
Keeping this as plain JSON + simple lookup functions on purpose — no database
needed for the hackathon MVP.
"""

import json
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"


def load_financial_products() -> list[dict]:
    """Load the full financial products dataset."""
    with open(DATA_DIR / "financial_products.json", encoding="utf-8") as f:
        return json.load(f)


def load_account_opening_process() -> list[dict]:
    """Load the full account-opening process dataset."""
    with open(DATA_DIR / "account_opening_process.json", encoding="utf-8") as f:
        return json.load(f)


def get_countries(products: list[dict], exclude_us: bool = True) -> list[str]:
    """Return the sorted list of distinct origin countries in the dataset."""
    countries = {p["country"] for p in products}
    if exclude_us:
        countries.discard("United States")
    return sorted(countries)


def get_products_for_country(products: list[dict], country: str) -> list[dict]:
    """Return all product entries for a given country."""
    return [p for p in products if p["country"] == country]


def find_product_by_term(products: list[dict], country: str, term: str) -> Optional[dict]:
    """
    Look up a product by matching the user's typed term (case-insensitive)
    against product_name_local and local_terms for the given country.
    """
    term_lower = term.strip().lower()
    for p in get_products_for_country(products, country):
        names = [p["product_name_local"].lower()] + [t.lower() for t in p["local_terms"]]
        if any(term_lower in name or name in term_lower for name in names):
            return p
    return None


def get_process_for_country(processes: list[dict], country: str) -> Optional[dict]:
    """Return the account-opening process entry for a given country."""
    for proc in processes:
        if proc["country"] == country:
            return proc
    return None
