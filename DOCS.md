# Documentation

## Overview

This project provides a lightweight JavaScript date utility library (`dates.js`) with no external dependencies. All functions are pure and side-effect free — they accept `Date` objects (or date strings) and return values without mutating the input.

---

## Functions Reference

### `formatDate(date, separator?)`

Formats a `Date` object into a `YYYY-MM-DD` string.

```js
formatDate(new Date("2026-06-16"));       // "2026-06-16"
formatDate(new Date("2026-06-16"), "/");  // "2026/06/16"
```

---

### `addDays(date, n)`

Returns a new `Date` that is `n` days after (or before, if negative) the given date.

```js
addDays(new Date("2026-06-16"), 7);   // 2026-06-23
addDays(new Date("2026-06-16"), -3);  // 2026-06-13
```

---

### `diffInDays(dateA, dateB)`

Returns the number of whole days between two dates. Positive if `dateB` is after `dateA`.

```js
diffInDays(new Date("2026-01-01"), new Date("2026-06-16"));  // 166
```

---

### `isPast(date)` / `isFuture(date)` / `isToday(date)`

Boolean checks relative to the current moment.

```js
isPast(new Date("2020-01-01"));    // true
isFuture(new Date("2030-01-01")); // true
isToday(new Date());              // true
```

---

### `startOfDay(date)` / `endOfDay(date)`

Returns a `Date` set to midnight (00:00:00.000) or just before midnight (23:59:59.999) on the given day.

```js
startOfDay(new Date("2026-06-16"));  // 2026-06-16T00:00:00.000
endOfDay(new Date("2026-06-16"));    // 2026-06-16T23:59:59.999
```

---

### `getDayName(date)` / `getMonthName(date)`

Returns the full English name of the day or month.

```js
getDayName(new Date("2026-06-16"));    // "Tuesday"
getMonthName(new Date("2026-06-16")); // "June"
```

---

### `prettyFormat(date, locale?, options?)`

Locale-aware formatting using `Intl.DateTimeFormat`.

```js
prettyFormat(new Date("2026-06-16"));
// "Tuesday, June 16, 2026"

prettyFormat(new Date("2026-06-16"), "de-DE");
// "Dienstag, 16. Juni 2026"
```

---

### `relativeTime(date)`

Returns a human-readable relative time string.

```js
relativeTime(new Date(Date.now() - 3 * 86400000));  // "3 days ago"
relativeTime(new Date(Date.now() + 2 * 3600000));   // "in 2 hours"
relativeTime(new Date());                           // "just now"
```

---

### `isLeapYear(year)`

Returns `true` if the given year is a leap year.

```js
isLeapYear(2024);  // true
isLeapYear(2026);  // false
```

---

### `daysInMonth(year, month)`

Returns the number of days in the given month (1-indexed).

```js
daysInMonth(2026, 2);   // 28  (February, non-leap)
daysInMonth(2024, 2);   // 29  (February, leap year)
daysInMonth(2026, 12);  // 31
```

---

## Usage

```js
import {
  formatDate, addDays, diffInDays,
  isPast, isFuture, isToday,
  startOfDay, endOfDay,
  getDayName, getMonthName,
  prettyFormat, relativeTime,
  isLeapYear, daysInMonth,
} from "./dates.js";

const today = new Date();
console.log(formatDate(today));          // "2026-06-16"
console.log(relativeTime(addDays(today, -2)));  // "2 days ago"
```

---

## Notes

- All functions treat dates in **local time** unless stated otherwise.
- Month values passed to `daysInMonth` are **1-indexed** (January = 1), matching human convention.
- `relativeTime` uses simple thresholds and is not a full i18n solution.
- For timezone-aware calculations, consider the native `Temporal` API (Stage 3) or `date-fns`.

---

## License

MIT
