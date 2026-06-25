"""Tests for budget.core."""

from budget.core import add_transaction


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the list length by one."""
    transactions = []
    transaction = {
        "date": "2026-01-01",
        "type": "income",
        "category": "salary",
        "description": "January salary",
        "amount": 3000000,
        "memo": "",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert len(updated_transactions) == 1


def test_add_transaction_preserves_negative_amount_expense() -> None:
    """Expense transactions should keep a negative amount."""
    transactions = []
    transaction = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert updated_transactions[0]["amount"] == -12000
    assert updated_transactions[0]["type"] == "지출"
    assert updated_transactions[0]["category"] == "식비"


def test_add_transaction_preserves_positive_amount_income() -> None:
    """Income transactions should keep a positive amount."""
    transactions = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert updated_transactions[0]["amount"] == 3500000
    assert updated_transactions[0]["type"] == "수입"
    assert updated_transactions[0]["memo"] == "1월급여"


def test_add_transaction_handles_empty_description() -> None:
    """Adding a transaction with an empty description should preserve it."""
    transactions = []
    transaction = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "",
        "amount": 25000,
        "memo": "중고마켓",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert updated_transactions[0]["description"] == ""
    assert updated_transactions[0]["amount"] == 25000
    assert updated_transactions[0]["memo"] == "중고마켓"
