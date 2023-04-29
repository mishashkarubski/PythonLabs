import unittest

from Lab_3.utils.serialize import JSONSerializer

TEST_GLOBAL_1 = 19


def test_func_0():
    return 3


def test_func_1(x):
    return x + 2


def test_func_2(x, y):
    return (TEST_GLOBAL_1 / (x ** 2 + 1)) + 2 * y


def test_func_3(x, y, operation):
    a = operation(x * operation(y)) + TEST_GLOBAL_1

    def inner_test_func_3(b):
        """Inner function of ``test_func_3.``"""
        return (x + b) / (y + a)

    return inner_test_func_3(y / x)


class FunctionsCase(unittest.TestCase):
    json_ser = JSONSerializer()

    def test_zero_arguments(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(test_func_0))(),
            test_func_0()
        )

    def test_one_argument(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(test_func_1))(0),
            test_func_1(0))

    def test_globals(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(test_func_2))(12, -3),
            test_func_2(12, -3))

    def test_closures(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(test_func_3))(2, -3, lambda x: x**2),
            test_func_3(2, -3, lambda x: x**2))


class LambdasCase(unittest.TestCase):
    json_ser = JSONSerializer()

    def test_basic_lambdas(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(lambda x: x ** 2 / 2))(10),
            (lambda x: x ** 2 / 2)(10))
        self.assertEqual(
            self.json_ser.loads(
                self.json_ser.dumps(lambda x, y, z: (x + y - z) ** 2 / 2)
            )(10, 5, 3),
            (lambda x, y, z: (x + y - z) ** 2 / 2)(10, 5, 3))


if __name__ == '__main__':
    unittest.main()
