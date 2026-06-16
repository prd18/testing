"""Tests for tasks.models."""
import pytest
from taskmanager.models import Priority, Task


class TestPriority:
    def test_values(self):
        assert Priority.LOW.value == "low"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.HIGH.value == "high"

    def test_from_string(self):
        assert Priority("high") is Priority.HIGH


class TestTask:
    def test_defaults(self):
        t = Task("Write tests")
        assert t.title == "Write tests"
        assert t.priority == Priority.MEDIUM
        assert t.completed is False
        assert t.due_date is None
        assert len(t.id) == 8

    def test_custom_id_preserved(self):
        t = Task("Fix bug", task_id="abc12345")
        assert t.id == "abc12345"

    def test_round_trip(self):
        t = Task(
            title="Deploy service",
            description="Push to prod",
            priority=Priority.HIGH,
            due_date="2026-07-01",
        )
        data = t.to_dict()
        restored = Task.from_dict(data)

        assert restored.id == t.id
        assert restored.title == t.title
        assert restored.description == t.description
        assert restored.priority == t.priority
        assert restored.due_date == t.due_date
        assert restored.completed == t.completed

    def test_completion_fields(self):
        t = Task("Ship feature")
        assert t.completed is False
        assert t.completed_at is None
        t.completed = True
        t.completed_at = "2026-06-16T12:00:00"
        data = t.to_dict()
        assert data["completed"] is True
        assert data["completed_at"] == "2026-06-16T12:00:00"

    def test_summary_line_contains_title(self):
        t = Task("My task", priority=Priority.LOW)
        line = t.summary_line(1)
        assert "My task" in line

    def test_priority_coercion_from_string(self):
        t = Task("Task", priority="high")
        assert t.priority == Priority.HIGH
