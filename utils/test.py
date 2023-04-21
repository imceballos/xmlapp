"""Unit tests for Avicena Patient Mapper."""

import unittest
from utils import UtilFunctions
from encrypt import decode_from_base64, encode_to_base64

class Testing(unittest.TestCase):
    """Unit tests"""

    #-----get_file_info--------------------------------------------------------
    def test_get_file_info_one(self):
        output = {'filename': 'utils.py', 'size': 4057, 'creation_date': '2023-04-03 23:19:16'}
        result = UtilFunctions().get_file_info("utils.py")
        self.assertEqual(result, output)
    #--------------------------------------------------------------------------

    #def test_map_two(self):
    #    output = {'filename': 'utils.py', 'size': 4057, 'creation_date': '2023-04-03 23:19:16'}
    #    result = UtilFunctions().get_file_info("settings.py")
    #    self.assertEqual(result, output)

    #-----get_func_filename---------------------------------------------------
    def test_get_func_filename_one(self):
        output =
        result = UtilFunctions().get_func_filename()
        self.assertEqual(result, output)
    
    def test_get_func_filename_two(self):
        output = 
        result = UtilFunctions().get_func_filename()
        self.assertEqual(result, output)
    
    def test_get_func_filename_three(self):
        output = 
        result = UtilFunctions().get_func_filename()
        self.assertEqual(result, output)
    #--------------------------------------------------------------------------

    #-----get_write_fun_filename-----------------------------------------------
    def test_get_write_func_filename_one(self):
        output = "CW1_REQUEST_XUD_TIMESTAMP_WRITE"
        result = UtilFunctions().get_write_func_filename("input_b_0")
        self.assertEqual(result, output)

    def test_get_write_func_filename_two(self):
        output = "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_WRITE"
        result = UtilFunctions().get_write_func_filename("input_a_0")
        self.assertEqual(result, output)
    #--------------------------------------------------------------------------

    #-----get_list_directory---------------------------------------------------
    def test_list_directory(self):
        output =
        result = UtilFunctions().list_directory( , ):
        self.assertEqual(result, output)
    #--------------------------------------------------------------------------

    #-----get_decode_from_base64-----------------------------------------------
    def test_decode_from_base64(self):
        output = 
        result = decode_from_base64()
        self.assertEqual(result, output)
    #--------------------------------------------------------------------------

    #-----get_encode_to_base64-------------------------------------------------
    def test_encode_to_base64(self):
        output =
        result = encode_to_base64()
        self.assertEqual(result, output)
    #--------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()