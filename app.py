from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.responses import HTMLResponse, Response

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Annotated

import business as business
from datetime import datetime
from pydantic import BaseModel

import os
import re
import xml.etree.ElementTree as ET
import uuid

fake_users_db = {
    "iceballos": {
        "username": "iceballos",
        "full_name": "Israel Ceballos",
        "email": "iceballos@uc.uc",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "andrei": {
        "username": "andrei",
        "full_name": "Andrei Popescu",
        "email": "andrei@spvirgogroup.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


app = FastAPI()

# Mount static and template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
    The function receives a filepath and return any
    Input variables: filepath: str
    """
    if re.search(r'MESSAGE_XUD_DTYPE', filepath):
        return "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_READ"
    elif re.search(r'CW1', filepath):
        return "CW1_REQUEST_XUD_TIMESTAMP_READ"

def get_write_func_filename(option: str) -> str:
    mapper = {
        "input_a_0": "CW1_REQUEST_XUD_TIMESTAMP_WRITE",
        "input_b_0": "MESSAGE_XUD_DTYPE_TB_TIMESTAMP_WRITE"

    }
    return mapper.get(option, "")
    
@app.get("/")
async def index(request: Request):
    file_list = os.listdir("test_files")
    files = [{"name": file, "size": os.path.getsize(os.path.join("test_files", file))} for file in file_list]
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("test_files", filename)
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
async def show_form(request: Request):
    """
    View that displays a form with an input field for uploading a file
    """
    return templates.TemplateResponse("form.html", {"request": request})



@app.post("/form", response_class=HTMLResponse)
async def process_form(file: UploadFile, request: Request):
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

@app.post("/delete_file/{filename}")
async def delete_file(filename: str, request: Request):
    file_path = os.path.join("test_files", filename)
    try:
        os.remove(file_path)
        return {"message": f"Successfully deleted {filename}"}
        #file_list = os.listdir("test_files")
        #files = [{"name": file, "size": os.path.getsize(os.path.join("test_files", file))} for file in file_list]
        #return templates.TemplateResponse("index.html", {"request": request, "files": files, "message": f"Successfully deleted {filename}"})
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
    option = list(data.keys())[0]
    if option == "input_a_0":
        datas = {    
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
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user