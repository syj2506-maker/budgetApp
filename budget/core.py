"""Core business logic for the budget CLI app."""

from __future__ import annotations

import csv
from typing import Any, Dict, List


Transaction = Dict[str, Any]


def add_transaction(transactions: List[Transaction], transaction: Transaction) -> List[Transaction]:
    """Add a transaction to the list and return the updated list."""
    updated_transactions = list(transactions)
    updated_transactions.append(
        {
            "date": transaction["date"],
            "type": transaction["type"],
            "category": transaction["category"],
            "description": transaction["description"],
            "amount": transaction["amount"],
            "memo": transaction["memo"],
        }
    )
    return updated_transactions


def load_transactions_from_csv(csv_path: str) -> List[Transaction]:
    """Load transactions from a CSV file and return them as a list."""
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            {
                "date": row["date"],
                "type": row["type"],
                "category": row["category"],
                "description": row["description"],
                "amount": int(row["amount"]),
                "memo": row["memo"],
            }
            for row in reader
        ]


def get_balance(transactions: List[Transaction]) -> float:
    """Return the balance computed from the transaction list."""
    if not transactions:
        return 0.0

    return float(sum(transaction["amount"] for transaction in transactions))


def filter_by_category(transactions: List[Transaction], category: str) -> List[Transaction]:
    """Return transactions matching the given category."""
    normalized_category = category.casefold()
    return [
        transaction
        for transaction in transactions
        if str(transaction["category"]).casefold() == normalized_category
    ]


def monthly_summary(transactions: List[Transaction]) -> Dict[str, Dict[str, float]]:
    """Return monthly income, expense, and net summary."""
    summary: Dict[str, Dict[str, float]] = {}

    for transaction in transactions:
        month = str(transaction["date"])[:7]
        amount = transaction["amount"]
        month_summary = summary.setdefault(
            month,
            {"income": 0, "expense": 0, "net": 0},
        )
        if amount >= 0:
            month_summary["income"] += amount
        else:
            month_summary["expense"] += amount
        month_summary["net"] += amount

    return summary
