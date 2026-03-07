"""
AI Client - handles all OpenAI API calls for
generating personalized financial advice.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.storage import get_all, get_by_month
from datetime import datetime

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Always use cheapest model
MODEL = "gpt-4o-mini"


def _build_context(year: int, month: int) -> str:
    """Build a financial summary string to send to OpenAI."""

    expenses = get_by_month("expenses", year, month)
    income = get_by_month("income", year, month)
    budgets = get_all("budgets")

    # Calculate totals
    total_expenses = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in income)
    net = total_income - total_expenses

    # Group expenses by category
    by_category = {}
    for e in expenses:
        cat = e.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + e["amount"]

    # Build budget comparison
    budget_status = []
    for b in budgets:
        cat = b["category"]
        spent = by_category.get(cat, 0)
        limit = b["amount"]
        status = "OVER" if spent > limit else "OK"
        budget_status.append(f"  - {cat}: spent ${spent:.2f} / limit ${limit:.2f} [{status}]")

    context = f"""
Financial Summary for {datetime(year, month, 1).strftime('%B %Y')}:

INCOME:
  - Total Income: ${total_income:.2f}

EXPENSES:
  - Total Expenses: ${total_expenses:.2f}
  - Net Savings: ${net:.2f}

SPENDING BY CATEGORY:
{chr(10).join(f'  - {k}: ${v:.2f}' for k, v in by_category.items()) or '  - No expenses logged'}

BUDGET STATUS:
{chr(10).join(budget_status) or '  - No budgets set'}
"""
    return context


def generate_advice(year: int | None = None, month: int | None = None) -> dict:
    """
    Generate personalized financial advice using OpenAI.
    Returns advice text and token usage.
    """
    now = datetime.now()
    year = year or now.year
    month = month or now.month

    context = _build_context(year, month)

    prompt = f"""
You are a helpful personal finance coach. Based on the financial data below,
give 3-5 specific, actionable pieces of advice to help the user save more money
and stay within their budgets. Be encouraging but honest.

{context}

Format your response as a numbered list. Keep it concise and practical.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a friendly personal finance coach who gives practical, actionable advice."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500,  # Keep costs low
        temperature=0.7
    )

    advice_text = response.choices[0].message.content

    return {
        "advice": advice_text,
        "month": datetime(year, month, 1).strftime("%B %Y")
    }