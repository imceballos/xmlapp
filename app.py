from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse, HTMLResponse, Response

from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Annotated, Dict
from datetime import datetime, timedelta

import os
import uuid

from utils.auth import OAuth2PasswordBearerWithCookie, AuthenticationMethods
from utils.settings import Settings
from utils.models import User, File, get_user
from utils.login import LoginForm
from utils.utils import UtilFunctions
from utils.encrypt import decode_from_base64, encode_to_base64
import business as business

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

settings = Settings()
auth_method = AuthenticationMethods(settings)
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token", settings = settings)

TEST_FILE = os.getenv("TEST_FILE")


def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    user = auth_method.decode_token(token)
    return user

    
@app.get("/statusfiles")
async def index(request: Request):
    """
    gets the list of files from the directory, creates a list of dictionaries with the name and size fields, and returns an HTML response
    with the generated file list
    """
    file_list = os.listdir("test_files")
    files = [{"name": file, "size": os.path.getsize(os.path.join("test_files", file))} for file in file_list]
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@app.get("/download/{folder}/{filename}")
async def download_file(folder: str, filename: str):
    """
    Endpoint that returns the content of a file as a download
    """
    decoded_text = decode_from_base64(folder)
    file_path = os.path.join(decoded_text, filename)
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@app.get("/file/{filename}")
async def read_file(filename: str):
    """
    Endpoint that returns the file info for a specific file
    """
    filepath = os.path.join("xml_files", filename)
    if os.path.isfile(filepath) and filename.endswith(".xml"):
        return UtilFunctions().get_file_info(filepath)
    else:
        return {"error": "File not found"}


@app.get("/form", response_class=HTMLResponse)
async def show_form(request: Request, user: User = Depends(get_current_user_from_token)):
    """
    View that displays a form with an input field for uploading a file
    """
    return templates.TemplateResponse("form.html", {"request": request})



@app.post("/form", response_class=HTMLResponse)
async def process_form(file: UploadFile, request: Request, user: User = Depends(get_current_user_from_token)):
    """
    Endpoint that processes the uploaded file and saves it to disk
    """    
    # Save the uploaded file to disk
    contents = await file.read()
    filename = file.filename
    
    xml_parser = getattr(business, UtilFunctions().get_func_filename(filename))
    data = await xml_parser(contents)
    
    return templates.TemplateResponse("table.html", {"data": data, "request": request})

@app.post("/delete_file/{filename}/{folder}")
async def delete_file(request: Request, filename: str, folder: str):
    decoded_text = decode_from_base64(folder)
    file_path = os.path.join(decoded_text, filename)
    try:
        UtilFunctions().delete_directory(file_path)
        return {"message": f"Successfully deleted {filename}"}
    except FileNotFoundError:
        return {"error": f"File not found: {filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/formpost", response_class=HTMLResponse)
async def post_form(request: Request):
    """
    View that displays a form with an input field for uploading a file
    """
    return templates.TemplateResponse("formpost.html", {"request": request})


