from utils import convert_file_to_epub
from utils import download_storage_tmp
from utils import upload_output
from fastapi import FastAPI
from model import Item
import os

from pydantic import BaseModel

app = FastAPI()
app.title = "API - Calibre Epub Converter"
app.version = "0.0.1"

class Message(BaseModel):
    message: str

@app.get("/", tags=["Settings"])
def home():
    return {"health_check": "OK", "model_version": "1.1"}

@app.post("/convert2epub")
def convert2epub(item: Item): 
    """Converts a file to EPUB format and uploads the result to Cloud Storage.

    This function handles a POST request to the "/convert2epub" endpoint. 
    It expects an `Item` object in the request body containing the input 
    bucket and file path.

    The function performs the following steps:

    1. Downloads the file from Cloud Storage.
    2. Converts the downloaded file to EPUB format using Calibre.
    3. Uploads the converted EPUB to the specified output bucket in Cloud Storage.
    4. Returns a JSON response with status code, message, and the uploaded file URL.

    Args:
        item: An Item object containing the input bucket name and file path.

    Returns:
        A dictionary containing the following keys:
            statusCode (int): HTTP status code (200 for success, 500 for error).
            message (str): Descriptive message about the conversion process.
            url (str): Public URL of the uploaded EPUB file (if successful).
    """
    
    payload = {
        "statusCode": None,
        "message": None,
        "url": None
    }

    try:
        input_file_name = download_storage_tmp(item)
        output_file_name = convert_file_to_epub(input_file_name)
        output_url = upload_output(item, output_file_name)
    except (RuntimeError, FileNotFoundError) as e:
        payload["statusCode"], payload["message"] = 500, str(e)
    except:
        payload["statusCode"], payload["message"] = 500, f"Something went wrong. Review the data provided {item}"
    else:
        payload["statusCode"] = 200
        payload["message"] = "File converted and copied successfully"
        payload["url"] = output_url
        os.remove(input_file_name)
        os.remove(output_file_name)
    finally:
        return payload