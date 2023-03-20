import xml.etree.ElementTree as ET

async def CW1_REQUEST_XUD_TIMESTAMP_READ(file: str):

    root = ET.fromstring(file)
    result = {}

    data_target = root.find('DocumentRequest/DataContext/DataTargetCollection/DataTarget')
    data_target_type = data_target.find('Type').text
    data_target_key = data_target.find('Key').text

    result['Data Target Type'] = data_target_type 
    result['Data Target Key'] = data_target_key

    company_code = root.find('DocumentRequest/DataContext/Company/Code').text
    result['Company code'] = company_code

    filter_type = root.find('DocumentRequest/FilterCollection/Filter/Type').text
    filter_value = root.find('DocumentRequest/FilterCollection/Filter/Value').text

    result['Filter Type'] = filter_type
    result['Filter Value'] = filter_value

    enterprise_id = root.find('DocumentRequest/DataContext/EnterpriseID').text
    server_id = root.find('DocumentRequest/DataContext/ServerID').text

    result['Enterprise ID'] = enterprise_id
    result['Server ID'] = server_id

    result = [{"col1": x, "col2": y} for x,y in result.items()]

    return result