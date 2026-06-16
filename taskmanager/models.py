"""
Data models for the Task Manager.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def display(self) -> str:
        colors = {
            Priority.LOW: "\033[32m",      # green
            Priority.MEDIUM: "\033[33m",   # yellow
            Priority.HIGH: "\033[31m",     # red
        }
        reset = "\033[0m"
        labels = {
            Priority.LOW: "LOW   ",
            Priority.MEDIUM: "MEDIUM",
            Priority.HIGH: "HIGH  ",
        }
        return f"{colors[self]}{labels[self]}{reset}"


class Task:
    """Represents a single task."""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[str] = None,
        task_id: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[str] = None,
        completed_at: Optional[str] = None,
    ):
        self.id: str = task_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.priority = Priority(priority) if isinstance(priority, str) else priority
        self.due_date = due_date  # stored as "YYYY-MM-DD" string or None
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.completed_at = completed_at

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", Priority.MEDIUM.value),
            due_date=data.get("due_date"),
            task_id=data["id"],
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
        )

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _due_display(self) -> str:
        if not self.due_date:
            return ""
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            delta = (due - today).days
            if delta < 0:
                label = f"\033[31mOVERDUE ({-delta}d)\033[0m"
            elif delta == 0:
                label = "\033[33mDUE TODAY\033[0m"
            elif delta <= 3:
                label = f"\033[33mdue in {delta}d\033[0m"
            else:
                label = f"due {self.due_date}"
            return f"  [{label}]"
        except ValueError:
            return f"  [due {self.due_date}]"

    def summary_line(self, index: int) -> str:
        status = "\033[32m✓\033[0m" if self.completed else " "
        title_fmt = f"\033[2m{self.title}\033[0m" if self.completed else self.title
        return (
            f"  [{status}] {index:>3}.  {self.priority.display}  "
            f"\033[90m#{self.id}\033[0m  {title_fmt}{self._due_display()}"
        )
