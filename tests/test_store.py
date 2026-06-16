"""Tests for tasks.store."""
import json
import pytest
from pathlib import Path

from taskmanager.models import Priority, Task
from taskmanager.store import TaskStore


@pytest.fixture
def tmp_store(tmp_path):
    """Return a TaskStore backed by a temp file."""
    return TaskStore(store_path=tmp_path / "tasks.json")


class TestTaskStore:
    def test_empty_on_init(self, tmp_store):
        assert tmp_store.all() == []

    def test_add_and_retrieve(self, tmp_store):
        t = Task("Buy groceries")
        tmp_store.add(t)
        all_tasks = tmp_store.all()
        assert len(all_tasks) == 1
        assert all_tasks[0].title == "Buy groceries"

    def test_persistence(self, tmp_path):
        path = tmp_path / "tasks.json"
        s1 = TaskStore(store_path=path)
        s1.add(Task("Persist me"))

        s2 = TaskStore(store_path=path)
        assert len(s2.all()) == 1
        assert s2.all()[0].title == "Persist me"

    def test_pending_excludes_completed(self, tmp_store):
        t1 = Task("Active")
        t2 = Task("Done")
        t2.completed = True
        tmp_store.add(t1)
        tmp_store.add(t2)

        pending = tmp_store.pending()
        assert len(pending) == 1
        assert pending[0].title == "Active"

    def test_completed_returns_only_done(self, tmp_store):
        t1 = Task("Active")
        t2 = Task("Done")
        t2.completed = True
        tmp_store.add(t1)
        tmp_store.add(t2)

        done = tmp_store.completed()
        assert len(done) == 1
        assert done[0].title == "Done"

    def test_get_by_id(self, tmp_store):
        t = Task("Find me", task_id="abcd1234")
        tmp_store.add(t)
        found = tmp_store.get_by_id("abcd1234")
        assert found is not None
        assert found.title == "Find me"

    def test_get_by_id_prefix(self, tmp_store):
        t = Task("Find me", task_id="abcd1234")
        tmp_store.add(t)
        found = tmp_store.get_by_id("abcd")
        assert found is not None

    def test_get_by_id_missing(self, tmp_store):
        assert tmp_store.get_by_id("nope") is None

    def test_get_by_index(self, tmp_store):
        t1 = Task("First")
        t2 = Task("Second")
        tmp_store.add(t1)
        tmp_store.add(t2)
        found = tmp_store.get_by_index(1)
        assert found.title == "First"

    def test_get_by_index_out_of_range(self, tmp_store):
        tmp_store.add(Task("Only"))
        assert tmp_store.get_by_index(99) is None

    def test_update(self, tmp_store):
        t = Task("Update me")
        tmp_store.add(t)
        t.completed = True
        tmp_store.update(t)

        reloaded = TaskStore(store_path=tmp_store.path)
        assert reloaded.all()[0].completed is True

    def test_delete(self, tmp_store):
        t = Task("Delete me")
        tmp_store.add(t)
        tmp_store.delete(t)
        assert tmp_store.all() == []

    def test_stats(self, tmp_store):
        tmp_store.add(Task("p1", priority=Priority.HIGH))
        t2 = Task("p2", priority=Priority.LOW)
        t2.completed = True
        tmp_store.add(t2)

        s = tmp_store.stats()
        assert s["total"] == 2
        assert s["completed"] == 1
        assert s["pending"] == 1
        assert s["by_priority"]["high"] == 1
        assert s["by_priority"]["low"] == 0  # completed not counted

    def test_handles_corrupt_file(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("not json!")
        store = TaskStore(store_path=path)
        assert store.all() == []
