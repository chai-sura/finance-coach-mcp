"""
Income tool - handles logging and retrieving income entries.
"""

from utils.storage import add, get_all, get_by_month, delete
from datetime import datetime


def log_income(amount: float, source: str, date: str = None, note: str = "") -> dict:
    """
    Log a new income entry.

    Args:
        amount: Income amount in dollars e.g. 3000.00
        source: Income source e.g. salary, freelance, investment, gift
        date:   Date in YYYY-MM-DD format, defaults to today
        note:   Optional note about the income

    Returns:
        The saved income entry
    """
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    entry = {
        "amount": round(amount, 2),
        "source": source.lower().strip(),
        "date":   date or datetime.now().strftime("%Y-%m-%d"),
        "note":   note.strip()
    }

    saved = add("income", entry)
    return {
        "success": True,
        "message": f"Logged ${amount:.2f} income from {source}",
        "entry":   saved
    }


def get_income(month: int = None, year: int = None) -> dict:
    """
    Get all income entries, optionally filtered by month and year.

    Args:
        month: Month number 1-12, defaults to current month
        year:  Year e.g. 2026, defaults to current year

    Returns:
        List of income entries and total amount
    """
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    income = get_by_month("income", year, month)
    total = sum(i["amount"] for i in income)

    return {
        "income": income,
        "total":  round(total, 2),
        "count":  len(income),
        "month":  datetime(year, month, 1).strftime("%B %Y")
    }


def get_income_by_source() -> dict:
    """
    Get all income grouped by source with totals.

    Returns:
        Dictionary of source totals
    """
    income = get_all("income")
    by_source = {}

    for i in income:
        source = i.get("source", "other")
        by_source[source] = round(by_source.get(source, 0) + i["amount"], 2)

    # Sort by highest income first
    sorted_sources = dict(
        sorted(by_source.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "by_source": sorted_sources,
        "total":     round(sum(by_source.values()), 2)
    }


def delete_income(income_id: str) -> dict:
    """
    Delete an income entry by ID.

    Args:
        income_id: The ID of the income entry to delete

    Returns:
        Success or failure message
    """
    deleted = delete("income", income_id)
    return {
        "success": deleted,
        "message": f"Income {income_id} deleted" if deleted else f"Income {income_id} not found"
    }