import requests
import json

url = "http://127.0.0.1:5006/adminreset"

payload = json.dumps({
  "Admin": {
    "id": 12345,
    "username": "Charan",
    "pass": "hehehelol"
  },
  "username": "Janis Doe"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)