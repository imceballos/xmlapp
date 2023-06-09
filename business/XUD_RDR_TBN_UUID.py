import xml.etree.ElementTree as ET


async def XUD_RDR_TBN_UUID_READ(file: str):
    """
    Take the XML file XUD_RDR_TBN_UUID.xml in string format, read it and return a dictionary with its field names as keys and its contents as values.
    """
    root = ET.fromstring(file)
    result = {}

    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    Status = root.find("ns:Status", ns).text
    result["Status"] = Status

    Event = root.find("ns:Data/ns:UniversalEvent/ns:Event", ns)

    DataContext = Event.find("ns:DataContext", ns)

    DataSourceCollection = DataContext.find("ns:DataSourceCollection", ns)

    DataSource = DataContext.find("ns:DataSourceCollection/ns:DataSource", ns)

    DataSource_Type = DataSource.find("ns:Type", ns).text
    DataSource_Key = DataSource.find("ns:Key", ns).text
    result["DataSource_Type"] = DataSource_Type
    result["DataSource_Key"] = DataSource_Key

    Company = DataContext.find("ns:Company", ns)

    Company_Code = Company.find("ns:Code", ns).text
    result["CompanyCode"] = Company_Code

    Country = Company.find("ns:Country", ns).text

    Company_Country_Code = Company.find("ns:Country/ns:Code", ns).text
    Company_Country_Name = Company.find("ns:Country/ns:Name", ns).text
    result["Company_Country_Code"] = Company_Country_Code
    result["Company_Country_Name"] = Company_Country_Name

    Company_Name = Company.find("ns:Name", ns).text
    result["Company_Name"] = Company_Name

    DataProvider = DataContext.find("ns:DataProvider", ns).text
    result["DataProvider"] = DataProvider

    EnterPriseID = DataContext.find("ns:EnterpriseID", ns).text
    result["EnterPriseID"] = EnterPriseID

    ServerID = DataContext.find("ns:ServerID", ns).text
    result["ServerID"] = ServerID

    EventTime = Event.find("ns:EventTime", ns).text
    result["EventTime"] = EventTime

    EventType = Event.find("ns:EventType", ns).text
    result["EventType"] = EventType

    IsEstimate = Event.find("ns:IsEstimate", ns).text
    result["IsEstimate"] = IsEstimate

    AttachedDocumentCollection = Event.find("ns:AttachedDocumentCollection", ns)

    AttachedDocument = AttachedDocumentCollection.find(
        "ns:AttachedDocument", ns
    )

    FileName = AttachedDocument.find("ns:FileName", ns).text
    result["FileName"] = FileName

    ImageData = AttachedDocument.find("ns:ImageData", ns).text
    result["ImageData"] = ImageData

    Type = AttachedDocument.find("ns:Type", ns)

    Type_Code = Type.find("ns:Code", ns).text
    Type_Description = Type.find("ns:Description", ns).text
    result["Type_Code"] = Type_Code
    result["Type_Description"] = Type_Description

    DocumentID = AttachedDocument.find("ns:DocumentID", ns).text
    result["DocumentID"] = DocumentID

    IsPublished = AttachedDocument.find("ns:IsPublished", ns).text
    result["IsPublished"] = IsPublished

    SaveDateUTC = AttachedDocument.find("ns:SaveDateUTC", ns).text
    result["SaveDateUTC"] = SaveDateUTC

    SavedBy = AttachedDocument.find("ns:SavedBy", ns)

    SavedBy_Code = SavedBy.find("ns:Code", ns).text
    SavedBy_Name = SavedBy.find("ns:Name", ns).text
    result["SavedBy_Code"] = SavedBy_Code
    result["SavedBy_Name"] = SavedBy_Name
 
    Source = AttachedDocument.find("ns:Source", ns)
    Source_Code = Source.find("ns:Code", ns).text
    Source_Description = Source.find("ns:Description", ns).text
    result['Source_Code'] = Source_Code
    result['Source_Description'] = Source_Description

    VisibleBranchCode = AttachedDocument.find("ns:VisibleBranchCode", ns).text
    result['VisibleBranchCode'] = VisibleBranchCode

    VisibleCompanyCode = AttachedDocument.find("ns:VisibleCompanyCode", ns).text
    result['VisibleCompanyCode'] = VisibleCompanyCode

    VisibleDepartmentCode = AttachedDocument.find("ns:VisibleDepartmentCode", ns).text
    result['VisibleDepartmentCode'] = VisibleDepartmentCode

    MessageNumberCollection = root.find("ns:MessageNumberCollection", ns)

    MessageNumber = MessageNumberCollection.find("ns:MessageNumber", ns).text
    result["MessageNumber"] = MessageNumber

    result = [{"col1": x, "col2": y} for x, y in result.items()]
    return result


