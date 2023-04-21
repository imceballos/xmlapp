from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse, HTMLResponse, Response

from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Annotated, Dict
from datetime import datetime, timedelta
import paramiko
import os
import uuid

from utils.auth import OAuth2PasswordBearerWithCookie, AuthenticationMethods
from utils.settings import Settings
from utils.models import User, File, get_user
from utils.login import LoginForm
from utils.utils import UtilFunctions
from utils.encrypt import decode_from_base64, encode_to_base64
from utils.sftp import SFTPDownloader

import business as business
import asyncio
import asyncssh

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


@app.get("/download/{filename}/{folder}/{status}")
async def download_file(folder: str, filename: str, status: str):
    """
    Endpoint that returns the content of a file as a download
    """
    decoded_text = decode_from_base64(folder)
    file_path = os.path.join(f"{decoded_text}/",status, filename)
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
    print("Estoy aca")
    print(data)
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
    elif option == "input_h_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_h_0"), 
                    "datatarget_type": data.get("input_h_1"), 
                    "datatarget_key": data.get("input_h_2"),
                    "company_code": data.get("input_h_3"),
                    "enterpriseid": data.get("input_h_4"),
                    "serverid": data.get("input_h_5"),
                    "description": data.get("input_h_6"),
                    "iscustom_description": data.get("input_h_7"),
                    "notetext": data.get("input_h_8"),
                    "notecontext_node": data.get("input_h_9"),
                    "visibility_code": data.get("input_h_10"),
                    "address_type": data.get("input_h_11"),
                    "organization_code": data.get("input_h_12"),
                    "customizedfield_datatype": data.get("input_h_13"),
                    "customized_field_key": data.get("input_h_14"),
                    "customized_field_value": data.get("input_h_15")
                }
        
    elif option == "input_i_0":
        data = {
                    "option": option, 
                    "filename": data.get("input__0"), 
                    "datatarget_type": data.get("input_i_1"), 
                    "datatarget_key": data.get("input_i_2"),
                    "company_code": data.get("input_i_3"),
                    "enterpriseid": data.get("input_i_4"),
                    "serverid": data.get("input_i_5"),
                    "transportbookingdirection_code": data.get("input_i_6"),
                    "transportBookingDirection_description": data.get("input_i_7"),
                    "addresstype": data.get("input_i_8"),
                    "organizationcode": data.get("input_i_9"),
                    "branch_code": data.get("input_i_10"),
                    "currency_code": data.get("input_i_11"),
                    "department_code": data.get("input_i_12"),
                    "chargeline_branch_code": data.get("input_i_13"),
                    "chargeline_chargecode_code": data.get("input_i_14"),
                    "chargeline_costlocalamount": data.get("input_i_15"),
                    "chargeline_costosamount": data.get("input_i_16"),
                    "chargeline_chargeline_costoscurrency_code": data.get("input_i_17"),
                    "chargeline_costosgstvatamount": data.get("input_i_18"),
                    "chargeline_creditor_type": data.get("input_i_19"),
                    "chargeline_creditor_key": data.get("input_i_20"),
                    "chargeline_department_code": data.get("input_i_21"),
                    "chargeline_displaysequence": data.get("input_i_22"),
                    "chargeline_importmetadata_instruction": data.get("input_i_23"),
                    "chargeline_supplierreference": data.get("input_i_24")
                }
        
    elif option == "input_j_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_j_0"), 
                    "status": data.get("input_j_1"), 
                    "dataSource_type": data.get("input_j_2"),
                    "dataSource_key": data.get("input_j_3"),
                    "companycode": data.get("input_j_4"),
                    "company_countrycode": data.get("input_j_5"),
                    "company_country_name": data.get("input_j_6"),
                    "company_name": data.get("input_j_7"),
                    "dataprovider": data.get("input_j_8"),
                    "enterpriseid": data.get("input_j_9"),
                    "serverid": data.get("input_j_10"),
                    "eventtime": data.get("input_j_11"),
                    "eventtype": data.get("input_j_12"),
                    "isestimate": data.get("input_j_13"),
                    "filename": data.get("input_j_14"),
                    "imagedata": data.get("input_j_15"),
                    "type_code": data.get("input_j_16"),
                    "type_description": data.get("input_j_17"),
                    "documentid": data.get("input_j_18"),
                    "ispublished": data.get("input_j_19"),
                    "savedateutc": data.get("input_j_20"),
                    "savedby_code": data.get("input_j_21"),
                    "savedby_name": data.get("input_j_22"),
                    "messagenumber": data.get("input_j_23")
                }

    elif option == "input_k_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_k_0"), 
                    "datatarget_type": data.get("input_k_1"), 
                    "datatarget_key": data.get("input_k_2"),
                    "company_code": data.get("input_k_3"),
                    "enterpriseid": data.get("input_k_4"),
                    "serverid": data.get("input_k_5"),
                    "description": data.get("input_k_6"),
                    "iscustomdescription": data.get("input_k_7"),
                    "notetext": data.get("input_k_8"),
                    "notecontext_code": data.get("input_k_9"),
                    "visibility_code": data.get("input_k_10"),
                    "addresstype": data.get("input_k_11"),
                    "organizationcode": data.get("input_k_12"),
                    "customizedfield_datatype": data.get("input_k_13"),
                    "customizedfield_key": data.get("input_k_14"),
                    "customizedfield_value": data.get("input_k_15")
                }
        
    elif option == "input_l_0":
        data = {
                    "option": option, 
                    "filename": data.get("input_l_0"), 
                    "datatarget_type": data.get("input_l_1"), 
                    "datatarget_key": data.get("input_l_2"),
                    "company_code": data.get("input_l_3"),
                    "enterpriseid": data.get("input_l_4"),
                    "serverid": data.get("input_l_5"),
                    "eventtime": data.get("input_l_6"),
                    "eventtype": data.get("input_l_7"),
                    "eventreference": data.get("input_l_8"),
                    "isestimate": data.get("input_l_9")
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
    with open(file_path, "rb") as file:
        contents = file.read()

    xml_parser = getattr(business, UtilFunctions().get_func_filename(filename))
    data = await xml_parser(contents)
    if any(file_path.endswith(ext) for ext in ('.jpg', '.png', '.txt', 'pdf')):
        return data

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
    #await asyncio.to_thread(downloader.download_files, folder_path)
    #await asyncio.gather(downloader.download_files(folder_path))
    #await asyncio.gather(download_new_files(folder_path))

    encoded_text = encode_to_base64(folder_path)
    folder_level = folder_path.split("/")[-1]
    accepted_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "accepted")
    rejected_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "rejected")
    pending_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "pending")
    return templates.TemplateResponse("index.html", {"request": request, "accepted_files": accepted_files, 
            "rejected_files": rejected_files, "pending_files": pending_files, "folder_level": folder_level})


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
async def update_file_status(files: List[File]):
    files = files[0]
    decoded_text = decode_from_base64(files.folder)
    source_file = f"{decoded_text}/{files.currentstatus}/{files.name}"
    destination_file =  f"{decoded_text}/{files.status}/{files.name}"
    if files.name in os.listdir(f"{decoded_text}/{files.status}"):
        if files.name.split('.')[0]+'-2'+'.xml' in os.listdir(f"{decoded_text}/{files.status}"):
            n=2
            for f in os.listdir(f"{decoded_text}/{files.status}"):
                if files.name.split('.')[0]+'-' in f:
                    last_n = int(f.split('-')[1].split('.')[0])
                    if last_n > n:
                        n = last_n
            os.rename(source_file, destination_file.split('.')[0]+'-'+str(n+1)+'.xml')
            n=3
        else:
            os.rename(source_file, destination_file.split('.')[0]+'-'+str(2)+'.xml')

    else:
        os.rename(source_file, destination_file)
    #await asyncio.to_thread(downloader.upload_files, destination_file, f"trufa/{files.status}/")
    return {"message": "Successfully updated"}
