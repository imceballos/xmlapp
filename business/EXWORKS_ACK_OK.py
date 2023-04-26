import xml.etree.ElementTree as ET


async def EXWORKS_ACK_OK_READ(file: str):
    """
    Take the XML file EXWORKS_ACK_OK.xml in string format, read it and return a dictionary with its field names as keys and its contents as values.
    """
    root = ET.fromstring(file)
    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2012/11"}
    result = {}

    event_time = root.find("ns:Event/ns:EventTime", ns).text
    event_type = root.find("ns:Event/ns:EventType", ns).text
    event_reference = root.find("ns:Event/ns:EventReference", ns).text

    result["Event_Time"] = event_time
    result["Event_Type"] = event_type
    result["EventReference"] = event_reference

    datatarget_type = root.find(
        "ns:Event/ns:DataContext/ns:DataTargetCollection/ns:DataTarget/ns:Type",
        ns,
    ).text
    datatarget_key = root.find(
        "ns:Event/ns:DataContext/ns:DataTargetCollection/ns:DataTarget/ns:Key",
        ns,
    ).text

    result["DataTarget_Type"] = datatarget_type
    result["DataTarget_Key"] = datatarget_key

    company_code = root.find(
        "ns:Event/ns:DataContext/ns:Company/ns:Code", ns
    ).text
    enterprise_id = root.find(
        "ns:Event/ns:DataContext/ns:EnterpriseID", ns
    ).text
    server_id = root.find("ns:Event/ns:DataContext/ns:ServerID", ns).text

    result["Company_Code"] = company_code
    result["Enterprise_ID"] = enterprise_id
    result["Server_ID"] = server_id

    is_estimate = root.find("ns:Event/ns:IsEstimate", ns).text
    result["Is_Estimate"] = is_estimate

    result = [{"col1": x, "col2": y} for x, y in result.items()]
    return result


async def EXWORKS_ACK_OK_WRITE(data: dict, folder_path: str):
    """
    Take a dictionary and create an XML file with its information using the format of the XML file EXWORKS_ACK_OK.xml.
    """   
    tree = ET.parse("xml_files/EXWORKS_ACK_OK.xml")
    root = tree.getroot()
    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2012/11"}

    ET.register_namespace(
        "", "http://www.cargowise.com/Schemas/Universal/2012/11"
    )

    datatarget_type = root.find(
        "ns:Event/ns:DataContext/ns:DataTargetCollection/ns:DataTarget/ns:Type",
        ns,
    )
    datatarget_key = root.find(
        "ns:Event/ns:DataContext/ns:DataTargetCollection/ns:DataTarget/ns:Key",
        ns,
    )

    datatarget_type.text = data.get("datatarget_type", "")
    datatarget_key.text = data.get("datatarget_key", "")

    company_code = root.find(
        "ns:Event/ns:DataContext/ns:Company/ns:Code", ns
    )
    enterprise_id = root.find(
        "ns:Event/ns:DataContext/ns:EnterpriseID", ns
    )
    server_id = root.find("ns:Event/ns:DataContext/ns:ServerID", ns)

    company_code.text = data.get("company_code", "")
    enterprise_id.text = data.get("enterprise_id", "")
    server_id.text = data.get("server_id", "")

    event_time = root.find("ns:Event/ns:EventTime", ns)
    event_type = root.find("ns:Event/ns:EventType", ns)
    event_reference = root.find("ns:Event/ns:EventReference", ns)

    event_time.text = data.get("event_time", "")
    event_type.text = data.get("event_type", "")
    event_reference.text = data.get("event_reference", "")

    is_estimate = root.find("ns:Event/ns:IsEstimate", ns)
    is_estimate.text = data.get("is_estimate", "")

    filename_xml = data.get("filename", "")
    file_path = f'{folder_path}/acknowledge/pending/{filename_xml}'
    tree.write(file_path, encoding="utf-8", xml_declaration=True)