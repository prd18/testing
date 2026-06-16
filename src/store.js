'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const DATA_DIR  = path.join(os.homedir(), '.taskr');
const DATA_FILE = path.join(DATA_DIR, 'tasks.json');

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// Sanitize a single task object loaded from disk to prevent prototype pollution.
// Returns a plain object with only the known safe fields; drops any __proto__,
// constructor, or other dangerous keys that could pollute Object.prototype.
function sanitizeTask(raw) {
  if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) return null;
  return Object.assign(Object.create(null), {
    id:          typeof raw.id          === 'number'  ? raw.id          : undefined,
    title:       typeof raw.title       === 'string'  ? raw.title       : '',
    priority:    typeof raw.priority    === 'string'  ? raw.priority    : 'medium',
    dueDate:     typeof raw.dueDate     === 'string'  ? raw.dueDate     : null,
    done:        typeof raw.done        === 'boolean' ? raw.done        : false,
    createdAt:   typeof raw.createdAt   === 'string'  ? raw.createdAt   : '',
    completedAt: typeof raw.completedAt === 'string'  ? raw.completedAt : undefined,
  });
}

function load() {
  ensureDataDir();
  if (!fs.existsSync(DATA_FILE)) {
    return [];
  }
  try {
    // Use JSON.parse with a reviver that blocks __proto__ and constructor keys
    // to prevent prototype pollution attacks on tampered data files.
    const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'), (key, value) => {
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
        return undefined; // drop dangerous keys
      }
      return value;
    });
    if (!Array.isArray(data)) return [];
    return data.map(sanitizeTask).filter(t => t !== null && typeof t.id === 'number');
  } catch {
    return [];
  }
}

function save(tasks) {
  ensureDataDir();
  fs.writeFileSync(DATA_FILE, JSON.stringify(tasks, null, 2), 'utf8');
}

module.exports = { load, save };
