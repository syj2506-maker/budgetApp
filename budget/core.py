"""Core business logic for the budget CLI app."""

from __future__ import annotations

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
    pass


def get_balance(transactions: List[Transaction]) -> float:
    """Return the balance computed from the transaction list."""
    pass


def filter_by_category(transactions: List[Transaction], category: str) -> List[Transaction]:
    """Return transactions matching the given category."""
    pass


def monthly_summary(transactions: List[Transaction]) -> Dict[str, Dict[str, float]]:
    """Return monthly income, expense, and net summary."""
    pass
