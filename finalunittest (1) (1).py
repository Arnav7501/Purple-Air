import unittest
import finalassgn as assgn


class TestCC(unittest.TestCase):
  
    def test_load_data(self):
        purple_air = assgn.DataSet()
        self.assertEqual(6147,  purple_air.load_file())

    
if __name__ == "__main__":
    unittest.main()

r"""
Sample Run #1
147  lines loaded
.
----------------------------------------------------------------------
Ran 1 test in 0.013s

OK
"""