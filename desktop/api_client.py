import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def upload_csv(file_path):
    url = f"{API_BASE_URL}/upload/"

    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Upload failed: {response.text}")
