import os.path
import unittest

from Lab_3.utils.serialize import JSONSerializer
from config import DATA_DIR


class JSONBasicTypesCase(unittest.TestCase):
    ser = JSONSerializer()

    def test_dumps_only(self):
        self.assertEqual(self.ser.dumps("14"), "'14'")
        self.assertEqual(self.ser.dumps(14), "14")
        self.assertEqual(self.ser.dumps(14.0), "14.0")
        self.assertEqual(self.ser.dumps(14j+0.9), "(0.9+14j)")
        self.assertEqual(self.ser.dumps("False"), "'False'")
        self.assertEqual(self.ser.dumps(False), "False")
        self.assertEqual(self.ser.dumps(""), "''")

    def test_loads_only(self):
        self.assertEqual(self.ser.loads("'14'"), "14")
        self.assertEqual(self.ser.loads("14"), 14)
        self.assertEqual(self.ser.loads("14.0"), 14.0)
        self.assertEqual(self.ser.loads("(0.9+14j)"), 0.9+14j)
        self.assertEqual(self.ser.loads("False"), False)
        self.assertEqual(self.ser.loads("'False'"), "False")
        self.assertEqual(self.ser.loads(""), None)

    def test_dumps_and_loads(self):
        self.assertEqual(self.ser.loads(self.ser.dumps("14")), "14")
        self.assertEqual(self.ser.loads(self.ser.dumps(14)), 14)
        self.assertEqual(self.ser.loads(self.ser.dumps(14.0)), 14.0)
        self.assertEqual(self.ser.loads(self.ser.dumps(0.9+14j)), 0.9+14j)
        self.assertEqual(self.ser.loads(self.ser.dumps("False")), "False")
        self.assertEqual(self.ser.loads(self.ser.dumps(False)), False)
        self.assertEqual(self.ser.loads(self.ser.dumps("")), "")

    def test_dump_and_load(self):
        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.ser.dump("14", fw)
            fw.seek(0)
            self.assertEqual(self.ser.load(fr), '14')

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.ser.dump(14, fw)
            fw.seek(0)
            self.assertEqual(self.ser.load(fr), 14)

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.ser.dump(14.0, fw)
            fw.seek(0)
            self.assertEqual(self.ser.load(fr), 14.0)

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.ser.dump(0.9j+14, fw)
            fw.seek(0)
            self.assertEqual(self.ser.load(fr), 0.9j+14)

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.ser.dump("False", fw)
            fw.seek(0)
            self.assertEqual(self.ser.load(fr), "False")

        with (
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "w+") as fw,
            open(os.path.join(DATA_DIR, "dump_and_load.json"), "r") as fr
        ):
            self.ser.dump(False, fw)
            fw.seek(0)
            self.assertEqual(self.ser.load(fr), False)


if __name__ == '__main__':
    unittest.main()
