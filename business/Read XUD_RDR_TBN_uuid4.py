import xml.etree.ElementTree as ET


async def Read_XUD_RDR_TBN_uuid4 (file: str):
    root = ET.fromstring(file)
    result = {}

    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2011/11'}

#get the value of the Status element
    Status=root.find('ns:Status', ns).text
    result['Status'] = Status

#-------------------------------------------------------------------------------------------------------------

#get the elements of the Data/UniversalEvent/Event
    Event = root.find('ns:Data/ns:UniversalEvent/ns:Event', ns)

#-------------------------------------------------------------------------------------------------------------

#get the elements of the DataContext
    DataContext = Event.find('ns:DataContext', ns)

#get the elements of the DataSourceCollection
    DataSourceCollection = DataContext.find('ns:DataSourceCollection', ns)

#get the elements of the DataSource
    DataSource = DataContext.find('ns:DataSourceCollection/ns:DataSource', ns)

#get the value of the Type and Key element
    DataSource_Type = DataSource.find('ns:Type', ns).text
    DataSource_Key = DataSource.find('ns:Key', ns).text
    result['DataSource_Type'] = DataSource_Type
    result['DataSource_Key'] = DataSource_Key

#get the elements of the Company
    Company = DataContext.find('ns:Company', ns)

#get the value of Code
    Company_Code = Company.find('ns:Code', ns).text
    result['CompanyCode'] = Company_Code

#get the elements of Country
    Country = Company.find('ns:Country', ns).text

#get the values of the elements Code and Name
    Company_Country_Code = Company.find('ns:Country/ns:Code', ns).text
    Company_Country_Name = Company.find('ns:Country/ns:Name', ns).text
    result['Company_Country_Code'] = Company_Country_Code
    result['Company_Country_Name'] = Company_Country_Name

#get the value of Name
    Company_Name = Company.find('ns:Name', ns).text
    result['Company_Name'] = Company_Name

#get the value of the DataProvider
    DataProvider = DataContext .find('ns:DataProvider', ns).text
    result['DataProvider']= DataProvider

#get the value of the EnterpriseID
    EnterPriseID = DataContext.find('ns:EnterpriseID', ns).text
    result['EnterPriseID']= EnterPriseID

#get the value of the ServerID
    ServerID = DataContext.find('ns:ServerID', ns).text
    result['ServerID']=ServerID

#-------------------------------------------------------------------------------------------------------------

#get the value of the EventTime
    EventTime = Event.find('ns:EventTime', ns).text
    result['EventTime']=EventTime

#-------------------------------------------------------------------------------------------------------------

#get the value of the EventType
    EventType = Event.find('ns:EventType', ns).text
    result['EventType']= EventType

#-------------------------------------------------------------------------------------------------------------

#get the value of the IsEstimate
    IsEstimate = Event.find('ns:IsEstimate', ns).text
    result['IsEstimate']= IsEstimate

#-------------------------------------------------------------------------------------------------------------

#get de elements of AttachedDocumentCollection
    AttachedDocumentCollection = Event.find('ns:AttachedDocumentCollection', ns)

#get de elements of AttachedDocument
    AttachedDocument = AttachedDocumentCollection.find('ns:AttachedDocument', ns)

#get the value of the element FileName
    FileName = AttachedDocument.find('ns:FileName', ns).text
    result['FileName']= FileName

#get the value of the element ImageData
    ImageData = AttachedDocument.find('ns:ImageData', ns).text
    result['ImageData']=ImageData

#get de elements of Type
    Type = AttachedDocument.find('ns:Type', ns)

#get the value of the elements Type and Description
    Type_Code = Type.find('ns:Code', ns).text
    Type_Description = Type.find('ns:Description', ns).text
    result['Type_Code']=Type_Code
    result['Type_Description']=Type_Description

#get the value of the element DocumentID
    DocumentID = AttachedDocument.find('ns:DocumentID', ns).text
    result['DocumentID']= DocumentID

#get the value of the element IsPublished
    IsPublished = AttachedDocument.find('ns:IsPublished', ns).text
    result['IsPublished']= IsPublished

#get the value of the element SaveDateUTC
    SaveDateUTC= AttachedDocument.find('ns:SaveDateUTC', ns).text
    result['SaveDateUTC']= SaveDateUTC

#get the elements of SavedBy
    SavedBy = AttachedDocument.find('ns:SavedBy', ns)

#get the value of the element Code and Name
    SavedBy_Code = SavedBy.find('ns:Code', ns).text
    SavedBy_Name = SavedBy.find('ns:Name', ns).text
    result['SavedBy_Code']= SavedBy_Code
    result['SavedBy_Name']= SavedBy_Name

    #get the elements of the MessageNumberCollection
    MessageNumberCollection = root.find('ns:MessageNumberCollection', ns)

    #get the value of the element MessageNumber
    MessageNumber = MessageNumberCollection.find('ns:MessageNumber', ns).text
    result['MessageNumber']= MessageNumber

    return

"""

get de elements of AttachedDocument
AttachedDocument = AttachedDocumentCollection.find('ns:AttachedDocument', ns)

get the value of the element FileName
FileName = AttachedDocument.find('ns:FileName', ns).text
result['File Name 2']= FileName

get the value of the element ImageData
ImageData = AttachedDocument.find('ns:ImageData', ns).text
result['Image Data 2']=ImageData

get de elements of Type
Type = AttachedDocument.find('ns:Type', ns)

get the value of the elements Type and Description
Type_Code = Type.find('ns:Code', ns).text
Type_Description = Type.find('ns:Description', ns).text
result['Type_Code 2']=Type_Code
result['Type_Description 2']=Type_Description

get the value of the element DocumentID
DocumentID = AttachedDocument.find('ns:DocumentID', ns).text
result['DocumentID 2']= DocumentID

get the value of the element IsPublished
IsPublished = AttachedDocument.find('ns:IsPublished', ns).text
result['Is Published 2']= IsPublished

get the value of the element SaveDateUTC
SaveDateUTC= AttachedDocument.find('ns:SaveDateUTC', ns).text
result['Save Date UTC 2']= SaveDateUTC

get the elementS of SavedBy
SavedBy = AttachedDocument.find('ns:SavedBy', ns)

get the value of the element Code and Name
SavedBy_Code = SavedBy.find('ns:Code', ns).text
SavedBy_Name = SavedBy.find('ns:Name', ns).text
result['SavedBy_Code 2']= SavedBy_Code
result['SavedBy_Name 2']= SavedBy_Name
"""

#-------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------