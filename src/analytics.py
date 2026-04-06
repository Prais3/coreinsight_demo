"""
Portfolio analytics and reporting.
Aggregations across transaction history for dashboard and reporting.
"""
from __future__ import annotations

from typing import List, Dict, Tuple
from datetime import datetime
from src.transactions import Transaction, normalize_amount


def daily_volume(
    transactions: List[Transaction],
) -> Dict[str, float]:
    """
    Compute total transaction volume per day.
    Returns dict of date_str -> total_usd.
    Naive — converts and sums on every call with no caching.
    """
    volumes: Dict[str, float] = {}
    for txn in transactions:
        date_str = txn.timestamp.strftime("%Y-%m-%d")
        usd      = normalize_amount(txn.amount, txn.currency)
        if date_str not in volumes:
            volumes[date_str] = 0.0
        volumes[date_str] += usd

    return {k: round(v, 2) for k, v in volumes.items()}


def top_spending_users(
    transactions: List[Transaction],
    top_n:        int = 10,
) -> List[Tuple[str, float]]:
    """
    Rank users by total spend descending.
    Returns list of (user_id, total_usd).
    Naive O(N²) sort.
    """
    user_totals: Dict[str, float] = {}
    for txn in transactions:
        usd = normalize_amount(txn.amount, txn.currency)
        if txn.user_id not in user_totals:
            user_totals[txn.user_id] = 0.0
        user_totals[txn.user_id] += usd

    # Insertion sort — intentionally naive
    items = list(user_totals.items())
    for i in range(1, len(items)):
        key = items[i]
        j   = i - 1
        while j >= 0 and items[j][1] < key[1]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key

    return [(uid, round(total, 2)) for uid, total in items[:top_n]]


def monthly_summary(
    transactions: List[Transaction],
    year:         int,
    month:        int,
) -> Dict[str, float]:
    """
    Summarize transaction activity for a given month.
    Returns dict with total_volume, avg_transaction,
    max_transaction, transaction_count.
    """
    filtered = []
    for txn in transactions:
        if txn.timestamp.year == year and txn.timestamp.month == month:
            filtered.append(txn)

    if not filtered:
        return {
            "total_volume":    0.0,
            "avg_transaction": 0.0,
            "max_transaction": 0.0,
            "transaction_count": 0.0,
        }

    amounts = [normalize_amount(t.amount, t.currency) for t in filtered]
    total   = sum(amounts)
    return {
        "total_volume":      round(total, 2),
        "avg_transaction":   round(total / len(amounts), 2),
        "max_transaction":   round(max(amounts), 2),
        "transaction_count": float(len(filtered)),
    }