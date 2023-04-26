import unittest

from Lab_3.utils.serialize import JSONSerializer

TEST_GLOBAL_1 = 19


def test_func_1(x):
    return x + 2


def test_func_2(x, y):
    return x ** 2 + 2 * y


class FunctionsCase(unittest.TestCase):
    json_ser = JSONSerializer()

    def test_one_argument(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(test_func_1))(0),
            test_func_1(0))

    def test_two_arguments(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(test_func_2))(0, 0),
            test_func_2(0, 0))


class LambdasCase(unittest.TestCase):
    json_ser = JSONSerializer()

    def test_basic_lambdas(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(lambda x: x**2 / 2))(10),
            (lambda x: x ** 2 / 2)(10))
        self.assertEqual(
            self.json_ser.loads(
                self.json_ser.dumps(lambda x, y, z: (x + y - z) ** 2 / 2)
            )(10, 5, 3),
            (lambda x, y, z: (x + y - z) ** 2 / 2)(10, 5, 3))


if __name__ == '__main__':
    unittest.main()
