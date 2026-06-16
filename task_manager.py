#!/usr/bin/env python3
"""
task_manager.py — A simple command-line task manager.

Commands:
  add      Add a new task
  list     List pending tasks (default view)
  done     Mark a task as completed
  delete   Delete a task permanently
  show     Show full details of a task
  stats    Display task statistics
  clear    Remove all completed tasks
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent))

from taskmanager.models import Priority, Task
from taskmanager.store import TaskStore

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
CYAN  = "\033[36m"
GREEN = "\033[32m"
RED   = "\033[31m"


def header(text: str) -> None:
    width = 60
    print(f"\n{BOLD}{CYAN}{'─' * width}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'─' * width}{RESET}")


def success(msg: str) -> None:
    print(f"\n  {GREEN}✓{RESET}  {msg}\n")


def error(msg: str) -> None:
    print(f"\n  {RED}✗{RESET}  {msg}\n", file=sys.stderr)


def resolve_task(store: TaskStore, target: str) -> Task | None:
    """Resolve a task by numeric index or ID prefix."""
    try:
        idx = int(target)
        task = store.get_by_index(idx)
    except ValueError:
        task = store.get_by_id(target)
    if task is None:
        error(f"No task found for '{target}'.")
    return task


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_add(args, store: TaskStore) -> None:
    title = " ".join(args.title)
    task = Task(
        title=title,
        description=args.description or "",
        priority=Priority(args.priority),
        due_date=args.due,
    )
    store.add(task)
    success(f"Added task #{task.id}: \"{task.title}\"  [{task.priority.value}]")


def cmd_list(args, store: TaskStore) -> None:
    show_all = getattr(args, "all", False)
    tasks = store.all() if show_all else store.pending()

    if not tasks:
        print(f"\n  {DIM}No tasks found.{RESET}\n")
        return

    header("Tasks — pending" if not show_all else "Tasks — all")
    print(f"\n  {'':5}  {'PRIORITY':10}  {'ID':10}  TITLE\n")
    for i, task in enumerate(tasks, 1):
        print(task.summary_line(i))
    print()

    if not show_all:
        stats = store.stats()
        print(f"  {DIM}{stats['pending']} pending · {stats['completed']} completed{RESET}\n")


def cmd_done(args, store: TaskStore) -> None:
    task = resolve_task(store, args.task)
    if task is None:
        sys.exit(1)
    if task.completed:
        error(f"Task #{task.id} is already completed.")
        sys.exit(1)
    task.completed = True
    task.completed_at = datetime.now().isoformat(timespec="seconds")
    store.update(task)
    success(f"Marked task #{task.id} as done: \"{task.title}\"")


def cmd_delete(args, store: TaskStore) -> None:
    task = resolve_task(store, args.task)
    if task is None:
        sys.exit(1)
    store.delete(task)
    success(f"Deleted task #{task.id}: \"{task.title}\"")


def cmd_show(args, store: TaskStore) -> None:
    task = resolve_task(store, args.task)
    if task is None:
        sys.exit(1)

    status_str = f"{GREEN}Completed{RESET}" if task.completed else "Pending"
    header(f"Task #{task.id}")
    print(f"\n  {BOLD}Title      {RESET} {task.title}")
    print(f"  {BOLD}Status     {RESET} {status_str}")
    print(f"  {BOLD}Priority   {RESET} {task.priority.display}")
    if task.description:
        print(f"  {BOLD}Description{RESET} {task.description}")
    if task.due_date:
        print(f"  {BOLD}Due Date   {RESET} {task.due_date}")
    print(f"  {BOLD}Created    {RESET} {task.created_at}")
    if task.completed_at:
        print(f"  {BOLD}Completed  {RESET} {task.completed_at}")
    print()


def cmd_stats(args, store: TaskStore) -> None:
    s = store.stats()
    header("Statistics")
    print(f"\n  Total tasks   : {BOLD}{s['total']}{RESET}")
    print(f"  Pending       : {s['pending']}")
    print(f"  Completed     : {GREEN}{s['completed']}{RESET}")
    print(f"\n  Pending by priority:")
    for p in Priority:
        count = s["by_priority"][p.value]
        bar = "█" * count
        print(f"    {p.display}  {bar or '(none)'} ({count})")
    print()


def cmd_clear(args, store: TaskStore) -> None:
    completed = store.completed()
    if not completed:
        print(f"\n  {DIM}No completed tasks to clear.{RESET}\n")
        return
    for task in completed:
        store.delete(task)
    success(f"Removed {len(completed)} completed task(s).")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task",
        description="A simple command-line task manager.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", nargs="+", help="Task title (words joined)")
    p_add.add_argument("-d", "--description", help="Longer description")
    p_add.add_argument(
        "-p", "--priority",
        choices=[p.value for p in Priority],
        default=Priority.MEDIUM.value,
        help="Priority level (default: medium)",
    )
    p_add.add_argument("--due", metavar="YYYY-MM-DD", help="Due date")

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("-a", "--all", action="store_true", help="Show completed tasks too")

    # done
    p_done = sub.add_parser("done", help="Mark a task as completed")
    p_done.add_argument("task", help="Task number (from list) or ID prefix")

    # delete
    p_del = sub.add_parser("delete", help="Delete a task permanently")
    p_del.add_argument("task", help="Task number (from list) or ID prefix")

    # show
    p_show = sub.add_parser("show", help="Show full task details")
    p_show.add_argument("task", help="Task number (from list) or ID prefix")

    # stats
    sub.add_parser("stats", help="Show task statistics")

    # clear
    sub.add_parser("clear", help="Remove all completed tasks")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        # Default: list pending tasks
        args.all = False
        cmd_list(args, TaskStore())
        return

    store = TaskStore()
    dispatch = {
        "add":    cmd_add,
        "list":   cmd_list,
        "done":   cmd_done,
        "delete": cmd_delete,
        "show":   cmd_show,
        "stats":  cmd_stats,
        "clear":  cmd_clear,
    }
    dispatch[args.command](args, store)


if __name__ == "__main__":
    main()
