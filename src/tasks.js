'use strict';

const { load, save } = require('./store');

const PRIORITIES = { high: 1, medium: 2, low: 3 };

// ─── helpers ────────────────────────────────────────────────────────────────

function nextId(tasks) {
  return tasks.length === 0 ? 1 : Math.max(...tasks.map(t => t.id)) + 1;
}

function todayStr() {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

function isOverdueOrDueToday(task) {
  if (!task.dueDate) return false;
  return task.dueDate <= todayStr();
}

// ─── commands ───────────────────────────────────────────────────────────────

function addTask({ title, priority = 'medium', dueDate }) {
  if (!title) throw new Error('Task title is required');
  if (priority && !PRIORITIES[priority]) {
    throw new Error(`Priority must be one of: ${Object.keys(PRIORITIES).join(', ')}`);
  }
  if (dueDate && !/^\d{4}-\d{2}-\d{2}$/.test(dueDate)) {
    throw new Error('Due date must be in YYYY-MM-DD format');
  }

  const tasks = load();
  const task = {
    id:        nextId(tasks),
    title,
    priority,
    dueDate:   dueDate || null,
    done:      false,
    createdAt: new Date().toISOString(),
  };
  tasks.push(task);
  save(tasks);
  return task;
}

function listTasks({ showDone = false } = {}) {
  const tasks = load();
  return showDone ? tasks : tasks.filter(t => !t.done);
}

function completeTask(id) {
  const tasks = load();
  const task  = tasks.find(t => t.id === id);
  if (!task) throw new Error(`Task #${id} not found`);
  task.done      = true;
  task.completedAt = new Date().toISOString();
  save(tasks);
  return task;
}

function deleteTask(id) {
  const tasks   = load();
  const index   = tasks.findIndex(t => t.id === id);
  if (index === -1) throw new Error(`Task #${id} not found`);
  const [removed] = tasks.splice(index, 1);
  save(tasks);
  return removed;
}

// ─── focus mode (NEW FEATURE) ────────────────────────────────────────────────
// Returns an object with:
//   focused  – tasks due today or overdue, not yet done, sorted by priority
//   progress – { done, total, pct } for ALL tasks
//   bar      – ASCII progress bar string

function focusMode() {
  const tasks   = load();
  const total   = tasks.length;
  const done    = tasks.filter(t => t.done).length;
  const pct     = total === 0 ? 0 : Math.round((done / total) * 100);

  const BAR_WIDTH = 30;
  const filled    = Math.round((pct / 100) * BAR_WIDTH);
  const bar       = '[' + '█'.repeat(filled) + '░'.repeat(BAR_WIDTH - filled) + ']';

  const focused = tasks
    .filter(t => !t.done && isOverdueOrDueToday(t))
    .sort((a, b) => (PRIORITIES[a.priority] || 99) - (PRIORITIES[b.priority] || 99));

  return { focused, progress: { done, total, pct }, bar };
}

module.exports = { addTask, listTasks, completeTask, deleteTask, focusMode };
