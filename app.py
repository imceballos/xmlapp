from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse
from passlib.context import CryptContext

from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
import json
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Annotated
from jose import JWTError, jwt
import base64
from datetime import datetime, timedelta

import os
import re
import xml.etree.ElementTree as ET
from typing import Dict
import uuid

from utils.auth import OAuth2PasswordBearerWithCookie
from utils.auth import AuthenticationMethods
from utils.settings import Settings
from utils.models import User, get_user
from utils.login import LoginForm
import business as business


app = FastAPI()

# Mount static and template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
settings = Settings()
auth_method = AuthenticationMethods(settings)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token", settings = settings)


def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    user = auth_method.decode_token(token)
    return user


def get_file_info(filepath: str) -> dict:
    """
    Given a filepath, return the filename, size, and creation date of the file
    """
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    creation_date = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
    return {"filename": filename, "size": size, "creation_date": creation_date}

def get_func_filename(filepath: str) -> str:
    """
    Get a string as input (filepath) and returns another string as output.
    If the string contains the pattern "MESSAGE_XUD_DTYPE",  
    returns "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_READ". If contains the pattern "CW1" 
    returns the string "CW1_REQUEST_XUD_TIMESTAMP_READ"
    """
    if re.search(r'MESSAGE_XUD_DTYPE', filepath):
        return "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_READ"
    elif re.search(r'CW1', filepath):
        return "CW1_REQUEST_XUD_TIMESTAMP_READ"

def get_write_func_filename(option: str) -> str:
    """
    Given a string as input (option), returns another string as output according to the dictionary
    """
    mapper = {
        "input_a_0": "CW1_REQUEST_XUD_TIMESTAMP_WRITE",
        "input_b_0": "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_WRITE"

    }
    return mapper.get(option, "")
    
@app.get("/")
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
    encoded_bytes = folder.encode('ascii')

    # Use Base64 to decode the bytes
    decoded_bytes = base64.b64decode(encoded_bytes)

    # Convert the decoded bytes to a string
    decoded_text = decoded_bytes.decode('ascii')
    file_path = os.path.join(decoded_text, filename)
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@app.get("/file/{filename}")
async def read_file(filename: str):
    """
    Endpoint that returns the file info for a specific file
    """
    filepath = os.path.join("xml_files", filename)
    if os.path.isfile(filepath) and filename.endswith(".xml"):
        return get_file_info(filepath)
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
    # Generate a unique filename
    #filename = f"{uuid.uuid4()}.xml"
    
    # Save the uploaded file to disk
    contents = await file.read()
    filename = file.filename
    
    xml_parser = getattr(business, get_func_filename(filename))

    data = await xml_parser(contents)
    
    return templates.TemplateResponse("table.html", {"data": data, "request": request})

@app.post("/delete_file/{filename}/{folder}")
async def delete_file(request: Request, filename: str, folder: str):
    encoded_bytes = folder.encode('ascii')

    # Use Base64 to decode the bytes
    decoded_bytes = base64.b64decode(encoded_bytes)

    # Convert the decoded bytes to a string
    decoded_text = decoded_bytes.decode('ascii')
    file_path = os.path.join(decoded_text, filename)
    try:
        os.remove(file_path)
        return {"message": f"Successfully deleted {filename}"}
    except FileNotFoundError:
        return {"error": f"File not found: {filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/formpost", response_class=HTMLResponse)
async def post_form(request: Request, user: User = Depends(get_current_user_from_token)):
    """
    View that displays a form with an input field for uploading a file
    """
    return templates.TemplateResponse("formpost.html", {"request": request})


@app.post("/formpost")
async def process_form(data: dict, request: Request, user: User = Depends(get_current_user_from_token)):
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
    xml_writer = getattr(business, get_write_func_filename(option))
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
    expires = request.cookies
    print("sfdjknfsrjkf")
    print(expires)
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
        # user is not authenticated, redirect to the login view
        return RedirectResponse(url="/auth/login")

    # for all other HTTPExceptions, return the exception as is
    return exc


