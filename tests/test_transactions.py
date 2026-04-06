from datetime import datetime
from src.transactions import (
    Transaction, normalize_amount, filter_by_status,
    calculate_total, categorize_spending, detect_duplicates,
)


def _txn(**kwargs):
    defaults = dict(
        id="t1", amount=100.0, currency="USD",
        merchant="ACME", category="retail",
        timestamp=datetime(2024, 1, 1, 12, 0, 0),
        user_id="u1", status="completed",
    )
    defaults.update(kwargs)
    return Transaction(**defaults)


def test_normalize_usd():
    assert normalize_amount(100.0, "USD") == 100.0

def test_normalize_eur():
    assert normalize_amount(100.0, "EUR") == 108.0

def test_filter_by_status():
    txns = [_txn(status="completed"), _txn(id="t2", status="pending")]
    assert len(filter_by_status(txns, "completed")) == 1

def test_calculate_total():
    txns = [_txn(amount=100.0), _txn(id="t2", amount=200.0)]
    assert calculate_total(txns) == 300.0

def test_categorize_spending():
    txns = [
        _txn(category="food",   amount=50.0),
        _txn(id="t2", category="food",   amount=30.0),
        _txn(id="t3", category="travel", amount=200.0),
    ]
    cats = categorize_spending(txns)
    assert cats["food"]   == 80.0
    assert cats["travel"] == 200.0

def test_detect_duplicates_found():
    t = datetime(2024, 1, 1, 12, 0, 0)
    txns = [
        _txn(id="t1", timestamp=t),
        _txn(id="t2", timestamp=t),
    ]
    assert len(detect_duplicates(txns)) == 1

def test_detect_duplicates_none():
    txns = [
        _txn(id="t1", amount=100.0),
        _txn(id="t2", amount=200.0),
    ]
    assert detect_duplicates(txns) == []