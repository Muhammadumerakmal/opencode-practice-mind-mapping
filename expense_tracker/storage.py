import json
import shutil
from datetime import date
from pathlib import Path
from typing import List

from expense_tracker.models import Expense

DATA_FILE = Path("expenses.json")
BACKUP_FILE = Path("expenses.json.bak")


def load_expenses() -> List[Expense]:
    if not DATA_FILE.exists():
        return []

    try:
        raw = DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        return [_dict_to_expense(item) for item in data]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        shutil.copy2(DATA_FILE, BACKUP_FILE)
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []


def save_expenses(expenses: List[Expense]) -> None:
    data = [_expense_to_dict(e) for e in expenses]
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _expense_to_dict(e: Expense) -> dict:
    return {
        "amount": e.amount,
        "category": e.category,
        "note": e.note,
        "date": e.date.isoformat(),
    }


def _dict_to_expense(d: dict) -> Expense:
    return Expense(
        amount=float(d["amount"]),
        category=str(d["category"]),
        note=str(d["note"]),
        date=date.fromisoformat(d["date"]),
    )


