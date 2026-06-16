'use strict';

// Override the data file path so tests never touch ~/.taskr
const os   = require('os');
const path = require('path');
const fs   = require('fs');

const TEST_DIR  = path.join(os.tmpdir(), '.taskr-test-' + process.pid);
const TEST_FILE = path.join(TEST_DIR, 'tasks.json');

// Monkey-patch store before loading tasks module
const store = require('../src/store');
const origLoad = store.load.bind(store);
const origSave = store.save.bind(store);

store.load = function () {
  if (!fs.existsSync(TEST_FILE)) return [];
  return JSON.parse(fs.readFileSync(TEST_FILE, 'utf8'));
};
store.save = function (tasks) {
  fs.mkdirSync(TEST_DIR, { recursive: true });
  fs.writeFileSync(TEST_FILE, JSON.stringify(tasks, null, 2), 'utf8');
};

const { addTask, listTasks, completeTask, deleteTask, focusMode } = require('../src/tasks');

// ─── tiny test harness ───────────────────────────────────────────────────────
let passed = 0, failed = 0;

function test(name, fn) {
  // Reset task file before each test
  if (fs.existsSync(TEST_FILE)) fs.unlinkSync(TEST_FILE);
  try {
    fn();
    console.log(`  ✓  ${name}`);
    passed++;
  } catch (e) {
    console.error(`  ✗  ${name}`);
    console.error('     ', e.message);
    failed++;
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg || 'assertion failed');
}

// ─── tests ───────────────────────────────────────────────────────────────────
console.log('\ntaskr test suite\n');

test('addTask creates a task with defaults', () => {
  const t = addTask({ title: 'hello' });
  assert(t.id === 1,           'id should be 1');
  assert(t.title === 'hello',  'title mismatch');
  assert(t.priority === 'medium', 'default priority should be medium');
  assert(t.done === false,     'should not be done');
  assert(t.dueDate === null,   'dueDate should be null');
});

test('addTask throws when title is missing', () => {
  let threw = false;
  try { addTask({}); } catch { threw = true; }
  assert(threw, 'should have thrown');
});

test('addTask throws for invalid priority', () => {
  let threw = false;
  try { addTask({ title: 'x', priority: 'urgent' }); } catch { threw = true; }
  assert(threw, 'should have thrown on invalid priority');
});

test('addTask throws for invalid date format', () => {
  let threw = false;
  try { addTask({ title: 'x', dueDate: '16-06-2026' }); } catch { threw = true; }
  assert(threw, 'should have thrown on invalid date');
});

test('addTask increments IDs', () => {
  const a = addTask({ title: 'first' });
  const b = addTask({ title: 'second' });
  assert(b.id === a.id + 1, 'second task id should be first + 1');
});

test('listTasks returns only open tasks by default', () => {
  addTask({ title: 'open' });
  const t2 = addTask({ title: 'done task' });
  completeTask(t2.id);

  const open = listTasks();
  assert(open.length === 1,            'should return 1 open task');
  assert(open[0].title === 'open',     'wrong task returned');
});

test('listTasks --all returns all tasks', () => {
  addTask({ title: 'a' });
  const b = addTask({ title: 'b' });
  completeTask(b.id);

  const all = listTasks({ showDone: true });
  assert(all.length === 2, 'should return 2 tasks');
});

test('completeTask marks task as done', () => {
  const t = addTask({ title: 'finish me' });
  const done = completeTask(t.id);
  assert(done.done === true,           'done should be true');
  assert(done.completedAt,             'completedAt should be set');
});

test('completeTask throws for unknown id', () => {
  let threw = false;
  try { completeTask(999); } catch { threw = true; }
  assert(threw, 'should throw for unknown id');
});

test('deleteTask removes the task', () => {
  const t = addTask({ title: 'delete me' });
  deleteTask(t.id);
  const tasks = listTasks({ showDone: true });
  assert(tasks.length === 0, 'task should be removed');
});

test('deleteTask throws for unknown id', () => {
  let threw = false;
  try { deleteTask(999); } catch { threw = true; }
  assert(threw, 'should throw for unknown id');
});

// ── focus mode tests ─────────────────────────────────────────────────────────
test('focusMode returns empty focused list when no tasks exist', () => {
  const { focused, progress } = focusMode();
  assert(focused.length === 0,  'focused should be empty');
  assert(progress.total === 0,  'total should be 0');
  assert(progress.pct === 0,    'pct should be 0');
});

test('focusMode includes overdue tasks', () => {
  addTask({ title: 'overdue',  dueDate: '2020-01-01', priority: 'high' });
  addTask({ title: 'future',   dueDate: '2099-12-31', priority: 'low'  });
  addTask({ title: 'no date'                                            });

  const { focused } = focusMode();
  assert(focused.length === 1,             'only overdue task should appear');
  assert(focused[0].title === 'overdue',   'wrong task in focus');
});

test('focusMode includes due-today tasks', () => {
  const today = new Date().toISOString().slice(0, 10);
  addTask({ title: 'due today', dueDate: today, priority: 'medium' });

  const { focused } = focusMode();
  assert(focused.length === 1,              'today\'s task should appear');
  assert(focused[0].title === 'due today',  'wrong task');
});

test('focusMode excludes completed tasks', () => {
  const today = new Date().toISOString().slice(0, 10);
  const t = addTask({ title: 'done overdue', dueDate: today });
  completeTask(t.id);

  const { focused } = focusMode();
  assert(focused.length === 0, 'done task should not appear in focus');
});

test('focusMode sorts by priority (high first)', () => {
  const today = new Date().toISOString().slice(0, 10);
  addTask({ title: 'low task',    dueDate: today, priority: 'low'    });
  addTask({ title: 'high task',   dueDate: today, priority: 'high'   });
  addTask({ title: 'medium task', dueDate: today, priority: 'medium' });

  const { focused } = focusMode();
  assert(focused[0].priority === 'high',   'first should be high priority');
  assert(focused[1].priority === 'medium', 'second should be medium priority');
  assert(focused[2].priority === 'low',    'third should be low priority');
});

test('focusMode progress bar reflects completion', () => {
  addTask({ title: 'a' });
  addTask({ title: 'b' });
  const c = addTask({ title: 'c' });
  completeTask(c.id);

  const { progress, bar } = focusMode();
  assert(progress.total === 3,  'total should be 3');
  assert(progress.done  === 1,  'done should be 1');
  assert(progress.pct   === 33, 'pct should be 33');
  assert(bar.startsWith('['),   'bar should start with [');
  assert(bar.endsWith(']'),     'bar should end with ]');
});

// ─── summary ─────────────────────────────────────────────────────────────────
console.log('');
console.log(`Results: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
