import requests
import json

url = "http://127.0.0.1:5007/loginapp"

payload = json.dumps({
  "UserID": "0001",
  "AppID": "001",
  "Password": "6Ea)V"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
