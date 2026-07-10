from datetime import date
from pathlib import Path

import pytest

from expense_tracker.cli import main
from expense_tracker.models import Expense
from expense_tracker.storage import load_expenses, save_expenses


def test_add_expense(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    main(["add", "500", "food", "--note", "biryani lunch"])
    expenses = load_expenses()
    assert len(expenses) == 1
    assert expenses[0].amount == 500.0
    assert expenses[0].category == "food"
    assert expenses[0].note == "biryani lunch"
    assert expenses[0].date == date.today()


def test_list_no_expenses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    main(["list"])
    captured = capsys.readouterr()
    assert "No expenses found." in captured.out


def test_list_with_expenses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    save_expenses([
        Expense(amount=500.0, category="food", note="lunch", date=date(2026, 7, 10)),
    ])
    main(["list"])
    captured = capsys.readouterr()
    assert "500.00" in captured.out
    assert "food" in captured.out


def test_summary_no_expenses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    main(["summary"])
    captured = capsys.readouterr()
    assert "No expenses" in captured.out


def test_delete_expense(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    main(["add", "500", "food", "--note", "biryani lunch"])
    main(["add", "1200", "transport", "--note", "fuel"])
    main(["delete", "1"])
    expenses = load_expenses()
    assert len(expenses) == 1
    assert expenses[0].amount == 1200.0
    assert expenses[0].category == "transport"


def test_delete_out_of_range(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    main(["delete", "1"])
    captured = capsys.readouterr()
    assert "out of range" in captured.out


def test_summary_with_multiple_categories(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    save_expenses([
        Expense(amount=500.0, category="food", note="lunch", date=date.today()),
        Expense(amount=1200.0, category="transport", note="fuel", date=date.today()),
        Expense(amount=350.0, category="food", note="snacks", date=date.today()),
    ])
    main(["summary"])
    captured = capsys.readouterr()
    assert "food" in captured.out
    assert "transport" in captured.out
    assert "850.00" in captured.out
    assert "1200.00" in captured.out
    assert "2050.00" in captured.out
