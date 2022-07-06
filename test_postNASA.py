import unittest
from postNASA import *
import sqlalchemy as db
import pandas as pd

class TestpostYT(unittest.TestCase):

    # test to see if get channel will return string
    def test_returnValue_datatype_for_dayinMonth(self):
        self.assertEqual(True,day_in_month(31,12))
        self.assertEqual(False,day_in_month(-4,-1))
        self.assertEqual(False,day_in_month(29,2))
        self.assertEqual(True,day_in_month(1,2))
        self.assertEqual(True,day_in_month(31,12))
        self.assertEqual(True,day_in_month(1,4))
        self.assertEqual(False,day_in_month(31,6))
        self.assertEqual(True,day_in_month(30,9))


if __name__ == '__main__':
    unittest.main()

