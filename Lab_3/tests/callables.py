import unittest

from Lab_3.utils.serialize import JSONSerializer


def test_func_1(x):
    return x + 2


def test_func_2(x, y):
    return x ** 2 + 2 * y


class JSONFunctionsCase(unittest.TestCase):
    ser = JSONSerializer()

    def test_one_argument(self):
        self.assertEqual(
            self.ser.loads(self.ser.dumps(test_func_1))(0),
            test_func_1(0))

    def test_two_arguments(self):
        self.assertEqual(
            self.ser.loads(self.ser.dumps(test_func_2))(0, 0),
            test_func_2(0, 0))


if __name__ == '__main__':
    unittest.main()
