import requests
import json

url = "http://127.0.0.1:5009/checkleak"

payload = json.dumps({
  "password": "37y8ugf"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)