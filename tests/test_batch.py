from datetime import datetime
from src.transactions import Transaction
from src.batch import reconcile_batch, compute_settlement_fees


def _txn(**kwargs):
    defaults = dict(
        id="t1", amount=100.0, currency="USD",
        merchant="ACME", category="retail",
        timestamp=datetime(2024, 1, 1, 12, 0, 0),
        user_id="u1", status="completed",
    )
    defaults.update(kwargs)
    return Transaction(**defaults)


def test_reconcile_single_user():
    txns = [_txn(amount=100.0), _txn(id="t2", amount=200.0)]
    result = reconcile_batch(txns)
    assert result["u1"] == 300.0

def test_reconcile_multiple_users():
    txns = [
        _txn(id="t1", user_id="u1", amount=100.0),
        _txn(id="t2", user_id="u2", amount=250.0),
    ]
    result = reconcile_batch(txns)
    assert result["u1"] == 100.0
    assert result["u2"] == 250.0

def test_settlement_fees():
    txns = [_txn(merchant="ACME", amount=1000.0)]
    fees = compute_settlement_fees(txns)
    assert fees["ACME"] == 2.0