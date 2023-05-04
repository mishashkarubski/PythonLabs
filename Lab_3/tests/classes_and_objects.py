import unittest

from Lab_3.utils.serialize import JSONSerializer


class TestClass1:
    SOME_PROP_1 = {
        'a': None,
        'b': True,
        'c': False
    }

    def __init__(self, aa):
        self.a = 4
        self.aa = aa

    def test_bound_1(self):
        return self.a + self.aa

    @staticmethod
    def test_static_1(a):
        return a * 3


class TestClass2(TestClass1):
    SOME_PROP_2 = 'ahuha2 aboba@ amuga'

    def __init__(self, bb):
        super().__init__(bb * 2)
        self.b = 5
        self.bb = bb - 0.8

    @classmethod
    def test_class_2(cls):
        return cls.SOME_PROP_1


class WithoutInheritanceCase(unittest.TestCase):
    json_ser = JSONSerializer()

    def test_no_inheritance(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(TestClass1))(12).test_bound_1(),
            TestClass1(12).test_bound_1()
        )
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(TestClass1)).test_static_1(2),
            TestClass1.test_static_1(2)
        )

    def test_single_class_inheritance(self):
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(TestClass2)).SOME_PROP_1,
            TestClass2.SOME_PROP_1
        )
        self.assertEqual(
            self.json_ser.loads(self.json_ser.dumps(TestClass2))(12).test_bound_1(),
            TestClass2(12).test_bound_1()
        )
        self.assertEqual(
            self.json_ser.loads(
                self.json_ser.dumps(TestClass2)
            ).test_class_2(self.json_ser.loads(self.json_ser.dumps(TestClass2))),
            TestClass2.test_class_2()
        )


if __name__ == '__main__':
    unittest.main()
