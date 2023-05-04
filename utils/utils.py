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

    def get_input_to_write(self, data: dict, option: str):
        if option == "input_a_0":
            data = {    
                        "option": option, 
                        "filename": data.get("input_a_0"), 
                        "data_target_type": data.get("input_a_1"), 
                        "data_target_key": data.get("input_a_2"),
                        "company_code": data.get("input_a_3"),
                        "enterprise_id": data.get("input_a_4"),
                        "server_id": data.get("input_a_5"),
                        "filter_type": data.get("input_a_6"),
                        "filter_value": data.get("input_a_7")
                    }
        elif option == "input_b_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_b_0"), 
                        "status": data.get("input_b_1"), 
                        "data_source_type": data.get("input_b_2"),
                        "data_source_key": data.get("input_b_3"),          
                        "company_code": data.get("input_b_4"),
                        "company_country_code": data.get("input_b_5"),
                        "company_country_name": data.get("input_b_6"),
                        "company_name": data.get("input_b_7"),
                        "data_provider": data.get("input_b_8"),
                        "enterprise_id": data.get("input_b_9"),
                        "server_id": data.get("input_b_10"),
                        "event_time": data.get("input_b_11"),
                        "event_type": data.get("input_b_12"),
                        "is_estimate": UtilFunctions().is_empty(data.get("input_b_13", "") ,"false"),
                        "attached_filename": data.get("input_b_14", "NO ATTACHED PDF DOCUMENT"),
                        "image_data": data.get("input_b_15", "NO ATTACHED PDF DOCUMENT"),
                        "document_type_code": data.get("input_b_16"),
                        "document_type_description": data.get("input_b_17"),
                        "document_id": data.get("input_b_18"),
                        "is_published": UtilFunctions().is_empty(data.get("input_b_19", "") ,"false"),
                        #"save_date_utc": data.get("input_b_20", ""),
                        "save_date_utc": str(datetime.utcnow()),
                        "document_saved_by_code": data.get("input_b_20"),
                        "document_saved_by_name": data.get("input_b_21")                  
                        }
        elif option == "input_c_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_c_0"), 
                        "data_target_type": data.get("input_c_1"), 
                        "data_target_key": data.get("input_c_2"),
                        "company_code": data.get("input_c_3"),
                        "enterprise_id": data.get("input_c_4"),
                        "server_id": data.get("input_c_5"),
                        "event_time": str(datetime.now()),
                        "event_type": data.get("input_c_6"),
                        "event_reference": data.get("input_c_7"),
                        "is_estimate": UtilFunctions().is_empty(data.get("input_c_8", "") ,"false"),
                    }
        elif option == "input_d_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_d_0"), 
                        "datatarget_type": data.get("input_d_1"),
                        "datatarget_key": data.get("input_d_2"),
                        "company_code": data.get("input_d_3"),
                        "enterprise_id": data.get("input_d_4"),
                        "server_id": data.get("input_d_5"),
                        "event_time": str(datetime.now()), 
                        "event_type": data.get("input_d_6"),
                        "event_reference": data.get("input_d_7"),
                        "is_estimate": UtilFunctions().is_empty(data.get("input_d_8", "") ,"false"),

                    }
        elif option == "input_e_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_e_0"), 
                        "datatarget_type": data.get("input_e_1"), 
                        "datatarget_key": data.get("input_e_2"),
                        "company_code": data.get("input_e_3"),
                        "enterprise_id": data.get("input_e_4"),
                        "server_id": data.get("input_e_5"),
                        "description": data.get("input_e_6"),
                        "iscustom_description": UtilFunctions().is_empty(data.get("input_e_7", "") ,"false"),
                        "notetext": data.get("input_e_8"),
                        "notecontext_code": data.get("input_e_9"),
                        "visibility_code": data.get("input_e_10"),
                        "address_type": data.get("input_e_11"),
                        "organization_code": data.get("input_e_12"),
                        "customizedfield_datatype": data.get("input_e_13"),
                        "customizedfield_key": data.get("input_e_14"),
                        "customizedfield_value": data.get("input_e_15")
                    } 
        elif option == "input_f_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_f_0"), 
                        "datatarget_type": data.get("input_f_1"), 
                        "datatarget_key": data.get("input_f_2"),
                        "company_code": data.get("input_f_3"),
                        "enterprise_id": data.get("input_f_4"),
                        "server_id": data.get("input_f_5"),
                        "transportbooking_direction_code": data.get("input_f_6"),
                        "transportbooking_direction_description": data.get("input_f_7"),
                        "address_type": data.get("input_f_8"),
                        "organization_code": data.get("input_f_9"),
                        "branch_code": data.get("input_f_10"),
                        "currency_code": data.get("input_f_11"),
                        "department_code": data.get("input_f_12"),
                        "chargeline_branch_code": data.get("input_f_13"),
                        "chargeline_chargecode_code": data.get("input_f_14"),
                        "chargeline_costlocal_amount": data.get("input_f_15"),
                        "chargeline_costos_amount": data.get("input_f_16"),
                        "chargeline_costoscurrency_code": data.get("input_f_17"),
                        "chargeline_costosgstvat_amount": data.get("input_f_18"),
                        "chargeline_creditor_type": data.get("input_f_19"),
                        "chargeline_creditor_key": data.get("input_f_20"),
                        "chargeline_department_code": data.get("input_f_21"),
                        "chargeline_display_sequence": data.get("input_f_22"),
                        "chargeline_importmetadata_instruction": data.get("input_f_23"),
                        "chargeline_supplierreference": data.get("input_f_24"),
                        "customizedfield_datatype": data.get("input_f_25"),
                        "customizedfield_key": data.get("input_f_26"),
                        "customizedfield_value": data.get("input_f_27")
                    }
        elif option == "input_g_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_g_0"), 
                        "datatarget_type": data.get("input_g_1"), 
                        "datatarget_key": data.get("input_g_2"),
                        "company_code": data.get("input_g_3"),
                        "enterprise_id": data.get("input_g_4"),
                        "server_id": data.get("input_g_5"),
                        "transport_bookingdirection_code": data.get("input_g_6"),
                        "transport_bookingdirection_description": data.get("input_g_7"),
                        "address_type": data.get("input_g_8"),
                        "organization_code": data.get("input_g_9"),
                        "branch_code": data.get("input_g_10"),
                        "currency_code": data.get("input_g_11"),
                        "department_code": data.get("input_g_12"),
                        "chargeline_branch_code": data.get("input_g_13"),
                        "chargeline_charge_code": data.get("input_g_14"),
                        "chargeline_costlocal_amount": data.get("input_g_15"),
                        "chargeline_costos_amount": data.get("input_g_16"),
                        "chargeline_costoscurrency_code": data.get("input_g_17"),
                        "chargeline_costosgstvat_amount": data.get("input_g_18"),
                        "chargeline_creditor_type": data.get("input_g_19"),
                        "chargeline_creditor_key": data.get("input_g_20"),
                        "chargeline_department_code": data.get("input_g_21"),
                        "chargeline_display_sequence": data.get("input_g_22"),
                        "chargeline_importmetadata_instruction": data.get("input_g_23"),
                        "chargeline_supplier_reference": data.get("input_g_24"),
                        "customizedfield_datatype": data.get("input_g_25"),
                        "customizedfield_key": data.get("input_g_26"),
                        "customizedfield_value": data.get("input_g_27")
                    }         
        elif option == "input_h_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_h_0"), 
                        "datatarget_type": data.get("input_h_1"), 
                        "datatarget_key": data.get("input_h_2"),
                        "company_code": data.get("input_h_3"),
                        "enterpriseid": data.get("input_h_4"),
                        "serverid": data.get("input_h_5"),
                        "description": data.get("input_h_6"),
                        "iscustom_description": UtilFunctions().is_empty(data.get("input_h_7", "") ,"false"),
                        "notetext": data.get("input_h_8"),
                        "notecontext_code": data.get("input_h_9"),
                        "visibility_code": data.get("input_h_10"),
                        "address_type": data.get("input_h_11"),
                        "organization_code": data.get("input_h_12"),
                        "customizedfield_datatype": data.get("input_h_13"),
                        "customized_field_key": data.get("input_h_14"),
                        "customized_field_value": data.get("input_h_15")
                    }
        elif option == "input_i_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_i_0"), 
                        "datatarget_type": data.get("input_i_1"), 
                        "datatarget_key": data.get("input_i_2"),
                        "company_code": data.get("input_i_3"),
                        "enterpriseid": data.get("input_i_4"),
                        "serverid": data.get("input_i_5"),
                        "transportbookingdirection_code": data.get("input_i_6"),
                        "transportbookingdirection_description": data.get("input_i_7"),
                        "addresstype": data.get("input_i_8"),
                        "organizationcode": data.get("input_i_9"),
                        "branch_code": data.get("input_i_10"),
                        "currency_code": data.get("input_i_11"),
                        "department_code": data.get("input_i_12"),
                        "chargeline_branch_code": data.get("input_i_13"),
                        "chargeline_chargecode_code": data.get("input_i_14"),
                        "chargeline_costlocalamount": data.get("input_i_15"),
                        "chargeline_costosamount": data.get("input_i_16"),
                        "chargeline_costoscurrency_code": data.get("input_i_17"),
                        "chargeline_costosgstvatamount": data.get("input_i_18"),
                        "chargeline_creditor_type": data.get("input_i_19"),
                        "chargeline_creditor_key": data.get("input_i_20"),
                        "chargeline_department_code": data.get("input_i_21"),
                        "chargeline_displaysequence": data.get("input_i_22"),
                        "chargeline_importmetadata_instruction": data.get("input_i_23"),
                        "chargeline_supplierreference": data.get("input_i_24")
                    }  
        elif option == "input_j_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_j_0"), 
                        "status": data.get("input_j_1"), 
                        "datasource_type": data.get("input_j_2"),
                        "datasource_key": data.get("input_j_3"),
                        "companycode": data.get("input_j_4"),
                        "companycountry_code": data.get("input_j_5"),
                        "companycountry_name": data.get("input_j_6"),
                        "company_name": data.get("input_j_7"),
                        "dataprovider": data.get("input_j_8"),
                        "enterpriseid": data.get("input_j_9"),
                        "serverid": data.get("input_j_10"),
                        "eventtime": str(datetime.now()),
                        "eventtype": data.get("input_j_11"),
                        "isestimate": UtilFunctions().is_empty(data.get("input_j_12", "") ,"false"),
                        "attacheddocument_filename": data.get("input_j_13"),
                        "imagedata": data.get("input_j_14"),
                        "type_code": data.get("input_j_15"),
                        "type_description": data.get("input_j_16"),
                        "documentid": data.get("input_j_17"),
                        "ispublished": UtilFunctions().is_empty(data.get("input_j_18", "") ,"false"),
                        "savedateutc": str(datetime.utcnow()),
                        "savedby_code": data.get("input_j_19"),
                        "savedby_name": data.get("input_j_20"),
                        "source_code": data.get("input_j_21"),
                        "source_description": data.get("input_j_22"),
                        "visible_branch_code": data.get("input_j_23"),               
                        "visible_company_code": data.get("input_j_24"),                   
                        "visible_department_code": data.get("input_j_25"),
                        "messagenumber": data.get("input_j_26")
                    }
        elif option == "input_k_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_k_0"), 
                        "datatarget_type": data.get("input_k_1"), 
                        "datatarget_key": data.get("input_k_2"),
                        "company_code": data.get("input_k_3"),
                        "enterpriseid": data.get("input_k_4"),
                        "serverid": data.get("input_k_5"),
                        "description": data.get("input_k_6"),
                        "iscustomdescription": UtilFunctions().is_empty(data.get("input_k_7", "") ,"false"),
                        "notetext": data.get("input_k_8"),
                        "notecontext_code": data.get("input_k_9"),
                        "visibility_code": data.get("input_k_10"),
                        "addresstype": data.get("input_k_11"),
                        "organizationcode": data.get("input_k_12"),
                        "customizedfield_datatype": data.get("input_k_13"),
                        "customizedfield_key": data.get("input_k_14"),
                        "customizedfield_value": data.get("input_k_15")
                    }
        elif option == "input_l_0":
            data = {
                        "option": option, 
                        "filename": data.get("input_l_0"), 
                        "datatarget_type": data.get("input_l_1"), 
                        "datatarget_key": data.get("input_l_2"),
                        "company_code": data.get("input_l_3"),
                        "enterpriseid": data.get("input_l_4"),
                        "serverid": data.get("input_l_5"),
                        "eventtime": str(datetime.now()),
                        "eventtype": data.get("input_l_6"),
                        "eventreference": data.get("input_l_7"),
                        "isestimate": UtilFunctions().is_empty(data.get("input_l_8", "") ,"false"),
                    }     
        return data
        


        
