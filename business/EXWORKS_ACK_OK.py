import xml.etree.ElementTree as ET

async def EXWORKS_ACK_OK_READ(file: str):
    
    root = ET.fromstring(file)
    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2012/11'}
    result = {}

    event_time = root.find('ns:Event/ns:EventTime', ns).text
    event_type = root.find('ns:Event/ns:EventType', ns).text
    event_reference = root.find('ns:Event/ns:EventReference', ns).text.strip('|')

    result['Event Time'] = event_time
    result['Event Type'] = event_type
    result['Event Reference'] = event_reference

    transport_booking_type = root.find('ns:Event/ns:DataContext/ns:DataTargetCollection/ns:DataTarget/ns:Type', ns).text
    transport_booking_key = root.find('ns:Event/ns:DataContext/ns:DataTargetCollection/ns:DataTarget/ns:Key', ns).text

    result['Data Target Type'] = transport_booking_type
    result['Data Target Key'] = transport_booking_key

    company_code = root.find('ns:Event/ns:DataContext/ns:Company/ns:Code', ns).text
    enterprise_id = root.find('ns:Event/ns:DataContext/ns:EnterpriseID', ns).text
    server_id = root.find('ns:Event/ns:DataContext/ns:ServerID', ns).text

    result['Company Code'] = company_code
    result['Enterprise ID'] = enterprise_id
    result['Server ID'] = server_id

    is_estimate = root.find('ns:Event/ns:IsEstimate', ns).text
    result['Is Estimate'] = is_estimate

    result = [{"col1": x, "col2": y} for x,y in result.items()]
    return result


async def ACK_OK_WRITE(file: str):
    root = ET.fromstring(file)

    ns = {'mw': 'http://www.cargowise.com/Schemas/Universal/2012/11'}

    result = {}

    Type = root.find('.//mw:Type', ns).text
    result['Type'] = Type

    key = root.find('.//mw:Key', ns).text
    result['Key'] = key

    code = root.find('.//mw:Code', ns).text
    result['Code'] = code

    enterpriseID = root.find('.//mw:EnterpriseID', ns).text
    result['Enterprise ID'] = enterpriseID

    serverID = root.find('.//mw:ServerID', ns).text
    result['Server ID'] = serverID

    eventTime = root.find('.//mw:EventTime', ns).text
    result['Event Time'] = eventTime

    eventType = root.find('.//mw:EventType', ns).text
    result['Event Type'] = eventType

    eventReference = root.find('.//mw:EventReference', ns).text
    result['Event Reference'] = eventReference

    isEstimate = root.find('.//mw:IsEstimate', ns).text
    result['Is Estimate'] = isEstimate

    return result
