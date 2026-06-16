# Python Cheatsheet

A comprehensive quick-reference guide for Python 3.x.

---

## Table of Contents
1. [Data Types](#data-types)
2. [Strings](#strings)
3. [Lists](#lists)
4. [Tuples](#tuples)
5. [Dictionaries](#dictionaries)
6. [Sets](#sets)
7. [Control Flow](#control-flow)
8. [Functions](#functions)
9. [Classes & OOP](#classes--oop)
10. [File I/O](#file-io)
11. [Error Handling](#error-handling)
12. [Comprehensions](#comprehensions)
13. [Modules & Imports](#modules--imports)
14. [Built-in Functions](#built-in-functions)
15. [Quick Tips](#quick-tips)

---

## Data Types

```python
# Integers
x = 42
x = int("42")

# Floats
y = 3.14
y = float("3.14")

# Booleans
flag = True
flag = bool(1)   # True
bool(0)          # False

# None
val = None

# Type checking
type(x)          # <class 'int'>
isinstance(x, int)  # True
```

---

## Strings

```python
s = "Hello, World!"

# Common methods
s.upper()           # "HELLO, WORLD!"
s.lower()           # "hello, world!"
s.strip()           # removes leading/trailing whitespace
s.lstrip()          # removes leading whitespace
s.rstrip()          # removes trailing whitespace
s.replace("Hello", "Hi")  # "Hi, World!"
s.split(", ")       # ["Hello", "World!"]
", ".join(["a", "b", "c"])  # "a, b, c"
s.startswith("Hello")  # True
s.endswith("!")     # True
s.find("World")     # 7
s.count("l")        # 3
s.isdigit()         # False
s.isalpha()         # False

# f-strings (Python 3.6+)
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age}")

# Multi-line strings
text = """
This is a
multi-line string
"""

# Slicing
s[0]       # "H"
s[-1]      # "!"
s[0:5]     # "Hello"
s[::2]     # every other character
s[::-1]    # reversed
```

---

## Lists

```python
lst = [1, 2, 3, 4, 5]

# Access
lst[0]          # 1
lst[-1]         # 5
lst[1:3]        # [2, 3]

# Modify
lst.append(6)       # [1, 2, 3, 4, 5, 6]
lst.insert(0, 0)    # [0, 1, 2, 3, 4, 5, 6]
lst.extend([7, 8])  # adds multiple elements
lst.remove(3)       # removes first occurrence of 3
lst.pop()           # removes & returns last item
lst.pop(0)          # removes & returns item at index 0
lst.clear()         # empties the list

# Info
len(lst)
lst.count(2)
lst.index(2)

# Sorting
lst.sort()              # in-place ascending
lst.sort(reverse=True)  # in-place descending
sorted(lst)             # returns new sorted list

# Other
lst.reverse()
lst.copy()
lst + [9, 10]       # concatenation
lst * 2             # repetition
3 in lst            # membership test
```

---

## Tuples

```python
t = (1, 2, 3)
t = 1, 2, 3         # parentheses optional

# Access (same as list slicing)
t[0]        # 1
t[-1]       # 3
t[1:3]      # (2, 3)

# Unpacking
a, b, c = t
first, *rest = t    # first=1, rest=[2, 3]

# Info
len(t)
t.count(1)
t.index(2)

# Immutable — cannot modify after creation
# Convert to list to modify
lst = list(t)
lst.append(4)
t = tuple(lst)
```

---

## Dictionaries

```python
d = {"name": "Alice", "age": 30}

# Access
d["name"]           # "Alice"
d.get("name")       # "Alice"
d.get("missing", "default")  # "default"

# Modify
d["city"] = "NYC"       # add/update
d.update({"age": 31, "job": "dev"})
del d["city"]
d.pop("age")            # removes & returns value
d.setdefault("lang", "Python")  # sets only if key absent

# Iteration
d.keys()
d.values()
d.items()           # key-value pairs

for key, val in d.items():
    print(key, val)

# Info
len(d)
"name" in d         # True

# Merging (Python 3.9+)
merged = d1 | d2
d1 |= d2            # in-place merge

# Dict from keys
dict.fromkeys(["a", "b", "c"], 0)  # {"a": 0, "b": 0, "c": 0}
```

---

## Sets

```python
s = {1, 2, 3, 4}
s = set([1, 2, 2, 3])  # deduplicates → {1, 2, 3}

# Modify
s.add(5)
s.remove(3)     # raises KeyError if missing
s.discard(3)    # no error if missing
s.pop()         # removes arbitrary element
s.clear()

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}

a | b           # union       → {1, 2, 3, 4}
a & b           # intersection → {2, 3}
a - b           # difference  → {1}
a ^ b           # symmetric diff → {1, 4}

a.issubset(b)
a.issuperset(b)
a.isdisjoint(b)

# Info
len(s)
3 in s          # membership test (O(1))
```

---

## Control Flow

```python
# if / elif / else
x = 10
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary
result = "even" if x % 2 == 0 else "odd"

# for loop
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 2):  # 2, 4, 6, 8
    print(i)

for item in [1, 2, 3]:
    print(item)

for idx, val in enumerate(["a", "b", "c"]):
    print(idx, val)

# while loop
n = 0
while n < 5:
    print(n)
    n += 1

# break / continue / else on loops
for i in range(10):
    if i == 3:
        continue    # skip 3
    if i == 7:
        break       # stop at 7
else:
    print("loop completed without break")

# match statement (Python 3.10+)
command = "quit"
match command:
    case "quit":
        print("Quitting")
    case "help":
        print("Showing help")
    case _:
        print("Unknown command")
```

---

## Functions

```python
# Basic
def greet(name):
    return f"Hello, {name}!"

# Default arguments
def greet(name="World"):
    return f"Hello, {name}!"

# *args and **kwargs
def func(*args, **kwargs):
    print(args)    # tuple of positional args
    print(kwargs)  # dict of keyword args

# Type hints (Python 3.5+)
def add(a: int, b: int) -> int:
    return a + b

# Lambda
square = lambda x: x ** 2
square(4)  # 16

# Docstrings
def divide(a, b):
    """
    Divide a by b.

    Args:
        a (float): numerator
        b (float): denominator

    Returns:
        float: result of division
    """
    return a / b

# Unpacking arguments
def point(x, y, z):
    return x, y, z

coords = [1, 2, 3]
point(*coords)

params = {"x": 1, "y": 2, "z": 3}
point(**params)
```

---

## Classes & OOP

```python
class Animal:
    species = "Unknown"  # class attribute

    def __init__(self, name, sound):
        self.name = name      # instance attribute
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __repr__(self):
        return f"Animal(name={self.name!r})"

    def __str__(self):
        return self.name

    @classmethod
    def create_dog(cls):
        return cls("Dog", "Woof")

    @staticmethod
    def is_animal(obj):
        return isinstance(obj, Animal)


class Dog(Animal):  # Inheritance
    def __init__(self, name):
        super().__init__(name, "Woof")

    def fetch(self, item):
        return f"{self.name} fetches the {item}"


# Properties
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2


# Common dunder methods
# __init__    constructor
# __str__     str(obj)
# __repr__    repr(obj)
# __len__     len(obj)
# __eq__      obj == other
# __lt__      obj < other
# __add__     obj + other
# __contains__ item in obj
# __iter__    iter(obj)
# __next__    next(obj)
# __enter__   with obj as ...
# __exit__    end of with block
```

---

## File I/O

```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Read all lines into list
with open("file.txt", "r") as f:
    lines = f.readlines()

# Write
with open("file.txt", "w") as f:
    f.write("Hello\n")

# Append
with open("file.txt", "a") as f:
    f.write("Another line\n")

# File modes
# "r"  — read (default)
# "w"  — write (truncates)
# "a"  — append
# "x"  — exclusive creation (fails if exists)
# "b"  — binary mode (e.g. "rb", "wb")
# "+"  — read+write (e.g. "r+")

# pathlib (recommended modern approach)
from pathlib import Path

p = Path("file.txt")
p.read_text()
p.write_text("content")
p.exists()
p.is_file()
p.is_dir()
p.suffix        # ".txt"
p.stem          # "file"
p.parent        # parent directory
list(p.parent.glob("*.txt"))  # glob pattern
```

---

## Error Handling

```python
# Basic try/except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# Multiple exceptions
try:
    val = int("abc")
except (ValueError, TypeError) as e:
    print(f"Error: {e}")

# else and finally
try:
    f = open("file.txt")
except FileNotFoundError:
    print("File not found")
else:
    # runs if no exception
    print(f.read())
    f.close()
finally:
    # always runs
    print("Done")

# Raising exceptions
def divide(a, b):
    if b == 0:
        raise ValueError("Denominator cannot be zero")
    return a / b

# Re-raising
try:
    risky()
except Exception as e:
    log(e)
    raise

# Custom exceptions
class AppError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

raise AppError("Something went wrong", code=500)

# Context managers
class ManagedResource:
    def __enter__(self):
        print("Acquiring resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        return False  # re-raise exceptions

with ManagedResource() as r:
    r.do_something()
```

---

## Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]

# Nested
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [n for row in matrix for n in row]

# Dict comprehension
squared = {x: x**2 for x in range(5)}
inverted = {v: k for k, v in d.items()}

# Set comprehension
unique_lengths = {len(word) for word in words}

# Generator expression (lazy — no list created)
total = sum(x**2 for x in range(1000))
gen   = (x**2 for x in range(10))
next(gen)   # 0
```

---

## Modules & Imports

```python
import os
import sys
import re
import json
import math
import random
import datetime
import itertools
import functools
import collections
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union, Any

# Useful aliases
import numpy as np
import pandas as pd

# Relative imports (inside packages)
from . import module
from ..utils import helper

# Common standard library uses
os.getcwd()
os.listdir(".")
os.path.join("dir", "file.txt")
os.environ.get("HOME")

sys.argv        # command-line arguments
sys.exit(0)

json.dumps({"key": "val"})   # dict → JSON string
json.loads('{"key": "val"}') # JSON string → dict

math.pi
math.sqrt(16)
math.floor(3.7)
math.ceil(3.2)

random.randint(1, 10)
random.choice([1, 2, 3])
random.shuffle(lst)

datetime.datetime.now()
datetime.date.today()
```

---

## Built-in Functions

```python
# Iteration helpers
range(10)
enumerate(iterable)
zip(a, b)
map(func, iterable)
filter(func, iterable)
reversed(lst)
sorted(iterable, key=lambda x: x[1], reverse=True)

# Aggregation
len(obj)
sum(iterable)
min(iterable)
max(iterable)
abs(-5)
round(3.14159, 2)

# Type conversion
int(), float(), str(), bool(), list(), tuple(), dict(), set()

# Functional
any(iterable)    # True if at least one element is truthy
all(iterable)    # True if all elements are truthy

# Introspection
dir(obj)         # list attributes/methods
help(obj)        # documentation
vars(obj)        # object's __dict__
id(obj)          # memory address
callable(obj)    # is it callable?

# I/O
print("hello", end="\n", sep=" ")
input("Enter value: ")

# Other
hash(obj)
hex(255)         # "0xff"
bin(10)          # "0b1010"
oct(8)           # "0o10"
chr(65)          # "A"
ord("A")         # 65
```

---

## Quick Tips

```python
# Swap variables
a, b = b, a

# Multiple assignment
x = y = z = 0

# Chained comparisons
0 < x < 10

# Walrus operator (Python 3.8+)
if (n := len(data)) > 10:
    print(f"Too many items: {n}")

# Dictionary get with default
value = d.get("key", "default")

# Safe list indexing
lst[0] if lst else None

# Flatten one level
import itertools
flat = list(itertools.chain.from_iterable(nested))

# Count occurrences
from collections import Counter
counts = Counter(["a", "b", "a", "c", "b", "a"])
counts.most_common(2)  # [("a", 3), ("b", 2)]

# Default dict
from collections import defaultdict
dd = defaultdict(list)
dd["key"].append(1)   # no KeyError

# Named tuple
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
p.x, p.y

# Decorators
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
```

---

*Generated as a quick-reference Python cheatsheet.*
