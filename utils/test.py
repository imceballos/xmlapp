"""Unit tests for Avicena Patient Mapper."""

import unittest
from utils import UtilFunctions

class Testing(unittest.TestCase):
    """Unit tests"""

    def test_get_file_info_one(self):
        output = {'filename': 'utils.py', 'size': 4057, 'creation_date': '2023-04-03 23:19:16'}
        result = UtilFunctions().get_file_info("utils.py")
        self.assertEqual(result, output)

    def test_map_two(self):
        output = {'filename': 'utils.py', 'size': 4057, 'creation_date': '2023-04-03 23:19:16'}
        result = UtilFunctions().get_file_info("settings.py")
        self.assertEqual(result, output)


    def test_get_func_filename_one(self):
        result = UtilFunctions().get_func_filename("sfdjlkfdsjlksfdjlk")
        

if __name__ == '__main__':
    unittest.main()