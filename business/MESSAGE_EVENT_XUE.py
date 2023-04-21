import xml.etree.ElementTree as ET


async def MESSAGE_EVENT_XUE_READ(file: str):
    """
    Take the XML file MESSAGE_EVENT_XUE.xml in string format, read it and return a dictionary with its field names as keys and its contents as values.
    """
    root = ET.fromstring(file)
    result = {}

    Event = root.find("Event")

    DataContext = Event.find("DataContext")

    DataTargetCollection = DataContext.find("DataTargetCollection")

    DataTarget = DataTargetCollection.find("DataTarget")

    DataTarget_Type = DataTarget.find("Type").text
    DataTarget_Key = DataTarget.find("Key").text
    result["DataTarget_Type"] = DataTarget_Type
    result["DataTarget_Key"] = DataTarget_Key

    Company = DataContext.find("Company")

    Company_Code = Company.find("Code").text
    result["Company_Code"] = Company_Code

    EnterpriseID = DataContext.find("EnterpriseID").text
    result["EnterpriseID"] = EnterpriseID

    ServerID = DataContext.find("ServerID").text
    result["ServerID"] = ServerID

    EventTime = Event.find("EventTime").text
    result["EventTime"] = EventTime

    EventType = Event.find("EventType").text
    result["EventType"] = EventType

    EventReference = Event.find("EventReference").text
    result["EventReference"] = EventReference

    IsEstimate = Event.find("IsEstimate").text
    result["IsEstimate"] = IsEstimate

    result = [{"col1": x, "col2": y} for x, y in result.items()]
    return result


async def MESSAGE_EVENT_XUE_WRITE(data: dict):
    """
    Take a dictionary and create an XML file with its information using the format of the XML file MESSAGE_EVENT_XUE.xml.
    """
    tree = ET.parse("xml_files/")
    root = tree.getroot()

    Event = root.find("Event")

    DataContext = Event.find("DataContext")

    DataTargetCollection = DataContext.find("DataTargetCollection")

    DataTarget = DataTargetCollection.find("DataTarget")

    DataTarget_Type = DataTarget.find("Type")
    DataTarget_Key = DataTarget.find("Key")
    DataTarget_Type.text = data.get("datatarget_type", "")
    DataTarget_Key.text = data.get("datatarget_key", "")

    Company = DataContext.find("Company")

    Company_Code = Company.find("Code")
    Company_Code.text = data.get("company_code", "")

    EnterpriseID = DataContext.find("EnterpriseID")
    EnterpriseID.text = data.get("enterpriseid", "")

    ServerID = DataContext.find("ServerID")
    ServerID.text = data.get("serverid", "")

    EventTime = Event.find("EventTime")
    EventTime.text = data.get("eventtime", "")

    EventType = Event.find("EventType")
    EventType.text = data.get("eventtype", "")

    EventReference = Event.find("EventReference")
    EventReference.text = data.get("eventreference", "")

    IsEstimate = Event.find("IsEstimate")
    IsEstimate.text = data.get("isestimate", "")

    filename_xml = data.get("filename", "")
    file_path = f"test_files\{filename_xml}"
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
