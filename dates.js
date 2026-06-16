/**
 * dates.js — A collection of simple, practical JavaScript date utilities.
 *
 * No external dependencies required — all built on the native Date API.
 */

// ─── 1. Get today's date ────────────────────────────────────────────────────

const today = new Date();
console.log("Today (ISO):", today.toISOString());
console.log("Today (locale):", today.toLocaleDateString());

// ─── 2. Format a date as YYYY-MM-DD ────────────────────────────────────────

function formatDate(date) {
  const year  = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0"); // month is 0-indexed
  const day   = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

console.log("Formatted today:", formatDate(new Date())); // e.g. "2026-06-16"

// ─── 3. Add or subtract days ────────────────────────────────────────────────

function addDays(date, n) {
  const result = new Date(date);
  result.setDate(result.getDate() + n);
  return result;
}

console.log("7 days from now:", formatDate(addDays(new Date(), 7)));
console.log("30 days ago:", formatDate(addDays(new Date(), -30)));

// ─── 4. Difference between two dates (in days) ─────────────────────────────

function diffInDays(dateA, dateB) {
  const MS_PER_DAY = 1000 * 60 * 60 * 24;
  return Math.round((dateB - dateA) / MS_PER_DAY);
}

const yearStart = new Date("2026-01-01");
const yearEnd   = new Date("2026-12-31");
console.log("Days in 2026:", diffInDays(yearStart, yearEnd)); // 364

// ─── 5. Check if a date is in the past or future ───────────────────────────

function isPast(date)   { return date < new Date(); }
function isFuture(date) { return date > new Date(); }
function isToday(date) {
  const now = new Date();
  return (
    date.getFullYear() === now.getFullYear() &&
    date.getMonth()    === now.getMonth()    &&
    date.getDate()     === now.getDate()
  );
}

console.log("Is 2020-01-01 in the past?", isPast(new Date("2020-01-01")));   // true
console.log("Is 2030-01-01 in the future?", isFuture(new Date("2030-01-01"))); // true
console.log("Is today today?", isToday(new Date()));                          // true

// ─── 6. Start and end of a day ─────────────────────────────────────────────

function startOfDay(date) {
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  return d;
}

function endOfDay(date) {
  const d = new Date(date);
  d.setHours(23, 59, 59, 999);
  return d;
}

console.log("Start of today:", startOfDay(new Date()).toISOString());
console.log("End of today:", endOfDay(new Date()).toISOString());

// ─── 7. Get the human-readable day and month names ─────────────────────────

const DAY_NAMES   = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const MONTH_NAMES = ["January","February","March","April","May","June",
                     "July","August","September","October","November","December"];

function getDayName(date)   { return DAY_NAMES[date.getDay()]; }
function getMonthName(date) { return MONTH_NAMES[date.getMonth()]; }

console.log("Day name:", getDayName(new Date()));
console.log("Month name:", getMonthName(new Date()));

// ─── 8. Locale-aware pretty formatting via Intl ─────────────────────────────

function prettyFormat(date, locale = "en-US") {
  return new Intl.DateTimeFormat(locale, {
    weekday: "long",
    year:    "numeric",
    month:   "long",
    day:     "numeric",
  }).format(date);
}

console.log("Pretty (en-US):", prettyFormat(new Date()));
console.log("Pretty (fr-FR):", prettyFormat(new Date(), "fr-FR"));

// ─── 9. Relative time (e.g. "3 days ago", "in 2 weeks") ───────────────────

function relativeTime(date) {
  const MS_PER_MINUTE = 60 * 1000;
  const MS_PER_HOUR   = 60 * MS_PER_MINUTE;
  const MS_PER_DAY    = 24 * MS_PER_HOUR;
  const MS_PER_WEEK   = 7  * MS_PER_DAY;

  const diff = date - new Date(); // positive = future, negative = past
  const abs  = Math.abs(diff);
  const suffix = diff < 0 ? "ago" : "from now";

  if (abs < MS_PER_MINUTE)  return "just now";
  if (abs < MS_PER_HOUR)    return `${Math.round(abs / MS_PER_MINUTE)} minute(s) ${suffix}`;
  if (abs < MS_PER_DAY)     return `${Math.round(abs / MS_PER_HOUR)} hour(s) ${suffix}`;
  if (abs < MS_PER_WEEK)    return `${Math.round(abs / MS_PER_DAY)} day(s) ${suffix}`;
  return `${Math.round(abs / MS_PER_WEEK)} week(s) ${suffix}`;
}

console.log("5 days ago:", relativeTime(addDays(new Date(), -5)));
console.log("In 2 weeks:", relativeTime(addDays(new Date(), 14)));

// ─── 10. Check if a year is a leap year ───────────────────────────────────

function isLeapYear(year) {
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

console.log("2024 is leap year:", isLeapYear(2024)); // true
console.log("2026 is leap year:", isLeapYear(2026)); // false

// ─── 11. Get number of days in a month ────────────────────────────────────

function daysInMonth(year, month) {
  // Day 0 of the NEXT month = last day of the current month
  return new Date(year, month, 0).getDate();
}

console.log("Days in Feb 2024:", daysInMonth(2024, 2)); // 29 (leap year)
console.log("Days in Feb 2026:", daysInMonth(2026, 2)); // 28

// ─── 12. Timestamps ────────────────────────────────────────────────────────

const ts   = Date.now();                 // milliseconds since Unix epoch
const back = new Date(ts);              // convert back to Date
console.log("Timestamp (ms):", ts);
console.log("From timestamp:", back.toISOString());
