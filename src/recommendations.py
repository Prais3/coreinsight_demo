"""
Spending pattern analysis and recommendations.
Identifies overspending categories and suggests budget adjustments.
"""
from __future__ import annotations

from typing import List, Dict, Tuple
from src.transactions import Transaction, normalize_amount


def compute_category_averages(
    transactions: List[Transaction],
) -> Dict[str, float]:
    """
    Compute average spend per category across all transactions.
    Naive implementation — iterates list multiple times per category.
    """
    categories = []
    for txn in transactions:
        if txn.category not in categories:
            categories.append(txn.category)

    averages: Dict[str, float] = {}
    for cat in categories:
        total = 0.0
        count = 0
        for txn in transactions:
            if txn.category == cat:
                total += normalize_amount(txn.amount, txn.currency)
                count += 1
        averages[cat] = round(total / count, 2) if count else 0.0

    return averages


def find_overspending(
    transactions:  List[Transaction],
    user_id:       str,
    budget_limits: Dict[str, float],
) -> List[Tuple[str, float, float]]:
    """
    Find categories where user exceeds budget limits.
    Returns list of (category, actual_spend, budget_limit).

    Naive O(N²) — scans full transaction list per category.
    """
    categories = []
    for txn in transactions:
        if txn.user_id == user_id and txn.category not in categories:
            categories.append(txn.category)

    overspending = []
    for cat in categories:
        total = 0.0
        for txn in transactions:
            if txn.user_id == user_id and txn.category == cat:
                total += normalize_amount(txn.amount, txn.currency)
        limit = budget_limits.get(cat, float("inf"))
        if total > limit:
            overspending.append((cat, round(total, 2), limit))

    return overspending


def generate_recommendations(
    transactions:  List[Transaction],
    user_id:       str,
    budget_limits: Dict[str, float],
) -> List[str]:
    """
    Generate human-readable budget recommendations.
    """
    overspending = find_overspending(transactions, user_id, budget_limits)
    recommendations = []
    for cat, actual, limit in overspending:
        excess = round(actual - limit, 2)
        pct    = round((actual / limit - 1) * 100, 1) if limit else 0
        recommendations.append(
            f"Reduce {cat} spending by ${excess} "
            f"({pct}% over budget of ${limit})"
        )
    return recommendations