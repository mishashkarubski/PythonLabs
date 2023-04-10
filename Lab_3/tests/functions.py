import unittest

from Lab_3.utils.serialize import JSONSerializer


def test_func_1(x):
    return x + 2


def test_func_2(x, y):
    return x ** 2 + 2 * y


class JSONFunctionsCase(unittest.TestCase):
    ser = JSONSerializer()

    def test_obe_argument(self):
        self.assertEqual(
            self.ser.loads(self.ser.dumps(test_func_1)).__code__,
            test_func_1.__code__
        )

    def test_two_arguments(self):
        self.assertEqual(
            self.ser.loads(self.ser.dumps(test_func_2)).__code__,
            test_func_2.__code__
        )


if __name__ == '__main__':
    unittest.main()