async def XUD_RDR_TBN_UUID_WRITE(data: dict, folder_path: str):
    """
    Take a dictionary and create an XML file with its information using the format of the XML file XUD_RDR_TBN_UUID.xml.
    """
    tree = ET.parse(
        "xml_files/XUD_RDR_TBN_UUID.xml"
    )
    root = tree.getroot()

    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    ET.register_namespace(
        "", "http://www.cargowise.com/Schemas/Universal/2011/11"
    )

    Status = root.find("ns:Status", ns)
    Status.text = data.get("status", "")

    Event = root.find("ns:Data/ns:UniversalEvent/ns:Event", ns)

    DataContext = Event.find("ns:DataContext", ns)

    DataSourceCollection = DataContext.find("ns:DataSourceCollection", ns)

    DataSource = DataContext.find("ns:DataSourceCollection/ns:DataSource", ns)

    DataSource_Type = DataSource.find("ns:Type", ns)
    DataSource_Key = DataSource.find("ns:Key", ns)
    DataSource_Type.text = data.get("datasource_type", "")
    DataSource_Key.text = data.get("datasource_key", "")

    Company = DataContext.find("ns:Company", ns)

    Company_Code = Company.find("ns:Code", ns)
    Company_Code.text = data.get("companycode", "")

    Country = Company.find("ns:Country", ns)

    Company_Country_Code = Company.find("ns:Country/ns:Code", ns)
    Company_Country_Name = Company.find("ns:Country/ns:Name", ns)
    Company_Country_Code.text = data.get("companycountry_code", "")
    Company_Country_Name.text = data.get("companycountry_name", "")

    Company_Name = Company.find("ns:Name", ns)
    Company_Name.text = data.get("company_name", "")

    DataProvider = DataContext.find("ns:DataProvider", ns)
    DataProvider.text = data.get("dataprovider", "")

    EnterPriseID = DataContext.find("ns:EnterpriseID", ns)
    EnterPriseID.text = data.get("enterpriseid", "")

    ServerID = DataContext.find("ns:ServerID", ns)
    ServerID.text = data.get("serverid", "")

    EventTime = Event.find("ns:EventTime", ns)
    EventTime.text = data.get("eventtime", "")

    EventType = Event.find("ns:EventType", ns)
    EventType.text = data.get("eventtype", "")

    IsEstimate = Event.find("ns:IsEstimate", ns)
    IsEstimate.text = data.get("isestimate", "")

    AttachedDocumentCollection = Event.find("ns:AttachedDocumentCollection", ns)

    AttachedDocument = AttachedDocumentCollection.find(
        "ns:AttachedDocument", ns
    )

    FileName = AttachedDocument.find("ns:FileName", ns)
    FileName.text = data.get("attacheddocument_filename", "")

    ImageData = AttachedDocument.find("ns:ImageData", ns)
    ImageData.text = data.get("imagedata", "")

    Type = AttachedDocument.find("ns:Type", ns)

    Type_Code = Type.find("ns:Code", ns)
    Type_Description = Type.find("ns:Description", ns)
    Type_Code.text = data.get("type_code", "")
    Type_Description.text = data.get("type_description", "")

    DocumentID = AttachedDocument.find("ns:DocumentID", ns)
    DocumentID.text = data.get("documentid", "")

    IsPublished = AttachedDocument.find("ns:IsPublished", ns)
    IsPublished.text = data.get("ispublished", "")

    SaveDateUTC = AttachedDocument.find("ns:SaveDateUTC", ns)
    SaveDateUTC.text = data.get("savedateutc", "")

    SavedBy = AttachedDocument.find("ns:SavedBy", ns)

    SavedBy_Code = SavedBy.find("ns:Code", ns)
    SavedBy_Name = SavedBy.find("ns:Name", ns)
    SavedBy_Code.text = data.get("savedby_code", "")
    SavedBy_Name.text = data.get("savedby_name", "")

    MessageNumberCollection = root.find("ns:MessageNumberCollection", ns)

    MessageNumber = MessageNumberCollection.find("ns:MessageNumber", ns)
    MessageNumber.text = data.get("messagenumber", "")

    Source = AttachedDocument.find("ns:Source", ns)
    Source_Code = Source.find("ns:Code", ns)
    Source_Description = Source.find("ns:Description", ns)
    Source_Code.text = data.get('source_code', "")
    Source_Description.text = data.get('source_description', "")

    VisibleBranchCode = AttachedDocument.find("ns:VisibleBranchCode", ns)
    VisibleBranchCode.text = data.get('visible_branch_code', "")

    VisibleCompanyCode = AttachedDocument.find("ns:VisibleCompanyCode", ns)
    VisibleCompanyCode.text = data.get('visible_company_code', "")

    VisibleDepartmentCode = AttachedDocument.find("ns:VisibleDepartmentCode", ns)
    VisibleDepartmentCode.text = data.get('visible_department_code', "")

    filename_xml = data.get("filename", "")
    file_path = f'{folder_path}/staging/{filename_xml}'
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    file_size = os.path.getsize(file_path)
    return {"filename": filename_xml, "path": file_path, "size": file_size}