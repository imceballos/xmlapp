import xml.etree.ElementTree as ET

async def UPDATE_MESSAGE_PAYABLE_UPDATE_READ(file: str):

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

    TransportBookingDirection = Shipment.find('TransportBookingDirection')
    TransportBookingDirection_Code = TransportBookingDirection.find('Code').text
    TransportBookingDirection_Description = TransportBookingDirection.find('Description').text
    result['TransportBookingDirection_Code'] = TransportBookingDirection_Code
    result['TransportBookingDirection_Description'] = TransportBookingDirection_Description

    OrganizationAddressCollection = Shipment.find('OrganizationAddressCollection')
    OrganizationAddress = OrganizationAddressCollection.find('OrganizationAddress')
    AddressType = OrganizationAddress.find('AddressType').text
    OrganizationCode = OrganizationAddress.find('OrganizationCode').text
    result['AddressType'] = AddressType
    result['OrganizationCode'] = OrganizationCode

    JobCosting = Shipment.find('JobCosting')
    Branch = JobCosting.find('Branch')
    Branch_Code = Branch.find('Code').text
    result['Branch_Code'] = Branch_Code

    Currency = JobCosting.find('Currency')
    Currency_Code = Currency.find('Code').text
    result['Currency_Code'] = Currency_Code

    Department = JobCosting.find('Department')
    Department_Code = Department.find('Code').text
    result['Department_Code'] = Department_Code

    ChargeLineCollection = JobCosting.find('ChargeLineCollection')
    ChargeLine = ChargeLineCollection.find('ChargeLine')
    ChargeLine_Branch = ChargeLine.find('Branch')
    ChargeLine_Branch_Code = ChargeLine_Branch.find('Code').text
    result['ChargeLine_Branch_Code'] = ChargeLine_Branch_Code

    ChargeLine_ChargeCode = ChargeLine.find('ChargeCode')
    ChargeLine_ChargeCode_Code = ChargeLine_ChargeCode.find('Code').text
    result['ChargeLine_ChargeCode_Code'] = ChargeLine_ChargeCode_Code
    ChargeLine_CostLocalAmount = ChargeLine.find('CostLocalAmount').text
    result['ChargeLine_CostLocalAmount'] = ChargeLine_CostLocalAmount
    ChargeLine_CostOSAmount = ChargeLine.find('CostOSAmount').text
    result['ChargeLine_CostOSAmount'] = ChargeLine_CostOSAmount

    ChargeLine_CostOSCurrency = ChargeLine.find('CostOSCurrency')
    ChargeLine_ChargeLine_CostOSCurrency_Code = ChargeLine_CostOSCurrency.find('Code').text
    result['ChargeLine_ChargeLine_CostOSCurrency_Code'] = ChargeLine_ChargeLine_CostOSCurrency_Code
    ChargeLine_CostOSGSTVATAmount = ChargeLine.find('CostOSGSTVATAmount').text
    result['ChargeLine_CostOSGSTVATAmount'] = ChargeLine_CostOSGSTVATAmount

    ChargeLine_Creditor = ChargeLine.find('Creditor')
    ChargeLine_Creditor_Type = ChargeLine_Creditor.find('Type').text
    ChargeLine_Creditor_Key = ChargeLine_Creditor.find('Key').text
    result['ChargeLine_Creditor_Type'] = ChargeLine_Creditor_Type
    result['ChargeLine_Creditor_Key'] = ChargeLine_Creditor_Key

    ChargeLine_Department = ChargeLine.find('Department')
    ChargeLine_Department_Code = ChargeLine_Department.find('Code').text
    result['ChargeLine_Department_Code'] = ChargeLine_Department_Code
    ChargeLine_DisplaySequence = ChargeLine.find('DisplaySequence').text
    result['ChargeLine_DisplaySequence'] = ChargeLine_DisplaySequence

    ChargeLine_ImportMetaData = ChargeLine.find('ImportMetaData')
    ChargeLine_ImportMetaData_Instruction = ChargeLine_ImportMetaData.find('Instruction').text
    result['ChargeLine_ImportMetaData_Instruction'] = ChargeLine_ImportMetaData_Instruction
    ChargeLine_SupplierReference = ChargeLine.find('SupplierReference').text
    result['ChargeLine_SupplierReference'] = ChargeLine_SupplierReference

    result = [{"col1": x, "col2": y} for x,y in result.items()]

    return result

