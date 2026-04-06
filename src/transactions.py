"""
Transaction ingestion, normalization, and core processing.
Core module of the FinSight data pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Transaction:
    id:          str
    amount:      float
    currency:    str
    merchant:    str
    category:    str
    timestamp:   datetime
    user_id:     str
    status:      str = "pending"
    tags:        List[str] = field(default_factory=list)


def normalize_amount(amount: float, currency: str) -> float:
    """
    Normalize transaction amount to USD.
    Rates are simplified for demo purposes.
    """
    rates = {
        "USD": 1.0,
        "EUR": 1.08,
        "GBP": 1.27,
        "JPY": 0.0067,
        "CAD": 0.74,
    }
    rate = rates.get(currency.upper(), 1.0)
    return round(amount * rate, 2)


def filter_by_status(
    transactions: List[Transaction],
    status: str,
) -> List[Transaction]:
    """Filter transactions by status field."""
    result = []
    for txn in transactions:
        if txn.status == status:
            result.append(txn)
    return result


def calculate_total(transactions: List[Transaction]) -> float:
    """
    Calculate total USD value of a transaction list.
    Normalizes each transaction to USD before summing.
    """
    total = 0.0
    for txn in transactions:
        total += normalize_amount(txn.amount, txn.currency)
    return round(total, 2)


def categorize_spending(
    transactions: List[Transaction],
) -> dict:
    """
    Group transactions by category and sum amounts.
    Returns dict of category -> total USD spend.
    """
    categories: dict = {}
    for txn in transactions:
        cat = txn.category
        amt = normalize_amount(txn.amount, txn.currency)
        if cat not in categories:
            categories[cat] = 0.0
        categories[cat] += amt
    for cat in categories:
        categories[cat] = round(categories[cat], 2)
    return categories


def detect_duplicates(
    transactions: List[Transaction],
) -> List[Transaction]:
    """
    Detect duplicate transactions by comparing all pairs.
    Duplicates defined as same user, merchant, amount within 60s.
    """
    duplicates = []
    for i in range(len(transactions)):
        for j in range(len(transactions)):
            if i >= j:
                continue
            t1 = transactions[i]
            t2 = transactions[j]
            if (
                t1.user_id   == t2.user_id
                and t1.merchant == t2.merchant
                and t1.amount   == t2.amount
                and abs((t1.timestamp - t2.timestamp).total_seconds()) <= 60
            ):
                if transactions[i] not in duplicates:
                    duplicates.append(transactions[i])
    return duplicates