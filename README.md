# testing

A lightweight CLI task manager built in Python — no dependencies, just the standard library.

## Features

- Add tasks with a title, priority (`high` / `medium` / `low`), and optional due date
- Color-coded terminal output with overdue / due-soon highlighting
- Tasks are sorted by status, then priority, then ID
- Mark tasks done, delete individual tasks, or bulk-clear all completed ones
- Persistent storage in a local `.tasks.json` file

## Usage

```bash
# Add tasks
python3 tasks.py add "Write unit tests" --priority high --due 2026-06-20
python3 tasks.py add "Update docs" --priority medium
python3 tasks.py add "Bump dependencies" --priority low

# List all tasks (sorted by priority)
python3 tasks.py list

# Filter by status
python3 tasks.py list --filter pending
python3 tasks.py list --filter done

# Mark a task complete
python3 tasks.py done 1

# Delete a specific task
python3 tasks.py delete 2

# Remove all completed tasks at once
python3 tasks.py clear
```

## Options

| Command | Flag | Values | Default |
|---|---|---|---|
| `add` | `--priority` / `-p` | `high`, `medium`, `low` | `medium` |
| `add` | `--due` / `-d` | `YYYY-MM-DD` | none |
| `list` | `--filter` / `-f` | `all`, `pending`, `done` | `all` |

## Storage

Tasks are saved to `.tasks.json` in the same directory as `tasks.py`. You can commit this file to share tasks with a team or add it to `.gitignore` to keep it local.

## Requirements

Python 3.7 or later. No third-party packages needed.
