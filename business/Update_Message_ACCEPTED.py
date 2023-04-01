import xml.etree.ElementTree as ET

async def Update_Message_ACCEPTED_READ(file: str):
    root = ET.fromstring(file)
    result = {}

    #get the element of Shipment
    Shipment =root.find('Shipment')

    #-------------------------------------------------------------------------------------------------------------

    #get the elements of DataContext
    DataContext = Shipment.find('DataContext')

    #get the elements of DataTargetCollection
    DataTargetCollection = DataContext.find('DataTargetCollection')

    #get the elements of DataTarget
    DataTarget = DataTargetCollection.find('DataTarget')

    #get the values of the elements Type and Key
    DataTarget_Type = DataTarget.find('Type').text
    DataTarget_Key = DataTarget.find('Key').text
    result['DataTarget_Type'] = DataTarget_Type
    result['DataTarget_Key'] = DataTarget_Key

    #get the elements of Company
    Company = DataContext.find('Company')

    #get the value of the element Code
    Company_Code = Company.find('Code').text
    result['Company_Code'] = Company_Code

    #get the value of the element EnterpriseID
    EnterpriseID = DataContext.find('EnterpriseID').text
    result['EnterpriseID'] = EnterpriseID

    #get the value of the element ServerID
    ServerID = DataContext.find('ServerID').text
    result['ServerID'] = ServerID

#-------------------------------------------------------------------------------------------------------------

    #get the elements of NoteCollection
    NoteCollection = Shipment.find('NoteCollection')

    #get the elements of Note
    Note = NoteCollection.find('Note')

    #get the value of the element Description
    Description = Note.find('Description').text
    result['Description'] = Description

    #get the value of the element IsCustomDescription
    IsCustomDescription = Note.find('IsCustomDescription').text
    result['IsCustomDescription'] = IsCustomDescription

    #get the value of the element NoteText
    NoteText = Note.find('NoteText').text
    result['NoteText'] = NoteText

    #get the elements of NoteContext
    NoteContext = Note.find('NoteContext')

    #get the value of the element Code
    NoteContext_Code = NoteContext.find('Code').text
    result['NoteContext_Code'] = NoteContext_Code

    #get the elements of Visibility
    Visibility = Note.find('Visibility')

    #get the value of the element Code
    Visibility_Code = Visibility.find('Code').text
    result['Visibility_Code'] = Visibility_Code

#-------------------------------------------------------------------------------------------------------------

    #get the elements of OrganizationAddressCollection
    OrganizationAddressCollection = Shipment.find('OrganizationAddressCollection')

    #get the elements of OrganizationAddress
    OrganizationAddress = OrganizationAddressCollection.find('OrganizationAddress')

    #get the value of the element AddressType
    AddressType = OrganizationAddress.find('AddressType').text
    result['AddressType'] = AddressType

    #get the value of the element OrganizationCode
    OrganizationCode = OrganizationAddress.find('OrganizationCode').text
    result['OrganizationCode'] = OrganizationCode

#-------------------------------------------------------------------------------------------------------------

    #get the elements of CustomizedFieldCollection
    CustomizedFieldCollection = Shipment.find('CustomizedFieldCollection')

    #get the elements of CustomizedField
    CustomizedField = CustomizedFieldCollection.find('CustomizedField')

    #get the values of the element DataType, Key and Value
    CustomizedField_DataType = CustomizedField.find('DataType').text
    CustomizedField_Key = CustomizedField.find('Key').text
    CustomizedField_Value = CustomizedField.find('Value').text
    result['CustomizedField_DataType'] = CustomizedField_DataType
    result['CustomizedField_Key'] = CustomizedField_Key
    result['CustomizedField_Value'] = CustomizedField_Value
    
    return result
#-------------------------------------------------------------------------------------------------------------
async def Update_Message_ACCEPTED_WRITE(data: dict):

    tree = ET.parse('xml_files/Update_Message_ACCEPTED.xml')
    root = tree.getroot()


    #get the element of Shipment
    Shipment =root.find('Shipment')

