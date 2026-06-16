"""
JSON-backed persistence for tasks.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from taskmanager.models import Priority, Task

DEFAULT_STORE_PATH = Path.home() / ".task_manager" / "tasks.json"


class TaskStore:
    """Load and save tasks to a JSON file."""

    def __init__(self, store_path: Optional[Path] = None):
        self.path = Path(store_path) if store_path else DEFAULT_STORE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._tasks: List[Task] = []
        self._load()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not self.path.exists():
            self._tasks = []
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self._tasks = [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            self._tasks = []

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump([t.to_dict() for t in self._tasks], fh, indent=2)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def all(self) -> List[Task]:
        return list(self._tasks)

    def pending(self) -> List[Task]:
        return [t for t in self._tasks if not t.completed]

    def completed(self) -> List[Task]:
        return [t for t in self._tasks if t.completed]

    def get_by_id(self, task_id: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id or task.id.startswith(task_id):
                return task
        return None

    def get_by_index(self, index: int) -> Optional[Task]:
        """1-based index into the *pending* task list as displayed."""
        pending = self.pending()
        if 1 <= index <= len(pending):
            return pending[index - 1]
        return None

    def add(self, task: Task) -> Task:
        self._tasks.append(task)
        self._save()
        return task

    def update(self, task: Task) -> None:
        for i, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[i] = task
                break
        self._save()

    def delete(self, task: Task) -> None:
        self._tasks = [t for t in self._tasks if t.id != task.id]
        self._save()

    def stats(self) -> dict:
        all_tasks = self.all()
        total = len(all_tasks)
        done = sum(1 for t in all_tasks if t.completed)
        by_priority = {p.value: 0 for p in Priority}
        for t in all_tasks:
            if not t.completed:
                by_priority[t.priority.value] += 1
        return {
            "total": total,
            "completed": done,
            "pending": total - done,
            "by_priority": by_priority,
        }
