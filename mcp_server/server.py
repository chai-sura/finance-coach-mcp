"""
MCP Server - exposes all finance tools via Model Context Protocol.
This allows AI assistants to interact with your financial data using natural language.
"""

from mcp.server.fastmcp import FastMCP
from mcp_server.tools.expenses import log_expense, get_expenses, get_expenses_by_category, delete_expense
from mcp_server.tools.income import log_income, get_income, get_income_by_source, delete_income
from mcp_server.tools.budgets import set_budget, get_budgets, get_budget_alerts
from mcp_server.tools.summary import get_summary, get_monthly_trend
from mcp_server.tools.context import view_context, get_financial_health_score
from mcp_server.tools.advice import get_advice, get_advice_history, get_latest_advice

# Initialize MCP server
mcp = FastMCP("Finance Coach")

# EXPENSE TOOLS

@mcp.tool()
def log_expense_tool(amount: float, category: str, date: str = None, note: str = "") -> dict:
    """
    Log a new expense.
    Example: log $50 for groceries on 2026-03-07
    """
    return log_expense(amount, category, date, note)


@mcp.tool()
def get_expenses_tool(month: int = None, year: int = None) -> dict:
    """
    Get all expenses for a given month and year.
    Example: get expenses for March 2026
    """
    return get_expenses(month, year)


@mcp.tool()
def get_expenses_by_category_tool() -> dict:
    """
    Get all expenses grouped by category with totals.
    Example: show me spending by category
    """
    return get_expenses_by_category()


@mcp.tool()
def delete_expense_tool(expense_id: str) -> dict:
    """
    Delete an expense by ID.
    Example: delete expense expenses-1-20260307
    """
    return delete_expense(expense_id)


# INCOME TOOLS

@mcp.tool()
def log_income_tool(amount: float, source: str, date: str = None, note: str = "") -> dict:
    """
    Log a new income entry.
    Example: log $3000 salary income on 2026-03-01
    """
    return log_income(amount, source, date, note)


@mcp.tool()
def get_income_tool(month: int = None, year: int = None) -> dict:
    """
    Get all income for a given month and year.
    Example: get income for March 2026
    """
    return get_income(month, year)


@mcp.tool()
def get_income_by_source_tool() -> dict:
    """
    Get all income grouped by source with totals.
    Example: show me income by source
    """
    return get_income_by_source()


@mcp.tool()
def delete_income_tool(income_id: str) -> dict:
    """
    Delete an income entry by ID.
    Example: delete income income-1-20260307
    """
    return delete_income(income_id)


# BUDGET TOOLS

@mcp.tool()
def set_budget_tool(category: str, amount: float, period: str = "monthly") -> dict:
    """
    Set or update a budget limit for a category.
    Example: set $300 monthly budget for groceries
    """
    return set_budget(category, amount, period)


@mcp.tool()
def get_budgets_tool() -> dict:
    """
    Get all budgets with current spending status.
    Example: show me all my budgets
    """
    return get_budgets()


@mcp.tool()
def get_budget_alerts_tool() -> dict:
    """
    Get budgets that are over or close to their limit.
    Example: show me budget warnings
    """
    return get_budget_alerts()


# SUMMARY TOOLS

@mcp.tool()
def get_summary_tool(month: int = None, year: int = None) -> dict:
    """
    Get complete financial summary for a given month.
    Example: give me my financial summary for March 2026
    """
    return get_summary(month, year)


@mcp.tool()
def get_monthly_trend_tool(months: int = 6) -> dict:
    """
    Get income vs expenses trend over last N months.
    Example: show me my spending trend for last 6 months
    """
    return get_monthly_trend(months)


# CONTEXT TOOLS

@mcp.tool()
def view_context_tool(month: int = None, year: int = None) -> dict:
    """
    Get complete financial context for AI decision making.
    Example: give me full financial context for March 2026
    """
    return view_context(month, year)


@mcp.tool()
def get_financial_health_score_tool() -> dict:
    """
    Get financial health score out of 100.
    Example: what is my financial health score?
    """
    return get_financial_health_score()


# ADVICE TOOLS

@mcp.tool()
def get_advice_tool(month: int = None, year: int = None) -> dict:
    """
    Generate fresh AI financial advice for a given month.
    Example: give me financial advice for March 2026
    """
    return get_advice(month, year)


@mcp.tool()
def get_advice_history_tool() -> dict:
    """
    Get all previously generated advice entries.
    Example: show me my advice history
    """
    return get_advice_history()


@mcp.tool()
def get_latest_advice_tool() -> dict:
    """
    Get the most recently generated advice.
    Example: show me my latest financial advice
    """
    return get_latest_advice()


# RUN SERVER
if __name__ == "__main__":
    mcp.run()