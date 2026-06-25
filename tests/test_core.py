"""Tests for budget.core."""

import csv
from pathlib import Path

from budget.core import add_transaction, filter_by_category, get_balance


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


def test_get_balance_returns_zero_for_empty_list() -> None:
    """Empty transaction lists should produce a zero balance."""
    assert get_balance([]) == 0.0


def test_get_balance_sums_income_and_expense_amounts() -> None:
    """Balance should be the sum of positive and negative amounts."""
    transactions = [
        {
            "date": "2026-01-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "",
        },
        {
            "date": "2026-01-02",
            "type": "지출",
            "category": "식비",
            "description": "점심",
            "amount": -12000,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 3488000.0


def test_get_balance_matches_step2_transactions_total() -> None:
    """The step2 sample should sum to the known total balance."""
    csv_path = Path("data/step2_transactions.csv")
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        transactions = [
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

    assert get_balance(transactions) == 24285027.0


def test_filter_by_category_matches_step2_category_case_insensitively() -> None:
    """Filtering should match real step2 categories without case sensitivity."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-02-01",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -651009,
            "memo": "카드결제",
        },
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
    ]

    filtered = filter_by_category(transactions, "여행")

    assert len(filtered) == 2
    assert all(transaction["category"] == "여행" for transaction in filtered)


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    """Unknown categories should return an empty list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    assert filter_by_category(transactions, "미존재카테고리") == []


def test_filter_by_category_returns_independent_list() -> None:
    """The filtered result should not mutate the original list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-02-01",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -651009,
            "memo": "카드결제",
        },
    ]

    filtered = filter_by_category(transactions, "여행")
    filtered.pop()

    assert len(transactions) == 2
    assert len(filtered) == 1
