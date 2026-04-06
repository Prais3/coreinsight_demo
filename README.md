# FinSight — Transaction Analysis Platform

A financial data processing pipeline for transaction analysis,
fraud pattern detection, and spending recommendations.

## Features

- Transaction ingestion and normalization
- Multi-field search across transaction history  
- Batch processing for end-of-day reconciliation
- Spending pattern analysis and recommendations
- Portfolio analytics and reporting

## Performance

All performance-critical functions are continuously reviewed by
[CoreInsight](https://github.com/Prais3/coreinsight_cli) on every PR.
Optimizations are sandbox-verified before merge.

See the [pull request history](../../pulls?q=is%3Apr+is%3Aclosed)
for examples of CoreInsight catching real bottlenecks.

## Setup
```bash
pip install -r requirements.txt
python -m pytest tests/
```

## Structure
src/
├── transactions.py    # Core transaction processing
├── search.py          # Multi-field transaction search
├── batch.py           # Batch reconciliation processor
├── recommendations.py # Spending pattern recommendations
└── analytics.py       # Portfolio analytics and reporting