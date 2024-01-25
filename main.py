from Utils.VirusTotal import VTscan
from Utils.ClamAV import clamAV_file_scan
# from Utils.malwareb import download_file_from_malwarebazaar
from pathlib import Path
from Utils.PythonScriptsAnalysis import deobfuscate_python_code
from Utils.PythonScriptsAnalysis import analyze_python_code

current_folder = Path(__file__).parent

eicar_test = "https://secure.eicar.org/eicar.com.txt"
zipped_malware = "https://bazaar.abuse.ch/sample/298bda6934276760168fae06a92b2f71e51368e6c9356ee693f5bf3982d00d77/"
url_test = "https://codeload.github.com/ParrotSec/mimikatz/zip/refs/heads/master"
python_file_url = "https://raw.githubusercontent.com/spicesouls/Malware-Dump/main/OSX/Python/snap.py"

vt = VTscan()

# url to download
url_to_download = python_file_url
# Path to the script to be syntactically analysed
download_folder_path = current_folder / 'downloads'
if not download_folder_path.exists():
    download_folder_path.mkdir(parents=True)
script_path_to_analyze = download_folder_path / 'file_to_scan'

# Download the file from the URL
vt.download_file(url_to_download, script_path_to_analyze)

# Syntactic analysis of the script
# analyze_python_code(script_path_to_analyze)

# Path to the file with the obfuscated script
# obfuscated_file_path = script_path_to_analyze
# # Path to the file where the deobfuscated script will be saved
output_path = download_folder_path / 'deobfuscated_script.py'
# deobfuscated_file_path = current_folder / 'downloads' / 'deobfuscated_file.py'

# # Deobfuscation of the script before sending it for scanning
# deobfuscate_pyarmor(obfuscated_file_path, deobfuscated_file_path)
deobfuscate_python_code(script_path_to_analyze, output_path)

# Submit the downloaded file for scanning
if script_path_to_analyze.exists():
    data_id = vt.submit_file_for_scan(script_path_to_analyze)
    report = vt.generate_report(data_id)
    stats_data = report['data']['attributes']['stats']
    print("Virus Total Stats Data:")
    for key, value in stats_data.items():
        print(f"{key}: {value}")

clamAV_file_scan(script_path_to_analyze)

# Delete the downloaded file after scanning
# vt.delete_file(script_path_to_analyze)