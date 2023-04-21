import xml.etree.ElementTree as ET

async def UPDATE_MESSAGE_ALLOCATED_READ(file: str):

    root = ET.fromstring(file)
    result = {}

    Shipment =root.find('Shipment')

    DataContext = Shipment.find('DataContext')
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

    NoteCollection = Shipment.find('NoteCollection')
    Note = NoteCollection.find('Note')
    Description = Note.find('Description').text
    result['Description'] = Description
    IsCustomDescription = Note.find('IsCustomDescription').text
    result['IsCustomDescription'] = IsCustomDescription
    NoteText = Note.find('NoteText').text
    result['NoteText'] = NoteText
    NoteContext = Note.find('NoteContext')
    NoteContext_Code = NoteContext.find('Code').text
    result['NoteContext_Code'] = NoteContext_Code

    Visibility = Note.find('Visibility')
    Visibility_Code = Visibility.find('Code').text
    result['Visibility_Code'] = Visibility_Code

    OrganizationAddressCollection = Shipment.find('OrganizationAddressCollection')
    OrganizationAddress = OrganizationAddressCollection.find('OrganizationAddress')
    AddressType = OrganizationAddress.find('AddressType').text
    result['AddressType'] = AddressType

    OrganizationCode = OrganizationAddress.find('OrganizationCode').text
    result['OrganizationCode'] = OrganizationCode

    CustomizedFieldCollection = Shipment.find('CustomizedFieldCollection')
    CustomizedField = CustomizedFieldCollection.find('CustomizedField')
    CustomizedField_DataType = CustomizedField.find('DataType').text
    CustomizedField_Key = CustomizedField.find('Key').text
    CustomizedField_Value = CustomizedField.find('Value').text
    result['CustomizedField_DataType'] = CustomizedField_DataType
    result['CustomizedField_Key'] = CustomizedField_Key
    result['CustomizedField_Value'] = CustomizedField_Value

    result = [{"col1": x, "col2": y} for x,y in result.items()]

    return result


async def UPDATE_MESSAGE_ALLOCATED_WRITE(data: dict):

    tree = ET.parse('xml_files/UPDATE_MESSAGE_ALLOCATED.xml')
    root = tree.getroot()

    ns = {'ns': 'http://www.cargowise.com/Schemas/Universal/2011/11'}

    ET.register_namespace("", 'http://www.cargowise.com/Schemas/Universal/2011/11')

    Shipment =root.find('Shipment')

    DataContext = Shipment.find('DataContext')
    DataTargetCollection = DataContext.find('DataTargetCollection')
    DataTarget = DataTargetCollection.find('DataTarget')
    DataTarget_Type = DataTarget.find('Type')
    DataTarget_Key = DataTarget.find('Key')
    DataTarget_Type.text = data.get('datatarget_type', "")
    DataTarget_Key.text = data.get('datatarget_key', "")

    Company = DataContext.find('Company')
    Company_Code = Company.find('Code')
    Company_Code.text = data.get('company_code', "")

    EnterpriseID = DataContext.find('EnterpriseID')
    EnterpriseID.text = data.get('enterpriseid', "")

    ServerID = DataContext.find('ServerID')
    ServerID.text = data.get('serverid', "")

    NoteCollection = Shipment.find('NoteCollection')
    Note = NoteCollection.find('Note')
    Description = Note.find('Description')
    Description.text = data.get('description', "")
    IsCustomDescription = Note.find('IsCustomDescription')
    IsCustomDescription.text = data.get('iscustomdescription', "")
    NoteText = Note.find('NoteText')
    NoteText.text = data.get('notetext', "")
    NoteContext = Note.find('NoteContext')
    NoteContext_Code = NoteContext.find('Code')
    NoteContext_Code.text = data.get('notecontext_Code', "")

    Visibility = Note.find('Visibility')
    Visibility_Code = Visibility.find('Code')
    Visibility_Code.text = data.get('visibility_code', "")

    OrganizationAddressCollection = Shipment.find('OrganizationAddressCollection')
    OrganizationAddress = OrganizationAddressCollection.find('OrganizationAddress')
    AddressType = OrganizationAddress.find('AddressType')
    AddressType.text = data.get('addresstype', "")
    OrganizationCode = OrganizationAddress.find('OrganizationCode')
    OrganizationCode.text = data.get('organizationcode', "")

    CustomizedFieldCollection = Shipment.find('CustomizedFieldCollection')
    CustomizedField = CustomizedFieldCollection.find('CustomizedField')
    CustomizedField_DataType = CustomizedField.find('DataType')
    CustomizedField_Key = CustomizedField.find('Key')
    CustomizedField_Value = CustomizedField.find('Value')
    CustomizedField_DataType.text = data.get('customizedfield_datatype', "")
    CustomizedField_Key.text = data.get('customizedfield_key', "")
    CustomizedField_Value.text = data.get('customizedfield_value', "")

    filename_xml = data.get("filename", "")
    file_path = f'test_files/trucker5_2231231312/acknowledge/pending/{filename_xml}'
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
