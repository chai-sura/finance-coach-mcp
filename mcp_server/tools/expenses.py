"""
Expenses tool - handles logging and retrieving expenses.
"""

from utils.storage import add, get_all, get_by_month, delete
from datetime import datetime


def log_expense(amount: float, category: str, date: str = None, note: str = "") -> dict:
    """
    Log a new expense entry.

    Args:
        amount:   Expense amount in dollars e.g. 50.00
        category: Category e.g. groceries, dining, rent, transport
        date:     Date in YYYY-MM-DD format, defaults to today
        note:     Optional note about the expense

    Returns:
        The saved expense entry
    """
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    entry = {
        "amount":   round(amount, 2),
        "category": category.lower().strip(),
        "date":     date or datetime.now().strftime("%Y-%m-%d"),
        "note":     note.strip()
    }

    saved = add("expenses", entry)
    return {
        "success": True,
        "message": f"Logged ${amount:.2f} for {category}",
        "entry":   saved
    }


def get_expenses(month: int = None, year: int = None) -> dict:
    """
    Get all expenses, optionally filtered by month and year.

    Args:
        month: Month number 1-12, defaults to current month
        year:  Year e.g. 2026, defaults to current year

    Returns:
        List of expenses and total amount
    """
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    expenses = get_by_month("expenses", year, month)
    total = sum(e["amount"] for e in expenses)

    return {
        "expenses": expenses,
        "total":    round(total, 2),
        "count":    len(expenses),
        "month":    datetime(year, month, 1).strftime("%B %Y")
    }


def delete_expense(expense_id: str) -> dict:
    """
    Delete an expense by ID.

    Args:
        expense_id: The ID of the expense to delete

    Returns:
        Success or failure message
    """
    deleted = delete("expenses", expense_id)
    return {
        "success": deleted,
        "message": f"Expense {expense_id} deleted" if deleted else f"Expense {expense_id} not found"
    }


def get_expenses_by_category() -> dict:
    """
    Get all expenses grouped by category with totals.

    Returns:
        Dictionary of category totals
    """
    expenses = get_all("expenses")
    by_category = {}

    for e in expenses:
        cat = e.get("category", "other")
        by_category[cat] = round(by_category.get(cat, 0) + e["amount"], 2)

    # Sort by highest spending first
    sorted_categories = dict(
        sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "by_category": sorted_categories,
        "total":       round(sum(by_category.values()), 2)
    }