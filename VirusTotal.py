import requests
import os
from dotenv import load_dotenv
import base64
import shutil

VT_url = "https://www.virustotal.com/api/v3/urls"
class VTscan():
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from the environment
        self.api_key = os.getenv("VT_API_KEY")
        self.headers = {
            "x-apikey": self.api_key
        }

        if not self.api_key:
            raise ValueError("API Key not found in the .env file.")
    def get_api_key(self):
        return self.api_key

    def download_file(self, url, file_path):
        # Download file from the provided URL
        response = requests.get(url, stream=True)
        print(response)
        if response.status_code == 200:
            # Save the downloaded content to the specified file path
            with open(file_path, "wb") as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                print("File downloaded successfully.")
                return file_path
        else:
            print(f"Failed to download file from the URL: {url}")
            return None
    def delete_file(self, file_path):
        try:
            # Delete the specified file
            file_path.unlink()
            print(f"File {file_path} deleted successfully.")
        except OSError as e:
            print(f"Error deleting the file: {e}")
    def submit_file_for_scan(self, file_path, password=None):
        # Check if the file is a zip file and handle it accordingly
        if file_path.suffix.lower() == '.zip' and password:
            files = {"file": (file_path.name, file_path.open('rb'))}
            params = {"password": password}
            response = requests.post("https://www.virustotal.com/api/v3/files", files=files, params=params, headers=self.headers)
        else:
            # Proceed with submitting the file without a password for scanning
            file_size = file_path.stat().st_size
            if file_size <= 32 * 1024 * 1024:
                print(f"file size: {file_size}B")
                files = {"file": (file_path.name, file_path.open('rb'), 'application/zip')}
                response = requests.post("https://www.virustotal.com/api/v3/files", files=files, headers=self.headers)
            else:
                print(f"file size: {file_size}B")
                print("File is too big, trying another API")
                params = {"filename": file_path.name}
                response = requests.post("https://www.virustotal.com/api/v3/files/upload_url", params=params, headers=self.headers)
                if response.status_code == 200:
                    upload_url = response.json()["data"]["attributes"]["url"]
                    with open(file_path, "rb") as file:
                        response = requests.put(upload_url, data=file, headers={"Content-Type": "application/octet-stream"})
        
        if response.status_code == 200:
            response_json = response.json()
            data_id = response_json['data']['id']
            print(f"File submitted for scanning. Data ID: {data_id}")
            return data_id
        else:
            print(f"Failed to submit file for scanning. Status code: {response.status_code}")
            return None
    
    def generate_report(self, data_id):
        url = f"https://www.virustotal.com/api/v3/analyses/{data_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            report_data = response.json()
            # Handle the report data as needed
            return report_data
        else:
            print(f"Failed to generate report. Status code: {response.status_code}")
            return None
        
    def get_url_scan_id(self, url:str) -> str:
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_key,
            "content-type": "application/x-www-form-urlencoded"
        }
        response = requests.post(VT_url, 
                                 data={ "url": url },
                                 headers=headers)
        if response.status_code == 200:
            response_json = response.json()  # Parse JSON response
            analysis_id = response_json['data']['id']  # Extract 'id' value
            print(response_json)
            return analysis_id
        else:
            print(f"Failed to fetch analysis report. Status code: {response.status_code}")
            return None  # Or raise an exception as per your requirement
    
    def get_url_analysis_report(self, url:str) -> dict:
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_key,
        }
        id = self.get_url_scan_id(url)
        print(id)
        print(VT_url + "/" + id)
        print(base64.b64encode(url.encode('utf-8')))
        response = requests.get(VT_url,
                                data={"url": base64.b64encode(url.encode('utf-8'))}, 
                                headers=headers)
        if response.status_code == 200:
            return response.json
        else:
            print(f"Failed to fetch analysis report. Status code: {response.status_code}")
            raise Exception
