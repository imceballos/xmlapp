import xml.etree.ElementTree as ET

async def MESSAGE_EVENT_XUE_READ(file: str):

    root = ET.fromstring(file)
    result = {}

    Event =root.find('Event')

    DataContext = Event.find('DataContext')

    DataTargetCollection = DataContext.find('DataTargetCollection')

    DataTarget = DataTargetCollection.find('DataTarget')

    DataTarget_Type = DataTarget.find('Type').text
    DataTarget_Key = DataTarget.find('Key').text
    result['DataTarget_Type'] = DataTarget_Type
    result['DataTarget_Key'] = DataTarget_Key

    Company = DataContext.find('Company')

    Company_Code = Company.find('Code').text
    result['Company_Code'] = Company_Code

    EnterpriseID = DataContext.find('EnterpriseID').text
    result['EnterpriseID'] = EnterpriseID

    ServerID = DataContext.find('ServerID').text
    result['ServerID'] = ServerID

    EventTime = Event.find('EventTime').text
    result['EventTime'] = EventTime

    EventType = Event.find('EventType').text
    result['EventType'] = EventType

    EventReference = Event.find('EventReference').text
    result['EventReference'] = EventReference

    IsEstimate = Event.find('IsEstimate').text
    result['IsEstimate'] = IsEstimate

    result = [{"col1": x, "col2": y} for x,y in result.items()]
    return result