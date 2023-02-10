import requests
import json

url = "http://127.0.0.1:5005/loginmaster"

payload = json.dumps({
  "username": "Jane doe",
  "password": "57dgwkvgb3"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)