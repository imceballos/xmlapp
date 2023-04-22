import xml.etree.ElementTree as ET

async def MESSAGE_XUD_DTYPE_TB_TIMESTAMP_READ(file: str):
    """
    Take the XML file MESSAGE_XUD_DTYPE_TB_TIMESTAMP.xml in string format, read it and return a dictionary with its field names as keys and its contents as values.
    """
    root = ET.fromstring(file)
    result = {}

    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    # get the value of the Status element
    status = root.find("ns:Status", ns).text
    result["Status"] = status

    # get the value of the Type and Key elements of the DataSource
    datasource = root.find(
        "ns:Data/ns:UniversalEvent/ns:Event/ns:DataContext/ns:DataSourceCollection/ns:DataSource",
        ns,
    )
    datasource_type = datasource.find("ns:Type", ns).text
    datasource_key = datasource.find("ns:Key", ns).text
    result["DataSource Type"] = datasource_type
    result["DataSource Key"] = datasource_key

    # get the value of the Code element of the Company
    company = root.find(
        "ns:Data/ns:UniversalEvent/ns:Event/ns:DataContext/ns:Company", ns
    )
    company_code = company.find("ns:Code", ns).text
    company_name = company.find("ns:Name", ns).text
    company_country_code = company.find("ns:Country/ns:Code", ns).text
    company_country_name = company.find("ns:Country/ns:Name", ns).text

    result["Company code"] = company_code
    result["Company Name"] = company_name
    result["Company Country Code"] = company_country_code
    result["Company Country Name"] = company_country_name

    # get the value of the EventTime and EventType elements of the Event
    event = root.find("ns:Data/ns:UniversalEvent/ns:Event", ns)
    event_time = event.find("ns:EventTime", ns).text
    event_type = event.find("ns:EventType", ns).text
    is_estimate = event.find("ns:IsEstimate", ns).text

    result["Event Time"] = event_time
    result["Event Type"] = event_type
    result["Is Estimate"] = is_estimate

    document = root.find(
        "ns:Data/ns:UniversalEvent/ns:Event/ns:AttachedDocumentCollection/ns:AttachedDocument",
        ns,
    )
    filename = document.find("ns:FileName", ns).text
    imagedata = document.find("ns:ImageData", ns).text

    result["Filename"] = filename
    result["ImageData"] = imagedata.strip()

    # get the value of the Code and Description elements of the Type of the AttachedDocument
    document_type = document.find("ns:Type", ns)
    document_type_code = document_type.find("ns:Code", ns).text
    document_type_desc = document_type.find("ns:Description", ns).text

    result["Document Type Code"] = document_type_code
    result["Document Type Description"] = document_type_desc

    document_id = document.find("ns:DocumentID", ns).text
    is_published = document.find("ns:IsPublished", ns).text
    save_date_utc = document.find("ns:SaveDateUTC", ns).text

    result["Document ID"] = document_id
    result["Is Published"] = is_published
    result["Save Date UTC"] = save_date_utc

    # get the SavedBy attributes
    document_saved_by = document.find("ns:SavedBy", ns)
    dsb_code = document_saved_by.find("ns:Code", ns).text
    dsb_name = document_saved_by.find("ns:Name", ns).text

    result["Document Saved By Code"] = dsb_code
    result["Document Saved By Name"] = dsb_name

    result = [{"col1": x, "col2": y} for x, y in result.items()]

    return result


async def MESSAGE_XUD_DTYPE_TB_TIMESTAMP_WRITE(data: dict):
    """
    Take a dictionary and create an XML file with its information using the format of the XML file MESSAGE_XUD_DTYPE_TB_TIMESTAMP.xml.
    """
    tree = ET.parse("xml_files/MESSAGE_XUD_DTYPE_TB_TIMESTAMP.xml")
    root = tree.getroot()

    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    ET.register_namespace(
        "", "http://www.cargowise.com/Schemas/Universal/2011/11"
    )

    status = root.find("ns:Status", ns)
    status.text = data.get("status", "")

    datasource = root.find(
        "ns:Data/ns:UniversalEvent/ns:Event/ns:DataContext/ns:DataSourceCollection/ns:DataSource",
        ns,
    )
    datasource_type = datasource.find("ns:Type", ns)
    datasource_key = datasource.find("ns:Key", ns)

    datasource_type.text = data.get("data_source_type", "")
    datasource_key.text = data.get("data_source_key", "")

    company = root.find(
        "ns:Data/ns:UniversalEvent/ns:Event/ns:DataContext/ns:Company", ns
    )
    company_code = company.find("ns:Code", ns)
    company_name = company.find("ns:Name", ns)
    company_country_code = company.find("ns:Country/ns:Code", ns)
    company_country_name = company.find("ns:Country/ns:Name", ns)

    company_code.text = data.get("company_code", "")
    company_name.text = data.get("company_name", "")
    company_country_code.text = data.get("company_country_code", "")
    company_country_name.text = data.get("company_country_name", "")

    event = root.find("ns:Data/ns:UniversalEvent/ns:Event", ns)
    
    event_time = event.find("ns:EventTime", ns)
    event_type = event.find("ns:EventType", ns)
    is_estimate = event.find("ns:IsEstimate", ns)

    event_time.text = data.get("event_time", "")
    event_type.text = data.get("event_type", "")
    is_estimate.text = data.get("is_estimate", "")

    document = root.find(
        "ns:Data/ns:UniversalEvent/ns:Event/ns:AttachedDocumentCollection/ns:AttachedDocument",
        ns,
    )
    filename = document.find("ns:FileName", ns)
    imagedata = document.find("ns:ImageData", ns)

    filename.text = data.get("filename_attached", "")
    imagedata.text = data.get("image_data", "")

    # get the value of the Code and Description elements of the Type of the AttachedDocument
    document_type = document.find("ns:Type", ns)

    document_type_code = document_type.find("ns:Code", ns)
    document_type_desc = document_type.find("ns:Description", ns)

    document_type_code.text = data.get("document_type_code", "")
    document_type_desc.text = data.get("document_type_description", "")

    document_id = document.find("ns:DocumentID", ns)
    is_published = document.find("ns:IsPublished", ns)
    save_date_utc = document.find("ns:SaveDateUTC", ns)

    document_id.text = data.get("document_id", "")
    is_published.text = data.get("is_published", "")
    save_date_utc.text = data.get("save_date_utc", "")

    # get the SavedBy attributes
    document_saved_by = document.find("ns:SavedBy", ns)

    document_saved_by_code = document_saved_by.find("ns:Code", ns)
    document_saved_by_name = document_saved_by.find("ns:Name", ns)

    document_saved_by_code.text = data.get("document_saved_by_code", "")
    document_saved_by_name.text = data.get("document_saved_by_name", "")

    filename_xml = data.get("filename", "")
    file_path = f'test_files/trucker5_2231231312/acknowledge/pending/{filename_xml}'
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
