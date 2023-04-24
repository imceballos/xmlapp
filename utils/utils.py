import re
import os
from datetime import datetime
from typing import List

class UtilFunctions:

    def get_file_info(self, filepath: str) -> dict:
        """
        Given a filepath, return the filename, size, and creation date of the file
        """
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        creation_date = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        return {"filename": filename, "size": size, "creation_date": creation_date}

    def get_func_filename(self, filepath: str) -> str:
        """
        Get a string as input (filepath) and returns another string as output.
        If the string contains the pattern "MESSAGE_XUD_DTYPE",  
        returns "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_READ". If contains the pattern "CW1" 
        returns the string "CW1_REQUEST_XUD_TIMESTAMP_READ"
        """
        if any(filepath.endswith(ext) for ext in ('.jpg', '.png')):
            return "JPG_READ"
        elif filepath.endswith('.pdf'):
            return "PDF_READ"
        elif filepath.endswith('.txt'):
            return "TXT_READ"
        elif re.search(r'MESSAGE_XUD_DTYPE', filepath):
            return "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_READ"
        elif re.search(r'CW1', filepath):
            return "CW1_REQUEST_XUD_TIMESTAMP_READ"
        elif re.search(r'EXWORKS_ACK_OK', filepath):
            return "EXWORKS_ACK_OK_READ"
        elif re.search(r'EXWORKS_ACK_KO', filepath):
            return "EXWORKS_ACK_KO_READ"
        elif re.search(r'TBM_DOC_CIV', filepath):
            return "TBM_DOC_CIV_UUID_READ"
        elif re.search(r'UPDATE_MESSAGE_ACCEPTED', filepath):
            return "UPDATE_MESSAGE_ACCEPTED_READ"
        elif re.search(r'XUD_RDR_TBN_UUID', filepath):
            return "XUD_RDR_TBN_UUID_READ"
        elif re.search(r'UPDATE_MESSAGE_REJECTED', filepath):
            return "UPDATE_MESSAGE_REJECTED_READ"
        elif re.search(r'UPDATE_MESSAGE_PAYABLE_UPDATE', filepath):
            return "UPDATE_MESSAGE_PAYABLE_UPDATE_READ"
        elif re.search(r'UPDATE_MESSAGE_ALLOCATED', filepath):
            return "UPDATE_MESSAGE_ALLOCATED_READ"
        elif re.search(r'UPDATE_MESSAGE_ACCRUALS', filepath):
            return "UPDATE_MESSAGE_ACCRUALS_READ"
        elif re.search(r'UPDATE_MESSAGE_ACCRUALS_ACCEPTED', filepath):
            return "UPDATE_MESSAGE_ACCRUALS_ACCEPTED_READ"
        elif re.search(r'MESSAGE_EVENT_XUE', filepath):
            return "MESSAGE_EVENT_XUE_READ"

    def get_write_func_filename(self, option: str) -> str:
        """
        Given a string as input (option), returns another string as output according to the dictionary
        """
        mapper = {
            "input_a_0": "CW1_REQUEST_XUD_TIMESTAMP_WRITE",
            "input_b_0": "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_WRITE",
			"input_c_0": "EXWORKS_ACK_KO_WRITE",
			"input_d_0": "EXWORKS_ACK_OK_WRITE",
			"input_e_0": "UPDATE_MESSAGE_ACCEPTED_WRITE",
			"input_f_0": "UPDATE_MESSAGE_ACCRUALS_ACCEPTED_WRITE",
			"input_g_0": "UPDATE_MESSAGE_ACCRUALS_WRITE",
            "input_h_0": "UPDATE_MESSAGE_ALLOCATED_WRITE",
            "input_i_0": "UPDATE_MESSAGE_PAYABLE_UPDATE_WRITE",
            "input_j_0": "XUD_RDR_TBN_UUID_WRITE",
            "input_k_0": "UPDATE_MESSAGE_REJECTED_WRITE",
            "input_l_0": "MESSAGE_EVENT_XUE_WRITE"
        }
        return mapper.get(option, "")

    def get_files_by_condition(self, folder_path: str, encoded_text: str, condition: str):
        listed_files = [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/{condition}", file)), "folder": encoded_text} for file in os.listdir(f"{folder_path}/{condition}")]
        return listed_files
    
    def create_directory(self, folder_name: str):
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

    def create_subdirectories(self, main_folder: str, dir_names: List):
        self.create_directory(main_folder)
        for subfolder in dir_names:
            self.create_directory(f"{main_folder}/{subfolder}")
            self.create_directory(f"{main_folder}/{subfolder}/accepted")
            self.create_directory(f"{main_folder}/{subfolder}/rejected")
            self.create_directory(f"{main_folder}/{subfolder}/pending")

    def delete_directory(self, folder_name: str):
        if os.path.isdir(folder_name):
            os.remove(folder_name)
    
    def list_directory(self, folder_name: str, str_end: str = None):
        if os.path.isdir(folder_name):
            if str_end:
                return [f for f in os.listdir(folder_name) if f.endswith(str_end)]
            return [f for f in os.listdir(folder_name)]
            