@app.post("/formpost")
async def process_form(data: dict, request: Request):
    """
    Given a dictonary, a new dictionary is created with the corresponding keys and values,
    and a function is called to write the data to an XML file.
    """
    option = list(data.keys())[0]
    if option == "input_a_0":
        data = {    
                    "option": option, 
                    "filename": data.get("input_a_0"), 
                    "data_target_type": data.get("input_a_1"), 
                    "data_target_key": data.get("input_a_2"),
                    "company_code": data.get("input_a_3"),
                    "filter_type": data.get("input_a_4"),
                    "filter_value": data.get("input_a_5"),
                    "enterprise_id": data.get("input_a_6"),
                    "server_id": data.get("input_a_7")
                }
    elif option == "input_b_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_b_0"), 
                    "status": data.get("input_b_1"), 
                    "data_source_type": data.get("input_b_2"),
                    "data_source_key": data.get("input_b_3"),
                    "company_code": data.get("input_b_4"),
                    "company_name": data.get("input_b_5"),
                    "company_country_code": data.get("input_b_6"),
                    "company_country_name": data.get("input_b_7"),
                    "event_time": data.get("input_b_8"),
                    "event_type": data.get("input_b_9"),
                    "is_estimate": data.get("input_b_10"),
                    "filename_attached": data.get("input_b_11"),
                    "image_data": data.get("input_b_12"),
                    "document_type_code": data.get("input_b_13"),
                    "document_type_description": data.get("input_b_14"),
                    "document_id": data.get("input_b_15"),
                    "is_published": data.get("input_b_16"),
                    "save_date_utc": data.get("input_b_17"),
                    "document_saved_by_code": data.get("input_b_18"),
                    "document_saved_by_name": data.get("input_b_19")
                }
    elif option == "input_c_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_c_0"), 
                    "data_target_type": data.get("input_c_1"), 
                    "data_target_key": data.get("input_c_2"),
                    "company_code": data.get("input_c_3"),
                    "enterprise_id": data.get("input_c_4"),
                    "server_id": data.get("input_c_5"),
                    "event_time": data.get("input_c_6"),
                    "event_type": data.get("input_c_7"),
                    "event_reference": data.get("input_c_8"),
                    "is_estimate": data.get("input_C_9")
                }
    elif option == "input_d_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_d_0"), 
                    "event_time": data.get("input_d_1"), 
                    "event_type": data.get("input_d_2"),
                    "event_reference": data.get("input_d_3"),
                    "data_target_type": data.get("input_d_4"),
                    "data_target_key": data.get("input_d_5"),
                    "company_code": data.get("input_d_6"),
                    "enterprise_id": data.get("input_d_7"),
                    "server_id": data.get("input_d_8"),
                    "is_estimate": data.get("input_d_9")
                }
    elif option == "input_e_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_e_0"), 
                    "data_target_type": data.get("input_e_1"), 
                    "data_target_key": data.get("input_e_2"),
                    "company_code": data.get("input_e_3"),
                    "enterprise_id": data.get("input_e_4"),
                    "server_id": data.get("input_e_5"),
                    "description": data.get("input_e_6"),
                    "note_text": data.get("input_e_7"),
                    "note_context_code": data.get("input_e_8"),
                    "visibility_code": data.get("input_e_9"),
                    "address_type": data.get("input_e_10"),
                    "organization_code": data.get("input_e_11"),
                    "customized_field_datatype": data.get("input_e_12"),
                    "customized_field_key": data.get("input_e_13"),
                    "customized_field_value": data.get("input_e_14")
                } 
    elif option == "input_f_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_f_0"), 
                    "data_target_type": data.get("input_f_1"), 
                    "data_target_key": data.get("input_f_2"),
                    "company_code": data.get("input_f_3"),
                    "enterprise_id": data.get("input_f_4"),
                    "server_id": data.get("input_f_5"),
                    "transport_booking_direction_code": data.get("input_f_6"),
                    "transport_booking_direction_description": data.get("input_f_7"),
                    "address_type": data.get("input_f_8"),
                    "organization_code": data.get("input_f_9"),
                    "branch_code": data.get("input_f_10"),
                    "currency_code": data.get("input_f_11"),
                    "department_code": data.get("input_f_12"),
                    "charge_line_branch_code": data.get("input_f_13"),
                    "charge_line_charge_code": data.get("input_f_14"),
                    "charge_line_cost_local_amount": data.get("input_f_15"),
                    "charge_line_cost_os_amount": data.get("input_f_16"),
                    "charge_line_cost_os_currency_code": data.get("input_f_17"),
                    "charge_line_cost_os_gstvat_amount": data.get("input_f_18"),
                    "charge_line_creditor_type": data.get("input_f_19"),
                    "charge_line_creditor_key": data.get("input_f_20"),
                    "charge_line_department_code": data.get("input_f_21"),
                    "charge_line_display_sequence": data.get("input_f_22"),
                    "charge_line_import_metadata_instruction": data.get("input_f_23"),
                    "charge_line_supplier_reference": data.get("input_f_24"),
                    "customized_field_data_type": data.get("input_f_25"),
                    "customized_field_key": data.get("input_f_26"),
                    "customized_field_value": data.get("input_f_27")
                }
    elif option == "input_g_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_g_0"), 
                    "data_target_type": data.get("input_g_1"), 
                    "data_target_key": data.get("input_g_2"),
                    "company_code": data.get("input_g_3"),
                    "enterprise_id": data.get("input_g_4"),
                    "server_id": data.get("input_g_5"),
                    "transport_booking_direction_code": data.get("input_g_6"),
                    "transport_booking_direction_description": data.get("input_g_7"),
                    "address_type": data.get("input_g_8"),
                    "organization_code": data.get("input_g_9"),
                    "branch_code": data.get("input_g_10"),
                    "currency_code": data.get("input_g_11"),
                    "department_code": data.get("input_g_12"),
                    "charge_line_branch_code": data.get("input_g_13"),
                    "charge_line_charge_code": data.get("input_g_14"),
                    "charge_line_cost_local_amount": data.get("input_g_15"),
                    "charge_line_cost_os_amount": data.get("input_g_16"),
                    "charge_line_cost_os_currency_code": data.get("input_g_17"),
                    "charge_line_cost_os_gstvat_amount": data.get("input_g_18"),
                    "charge_line_creditor_type": data.get("input_g_19"),
                    "charge_line_creditor_key": data.get("input_g_20"),
                    "charge_line_department_code": data.get("input_g_21"),
                    "charge_line_display_sequence": data.get("input_g_22"),
                    "charge_line_import_metadata_instruction": data.get("input_g_23"),
                    "charge_line_supplier_reference": data.get("input_g_24"),
                    "customized_field_data_type": data.get("input_g_25"),
                    "customized_field_key": data.get("input_g_26"),
                    "customized_field_value": data.get("input_g_27")
                }         
    xml_writer = getattr(business, UtilFunctions().get_write_func_filename(option))
    datafile = await xml_writer(data)
    return {"message": "XML file successfully created"}

