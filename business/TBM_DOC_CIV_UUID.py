import xml.etree.ElementTree as ET


async def TBM_DOC_CIV_UUID_READ(file: str):
    """
    Take the XML file TBM_DOC_CIV_UUID.xml in string format, read it and return a dictionary with its field names as keys and its contents as values.
    """
    root = ET.fromstring(file)
    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}
    result = {}

    evento = root.find("ns:Data/ns:UniversalEvent/ns:Event", ns)

    documento = evento.find(
        "ns:AttachedDocumentCollection/ns:AttachedDocument", ns
    )
    nombre_archivo = documento.find("ns:FileName", ns).text
    fecha_guardado = documento.find("ns:SaveDateUTC", ns).text
    result["File Name"] = nombre_archivo
    result["Save Date UTC"] = fecha_guardado

    empresa = evento.find("ns:DataContext/ns:Company", ns)
    nombre_empresa = empresa.find("ns:Name", ns).text
    codigo_pais = empresa.find("ns:Country/ns:Code", ns).text
    result["Company Name"] = nombre_empresa
    result["Country Code"] = codigo_pais

    contexto = evento.find("ns:ContextCollection", ns)
    hawb_num = contexto.find(
        'ns:Context[ns:Type="HAWBNumber"]/ns:Value', ns
    ).text
    hawb_origen = contexto.find(
        'ns:Context[ns:Type="HAWBOriginIATAAirportCode"]/ns:Value', ns
    ).text
    hawb_destino = contexto.find(
        'ns:Context[ns:Type="HAWBDestinationIATAAirportCode"]/ns:Value', ns
    ).text
    hbol_origen = contexto.find(
        'ns:Context[ns:Type="HBOLOriginUNLOCO"]/ns:Value', ns
    ).text
    hbol_destino = contexto.find(
        'ns:Context[ns:Type="HBOLDestinationUNLOCO"]/ns:Value', ns
    ).text

    result["HAWB Number"] = hawb_num
    result["HAWB Origin IATA Airport Code"] = hawb_origen
    result["HAWB Destination IATA Airport Code"] = hawb_destino
    result["HBOL Origin UN/LOCODE"] = hbol_origen
    result["HBOL Destination UN/LOCODE"] = hbol_destino

    datasource = evento.find(
        "ns:DataContext/ns:DataSourceCollection/ns:DataSource", ns
    )
    datasource_type = datasource.find("ns:Type", ns).text
    datasource_key = datasource.find("ns:Key", ns).text
    result["Type"] = datasource_type
    result["Key"] = datasource_key

    result = [{"col1": x, "col2": y} for x, y in result.items()]
    return result


async def TBM_DOC_CIV_UUID_WRITE(data: dict, folder_path: str):
    """
    Take a dictionary and create an XML file with its information using the format of the XML file TBM_DOC_CIV_TB00001182_S00013457_uniqueID.xml.
    """
    tree = ET.parse("xml_files/TBM_DOC_CIV_UUID.xml")
    root = tree.getroot()

    ns = {"ns": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    ET.register_namespace(
        "", "http://www.cargowise.com/Schemas/Universal/2011/11"
    )

    evento = root.find("ns:Data/ns:UniversalEvent/ns:Event", ns)

    documento = evento.find(
        "ns:AttachedDocumentCollection/ns:AttachedDocument", ns
    )

    nombre_archivo = documento.find("ns:FileName", ns)
    fecha_guardado = documento.find("ns:SaveDateUTC", ns)

    nombre_archivo.text = data.get("nombre_archivo", "")
    fecha_guardado.text = data.get("fecha_guardado", "")

    empresa = evento.find("ns:DataContext/ns:Company", ns)
    nombre_empresa = empresa.find("ns:Name", ns)
    codigo_pais = empresa.find("ns:Country/ns:Code", ns)

    empresa.text = data.get("empresa", "")
    nombre_empresa.text = data.get("nombre_empresa", "")
    codigo_pais.text = data.get("codigo_pais", "")

    contexto = evento.find("ns:ContextCollection", ns)
    hawb_num = contexto.find('ns:Context[ns:Type="HAWBNumber"]/ns:Value', ns)
    hawb_origen = contexto.find(
        'ns:Context[ns:Type="HAWBOriginIATAAirportCode"]/ns:Value', ns
    )
    hawb_destino = contexto.find(
        'ns:Context[ns:Type="HAWBDestinationIATAAirportCode"]/ns:Value', ns
    )
    hbol_origen = contexto.find(
        'ns:Context[ns:Type="HBOLOriginUNLOCO"]/ns:Value', ns
    )
    hbol_destino = contexto.find(
        'ns:Context[ns:Type="HBOLDestinationUNLOCO"]/ns:Value', ns
    )

    contexto.text = data.get("contexto", "")
    hawb_num.text = data.get("hawb_num", "")
    hawb_origen.text = data.get("haw_origen", "")
    hawb_destino.text = data.get("hawb_destino", "")
    hbol_origen.text = data.get("hbol_origen", "")
    hbol_destino.text = data.get("hbol_destino", "")

    filename_xml = data.get("filename", "")
    file_path = f'{folder_path}/acknowledge/pending/{filename_xml}'
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
