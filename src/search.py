"""
Multi-field transaction search.
Added in v0.2 to support the transaction history UI.
"""
from __future__ import annotations

from typing import List, Optional
from src.transactions import Transaction


def search_transactions(
    transactions: List[Transaction],
    query:        str,
    fields:       Optional[List[str]] = None,
) -> List[Transaction]:
    """
    Search transactions by matching query string against
    merchant, category, tags, and user_id fields.

    Naive implementation — scans all transactions for each query.
    """
    if fields is None:
        fields = ["merchant", "category", "user_id"]

    results = []
    query_lower = query.lower()

    for txn in transactions:
        for field in fields:
            value = getattr(txn, field, "")
            if isinstance(value, list):
                value = " ".join(value)
            if query_lower in str(value).lower():
                if txn not in results:
                    results.append(txn)
    return results


def search_by_amount_range(
    transactions: List[Transaction],
    min_amount:   float,
    max_amount:   float,
) -> List[Transaction]:
    """Return transactions within a USD amount range."""
    from src.transactions import normalize_amount
    results = []
    for txn in transactions:
        usd = normalize_amount(txn.amount, txn.currency)
        if min_amount <= usd <= max_amount:
            results.append(txn)
    return results


def rank_merchants_by_spend(
    transactions: List[Transaction],
) -> List[tuple]:
    """
    Rank merchants by total spend descending.
    Returns list of (merchant, total_usd) tuples.
    Naive O(N²) sort.
    """
    from src.transactions import normalize_amount

    merchant_totals: dict = {}
    for txn in transactions:
        usd = normalize_amount(txn.amount, txn.currency)
        if txn.merchant not in merchant_totals:
            merchant_totals[txn.merchant] = 0.0
        merchant_totals[txn.merchant] += usd

    # Bubble sort — intentionally naive
    items = list(merchant_totals.items())
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j][1] < items[j + 1][1]:
                items[j], items[j + 1] = items[j + 1], items[j]

    return [(m, round(t, 2)) for m, t in items]