"""
Budgets tool - handles setting and tracking budget limits per category.
"""

from utils.storage import upsert_budget, get_all, get_by_month
from datetime import datetime


def set_budget(category: str, amount: float, period: str = "monthly") -> dict:
    """
    Set or update a budget limit for a category.

    Args:
        category: Expense category e.g. groceries, dining, rent
        amount:   Budget limit in dollars e.g. 300.00
        period:   Budget period - monthly or weekly, defaults to monthly

    Returns:
        The saved budget entry
    """
    if amount <= 0:
        raise ValueError("Budget amount must be greater than 0")

    if period not in ["monthly", "weekly"]:
        raise ValueError("Period must be monthly or weekly")

    saved = upsert_budget(
        category=category.lower().strip(),
        amount=round(amount, 2),
        period=period
    )

    return {
        "success": True,
        "message": f"Budget set for {category}: ${amount:.2f} {period}",
        "entry":   saved
    }


def get_budgets() -> dict:
    """
    Get all budgets with current spending status.

    Returns:
        List of budgets with spent amount and remaining balance
    """
    budgets = get_all("budgets")
    now = datetime.now()

    # Get current month expenses
    expenses = get_by_month("expenses", now.year, now.month)

    # Group expenses by category
    spent_by_category = {}
    for e in expenses:
        cat = e.get("category", "other")
        spent_by_category[cat] = round(
            spent_by_category.get(cat, 0) + e["amount"], 2
        )

    # Attach spending info to each budget
    enriched = []
    for b in budgets:
        cat = b["category"]
        spent = spent_by_category.get(cat, 0)
        limit = b["amount"]
        remaining = round(limit - spent, 2)
        percent_used = round((spent / limit) * 100, 1) if limit > 0 else 0

        enriched.append({
            **b,
            "spent":        spent,
            "remaining":    remaining,
            "percent_used": percent_used,
            "status":       "over" if spent > limit else "warning" if percent_used >= 80 else "ok"
        })

    return {
        "budgets": enriched,
        "count":   len(enriched),
        "month":   now.strftime("%B %Y")
    }


def get_budget_alerts() -> dict:
    """
    Get only budgets that are over limit or close to limit (80%+).

    Returns:
        List of budget alerts
    """
    result = get_budgets()
    alerts = [
        b for b in result["budgets"]
        if b["status"] in ["over", "warning"]
    ]

    return {
        "alerts": alerts,
        "count":  len(alerts),
        "month":  result["month"]
    }