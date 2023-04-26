import unittest

from Lab_3.utils.serialize import JSONSerializer


class JSONDataStructuresCase(unittest.TestCase):
    ser: JSONSerializer = JSONSerializer()

    def test_empty(self):
        self.assertEqual(self.ser.loads(self.ser.dumps({})), {})
        self.assertEqual(self.ser.loads(self.ser.dumps(())), ())
        self.assertEqual(self.ser.loads(self.ser.dumps([])), [])
        self.assertEqual(self.ser.loads(self.ser.dumps(set())), set())

    def test_single_value(self):
        self.assertEqual(self.ser.loads(self.ser.dumps({None: 0})), {None: 0})
        self.assertEqual(self.ser.loads(self.ser.dumps(([None]))), ([None]))
        self.assertEqual(self.ser.loads(self.ser.dumps([None])), [None])
        self.assertEqual(self.ser.loads(self.ser.dumps({None})), {None})

    def test_nested_multityped(self):
        test_1 = {
            1: 2,
            "3": [4, -1, "aboba {([sus])} '''imposter"],
            5: {
                6: '7',
                8: {
                    9: None,
                    'None': (True, False)
                },
            }
        }
        self.assertEqual(self.ser.loads(self.ser.dumps(test_1)), test_1)


if __name__ == '__main__':
    unittest.main()
