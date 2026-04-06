from datetime import datetime
from src.transactions import Transaction
from src.search import search_transactions, rank_merchants_by_spend


def _txn(**kwargs):
    defaults = dict(
        id="t1", amount=100.0, currency="USD",
        merchant="Starbucks", category="food",
        timestamp=datetime(2024, 1, 1, 12, 0, 0),
        user_id="u1", status="completed",
    )
    defaults.update(kwargs)
    return Transaction(**defaults)


def test_search_by_merchant():
    txns = [_txn(), _txn(id="t2", merchant="Amazon")]
    results = search_transactions(txns, "amazon")
    assert len(results) == 1
    assert results[0].merchant == "Amazon"

def test_search_no_results():
    txns = [_txn()]
    assert search_transactions(txns, "nonexistent") == []

def test_rank_merchants():
    txns = [
        _txn(merchant="A", amount=100.0),
        _txn(id="t2", merchant="B", amount=500.0),
        _txn(id="t3", merchant="A", amount=200.0),
    ]
    ranked = rank_merchants_by_spend(txns)
    assert ranked[0][0] == "B"
    assert ranked[1][0] == "A"