async def UPDATE_MESSAGE_PAYABLE_UPDATE_WRITE(data: dict):

    tree = ET.parse('xml_files/update_message_payable_update.xml')
    root = tree.getroot()

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

    TransportBookingDirection = Shipment.find('TransportBookingDirection')
    TransportBookingDirection_Code = TransportBookingDirection.find('Code')
    TransportBookingDirection_Description = TransportBookingDirection.find('Description')
    TransportBookingDirection_Code.text = data.get('transportbookingdirection_code', "")
    TransportBookingDirection_Description.text = data.get('transportbookingdirection_description', "")

    OrganizationAddressCollection = Shipment.find('OrganizationAddressCollection')
    OrganizationAddress = OrganizationAddressCollection.find('OrganizationAddress')
    AddressType = OrganizationAddress.find('AddressType')
    OrganizationCode = OrganizationAddress.find('OrganizationCode')
    AddressType.text = data.get('addresstype', "")
    OrganizationCode.text = data.get('organizationcode', "")

    JobCosting = Shipment.find('JobCosting')
    Branch = JobCosting.find('Branch')
    Branch_Code = Branch.find('Code')
    Branch_Code.text = data.get('branch_code', "")

    Currency = JobCosting.find('Currency')
    Currency_Code = Currency.find('Code')
    Currency_Code.text = data.get('currency_code', "")

    Department = JobCosting.find('Department')
    Department_Code = Department.find('Code')
    Department_Code.text = data.get('department_code', "")

    ChargeLineCollection = JobCosting.find('ChargeLineCollection')
    ChargeLine = ChargeLineCollection.find('ChargeLine')
    ChargeLine_Branch = ChargeLine.find('Branch')
    ChargeLine_Branch_Code = ChargeLine_Branch.find('Code')
    ChargeLine_Branch_Code.text = data.get('chargeline_branch_code', "")

    ChargeLine_ChargeCode = ChargeLine.find('ChargeCode')
    ChargeLine_ChargeCode_Code = ChargeLine_ChargeCode.find('Code')
    ChargeLine_ChargeCode_Code.text = data.get('chargeline_chargecode_code', "")
    ChargeLine_CostLocalAmount = ChargeLine.find('CostLocalAmount')
    ChargeLine_CostLocalAmount.text = data.get('chargeline_costlocalamount', "")
    ChargeLine_CostOSAmount = ChargeLine.find('CostOSAmount')
    ChargeLine_CostOSAmount.text = data.get('chargeline_costosamount', "")

    ChargeLine_CostOSCurrency = ChargeLine.find('CostOSCurrency')
    ChargeLine_CostOSCurrency_Code = ChargeLine_CostOSCurrency.find('Code')
    ChargeLine_CostOSCurrency_Code.text = data.get('chargeline_costoscurrency_code', "")
    ChargeLine_CostOSGSTVATAmount = ChargeLine.find('CostOSGSTVATAmount')
    ChargeLine_CostOSGSTVATAmount.text = data.get('chargeline_costosgstvatamount', "")

    ChargeLine_Creditor = ChargeLine.find('Creditor')
    ChargeLine_Creditor_Type = ChargeLine_Creditor.find('Type')
    ChargeLine_Creditor_Key = ChargeLine_Creditor.find('Key')
    ChargeLine_Creditor_Type.text = data.get('chargeline_creditor_type', "")
    ChargeLine_Creditor_Key.text = data.get('chargeline_creditor_key', "")

    ChargeLine_Department = ChargeLine.find('Department')
    ChargeLine_Department_Code = ChargeLine_Department.find('Code')
    ChargeLine_Department_Code.text = data.get('chargeline_department_code', "")
    ChargeLine_DisplaySequence = ChargeLine.find('DisplaySequence')
    ChargeLine_DisplaySequence.text = data.get('chargeline_displaysequence', "")

    ChargeLine_ImportMetaData = ChargeLine.find('ImportMetaData')
    ChargeLine_ImportMetaData_Instruction = ChargeLine_ImportMetaData.find('Instruction')
    ChargeLine_ImportMetaData_Instruction.text = data.get('chargeline_importmetadata_instruction', "")
    ChargeLine_SupplierReference = ChargeLine.find('SupplierReference')
    ChargeLine_SupplierReference.text = data.get('chargeline_supplierreference', "") 
    
    filename_xml = data.get("filename", "")
    file_path = f'test_files\{filename_xml}'
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
