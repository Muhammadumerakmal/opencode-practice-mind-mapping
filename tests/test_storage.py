from datetime import date
from pathlib import Path

import pytest

from expense_tracker.models import Expense
from expense_tracker.storage import load_expenses, save_expenses


def test_save_and_load(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    expenses = [
        Expense(amount=500.0, category="food", note="lunch", date=date(2026, 7, 10)),
        Expense(amount=1200.0, category="transport", note="fuel", date=date(2026, 7, 10)),
    ]
    save_expenses(expenses)
    loaded = load_expenses()
    assert loaded == expenses


def test_load_missing_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    loaded = load_expenses()
    assert loaded == []


def test_load_corrupt_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    data_file = tmp_path / "expenses.json"
    data_file.write_text("not valid json", encoding="utf-8")
    loaded = load_expenses()
    assert loaded == []


def test_load_empty_json_array(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    data_file = tmp_path / "expenses.json"
    data_file.write_text("[]", encoding="utf-8")
    loaded = load_expenses()
    assert loaded == []
