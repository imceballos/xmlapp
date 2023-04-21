import io
import base64
import pdfplumber

async def JPG_READ(file: str):
    file_type = "png"
    image = base64.b64encode(file).decode("utf-8")
    template = f'<html><body><img src="data:image/{file_type};base64,{image}"/></body></html>'
    return template

async def TXT_READ(file: str):
    template = f'<html><body><pre>{file}</pre></body></html>'
    return template

async def PDF_READ(file: str):
    pdf_file = io.BytesIO(file)

    with pdfplumber.open(pdf_file) as pdf:
        pages = pdf.pages
        content = ''
        for page in pages:
            content += page.extract_text()
    
    template = f'<html><body><pre>{content}</pre></body></html>'
    return template

