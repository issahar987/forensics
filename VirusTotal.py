import requests


class VTscan():
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from the environment
        self.api_key = os.getenv("API_KEY")

        if not self.api_key:
            raise ValueError("API Key not found in the .env file.")
    def get_api_key(self):
        return self.api_key