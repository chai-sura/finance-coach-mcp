"""
Summary tool - provides financial overview and spending analysis.
"""

from utils.storage import get_all, get_by_month
from datetime import datetime


def get_summary(month: int = None, year: int = None) -> dict:
    """
    Get a complete financial summary for a given month.

    Args:
        month: Month number 1-12, defaults to current month
        year:  Year e.g. 2026, defaults to current year

    Returns:
        Complete financial overview including income, expenses, savings
    """
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    expenses = get_by_month("expenses", year, month)
    income = get_by_month("income", year, month)
    budgets = get_all("budgets")

    # Core totals
    total_expenses = round(sum(e["amount"] for e in expenses), 2)
    total_income = round(sum(i["amount"] for i in income), 2)
    net_savings = round(total_income - total_expenses, 2)
    savings_rate = round((net_savings / total_income) * 100, 1) if total_income > 0 else 0

    # Group expenses by category
    by_category = {}
    for e in expenses:
        cat = e.get("category", "other")
        by_category[cat] = round(by_category.get(cat, 0) + e["amount"], 2)

    # Group income by source
    by_source = {}
    for i in income:
        source = i.get("source", "other")
        by_source[source] = round(by_source.get(source, 0) + i["amount"], 2)

    # Budget comparison
    budget_summary = []
    for b in budgets:
        cat = b["category"]
        spent = by_category.get(cat, 0)
        limit = b["amount"]
        percent = round((spent / limit) * 100, 1) if limit > 0 else 0
        budget_summary.append({
            "category":     cat,
            "spent":        spent,
            "limit":        limit,
            "percent_used": percent,
            "status":       "over" if spent > limit else "warning" if percent >= 80 else "ok"
        })

    # Top spending category
    top_category = max(by_category, key=by_category.get) if by_category else None

    return {
        "month":          datetime(year, month, 1).strftime("%B %Y"),
        "total_income":   total_income,
        "total_expenses": total_expenses,
        "net_savings":    net_savings,
        "savings_rate":   savings_rate,
        "by_category":    by_category,
        "by_source":      by_source,
        "budget_summary": budget_summary,
        "top_category":   top_category,
        "expense_count":  len(expenses),
        "income_count":   len(income)
    }


def get_monthly_trend(months: int = 6) -> dict:
    """
    Get income vs expenses trend over the last N months.

    Args:
        months: Number of months to look back, defaults to 6

    Returns:
        Month by month breakdown of income, expenses and savings
    """
    now = datetime.now()
    trend = []

    for i in range(months - 1, -1, -1):
        # Calculate month and year going backwards
        month = (now.month - i - 1) % 12 + 1
        year = now.year - ((now.month - i - 1) // 12)

        expenses = get_by_month("expenses", year, month)
        income = get_by_month("income", year, month)

        total_expenses = round(sum(e["amount"] for e in expenses), 2)
        total_income = round(sum(i["amount"] for i in income), 2)
        net_savings = round(total_income - total_expenses, 2)

        trend.append({
            "month":          datetime(year, month, 1).strftime("%b %Y"),
            "total_income":   total_income,
            "total_expenses": total_expenses,
            "net_savings":    net_savings
        })

    return {
        "trend":  trend,
        "months": months
    }