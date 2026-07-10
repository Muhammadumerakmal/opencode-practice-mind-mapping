# my-first-project

CLI expense tracker (Python) and OpenCode tutorial sandbox.

## Key facts

- Default branch is `main`, not `master`. Always push to `main`.
- No CI, linting, formatting, or typecheck tooling is configured.

## Project structure

- `main.py` — entry point
- `expense_tracker/` — app package (models, storage, CLI)
- `tests/` — pytest suite (11 tests, standard library only)
- `opencode.tuturial.md` — beginner's tutorial (read-only reference)

## Commands

```bash
python main.py add <amount> <category> [--note "..."]   # add expense
python main.py list                                       # list all
python main.py summary                                    # monthly summary
python main.py delete <index>                             # delete by 1-based index
python -m pytest                                          # run tests
```

Data is stored in `expenses.json` (gitignored). Corrupt files are auto-reset.
