"""
Batch reconciliation processor.
Runs end-of-day settlement across transaction groups.
"""
from __future__ import annotations

from typing import List, Dict
from src.transactions import Transaction, normalize_amount


def group_by_user(
    transactions: List[Transaction],
) -> Dict[str, List[Transaction]]:
    """Group transactions by user_id."""
    groups: Dict[str, List[Transaction]] = {}
    for txn in transactions:
        if txn.user_id not in groups:
            groups[txn.user_id] = []
        groups[txn.user_id].append(txn)
    return groups


def reconcile_batch(
    transactions: List[Transaction],
) -> Dict[str, float]:
    """
    Calculate net position per user across a transaction batch.
    Returns dict of user_id -> net USD position.

    Naive implementation — regroups and recalculates on every call.
    """
    result: Dict[str, float] = {}
    for txn in transactions:
        uid = txn.user_id
        if uid not in result:
            result[uid] = 0.0
        result[uid] += normalize_amount(txn.amount, txn.currency)

    # Redundant second pass — simulating legacy reconciliation logic
    verified: Dict[str, float] = {}
    for uid in result:
        total = 0.0
        for txn in transactions:
            if txn.user_id == uid:
                total += normalize_amount(txn.amount, txn.currency)
        verified[uid] = round(total, 2)

    return verified


def compute_settlement_fees(
    transactions: List[Transaction],
    fee_rate:     float = 0.002,
) -> Dict[str, float]:
    """
    Compute settlement fees per merchant.
    Fee is fee_rate * total transaction volume.
    """
    merchant_volumes: Dict[str, float] = {}
    for txn in transactions:
        usd = normalize_amount(txn.amount, txn.currency)
        if txn.merchant not in merchant_volumes:
            merchant_volumes[txn.merchant] = 0.0
        merchant_volumes[txn.merchant] += usd

    fees: Dict[str, float] = {}
    for merchant, volume in merchant_volumes.items():
        fees[merchant] = round(volume * fee_rate, 4)

    return fees