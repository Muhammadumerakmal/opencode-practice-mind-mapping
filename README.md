# Expense Tracker

A CLI expense tracker built with Python 3.10+ standard library only (argparse, json, dataclasses, datetime).

## Installation

```bash
# Clone the repo and enter the directory
git clone <repo-url> && cd expense-tracker

# No dependencies to install — Python standard library only
python --version         # requires Python 3.10+
```

## Usage

All commands are run via `main.py`.

### Add an expense

```bash
python main.py add <amount> <category> [--note "<note>"]
```

Examples:

```bash
python main.py add 500 food --note "biryani lunch"
python main.py add 1200 transport --note "fuel"
```

### List all expenses

```bash
python main.py list
```

Output shows a numbered table with date, category, amount, and note.

### Show monthly summary

```bash
python main.py summary
```

Displays totals per category for the current month.

### Delete an expense

```bash
python main.py delete <index>
```

The index is the 1-based number shown in the list output. Running `delete 2` removes the second expense shown in the list.

## Running tests

```bash
python -m pytest
```

## Data storage

Expenses are saved to `expenses.json` in the current directory. If the file is missing or corrupt it is reset automatically (a backup is saved as `expenses.json.bak`).
