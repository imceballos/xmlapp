import re
import os
from datetime import datetime
from typing import List
from .encrypt import encode_to_base64

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
        if folder_path.split("/")[-1] == "all_files":
            folder_path = folder_path[:-9]
            return self.get_all_files(folder_path, condition)
        return [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/{condition}", file)), "folder": encoded_text} for file in os.listdir(f"{folder_path}/{condition}")]
    
    def create_directory(self, folder_name: str):
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

    def create_subdirectories(self, main_folder: str, dir_names: List):
        self.create_directory(main_folder)
        for subfolder in dir_names:
            self.create_directory(f"{main_folder}/{subfolder}")

    def delete_directory(self, folder_name: str):
        if os.path.isdir(folder_name):
            os.remove(folder_name)
    
    def list_directory(self, folder_name: str, str_end: str = None):
        if os.path.isdir(folder_name):
            if str_end:
                return [f for f in os.listdir(folder_name) if f.endswith(str_end)]
            return [f for f in os.listdir(folder_name)]
            
    def get_all_files(self, folder_path, cond):
        folders = [os.path.join(folder_path,folder) for folder in os.listdir(folder_path)]
        element_cond = [self.get_files_directory(subpath, cond) for subpath in folders]
        file_sizes = {}

        for file_list in element_cond:
            for file_data in file_list:
                file_name = file_data['name']
                file_size = {'size': file_data['size'], 'folder': file_data['folder']}
                if file_name not in file_sizes or file_sizes[file_name]['size'] < file_size['size']:
                    file_sizes[file_name] = file_size

        max_size_files = [{'name': file_name, 'size': file_size['size'], 'folder': file_size['folder']} for file_name, file_size in file_sizes.items()]
        return max_size_files

    def get_files_directory(self, folder_path, cond):
        elements = set(os.listdir(os.path.join(folder_path, cond)))
        return [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/{cond}", file)), "folder": encode_to_base64(f"{folder_path}/")} for file in os.listdir(f"{folder_path}/{cond}")]
        #return set(os.listdir(os.path.join(folder_path, cond)))
    
    def is_empty(self, get_in, get_out):
        if get_in == None:
            return get_out
        elif get_in == "":
            return get_out
        elif len(get_in)==0:
            return get_out
        else:
            return get_in


    def replace_path(self, file_path, replacement):
        path_parts = file_path.split("/")
        new_path_parts = path_parts[:-2] + [replacement] + [path_parts[-1]]
        return "/".join(new_path_parts)
