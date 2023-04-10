import xml.etree.ElementTree as ET


async def UPDATE_MESSAGE_REJECTED_READ(file: str):

    root = ET.fromstring(file)
    result = {}

    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2011/11'}

    Shipment =root.find('ns:Shipment', ns)

    DataContext = Shipment.find('ns:DataContext', ns)

    DataTargetCollection = DataContext.find('ns:DataTargetCollection', ns)

    DataTarget = DataTargetCollection.find('ns:DataTarget', ns)

    DataTarget_Type = DataTarget.find('ns:Type', ns).text
    DataTarget_Key = DataTarget.find('ns:Key', ns).text
    result['DataTarget_Type'] = DataTarget_Type
    result['DataTarget_Key'] = DataTarget_Key

    Company = DataContext.find('ns:Company', ns)

    Company_Code = Company.find('ns:Code', ns).text
    result['Company_Code'] = Company_Code

    EnterpriseID = DataContext.find('ns:EnterpriseID', ns).text
    result['EnterpriseID'] = EnterpriseID

    ServerID = DataContext.find('ns:ServerID', ns).text
    result['ServerID'] = ServerID

    NoteCollection = Shipment.find('ns:NoteCollection', ns)

    Note = NoteCollection.find('ns:Note', ns)

    Description = Note.find('ns:Description', ns).text
    result['Description'] = Description

    IsCustomDescription = Note.find('ns:IsCustomDescription', ns).text
    result['IsCustomDescription'] = IsCustomDescription

    NoteText = Note.find('ns:NoteText', ns).text
    result['NoteText'] = NoteText

    NoteContext = Note.find('ns:NoteContext', ns)

    NoteContext_Code = NoteContext.find('ns:Code', ns).text
    result['NoteContext_Code'] = NoteContext_Code

    Visibility = Note.find('ns:Visibility', ns)

    Visibility_Code = Visibility.find('ns:Code', ns).text
    result['Visibility_Code'] = Visibility_Code

    OrganizationAddressCollection = Shipment.find('ns:OrganizationAddressCollection', ns)
    OrganizationAddress = OrganizationAddressCollection.find('ns:OrganizationAddress', ns)

    AddressType = OrganizationAddress.find('ns:AddressType', ns).text
    result['AddressType'] = AddressType

    OrganizationCode = OrganizationAddress.find('ns:OrganizationCode', ns).text
    result['OrganizationCode'] = OrganizationCode

    CustomizedFieldCollection = Shipment.find('ns:CustomizedFieldCollection', ns)
    CustomizedField = CustomizedFieldCollection.find('ns:CustomizedField', ns)

    CustomizedField_DataType = CustomizedField.find('ns:DataType', ns).text
    CustomizedField_Key = CustomizedField.find('ns:Key', ns).text
    CustomizedField_Value = CustomizedField.find('ns:Value', ns).text
    result['CustomizedField_DataType'] = CustomizedField_DataType
    result['CustomizedField_Key'] = CustomizedField_Key
    result['CustomizedField_Value'] = CustomizedField_Value

    result = [{"col1": x, "col2": y} for x,y in result.items()]
    return result