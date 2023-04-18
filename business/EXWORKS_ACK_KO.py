import xml.etree.ElementTree as ET

async def EXWORKS_ACK_KO_READ(file: str):

    root = ET.fromstring(file)
    result = {}

    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2012/11'}

    Event =root.find('ns:Event', ns)

    DataContext = Event.find('ns:DataContext', ns)

    DataTargetCollection = DataContext.find('ns:DataTargetCollection', ns)

    DataTarget = DataTargetCollection.find('ns:DataTarget', ns)

    DataTarget_Type = DataTarget.find('ns:Type', ns).text
    DataTarget_Key = DataTarget.find('ns:Key', ns).text
    result['Data Target_Type']=DataTarget_Type
    result['Data Target_Key']=DataTarget_Key

    Company = DataContext.find('ns:Company', ns)

    Company_Code = Company.find('ns:Code', ns).text
    result['Company_Code']=Company_Code

    EnterPriseID = DataContext.find('ns:EnterpriseID', ns).text
    result['EnterpriseID']=EnterPriseID

    ServerID = DataContext.find('ns:ServerID', ns).text
    result['ServerID']=ServerID

    EventTime = Event.find('ns:EventTime', ns).text
    result['EventTime']=EventTime

    EventType = Event.find('ns:EventType', ns).text
    result['EventType']=EventType

    EventReference = Event.find('ns:EventReference', ns).text
    result['EventReference']=EventReference

    IsEstimate = Event.find('ns:IsEstimate', ns).text
    result['IsEstimate']=IsEstimate

    result = [{"col1": x, "col2": y} for x,y in result.items()]

    return result

async def UPDATE_MESSAGE_REJECTED_WRITE(data: dict):

    tree = ET.parse('xml_files/EXWORKS_Message_Event_XUE_ACK_KO.xml')
    root = tree.getroot()
    data={}
    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2012/11'}

    ET.register_namespace("", "http://www.cargowise.com/Schemas/Universal/2012/11")

    #-------------------------------------------------------------------------------------------------------------

    Event =root.find('ns:Event', ns)

    #-------------------------------------------------------------------------------------------------------------

    DataContext = Event.find('ns:DataContext', ns)
    DataTargetCollection = DataContext.find('ns:DataTargetCollection', ns)
    DataTarget = DataTargetCollection.find('ns:DataTarget', ns)
    DataTarget_Type = DataTarget.find('ns:Type', ns)
    DataTarget_Key = DataTarget.find('ns:Key', ns)
    DataTarget_Type.text = data.get('datatarget_type', "" )
    DataTarget_Key.text = data.get('datatarget_key', "" )            

    Company = DataContext.find('ns:Company', ns)
    Company_Code = Company.find('ns:Code', ns)
    Company_Code.text = data.get('company_code', "" )

    EnterpriseID = DataContext.find('ns:EnterpriseID', ns)
    EnterpriseID.text = data.get('enterpriseid', "" )

    ServerID = DataContext.find('ns:ServerID', ns)
    ServerID.text = data.get('serverid,' "" )

    #-------------------------------------------------------------------------------------------------------------

    EventTime = Event.find('ns:EventTime', ns)
    EventTime.text = data.get('eventtime', "" )

    #-------------------------------------------------------------------------------------------------------------

    EventType = Event.find('ns:EventType', ns)
    EventType.text = data.get('eventtype', "" )

    #-------------------------------------------------------------------------------------------------------------

    EventReference = Event.find('ns:EventReference', ns)
    EventReference.text = data.get('eventreference', "" )

    #-------------------------------------------------------------------------------------------------------------

    IsEstimate = Event.find('ns:IsEstimate', ns)
    IsEstimate.text = data.get('isestimate', "" )

    #-------------------------------------------------------------------------------------------------------------

    filename_xml = data.get("filename", "")
    file_path = f'test_files\{filename_xml}'
    tree.write(file_path, encoding='utf-8', xml_declaration=True)