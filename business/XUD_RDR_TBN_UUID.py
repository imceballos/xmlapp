import xml.etree.ElementTree as ET

async def XUD_RDR_TBN_UUID_READ(file: str):
    root = ET.fromstring(file)
    result = {}

    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2011/11'}

    Status=root.find('ns:Status', ns).text
    result['Status'] = Status

    Event = root.find('ns:Data/ns:UniversalEvent/ns:Event', ns)

    DataContext = Event.find('ns:DataContext', ns)

    DataSourceCollection = DataContext.find('ns:DataSourceCollection', ns)

    DataSource = DataContext.find('ns:DataSourceCollection/ns:DataSource', ns)

    DataSource_Type = DataSource.find('ns:Type', ns).text
    DataSource_Key = DataSource.find('ns:Key', ns).text
    result['DataSource_Type'] = DataSource_Type
    result['DataSource_Key'] = DataSource_Key

    Company = DataContext.find('ns:Company', ns)

    Company_Code = Company.find('ns:Code', ns).text
    result['CompanyCode'] = Company_Code

    Country = Company.find('ns:Country', ns).text

    Company_Country_Code = Company.find('ns:Country/ns:Code', ns).text
    Company_Country_Name = Company.find('ns:Country/ns:Name', ns).text
    result['Company_Country_Code'] = Company_Country_Code
    result['Company_Country_Name'] = Company_Country_Name

    Company_Name = Company.find('ns:Name', ns).text
    result['Company_Name'] = Company_Name

    DataProvider = DataContext .find('ns:DataProvider', ns).text
    result['DataProvider']= DataProvider

    EnterPriseID = DataContext.find('ns:EnterpriseID', ns).text
    result['EnterPriseID']= EnterPriseID

    ServerID = DataContext.find('ns:ServerID', ns).text
    result['ServerID']=ServerID

    EventTime = Event.find('ns:EventTime', ns).text
    result['EventTime']=EventTime

    EventType = Event.find('ns:EventType', ns).text
    result['EventType']= EventType

    IsEstimate = Event.find('ns:IsEstimate', ns).text
    result['IsEstimate']= IsEstimate

    AttachedDocumentCollection = Event.find('ns:AttachedDocumentCollection', ns)

    AttachedDocument = AttachedDocumentCollection.find('ns:AttachedDocument', ns)

    FileName = AttachedDocument.find('ns:FileName', ns).text
    result['FileName']= FileName

    ImageData = AttachedDocument.find('ns:ImageData', ns).text
    result['ImageData']=ImageData

    Type = AttachedDocument.find('ns:Type', ns)

    Type_Code = Type.find('ns:Code', ns).text
    Type_Description = Type.find('ns:Description', ns).text
    result['Type_Code']=Type_Code
    result['Type_Description']=Type_Description

    DocumentID = AttachedDocument.find('ns:DocumentID', ns).text
    result['DocumentID']= DocumentID

    IsPublished = AttachedDocument.find('ns:IsPublished', ns).text
    result['IsPublished']= IsPublished

    SaveDateUTC= AttachedDocument.find('ns:SaveDateUTC', ns).text
    result['SaveDateUTC']= SaveDateUTC

    SavedBy = AttachedDocument.find('ns:SavedBy', ns)

    SavedBy_Code = SavedBy.find('ns:Code', ns).text
    SavedBy_Name = SavedBy.find('ns:Name', ns).text
    result['SavedBy_Code']= SavedBy_Code
    result['SavedBy_Name']= SavedBy_Name

    MessageNumberCollection = root.find('ns:MessageNumberCollection', ns)

    MessageNumber = MessageNumberCollection.find('ns:MessageNumber', ns).text
    result['MessageNumber']= MessageNumber

    return

async def XUD_RDR_TBN_UUID_WRITE(data: dict):

    tree = ET.parse('xml_files/XUD_RDR_TBN_UUID.xml')
    root = tree.getroot()

    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2011/11'}

    Status=root.find('ns:Status', ns)
    Status.text = data.get('status', "")

    Event = root.find('ns:Data/ns:UniversalEvent/ns:Event', ns)

    DataContext = Event.find('ns:DataContext', ns)

    DataSourceCollection = DataContext.find('ns:DataSourceCollection', ns)

    DataSource = DataContext.find('ns:DataSourceCollection/ns:DataSource', ns)

    DataSource_Type = DataSource.find('ns:Type', ns)
    DataSource_Key = DataSource.find('ns:Key', ns)
    DataSource_Type.text = data.get('datasource_type', "")
    DataSource_Key.text = data.get('datasource_key', "")

    Company = DataContext.find('ns:Company', ns)

    Company_Code = Company.find('ns:Code', ns)
    Company_Code.text = data.get('company_code', "")

    Country = Company.find('ns:Country', ns)

    Company_Country_Code = Company.find('ns:Country/ns:Code', ns)
    Company_Country_Name = Company.find('ns:Country/ns:Name', ns)
    Company_Country_Code.text = data.get('company_country_code', "")
    Company_Country_Name.text = data.get('company_country_name', "")

    Company_Name = Company.find('ns:Name', ns)
    Company_Name.text = data.get('company_name', "")

    DataProvider = DataContext .find('ns:DataProvider', ns)
    DataProvider.text = data.get('dataprovider', "")

    EnterPriseID = DataContext.find('ns:EnterpriseID', ns)
    EnterPriseID.text = data.get('enterpriseid', "")

    ServerID = DataContext.find('ns:ServerID', ns)
    ServerID.text = data.get('serverid', "")

    EventTime = Event.find('ns:EventTime', ns)
    EventTime.text = data.get('eventtime', "")

    EventType = Event.find('ns:EventType', ns)
    EventType.text = data.get('eventtype', "")

    IsEstimate = Event.find('ns:IsEstimate', ns)
    IsEstimate.text = data.get('isestimate', "")

    AttachedDocumentCollection = Event.find('ns:AttachedDocumentCollection', ns)

    AttachedDocument = AttachedDocumentCollection.find('ns:AttachedDocument', ns)

    FileName = AttachedDocument.find('ns:FileName', ns)
    FileName.text = data.get('filename', "")

    ImageData = AttachedDocument.find('ns:ImageData', ns)
    ImageData.text = data.get('imagedata', "")

    Type = AttachedDocument.find('ns:Type', ns)

    Type_Code = Type.find('ns:Code', ns)
    Type_Description = Type.find('ns:Description', ns)
    Type_Code.text = data.get('type_code', "")
    Type_Description.text =data.get('type_description', "")

    DocumentID = AttachedDocument.find('ns:DocumentID', ns)
    DocumentID.text = data.get('documentid', "")

    IsPublished = AttachedDocument.find('ns:IsPublished', ns)
    IsPublished.text = data.get('ispublished', "")

    SaveDateUTC= AttachedDocument.find('ns:SaveDateUTC', ns)
    SaveDateUTC.text = data.get('savedateutc', "")

    SavedBy = AttachedDocument.find('ns:SavedBy', ns)

    SavedBy_Code = SavedBy.find('ns:Code', ns)
    SavedBy_Name = SavedBy.find('ns:Name', ns)
    SavedBy_Code.text = data.get('savedby_code', "")
    SavedBy_Name.text = data.get('savedby_name', "")

    MessageNumberCollection = root.find('ns:MessageNumberCollection', ns)

    MessageNumber = MessageNumberCollection.find('ns:MessageNumber', ns)
    MessageNumber.text = data.get('messagenumber', "")

    filename_xml = data.get("filename", "")
    file_path = f'test_files/trucker5_2231231312/acknowledge/pending/{filename_xml}'
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
