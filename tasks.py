#!/usr/bin/env python3
"""
tasks.py — A lightweight CLI task manager.

Usage:
  python3 tasks.py add "Buy groceries" --priority high --due 2026-06-20
  python3 tasks.py list
  python3 tasks.py list --filter pending
  python3 tasks.py done <id>
  python3 tasks.py delete <id>
  python3 tasks.py clear
"""

import json
import os
import sys
import argparse
from datetime import datetime, date

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tasks.json")

# ANSI color codes
RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
GRAY    = "\033[90m"

PRIORITY_COLOR = {
    "high":   RED,
    "medium": YELLOW,
    "low":    CYAN,
}

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1

def format_due(due_str):
    if not due_str:
        return ""
    try:
        due = date.fromisoformat(due_str)
        today = date.today()
        delta = (due - today).days
        if delta < 0:
            return f"{RED}overdue by {-delta}d{RESET}"
        elif delta == 0:
            return f"{YELLOW}due today{RESET}"
        elif delta <= 3:
            return f"{YELLOW}due in {delta}d{RESET}"
        else:
            return f"{GRAY}due {due_str}{RESET}"
    except ValueError:
        return f"{GRAY}{due_str}{RESET}"

def cmd_add(args):
    tasks = load_tasks()
    task = {
        "id":        next_id(tasks),
        "title":     args.title,
        "priority":  args.priority,
        "due":       args.due,
        "status":    "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)
    color = PRIORITY_COLOR.get(args.priority, RESET)
    print(f"{GREEN}Added{RESET} [{color}{args.priority.upper()}{RESET}] "
          f"{BOLD}#{task['id']}{RESET} — {task['title']}")

def cmd_list(args):
    tasks = load_tasks()

    status_filter = args.filter
    if status_filter and status_filter != "all":
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        print(f"{GRAY}No tasks found.{RESET}")
        return

    # Sort: pending first, then by priority weight, then by id
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks_sorted = sorted(
        tasks,
        key=lambda t: (
            0 if t["status"] == "pending" else 1,
            priority_order.get(t["priority"], 9),
            t["id"],
        ),
    )

    pending_count  = sum(1 for t in tasks if t["status"] == "pending")
    done_count     = sum(1 for t in tasks if t["status"] == "done")

    print(f"\n{BOLD}Tasks{RESET}  "
          f"{YELLOW}{pending_count} pending{RESET}  "
          f"{GREEN}{done_count} done{RESET}\n")

    for t in tasks_sorted:
        p_color  = PRIORITY_COLOR.get(t["priority"], RESET)
        p_badge  = f"{p_color}[{t['priority'].upper():6}]{RESET}"
        id_badge = f"{BOLD}#{t['id']:>3}{RESET}"
        due_fmt  = format_due(t.get("due"))

        if t["status"] == "done":
            status_icon = f"{GREEN}✔{RESET}"
            title       = f"{GRAY}{t['title']}{RESET}"
        else:
            status_icon = f"{BLUE}○{RESET}"
            title       = t["title"]

        parts = [status_icon, id_badge, p_badge, title]
        if due_fmt:
            parts.append(due_fmt)

        print("  " + "  ".join(parts))

    print()

def cmd_done(args):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == args.id:
            if t["status"] == "done":
                print(f"{YELLOW}Task #{args.id} is already marked done.{RESET}")
            else:
                t["status"] = "done"
                t["completed_at"] = datetime.now().isoformat(timespec="seconds")
                save_tasks(tasks)
                print(f"{GREEN}Done!{RESET} Task #{args.id} — {t['title']}")
            return
    print(f"{RED}Task #{args.id} not found.{RESET}", file=sys.stderr)
    sys.exit(1)

def cmd_delete(args):
    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != args.id]
    if len(tasks) == original_len:
        print(f"{RED}Task #{args.id} not found.{RESET}", file=sys.stderr)
        sys.exit(1)
    save_tasks(tasks)
    print(f"{MAGENTA}Deleted{RESET} task #{args.id}")

def cmd_clear(args):
    tasks = load_tasks()
    done_tasks = [t for t in tasks if t["status"] == "done"]
    removed = len(done_tasks)
    tasks = [t for t in tasks if t["status"] != "done"]
    save_tasks(tasks)
    print(f"{MAGENTA}Cleared{RESET} {removed} completed task(s).")

def main():
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Lightweight CLI task manager",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")
    p_add.add_argument(
        "--priority", "-p",
        choices=["high", "medium", "low"],
        default="medium",
        help="Task priority (default: medium)",
    )
    p_add.add_argument(
        "--due", "-d",
        default=None,
        metavar="YYYY-MM-DD",
        help="Optional due date",
    )
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument(
        "--filter", "-f",
        choices=["all", "pending", "done"],
        default="all",
        help="Filter by status (default: all)",
    )
    p_list.set_defaults(func=cmd_list)

    # done
    p_done = sub.add_parser("done", help="Mark a task as completed")
    p_done.add_argument("id", type=int, help="Task ID")
    p_done.set_defaults(func=cmd_done)

    # delete
    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task ID")
    p_del.set_defaults(func=cmd_delete)

    # clear
    p_clear = sub.add_parser("clear", help="Remove all completed tasks")
    p_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
