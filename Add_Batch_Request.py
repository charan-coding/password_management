import requests
import json

url = "http://127.0.0.1:5004/addbatch"

payload = json.dumps({
  "number": 10
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
