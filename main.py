from VirusTotal import VTscan
from malwareb import download_file_from_malwarebazaar
from pathlib import Path
from PythonScriptsAnalysis import deobfuscate_pyarmor
from PythonScriptsAnalysis import analyze_python_code


eicar_test = "https://secure.eicar.org/eicar.com.txt"
zipped_malware = "https://bazaar.abuse.ch/sample/298bda6934276760168fae06a92b2f71e51368e6c9356ee693f5bf3982d00d77/"
url_test = "https://codeload.github.com/ParrotSec/mimikatz/zip/refs/heads/master"

vt = VTscan()

# print(vt.get_api_key())
# print(vt.get_url_analysis_report(url=eicar_test))

url_to_download = zipped_malware
downloaded_file_path = Path('/tmp/filetoscan.zip')
downloaded_file_path_unzipped = Path('/tmp/filetoscan_unzipped')

# Download the file from the URL
# vt.download_file(url_to_download, downloaded_file_path)
download_file_from_malwarebazaar(url_to_download, downloaded_file_path, downloaded_file_path_unzipped)

# Path to the script to be syntactically analysed
script_path_to_analyze = downloaded_file_path_unzipped

# Syntactic analysis of the script
analyze_python_code(script_path_to_analyze)


# Path to the file with the obfuscated script
obfuscated_file_path = downloaded_file_path_unzipped

# Path to the file where the deobfuscated script will be saved
deobfuscated_file_path = '/tmp/deobfuscated_file.py'

# Deobfuscation of the script before sending it for scanning
deobfuscate_pyarmor(obfuscated_file_path, deobfuscated_file_path)

# Submit the downloaded file for scanning
if downloaded_file_path.exists():
    data_id = vt.submit_file_for_scan(downloaded_file_path_unzipped)
    report = vt.generate_report(data_id)
    # print(report)
    # report_parsed = json.loads(report)
    print(report)
    stats_data = report['data']['attributes']['stats']
    print("Stats Data:")
    for key, value in stats_data.items():
        print(f"{key}: {value}")

# Delete the downloaded file after scanning
vt.delete_file(downloaded_file_path)
vt.delete_file(downloaded_file_path_unzipped)