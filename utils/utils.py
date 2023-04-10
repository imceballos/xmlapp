import re
import os
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
        if re.search(r'MESSAGE_XUD_DTYPE', filepath):
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
        print("OPTION", option)
        """
        Given a string as input (option), returns another string as output according to the dictionary
        """
        mapper = {
            "input_b_0": "CW1_REQUEST_XUD_TIMESTAMP_WRITE",
            "input_a_0": "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_WRITE"

        }
        return mapper.get(option, "")

    def get_files_by_condition(self, folder_path: str, encoded_text: str, condition: str):
        listed_files = [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/{condition}", file)), "folder": encoded_text} for file in os.listdir(f"{folder_path}/{condition}")]
        return listed_files
    
    def create_directory(self, folder_name: str):
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

    def create_subdirectories(self, main_folder: str, dir_names: List):
        create_directory(main_folder)
        for subfolder in dir_names:
            create_directory(f"{main_folder}/{subfolder}")
            create_directory(f"{main_folder}/{subfolder}/accepted")
            create_directory(f"{main_folder}/{subfolder}/rejected")
            create_directory(f"{main_folder}/{subfolder}/pending")

    def delete_directory(self, folder_name: str):
        if os.path.isdir(folder_name):
            os.remove(folder_name)
    
    def list_directory(self, folder_name: str, str_end: str = None):
        if os.path.isdir(folder_name):
            if str_end:
                return [f for f in os.listdir(folder_name) if f.endswith(str_end)]
            return [f for f in os.listdir(folder_name)]
            
