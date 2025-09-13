import unittest

from main import SumTwo


class TestMath(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(SumTwo([2, 7, 11, 15], 9), [0, 1])

    def test_ex2(self):
        self.assertEqual(SumTwo([3, 2, 4], 6), [1, 2])

    def test_ex3(self):
        self.assertEqual(SumTwo([3, 3], 6), [0, 1])

    def test_list(self):
        self.assertEqual(SumTwo((1, 2, 3, 4, 5), 3), 'None')

    def test_all_int(self):
        self.assertEqual(SumTwo([1, "2", 3, 4, 5], 3), 'None')

    def test_new_num(self):
        self.assertEqual(SumTwo([1, 2, 3, 4, 5, 2], 6), [0, 4])

    def test_no_numbers(self):
        self.assertEqual(SumTwo([], 3), 'None')

    def test_target_no_int(self):
        self.assertEqual(SumTwo([1, 2, 3, 4, 5], '3'), 'None')

    def test_no_int(self):
        self.assertEqual(SumTwo([1.1, 1.3, 3.0, 4.0], 3), "None")


if __name__ == '__main__':
    unittest.main()
