from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse, HTMLResponse, Response
from sqlalchemy import create_engine

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import os

from utils.auth import OAuth2PasswordBearerWithCookie, AuthenticationMethods
from utils.settings import Settings
from utils.models import User, File
from utils.login import LoginForm
from utils.utils import UtilFunctions
from UtilFunctions import get_input_to_write
from utils.encrypt import decode_from_base64, encode_to_base64
from utils.ftp import FTPDownloader
from models.base import Base
from models.xmlapp_db import Person, Connections, Files

import business as business


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

settings = Settings()
auth_method = AuthenticationMethods(settings)
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token", settings = settings)

TEST_FILE = os.getenv("TEST_FILE")

ddd = FTPDownloader("ftp.virgogroup.com.sg", "testaccount@virgogroup.com.sg", "wetest#1")

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
    file_path = decode_from_base64(folder)
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
async def process_form(data: dict, request: Request, user: User = Depends(get_current_user_from_token)):
    """
    Given a dictonary, a new dictionary is created with the corresponding keys and values,
    and a function is called to write the data to an XML file.
    """
    current_user = Person.find_by_id(user.id)
    current_conn = Connections.find_by_connname(current_user.currentconn)
    current_conn_path = current_conn.path
    current_conn_uuid = current_conn.uuid
    base_folder_path = current_conn_path
    option = list(data.keys())[0]
    data=get_input_to_write(data, option)
    xml_writer = getattr(business, UtilFunctions().get_write_func_filename(option))
    datafile = await xml_writer(data, current_conn_path)
    filename = datafile.get("filename", "")
    path = encode_to_base64(datafile.get("path", ""))
    size = datafile.get("size", "")

    newfile = Files(filename, path, current_conn_uuid, "pending", "1", size)
    newfile.save()
    _ = await xml_writer(data)
    return {"message": "XML file successfully created"}

@app.post("/token")
def login_for_access_token(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    user = auth_method.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth_method.create_access_token(data={"username": user.first_name})
    
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
    response = RedirectResponse(url="/auth/login")
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
    file_path = decode_from_base64(folder)
    with open(file_path, "rb") as file:
        contents = file.read()

    xml_parser = getattr(business, UtilFunctions().get_func_filename(filename))
    data = await xml_parser(contents)
    if any(file_path.endswith(ext) for ext in ('.jpg', '.png', '.txt', 'pdf')):
        return data

    return templates.TemplateResponse("table.html", {"data": data, "request": request, "filename": filename})

@app.get("/", response_class=HTMLResponse)
async def create_connection(request: Request, user: User = Depends(auth_method.get_current_user_from_cookie)):
    if user:
        folder_path = "test_files"
        print("Quiero ver aca hou")
        conn_asigned = [conn.connname for conn in Connections.find_conn_assignedto(user.id)]
        #folder_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
        return templates.TemplateResponse("connections.html", {"request": request, "folders": conn_asigned})
        #return RedirectResponse(url="/")
    return RedirectResponse(url="/auth/login")

@app.get("/folder/{folder_name}")
async def folder_detail(request: Request, folder_name: str, user: User = Depends(auth_method.get_current_user_from_cookie)):
    folder_path = f"test_files/{folder_name}"
    person = Person.find_by_id(user.id)
    person.update({"currentconn": folder_name})
    if not os.path.isdir(folder_path):
        return responses.PlainTextResponse("Folder not found", status_code=404)
    return templates.TemplateResponse("folder.html", {"request": request, "folder_name": folder_name})

@app.post("/create_connection")
async def create_connection_post(request: Request,
    name: str = Form(...),
    ip: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    user: User = Depends(get_current_user_from_token)
):
    assigned_to = user.id
    conn = Connections(name, ip, username, password, assigned_to)
    folder_path = "test_files"
    folder_name = f"test_files/{name}"
    conn.path = folder_name
    conn.save()

    required_subfolders = ["frombollore", "tobollore", "staging"]
    UtilFunctions().create_subdirectories(folder_name, required_subfolders)
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    context = {"request": request, "folders": folders}

    #print("Ver filtering")
    gg = Connections.find_by_connname("testinghelloworld1234")
    return  {"message": "Successfully updated"}

@app.get("/get_template")
async def perform_operation(request: Request, folder_path: str, user: User = Depends(auth_method.get_current_user_from_cookie)):
    print(Person.find_by_email("imceballos1@gmail.com"))
    #await asyncio.to_thread(downloader.download_files, folder_path)
    #await asyncio.gather(downloader.download_files(folder_path))
    #await asyncio.gather(download_new_files(folder_path))

    #ddd.download_files(folder_path)
    print("que hay aca")
    print(user.currentconn)
    current_user = Person.find_by_id(user.id)
    current_conn = current_user.currentconn
    current_conn_uuid = Connections.find_by_connname(current_conn).uuid
    print(current_conn_uuid)
    accepted_files = Files.find_by_status_assignedto("accepted", current_conn_uuid)
    rejected_files = Files.find_by_status_assignedto("rejected", current_conn_uuid)
    pending_files = Files.find_by_status_assignedto("pending", current_conn_uuid)
    print("files",accepted_files, rejected_files, pending_files)
    encoded_text = encode_to_base64(folder_path)
    folder_level = folder_path.split("/")[-1]
    print("HELLO WORLD")
    print(folder_level, folder_path, encoded_text)
    #accepted_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "accepted")
    #rejected_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "rejected")
    #pending_files = UtilFunctions().get_files_by_condition(folder_path, encoded_text, "pending")
    return templates.TemplateResponse("index.html", {"request": request, "accepted_files": accepted_files, 
            "rejected_files": rejected_files, "pending_files": pending_files, "folder_level": folder_level,
            "folder_path": f"{folder_path}/"})


@app.get("/recover_password")
async def recover_password(request: Request):
    return templates.TemplateResponse("recover_password.html", {"request": request})


@app.get("/help")
async def help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})


