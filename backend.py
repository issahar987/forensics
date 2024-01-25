from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from Utils.VirusTotal import VTscan
from Utils.ClamAV import clamAV_file_scan
from Utils.PythonScriptsAnalysis import analyze_python_code
from Utils.FileResults import results_file_preview, results_VT, results_ClamAV, results_AST
import json
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vt = VTscan()
app = FastAPI()
hold_results = {}
# Path to the script to be syntactically analysed
script_path_to_analyze = Path(__file__).parent / 'downloads' / 'file_to_scan'

# Allow requests from http://35.241.231.48:3000/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://35.241.231.48:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint that accepts a string using the POST method
@app.post("/send_url")
async def send_url(url_to_download: str):
    logger.info(f"Received URL to download: {url_to_download}")
    # Download the file from the URL
    vt.download_file(url_to_download, script_path_to_analyze)
    if script_path_to_analyze.exists():
        hold_results["results_file_preview"] = results_file_preview()
        hold_results["results_VT"] = results_VT(vt)
        hold_results["results_ClamAV"] = results_ClamAV()
        hold_results["results_AST"] = results_AST()
        return hold_results
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # elif:
    #     return {"error": "File wasn't dowloaded"}

# Endpoint that accepts a string using the POST method
@app.post("/get_preview")
async def get_preview(url_to_download: str):

    # Download the file from the URL
    vt.download_file(url_to_download, script_path_to_analyze)
    if script_path_to_analyze.exists():
        return results_file_preview()
    else:
        return {"error": "File wasn't dowloaded"}

# Endpoint with the GET method for VirusTotal scanning
@app.get("/virus_total_scan")
async def virus_total_scan():
    # Read the contents of 'result_VT.json'
    # result_path = Path(__file__).parent / 'downloads' / 'result_VT.json'
    # with open(result_path, 'r') as json_file:
    #     result_data = json.load(json_file)
    return hold_results["results_VT"]

# Endpoint with the GET method for ClamAV scanning
@app.get("/ClamAV_scan")
async def ClamAV_scan():
    # Read the contents of 'result_clamAV.json'
    # result_path = Path(__file__).parent / 'downloads' / 'result_clamAV.json'
    # with open(result_path, 'r') as json_file:
    #     result_data = json.load(json_file)
    return hold_results["results_ClamAV"]

# Endpoint with the GET method for Abstract Syntax Tree (AST) information
@app.get("/AST_info")
async def ast_info():
    # Read the contents of 'result_AST.json'
    # result_path = Path(__file__).parent / 'downloads' / 'result_AST.json'
    # with open(result_path, 'r') as json_file:
    #     result_data = json.load(json_file)
    return hold_results["results_AST"]

# Endpoint with the GET method for deobfuscation information
# @app.get("/deobfuscation_info")
# async def deobfuscation_info():
#     return {"message": "Deobfuscation information retrieved"}
