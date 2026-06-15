"""A simple Python utility module."""


def greet(name: str) -> str:
    """Return a greeting string for the given name."""
    return f"Hello, {name}!"


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


def main() -> None:
    print(greet("World"))
    print(f"3 + 4 = {add(3, 4)}")
    print(f"7 is even: {is_even(7)}")
    print(f"8 is even: {is_even(8)}")


if __name__ == "__main__":
    main()
