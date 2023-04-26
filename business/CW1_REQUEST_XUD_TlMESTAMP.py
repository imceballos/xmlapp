import xml.etree.ElementTree as ET


async def CW1_REQUEST_XUD_TIMESTAMP_READ(file: str):
    """
    Take the XML file CW1_REQUEST_XUD_TIMESTAMP.xml in string format, read it and return a dictionary with its field names as keys and its contents as values.
    """
    root = ET.fromstring(file)
    result = {}

    data_target = root.find(
        "DocumentRequest/DataContext/DataTargetCollection/DataTarget"
    )
    data_target_type = data_target.find("Type").text
    data_target_key = data_target.find("Key").text

    result["Data Target Type"] = data_target_type
    result["Data Target Key"] = data_target_key

    company_code = root.find("DocumentRequest/DataContext/Company/Code").text
    result["Company code"] = company_code

    filter_type = root.find("DocumentRequest/FilterCollection/Filter/Type").text
    filter_value = root.find(
        "DocumentRequest/FilterCollection/Filter/Value"
    ).text

    result["Filter Type"] = filter_type
    result["Filter Value"] = filter_value

    enterprise_id = root.find("DocumentRequest/DataContext/EnterpriseID").text
    server_id = root.find("DocumentRequest/DataContext/ServerID").text

    result["Enterprise ID"] = enterprise_id
    result["Server ID"] = server_id

    result = [{"col1": x, "col2": y} for x, y in result.items()]

    return result


async def CW1_REQUEST_XUD_TIMESTAMP_WRITE(data: dict, folder_path: str):
    """
    Take a dictionary and create an XML file with its information using the format of the XML file CW1_REQUEST_XUD_TIMESTAMP.xml.
    """
    tree = ET.parse("xml_files/CW1_REQUEST_XUD_TIMESTAMP.xml")
    root = tree.getroot()

    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    ET.register_namespace(
        "", "http://www.cargowise.com/Schemas/Universal/2011/11"
    )

    data_target = root.find(
        "DocumentRequest/DataContext/DataTargetCollection/DataTarget"
    )
    data_target_type = data_target.find("Type")
    data_target_key = data_target.find("Key")

    data_target_type.text = data.get("data_target_type", "")
    data_target_key.text = data.get("data_target_key", "")

    company_code = root.find("DocumentRequest/DataContext/Company/Code")
    company_code.text = data.get("company_code", "")

    enterprise_id = root.find("DocumentRequest/DataContext/EnterpriseID")
    server_id = root.find("DocumentRequest/DataContext/ServerID")

    enterprise_id.text = data.get("enterprise_id", "")
    server_id.text = data.get("server_id", "")

    filter_type = root.find("DocumentRequest/FilterCollection/Filter/Type")
    filter_value = root.find("DocumentRequest/FilterCollection/Filter/Value")

    filter_type.text = data.get("filter_type", "")
    filter_value.text = data.get("filter_value", "")

    filename_xml = data.get("filename", "")
    file_path = f'{folder_path}/acknowledge/pending/{filename_xml}'
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
