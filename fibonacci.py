# Fibonacci Series in Python
# Covers four common approaches: iterative, recursive, generator, and memoized


# 1. Iterative approach (most efficient for large n)
def fibonacci_iterative(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


# 2. Recursive approach (elegant but slow for large n)
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


# 3. Generator approach (memory efficient for very large sequences)
def fibonacci_generator(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# 4. Memoized / Dynamic Programming approach (fast + handles large n)
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


# --- Demo ---
if __name__ == "__main__":
    n = 10

    print(f"Iterative (first {n} terms):")
    print(fibonacci_iterative(n))

    print(f"\nRecursive (first {n} terms):")
    print([fibonacci_recursive(i) for i in range(n)])

    print(f"\nGenerator (first {n} terms):")
    print(list(fibonacci_generator(n)))

    print(f"\nMemoized (first {n} terms):")
    print([fibonacci_memo(i) for i in range(n)])
