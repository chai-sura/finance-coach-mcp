"""
Storage utility - handles all JSON read/write operations
for expenses, income, budgets and advice data.
"""

import json
import os
from datetime import datetime

# Path to data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Map store names to their JSON files
STORES = {
    "expenses": os.path.join(DATA_DIR, "expenses.json"),
    "income":   os.path.join(DATA_DIR, "income.json"),
    "budgets":  os.path.join(DATA_DIR, "budgets.json"),
    "advice":   os.path.join(DATA_DIR, "advice.json"),
}


def load(store: str) -> list[dict]:
    """Read all records from a JSON store."""
    path = STORES[store]
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save(store: str, data: list[dict]) -> None:
    """Write all records to a JSON store."""
    with open(STORES[store], "w") as f:
        json.dump(data, f, indent=2)


def add(store: str, entry: dict) -> dict:
    """Add a new record to a store with auto ID and timestamp."""
    data = load(store)
    entry["id"] = f"{store}-{len(data)+1}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    entry["created_at"] = datetime.now().isoformat()
    data.append(entry)
    save(store, data)
    return entry


def get_all(store: str) -> list[dict]:
    """Get all records from a store."""
    return load(store)


def get_by_month(store: str, year: int, month: int) -> list[dict]:
    """Filter records by year and month using the date field."""
    records = load(store)
    return [
        r for r in records
        if r.get("date", "").startswith(f"{year}-{month:02d}")
    ]


def delete(store: str, record_id: str) -> bool:
    """Delete a record by ID. Returns True if deleted."""
    data = load(store)
    filtered = [r for r in data if r.get("id") != record_id]
    if len(filtered) == len(data):
        return False  # nothing deleted
    save(store, filtered)
    return True


def upsert_budget(category: str, amount: float, period: str) -> dict:
    """Insert or update a budget for a category."""
    data = load("budgets")
    existing = next(
        (b for b in data if b["category"].lower() == category.lower()),
        None
    )
    if existing:
        existing["amount"] = amount
        existing["period"] = period
        existing["updated_at"] = datetime.now().isoformat()
        save("budgets", data)
        return existing
    return add("budgets", {
        "category": category,
        "amount": amount,
        "period": period
    })