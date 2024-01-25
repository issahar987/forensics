from fastapi import FastAPI
from pathlib import Path
from Utils.VirusTotal import VTscan
from Utils.ClamAV import clamAV_file_scan
from Utils.PythonScriptsAnalysis import analyze_python_code
import json

vt = VTscan()
app = FastAPI()

# Endpoint that accepts a string using the POST method
@app.post("/send_url")
async def send_url(url_to_download: str):
    # Path to the script to be syntactically analysed
    script_path_to_analyze = Path(__file__).parent / 'downloads' / 'file_to_scan'

    # Download the file from the URL
    vt.download_file(url_to_download, script_path_to_analyze)
    if script_path_to_analyze.exists():
        data_id = vt.submit_file_for_scan(script_path_to_analyze)
        report = vt.generate_report(data_id)
        stats_data = report['data']['attributes']['stats']
        with open(Path(__file__).parent / 'downloads' / 'result_VT.json', 'w') as json_file:
            json.dump(stats_data, json_file, indent=4)
        clamAV_file_scan(script_path_to_analyze)
        # Syntactic analysis of the script
        # analyze_python_code(script_path_to_analyze)
    return {"received_url": url_to_download}

# Endpoint with the GET method for VirusTotal scanning
@app.get("/virus_total_scan")
async def virus_total_scan():
    # Read the contents of 'result_VT.json'
    result_path = Path(__file__).parent / 'downloads' / 'result_VT.json'
    with open(result_path, 'r') as json_file:
        result_data = json.load(json_file)
    return result_data

# Endpoint with the GET method for ClamAV scanning
@app.get("/ClamAV_scan")
async def clamav_scan():
    # Read the contents of 'result_clamAV.json'
    result_path = Path(__file__).parent / 'downloads' / 'result_clamAV.json'
    with open(result_path, 'r') as json_file:
        result_data = json.load(json_file)
    return result_data

# Endpoint with the GET method for Abstract Syntax Tree (AST) information
@app.get("/AST_info")
async def ast_info():
    # Read the contents of 'result_AST.json'
    result_path = Path(__file__).parent / 'downloads' / 'result_AST.json'
    with open(result_path, 'r') as json_file:
        result_data = json.load(json_file)
    return result_data

# Endpoint with the GET method for deobfuscation information
@app.get("/deobfuscation_info")
async def deobfuscation_info():
    return {"message": "Deobfuscation information retrieved"}
