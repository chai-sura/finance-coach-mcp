"""
Context tool - provides complete financial profile for AI decision making.
This is what gets sent to OpenAI when generating advice.
"""

from utils.storage import get_all, get_by_month
from datetime import datetime
from mcp_server.tools.summary import get_summary, get_monthly_trend


def view_context(month: int = None, year: int = None) -> dict:
    """
    Get complete financial context for a given month.
    Used by AI to understand the user's full financial picture.

    Args:
        month: Month number 1-12, defaults to current month
        year:  Year e.g. 2026, defaults to current year

    Returns:
        Complete financial profile including summary, trends and raw data
    """
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    # Get current month summary
    summary = get_summary(month, year)

    # Get 6 month trend
    trend = get_monthly_trend(6)

    # Get all budgets
    budgets = get_all("budgets")

    # Get recent expenses (last 10)
    all_expenses = get_all("expenses")
    recent_expenses = sorted(
        all_expenses,
        key=lambda x: x.get("date", ""),
        reverse=True
    )[:10]

    # Get recent income (last 5)
    all_income = get_all("income")
    recent_income = sorted(
        all_income,
        key=lambda x: x.get("date", ""),
        reverse=True
    )[:5]

    # Calculate overall stats
    total_ever_spent = round(sum(e["amount"] for e in all_expenses), 2)
    total_ever_earned = round(sum(i["amount"] for i in all_income), 2)
    total_ever_saved = round(total_ever_earned - total_ever_spent, 2)

    # Find biggest spending category of all time
    all_by_category = {}
    for e in all_expenses:
        cat = e.get("category", "other")
        all_by_category[cat] = round(
            all_by_category.get(cat, 0) + e["amount"], 2
        )
    biggest_category = max(
        all_by_category, key=all_by_category.get
    ) if all_by_category else None

    return {
        "current_month":     summary,
        "trend":             trend,
        "budgets":           budgets,
        "recent_expenses":   recent_expenses,
        "recent_income":     recent_income,
        "all_time": {
            "total_spent":       total_ever_spent,
            "total_earned":      total_ever_earned,
            "total_saved":       total_ever_saved,
            "biggest_category":  biggest_category,
            "by_category":       all_by_category
        },
        "generated_at": datetime.now().isoformat()
    }


def get_financial_health_score() -> dict:
    """
    Calculate a simple financial health score out of 100.

    Scoring breakdown:
    - Savings rate 20%+     → 30 points
    - No budgets exceeded   → 25 points
    - Has income logged     → 20 points
    - Has budgets set       → 15 points
    - Expenses < income     → 10 points

    Returns:
        Score, breakdown and health status
    """
    now = datetime.now()
    summary = get_summary(now.month, now.year)
    budgets = get_all("budgets")

    score = 0
    breakdown = []

    # Savings rate check
    if summary["savings_rate"] >= 20:
        score += 30
        breakdown.append({"check": "Savings rate 20%+",        "points": 30, "passed": True})
    else:
        breakdown.append({"check": "Savings rate 20%+",        "points": 0,  "passed": False})

    # No budgets exceeded
    over_budget = [b for b in summary["budget_summary"] if b["status"] == "over"]
    if len(over_budget) == 0 and len(budgets) > 0:
        score += 25
        breakdown.append({"check": "No budgets exceeded",      "points": 25, "passed": True})
    else:
        breakdown.append({"check": "No budgets exceeded",      "points": 0,  "passed": False})

    # Has income logged
    if summary["total_income"] > 0:
        score += 20
        breakdown.append({"check": "Income logged this month", "points": 20, "passed": True})
    else:
        breakdown.append({"check": "Income logged this month", "points": 0,  "passed": False})

    # Has budgets set
    if len(budgets) > 0:
        score += 15
        breakdown.append({"check": "Budgets are set",          "points": 15, "passed": True})
    else:
        breakdown.append({"check": "Budgets are set",          "points": 0,  "passed": False})

    # Expenses less than income
    if summary["total_expenses"] < summary["total_income"]:
        score += 10
        breakdown.append({"check": "Expenses < Income",        "points": 10, "passed": True})
    else:
        breakdown.append({"check": "Expenses < Income",        "points": 0,  "passed": False})

    # Determine health status
    if score >= 80:
        status = "Excellent 🟢"
    elif score >= 60:
        status = "Good 🟡"
    elif score >= 40:
        status = "Fair 🟠"
    else:
        status = "Needs Attention 🔴"

    return {
        "score":     score,
        "status":    status,
        "breakdown": breakdown,
        "month":     now.strftime("%B %Y")
    }