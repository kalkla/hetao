import requests
import json

# Test form data upload
upload_url = "http://localhost:5000/upload"

# Test with form data (multipart)
files = {
    'file': ('test.png', b'test image data', 'image/png')
}

data = {
    'purpose': 'collection'
}

# Note: We'll still get 401 Unauthorized since we're not logged in, but the 415 error should be resolved
response = requests.post(upload_url, files=files, data=data)
print(f"Form upload response: {response.status_code} - {response.text.encode('utf-8').decode('unicode_escape')}")

# Test with JSON data
json_data = {
    'image': 'base64_encoded_image',
    'purpose': 'collection'
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(upload_url, headers=headers, json=json_data)
print(f"JSON upload response: {response.status_code} - {response.text.encode('utf-8').decode('unicode_escape')}")