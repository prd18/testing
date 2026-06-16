#!/usr/bin/env node
'use strict';

const { addTask, listTasks, completeTask, deleteTask, focusMode } = require('./tasks');

// ─── tiny ANSI helpers ───────────────────────────────────────────────────────
const c = {
  reset:  '\x1b[0m',
  bold:   '\x1b[1m',
  dim:    '\x1b[2m',
  red:    '\x1b[31m',
  green:  '\x1b[32m',
  yellow: '\x1b[33m',
  blue:   '\x1b[34m',
  magenta:'\x1b[35m',
  cyan:   '\x1b[36m',
  white:  '\x1b[37m',
};
const clr = (color, text) => `${c[color]}${text}${c.reset}`;
const bold = text => `${c.bold}${text}${c.reset}`;

function priorityColor(p) {
  if (p === 'high')   return clr('red',    p);
  if (p === 'medium') return clr('yellow', p);
  return                      clr('green',  p);
}

function formatDate(dateStr) {
  if (!dateStr) return clr('dim', '(no due date)');
  const today   = new Date().toISOString().slice(0, 10);
  if (dateStr < today) return clr('red',    dateStr + ' ⚠ overdue');
  if (dateStr === today) return clr('yellow', dateStr + ' ★ today');
  return clr('blue', dateStr);
}

function printTask(task) {
  const status = task.done ? clr('green', '✓') : clr('dim', '○');
  const id     = clr('dim', `#${String(task.id).padStart(3, '0')}`);
  const pri    = priorityColor(task.priority);
  const due    = formatDate(task.dueDate);
  const title  = task.done ? clr('dim', task.title) : task.title;
  console.log(`  ${status} ${id}  ${title.padEnd(40)} ${pri.padEnd(20)}  ${due}`);
}

function printHeader(text) {
  console.log('');
  console.log(bold(clr('cyan', text)));
  console.log(clr('dim', '─'.repeat(72)));
}

// ─── commands ────────────────────────────────────────────────────────────────

function cmdAdd(args) {
  // taskr add "title" [--priority high|medium|low] [--due YYYY-MM-DD]
  const title    = args[0];
  const priIdx   = args.indexOf('--priority');
  const dueIdx   = args.indexOf('--due');
  const priority = priIdx !== -1 ? args[priIdx + 1] : 'medium';
  const dueDate  = dueIdx !== -1 ? args[dueIdx  + 1] : undefined;

  try {
    const task = addTask({ title, priority, dueDate });
    console.log(clr('green', `✓ Task #${task.id} added: "${task.title}" [${task.priority}]${dueDate ? ' due ' + dueDate : ''}`));
  } catch (e) {
    console.error(clr('red', 'Error: ' + e.message));
    process.exit(1);
  }
}

function cmdList(args) {
  const showDone = args.includes('--all');
  const tasks    = listTasks({ showDone });

  printHeader('Tasks' + (showDone ? ' (including done)' : ''));
  if (tasks.length === 0) {
    console.log(clr('dim', '  No tasks found. Use: taskr add "your task"'));
    return;
  }
  console.log(clr('dim', '    id   title                                    priority              due'));
  tasks.forEach(printTask);
  console.log('');
}

function cmdDone(args) {
  const id = parseInt(args[0], 10);
  if (!id) { console.error(clr('red', 'Usage: taskr done <id>')); process.exit(1); }
  try {
    const task = completeTask(id);
    console.log(clr('green', `✓ Marked #${task.id} as done: "${task.title}"`));
  } catch (e) {
    console.error(clr('red', 'Error: ' + e.message));
    process.exit(1);
  }
}

function cmdDelete(args) {
  const id = parseInt(args[0], 10);
  if (!id) { console.error(clr('red', 'Usage: taskr delete <id>')); process.exit(1); }
  try {
    const task = deleteTask(id);
    console.log(clr('yellow', `✗ Deleted #${task.id}: "${task.title}"`));
  } catch (e) {
    console.error(clr('red', 'Error: ' + e.message));
    process.exit(1);
  }
}

// ─── FOCUS MODE (new feature) ────────────────────────────────────────────────
function cmdFocus() {
  const { focused, progress, bar } = focusMode();

  console.log('');
  console.log(bold('  ═══════════════════════════════════════════════════════════════════════'));
  console.log(bold(`  ${clr('magenta', '⬡  FOCUS MODE')}  —  tasks due today or overdue`));
  console.log(bold('  ═══════════════════════════════════════════════════════════════════════'));
  console.log('');

  // Progress bar
  const pctStr = `${progress.pct}%`;
  console.log(`  Overall progress:  ${clr('cyan', bar)}  ${bold(pctStr)}  (${progress.done}/${progress.total} done)`);
  console.log('');

  if (focused.length === 0) {
    console.log(clr('green', '  ✓ No tasks due today or overdue. You\'re all caught up!'));
  } else {
    console.log(clr('dim', `  ${focused.length} task${focused.length !== 1 ? 's' : ''} need${focused.length === 1 ? 's' : ''} your attention:\n`));
    console.log(clr('dim', '    id   title                                    priority              due'));
    focused.forEach(printTask);
  }

  console.log('');
  console.log(bold('  ═══════════════════════════════════════════════════════════════════════'));
  console.log('');
}

function cmdHelp() {
  console.log(`
${bold(clr('cyan', 'taskr — a simple CLI task manager'))}

${bold('Usage:')}
  taskr add <title> [--priority high|medium|low] [--due YYYY-MM-DD]
  taskr list [--all]
  taskr done <id>
  taskr delete <id>
  taskr focus          ${clr('magenta', '← NEW: shows today\'s urgent tasks + progress bar')}

${bold('Examples:')}
  taskr add "Write tests" --priority high --due 2026-06-16
  taskr add "Read email"  --priority low
  taskr list
  taskr done 1
  taskr focus
`);
}

// ─── entry point ─────────────────────────────────────────────────────────────

const [,, command, ...rest] = process.argv;

switch (command) {
  case 'add':    cmdAdd(rest);    break;
  case 'list':   cmdList(rest);   break;
  case 'done':   cmdDone(rest);   break;
  case 'delete': cmdDelete(rest); break;
  case 'focus':  cmdFocus();      break;
  default:       cmdHelp();       break;
}