@app.get("/showfolder")
async def show_folder(request: Request):
    return templates.TemplateResponse('folder.html', {"request": request})

@app.post("/perform_operation1")
async def perform_operation1(data: dict, request: Request):
    operation_id = data.get("operation_id", "")
    folder_name = data.get("folder_name", "")
    operation_folders = {
        0: "all_files",
        1: "request_to_trucker",
        2: "acknowledge",
        3: "trucker_response",
        4: "trucker_event_instruction_planning",
        5: "trucker_event_instruction_actual",
        6: "arrival_on_site",
        7: "pod_ppu"
    }        
    folder_path = f"test_files/{folder_name}"
    xml_files = UtilFunctions().list_directory(folder_path, ".xml")
    return {"url": "/get_template", "data": 1, "files":  xml_files, "folder_path": folder_path}

@app.post("/update_file_status")
async def update_file_status(files: List[File]):
    print("HORA DE VER ACA UPDATE")
    print(files)
    file_name = files[0].name
    file_folder = decode_from_base64(files[0].folder)
    file_status = files[0].status
    file_currentstatus = files[0].currentstatus
    source_file = file_folder
    print(file_folder, file_status)
    destination_file = UtilFunctions().replace_path(file_folder, file_status)
    file_updated = Files.find_by_path(encode_to_base64(file_folder))
    file_updated.update({"status": file_status})
    
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
    return {"message": "Successfully updated"}


@app.post("/download_files_ftp")
async def download_files_ftp(data: dict, user: User = Depends(auth_method.get_current_user_from_cookie)):
    print("VER NOW")
    print(data)
    received_files = ddd.download_files(data["folder_path"])
    current_user = Person.find_by_id(user.id)
    current_conn = Connections.find_by_connname(current_user.currentconn)
    current_conn_uuid = current_conn.uuid
    for cfile in received_files:
        if not Files.find_by_filename_assignedto(cfile.get("filename"), current_conn_uuid):
            newfile = Files(cfile.get("filename"), encode_to_base64(cfile.get("path")), current_conn_uuid, "pending", "1", cfile.get("size"))
            newfile.save()
    return {"message": "Successfully updated"}

@app.post("/send_files_ftp")
async def download_files_ftp(data: dict):
    print("estoy aca")
    folder_path = decode_from_base64(data["folder_path"])
    print(folder_path)
    #file_path = os.path.join(folder_path, f"{data['status']}/", data["filename"])
    print("Corrio el post o no")
    ddd.upload_file(folder_path)
    return {"message": "Successfully updated"}