@app.post("/token")
def login_for_access_token(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    user = auth_method.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth_method.create_access_token(data={"username": user.username})
    
    # Set an HttpOnly cookie in the response. `httponly=True` prevents 
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        httponly=True
    )  
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}

@app.get("/auth/login", response_class=HTMLResponse)
def login_get(request: Request):
    is_user = auth_method.get_current_user_from_cookie(request)
    if is_user is None:
        context = {
            "request": request,
        }
        return templates.TemplateResponse("login.html", context)
    return RedirectResponse(url="/")



@app.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/", status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form)
            form.__dict__.update(msg="Login Successful!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


@app.get("/auth/logout", response_class=HTMLResponse)
def login_get():
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    return response

@app.get("/profile", response_class=HTMLResponse)
def index(request: Request, user: User = Depends(get_current_user_from_token)):
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("profile.html", context)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Exception handler for HTTPExceptions. Redirects the user to the login page if they are not authenticated.
    """
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/auth/login")

    return exc


@app.get("/view_xml/{filename}/{folder}/{status}", response_class=HTMLResponse)
async def view_xml(request: Request, filename: str, folder: str, status: str):
    decoded_text = decode_from_base64(folder)
    file_path = f"{decoded_text}/{status}/{filename}"
    with open(file_path, "r") as file:
        contents = file.read()

    xml_parser = getattr(business, UtilFunctions().get_func_filename(filename))
    data = await xml_parser(contents)

    return templates.TemplateResponse("table.html", {"data": data, "request": request, "filename": filename})

@app.get("/", response_class=HTMLResponse)
async def create_connection(request: Request):
    folder_path = "test_files"
    folder_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    return templates.TemplateResponse("connections.html", {"request": request, "folders": folder_names})


@app.get("/folder/{folder_name}")
async def folder_detail(request: Request, folder_name: str):
    folder_path = f"test_files/{folder_name}"
    if not os.path.isdir(folder_path):
        return responses.PlainTextResponse("Folder not found", status_code=404)
    files = os.listdir(folder_path)
    return templates.TemplateResponse("folder.html", {"request": request, "folder_name": folder_name, "files": files})

@app.post("/create_connection")
async def create_connection_post(request: Request,
    name: str = Form(...),
    location: str = Form(...),
    company: str = Form(...)
):

    folder_path = "test_files"

    folder_name = f"test_files/{name}_{company}"
    required_subfolders = ["request_to_trucker", "acknowledge", 
                "trucker_response", "trucker_event_instruction_planning",
                "trucker_event_instruction_actual", "arrival_on_site","pod_ppu"]
    UtilFunctions().create_subdirectories(folder_name, required_subfolders)

    folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    context = {"request": request, "folders": folders}
    return templates.TemplateResponse("connections.html", context=context)


@app.get("/get_template")
async def perform_operation(request: Request, folder_path: str):

    encoded_text = encode_to_base64(folder_path)
    accepted_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "accepted")
    rejected_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "rejected")
    pending_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "pending")
    return templates.TemplateResponse("index.html", {"request": request, "accepted_files": accepted_files, "rejected_files": rejected_files, "pending_files": pending_files})


@app.get("/showfolder")
async def show_folder(request: Request):
    return templates.TemplateResponse('folder.html', {"request": request})

@app.post("/perform_operation1")
async def perform_operation1(data: dict, request: Request):
    operation_id = data.get("operation_id", "")
    folder_name = data.get("folder_name", "")
    operation_folders = {
        1: "request_to_trucker",
        2: "acknowledge",
        3: "trucker_response",
        4: "trucker_event_instruction_planning",
        5: "trucker_event_instruction_actual",
        6: "arrival_on_site",
        7: "pod_ppu"
    }
    folder_path = f"test_files/{folder_name}/{operation_folders[operation_id]}"
    xml_files = UtilFunctions().list_directory(folder_path, ".xml")

    return {"url": "/get_template", "data": 1, "files":  xml_files, "folder_path": folder_path}

@app.post("/update_file_status")
def update_file_status(files: List[File]):
    files = files[0]
    decoded_text = decode_from_base64(files.folder)
    source_file = os.path.join(decoded_text, files.currentstatus , files.name)
    destination_file =  os.path.join(decoded_text, files.status , files.name)
    os.rename(source_file, destination_file)
    return {"message": "Successfully updated"}
