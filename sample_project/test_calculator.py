import unittest

from calculator import add, subtract, multiply, divide, average


class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(4, 3), 12)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

    def test_average(self):
        self.assertAlmostEqual(average([2, 4, 6]), 4)
        self.assertAlmostEqual(average((1, 2, 3, 4)), 2.5)

    def test_average_empty(self):
        with self.assertRaises(ValueError):
            average([])

    def test_average_invalid_element(self):
        with self.assertRaises(TypeError):
            average([1, 'a', 3])

    def test_average_non_iterable(self):
        with self.assertRaises(TypeError):
            average(123)


if __name__ == "__main__":
    unittest.main()
