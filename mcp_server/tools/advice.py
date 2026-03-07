"""
Advice tool - generates and stores AI-powered financial advice
using OpenAI GPT-4o-mini.
"""

from utils.storage import add, get_all
from utils.ai_client import generate_advice
from datetime import datetime


def get_advice(month: int = None, year: int = None) -> dict:
    """
    Generate fresh AI financial advice for a given month.
    Saves the advice to advice.json for history.

    Args:
        month: Month number 1-12, defaults to current month
        year:  Year e.g. 2026, defaults to current year

    Returns:
        Generated advice text
    """
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    # Call OpenAI via ai_client
    result = generate_advice(year, month)

    # Save advice to history
    saved = add("advice", {
        "advice": result["advice"],
        "month":  result["month"],
    })

    return {
        "success":  True,
        "advice":   result["advice"],
        "month":    result["month"],
        "entry_id": saved["id"]
    }


def get_advice_history() -> dict:
    """
    Get all previously generated advice entries.

    Returns:
        List of all advice entries sorted by newest first
    """
    all_advice = get_all("advice")

    sorted_advice = sorted(
        all_advice,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    return {
        "history": sorted_advice,
        "count":   len(sorted_advice)
    }


def get_latest_advice() -> dict:
    """
    Get the most recently generated advice entry.

    Returns:
        Latest advice entry or message if none exists
    """
    all_advice = get_all("advice")

    if not all_advice:
        return {
            "success": False,
            "message": "No advice generated yet. Click Generate Advice to get started!"
        }

    latest = sorted(
        all_advice,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )[0]

    return {
        "success": True,
        "advice":  latest["advice"],
        "month":   latest.get("month", ""),
    }