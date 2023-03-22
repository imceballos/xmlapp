from fastapi import FastAPI, Request, Form, File, UploadFile
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse

from fastapi.responses import HTMLResponse, Response

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import business as business
from datetime import datetime
from pydantic import BaseModel

import os
import re
import xml.etree.ElementTree as ET
import uuid

app = FastAPI()

# Mount static and template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_file_info(filepath: str):
    """
    Given a filepath, return the filename, size, and creation date of the file
    """
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    creation_date = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
    return {"filename": filename, "size": size, "creation_date": creation_date}

def get_func_filename(filepath: str) -> str:
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


@app.get("/formpost", response_class=HTMLResponse)
async def post_form(request: Request):
    """
    View that displays a form with an input field for uploading a file
    """
    return templates.TemplateResponse("formpost.html", {"request": request})


@app.post("/formpost")
async def process_form(data: dict, request: Request):
    option = list(data.keys())[0]
    if option == "input_a_1":
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
    elif option == "input_b_1":
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
                    "filename": data.get("input_b_11"),
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

# esto es una pruba
# esto es otra pruba