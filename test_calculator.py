"""Tests for calculator.py"""
import unittest
from calculator import add, subtract, multiply, divide, average, factorial, is_prime


class TestAdd(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-1, -1), -2)


class TestSubtract(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(subtract(10, 4), 6)


class TestMultiply(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(multiply(3, 4), 12)


class TestDivide(unittest.TestCase):
    def test_basic(self):
        self.assertAlmostEqual(divide(10, 4), 2.5)

    def test_zero_division(self):
        with self.assertRaises(ValueError):
            divide(5, 0)


class TestAverage(unittest.TestCase):
    def test_single(self):
        self.assertEqual(average([5]), 5)

    def test_multiple(self):
        # average of [1, 2, 3] should be 2.0
        self.assertAlmostEqual(average([1, 2, 3]), 2.0)

    def test_empty(self):
        with self.assertRaises(ValueError):
            average([])


class TestFactorial(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(factorial(0), 1)

    def test_one(self):
        self.assertEqual(factorial(1), 1)

    def test_five(self):
        # 5! = 120
        self.assertEqual(factorial(5), 120)

    def test_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)


class TestIsPrime(unittest.TestCase):
    def test_primes(self):
        for p in [2, 3, 5, 7, 11, 13]:
            self.assertTrue(is_prime(p), f"{p} should be prime")

    def test_non_primes(self):
        for n in [0, 1, 4, 6, 8, 9]:
            self.assertFalse(is_prime(n), f"{n} should not be prime")


if __name__ == "__main__":
    unittest.main()
