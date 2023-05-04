import os.path
import unittest

from Lab_3.utils.serialize import JSONSerializer, XMLSerializer
from tests import DATA_DIR


class JSONBasicTypesCase(unittest.TestCase):
    json_ser = JSONSerializer()
    xml_ser = XMLSerializer()

    def test_dumps_only(self):
        self.assertEqual(self.json_ser.dumps("14"), '"14"')
        self.assertEqual(self.json_ser.dumps(14), "14")
        self.assertEqual(self.json_ser.dumps(14.0), "14.0")
        self.assertEqual(self.json_ser.dumps(14j + 0.9), "(0.9+14j)")
        self.assertEqual(self.json_ser.dumps("False"), '"False"')
        self.assertEqual(self.json_ser.dumps(False), "false")
        self.assertEqual(self.json_ser.dumps(""), '""')

    def test_loads_only(self):
        self.assertEqual(self.json_ser.loads('"14"'), "14")
        self.assertEqual(self.json_ser.loads("14"), 14)
        self.assertEqual(self.json_ser.loads("14.0"), 14.0)
        self.assertEqual(self.json_ser.loads("(0.9+14j)"), 0.9 + 14j)
        self.assertEqual(self.json_ser.loads("false"), False)
        self.assertEqual(self.json_ser.loads('"False"'), "False")
        self.assertEqual(self.json_ser.loads('""'), "")
        self.assertEqual(self.json_ser.loads(""), None)

    def test_dumps_and_loads(self):
        self.assertEqual(self.json_ser.loads(self.json_ser.dumps("14")), "14")
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps("14")), "14")

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(14)), 14)
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(14)), 14)

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(14.0)), 14.0)
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(14.0)), 14.0)

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(0.9 + 14j)), 0.9 + 14j)
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(0.9 + 14j)), 0.9 + 14j)

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps("False")), "False")
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps("False")), "False")

        self.assertEqual(self.json_ser.loads(self.json_ser.dumps(False)), False)
        self.assertEqual(self.xml_ser.loads(self.xml_ser.dumps(False)), False)

    def test_dump_and_load(self):
        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.json_ser.dump("14", fw)
            fw.seek(0)
            self.assertEqual(self.json_ser.load(fr), '14')

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.json_ser.dump(14, fw)
            fw.seek(0)
            self.assertEqual(self.json_ser.load(fr), 14)

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.json_ser.dump(14.0, fw)
            fw.seek(0)
            self.assertEqual(self.json_ser.load(fr), 14.0)

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.json_ser.dump(0.9j + 14, fw)
            fw.seek(0)
            self.assertEqual(self.json_ser.load(fr), 0.9j + 14)

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.json_ser.dump("False", fw)
            fw.seek(0)
            self.assertEqual(self.json_ser.load(fr), "False")

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.json_ser.dump(False, fw)
            fw.seek(0)
            self.assertEqual(self.json_ser.load(fr), False)


if __name__ == '__main__':
    unittest.main()