@app.get("/view_xml/{filename}/{folder}/{status}", response_class=HTMLResponse)
async def view_xml(request: Request, filename: str, folder: str, status: str):
    print("ESTOY ACA")
    print(filename)
    print(folder)
    print(status)
    encoded_bytes = folder.encode('ascii')

    # Use Base64 to decode the bytes
    decoded_bytes = base64.b64decode(encoded_bytes)

    # Convert the decoded bytes to a string
    decoded_text = decoded_bytes.decode('ascii')
    file_path = f"{decoded_text}/{status}/{filename}"
    print(filename, folder, file_path, decoded_text)
    with open(file_path, "r") as file:
        contents = file.read()

    xml_parser = getattr(business, get_func_filename(filename))
    data = await xml_parser(contents)

    return templates.TemplateResponse("table.html", {"data": data, "request": request, "filename": filename})

@app.get("/create_connection", response_class=HTMLResponse)
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
    # Create the connection object
    #connection = Connection(name=name, location=location, company=company)
    folder_path = "test_files"

    # Create the folder
    folder_name = f"test_files/{name}_{company}"
    required_subfolders = ["request_to_trucker", "acknowledge", 
                "trucker_response", "trucker_event_instruction_planning",
                "trucker_event_instruction_actual", "arrival_on_site","pod_ppu"]
    os.mkdir(folder_name)
    for subfolder in required_subfolders:
        os.mkdir(f"{folder_name}/{subfolder}")
        os.mkdir(f"{folder_name}/{subfolder}/accepted")
        os.mkdir(f"{folder_name}/{subfolder}/rejected")
        os.mkdir(f"{folder_name}/{subfolder}/pending")

    # TODO: Save the connection and folder information to a database

    # Return a success message
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    # Render the HTML template with the folder names
    context = {"request": request, "folders": folders}
    return templates.TemplateResponse("connections.html", context=context)

class OperationRequest(BaseModel):
    operation_id: dict

@app.get("/get_template")
async def perform_operation(request: Request, folder_path: str):
    #folder_path = request.query_params.get("folder_path", "")
    #folder_path = json.loads(folder_path) if folder_path else []
    file_list = os.listdir(folder_path)
    
    text_bytes = folder_path.encode('ascii')

    # Use Base64 to encode the bytes
    encoded_bytes = base64.b64encode(text_bytes)

    # Convert the encoded bytes to a string
    encoded_text = encoded_bytes.decode('ascii')
    accepted_files = [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/accepted", file)), "folder": encoded_text} for file in os.listdir(f"{folder_path}/accepted")]
    rejected_files = [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/rejected", file)), "folder": encoded_text} for file in os.listdir(f"{folder_path}/rejected")]
    pending_files = [{"name": file, "size": os.path.getsize(os.path.join(f"{folder_path}/pending", file)), "folder": encoded_text} for file in os.listdir(f"{folder_path}/pending")]

    files = [{"name": file, "size": os.path.getsize(os.path.join(folder_path, file)), "folder": encoded_text} for file in file_list]
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
    xml_files = [f for f in os.listdir(folder_path) if f.endswith(".xml")]
    
    # Do some operation here based on the operation_id
    # Render the corresponding template and return it as an HTML response
    return {"url": "/get_template", "data": 1, "files":  xml_files, "folder_path": folder_path}

class File(BaseModel):
    name: str
    folder: str
    status: str
    currentstatus: str

@app.post("/update_file_status")
def update_file_status(files: List[File]):
    files = files[0]
    encoded_bytes = files.folder.encode('ascii')
    # Use Base64 to decode the bytes
    decoded_bytes = base64.b64decode(encoded_bytes)
    current_status = files.currentstatus
    # Convert the decoded bytes to a string
    decoded_text = decoded_bytes.decode('ascii')
    # construct the full paths for the source and destination files
    source_file = os.path.join(decoded_text, current_status , files.name)
    destination_file =  os.path.join(decoded_text, files.status , files.name)
    # use os.rename() to move the file from the source to the destination folder
    os.rename(source_file, destination_file)
    return {"message": "Successfully updated"}
