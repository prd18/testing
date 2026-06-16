"""
utils.py — Collection of simple utility functions.
"""


def flatten(nested):
    """Flatten a nested list of arbitrary depth into a single list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def is_palindrome(s):
    """Return True if the string s is a palindrome (case-insensitive)."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]


def count_words(text):
    """Return a dictionary mapping each word to its occurrence count."""
    counts = {}
    for word in text.split():
        word = word.strip(".,!?;:\"'").lower()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def find_duplicates(items):
    """Return a list of items that appear more than once (each reported once)."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


def chunk(lst, size):
    """Split lst into consecutive chunks of the given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def safe_divide(a, b):
    """Divide a by b, returning None when b is zero."""
    if b == 0:
        return None
    return a / b
