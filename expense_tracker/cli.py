import argparse
from datetime import date
from typing import List

from expense_tracker.models import Expense
from expense_tracker.storage import load_expenses, save_expenses


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="expense-tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add_parser = sub.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Expense amount in PKR")
    add_parser.add_argument("category", type=str, help="Expense category")
    add_parser.add_argument("--note", type=str, default="", help="Optional note")

    sub.add_parser("list", help="List all expenses")

    sub.add_parser("summary", help="Show monthly summary by category")

    del_parser = sub.add_parser("delete", help="Delete an expense by index")
    del_parser.add_argument("index", type=int, help="Index of the expense to delete (1-based)")

    return parser


def handle_add(args: argparse.Namespace) -> None:
    expense = Expense(
        amount=args.amount,
        category=args.category,
        note=args.note,
        date=date.today(),
    )
    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense: PKR {expense.amount:.2f} on {expense.category}")


def handle_list() -> None:
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'#':<3} {'DATE':<12} {'CATEGORY':<12} {'AMOUNT':>10}  NOTE")
    print("-" * 64)
    for i, e in enumerate(expenses, start=1):
        date_str = e.date.isoformat()
        print(f"{i:<3} {date_str:<12} {e.category:<12} {e.amount:>10.2f}  {e.note}")


def handle_summary() -> None:
    expenses = load_expenses()
    today = date.today()
    monthly = [e for e in expenses if e.date.year == today.year and e.date.month == today.month]

    if not monthly:
        print(f"No expenses for {today.strftime('%B %Y')}.")
        return

    totals: dict[str, float] = {}
    for e in monthly:
        totals[e.category] = totals.get(e.category, 0.0) + e.amount

    print(f"=== {today.strftime('%B %Y')} Summary ===")
    grand = 0.0
    for cat, total in sorted(totals.items()):
        print(f"{cat:<12} {total:>10.2f} PKR")
        grand += total
    print("-" * 30)
    print(f"{'TOTAL':<12} {grand:>10.2f} PKR")


def handle_delete(args: argparse.Namespace) -> None:
    expenses = load_expenses()
    idx = args.index - 1
    if idx < 0 or idx >= len(expenses):
        print(f"Error: index {args.index} is out of range. There are {len(expenses)} expenses.")
        return
    removed = expenses.pop(idx)
    save_expenses(expenses)
    print(f"Deleted expense #{args.index}: PKR {removed.amount:.2f} on {removed.category}")


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        handle_add(args)
    elif args.command == "list":
        handle_list()
    elif args.command == "summary":
        handle_summary()
    elif args.command == "delete":
        handle_delete(args)
