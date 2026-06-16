# testing

A JavaScript date utilities library with a collection of practical helper functions for common date operations.

## About

This repository contains `dates.js`, a lightweight, zero-dependency JavaScript module covering the most common date manipulation and formatting tasks.

## Features

- Format dates as `YYYY-MM-DD` strings
- Add or subtract days from any date
- Calculate the difference in days between two dates
- Check if a date is in the past, future, or today
- Get the start and end of a day
- Get human-readable day and month names
- Locale-aware pretty formatting via `Intl.DateTimeFormat`
- Relative time strings (e.g. "3 days ago", "in 2 days")
- Leap year detection
- Days-in-month calculation
- Timestamp utilities

## Usage

```javascript
import {
  formatDate,
  addDays,
  diffInDays,
  isPast,
  isFuture,
  isToday,
  relativeTime,
  isLeapYear,
  daysInMonth,
  prettyFormat,
} from "./dates.js";

const today = new Date();

console.log(formatDate(today));                         // "2026-06-16"
console.log(addDays(today, 7));                         // one week from today
console.log(diffInDays(new Date("2026-01-01"), today)); // 166
console.log(isPast(new Date("2020-01-01")));            // true
console.log(relativeTime(addDays(today, -3)));          // "3 days ago"
console.log(isLeapYear(2024));                          // true
console.log(daysInMonth(2026, 1));                      // 28 (February 2026)
console.log(prettyFormat(today));                       // "Monday, June 16, 2026"
```

## Getting Started

No installation required. Just include `dates.js` in your project and import the functions you need.

```bash
# Clone the repo
git clone https://github.com/prd18/testing.git
cd testing
```

## File Structure

```
testing/
├── README.md   # this file
└── dates.js    # date utility functions
```

## License

MIT
