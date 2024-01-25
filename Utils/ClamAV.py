import pyclamd
import pathlib

def clamAV_file_scan(file_path: pathlib.Path) -> None:
    file_path_str = str(file_path)
    try:
        cd = pyclamd.ClamdUnixSocket()

        # Check if the connection to the ClamAV daemon is active
        if not cd.ping():
            print('No connection to the ClamAV daemon.')
            return

        # Check the file
        scan_result = cd.scan_file(file_path_str)
        if not scan_result:
            return {'scan_result': "Cannot scan file of this type"}
        if scan_result[file_path_str] == 'OK':
            print(f'The file {file_path_str} is safe.')
        else:
            print(f'The file {file_path_str} is potentially unsafe! Scan result: {scan_result[file_path_str]}')
        # Save the scan results to a JSON file
        return {
            'scan_result': scan_result[file_path_str]
        }
        # with open(Path(__file__).parent / 'downloads' / 'result_clamAV.json', 'w') as json_file:
        #     json.dump(result_data, json_file, indent=4)
        # print("Scan results saved to 'result_clamAV.json'")
    except pyclamd.ConnectionError:
        print('Error connecting to the ClamAV daemon.')
        return {'scan_result': 'Error connecting to the ClamAV daemon.'}
