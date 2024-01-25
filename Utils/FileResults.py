import magic
from pathlib import Path
from VirusTotal import VTscan
from ClamAV import clamAV_file_scan
from time import sleep
from PythonScriptsAnalysis import analyze_python_code


# Path to the script to be syntactically analysed
script_path_to_analyze = Path(__file__).parents[1] / 'downloads' / 'file_to_scan'

def results_file_preview() -> dict:
    preview = {}
    preview["file_type"] = magic.from_file(script_path_to_analyze)
    preview["file_size"] =  f"{round(script_path_to_analyze.stat().st_size / (1024 * 1024), 3)}MB"
    print(preview)
    return preview

def results_VT(vt: VTscan) -> dict:
    # if script_path_to_analyze.exists():
    data_id = vt.submit_file_for_scan(script_path_to_analyze)
    sleep(2)
    report = vt.generate_report(data_id)
    VT_results = report['data']['attributes']['stats']
    print(VT_results)
    return VT_results

def results_ClamAV() -> dict:
    return clamAV_file_scan(script_path_to_analyze)

def results_AST() -> dict:
    try:
        return analyze_python_code(script_path_to_analyze)
    except Exception as e:
        print(e)
        return "This is not a script"

# results_file_preview()
# results_VT(vt = VTscan())
# results_ClamAV()
# results_AST()