#-------------------------------------------------------------------------------------------------------------

    #get the elements of DataContext
    DataContext = Shipment.find('DataContext')

    #get the elements of DataTargetCollection
    DataTargetCollection = DataContext.find('DataTargetCollection')

    #get the elements of DataTarget
    DataTarget = DataTargetCollection.find('DataTarget')

    #get the values of the elements Type and Key
    DataTarget_Type = DataTarget.find('Type')
    DataTarget_Key = DataTarget.find('Key')

    DataTarget_Type.text = data.get("DataTarget_Type", "")
    DataTarget_Key.text = data.get("DataTarget_Key", "")

    #get the elements of Company
    Company = DataContext.find('Company')

    #get the value of the element Code
    Company_Code = Company.find('Code')

    Company_Code.text = data.get("Company_Code","")

    #get the value of the element EnterpriseID
    EnterpriseID = DataContext.find('EnterpriseID')
    EnterpriseID.text = data.get("EnterpriseID", "")

    #get the value of the element ServerID
    ServerID = DataContext.find('ServerID')
    ServerID.text = data.get("ServerID", "")

    #-------------------------------------------------------------------------------------------------------------

    #get the elements of NoteCollection
    NoteCollection = Shipment.find('NoteCollection')

    #get the elements of Note
    Note = NoteCollection.find('Note')

    #get the value of the element Description
    Description = Note.find('Description')
    Description.text = data.get("Description", "")

    #get the value of the element IsCustomDescription
    IsCustomDescription = Note.find('IsCustomDescription')
    IsCustomDescription.text = data.get("IsCustomDescription", "")

    #get the value of the element NoteText
    NoteText = Note.find('NoteText')
    NoteText.text = data.get("NoteText", "")

    #get the elements of NoteContext
    NoteContext = Note.find('NoteContext')

    #get the value of the element Code
    NoteContext_Code = NoteContext.find('Code')
    NoteContext_Code.text = data.get("NoteContext_Code", "")

    #get the elements of Visibility
    Visibility = Note.find('Visibility')

    #get the value of the element Code
    Visibility_Code = Visibility.find('Code')
    Visibility_Code.text = data.get("Visibility_Code", "")

    #-------------------------------------------------------------------------------------------------------------

    #get the elements of OrganizationAddressCollection
    OrganizationAddressCollection = Shipment.find('OrganizationAddressCollection')

    #get the elements of OrganizationAddress
    OrganizationAddress = OrganizationAddressCollection.find('OrganizationAddress')

    #get the value of the element AddressType
    AddressType = OrganizationAddress.find('AddressType')
    AddressType.text = data.get("AddressType", "")

    #get the value of the element OrganizationCode
    OrganizationCode = OrganizationAddress.find('OrganizationCode')
    OrganizationCode.text = data.get("OrganizationCode", "")

#-------------------------------------------------------------------------------------------------------------

    #get the elements of CustomizedFieldCollection
    CustomizedFieldCollection = Shipment.find('CustomizedFieldCollection')

    #get the elements of CustomizedField
    CustomizedField = CustomizedFieldCollection.find('CustomizedField')

    #get the values of the element DataType, Key and Value
    CustomizedField_DataType = CustomizedField.find('DataType')
    CustomizedField_Key = CustomizedField.find('Key')
    CustomizedField_Value = CustomizedField.find('Value')
    CustomizedField_DataType.text = data.get("CustomizedField_DataType", "")
    CustomizedField_Key.text = data.get("CustomizedField_Key", "")
    CustomizedField_Value.text = data.get("CustomizedField_Value", "")

#-------------------------------------------------------------------------------------------------------------

    filename_xml = data.get("filename", "")
    file_path = f'test_files\{filename_xml}'
    tree.write(file_path, encoding='utf-8', xml_declaration=True)