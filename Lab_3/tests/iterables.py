import unittest

from Lab_3.xjst.serialize import JSONSerializer, XMLSerializer


class JSONDataStructuresCase(unittest.TestCase):
    json_ser: JSONSerializer = JSONSerializer()
    xml_ser: XMLSerializer = XMLSerializer()

    def test_empty(self):
        self.assertEqual(self.json_ser.loads(self.json_ser.dumps({})), {})
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps({})), {})

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(())), ())
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(())), ())

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps([])), [])
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps([])), [])

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(set())), set())
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(set())), set())

    def test_single_value(self):
        self.assertEqual(self.json_ser.loads(self.json_ser.dumps({None: 0})), {None: 0})
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps({None: 0})), {None: 0})

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(([None]))), ([None]))
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(([None]))), ([None]))

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps([None])), [None])
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps([None])), [None])

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps({None})), {None})
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps({None})), {None})

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
        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(test_1)), test_1)
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(test_1)), test_1)


if __name__ == '__main__':
    unittest.main()
