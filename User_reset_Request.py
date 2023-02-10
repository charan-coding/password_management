import requests
import json

url = "http://127.0.0.1:5003/resetmaster"

payload = json.dumps({
  "username": "Jane doe",
  "oldpassword": "57dgwkvgb3",
  "newpassword": "57dgwkvgb3"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
