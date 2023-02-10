import requests
import json

url = "http://127.0.0.1:5002/updatepolicy"

payload = json.dumps({
  "Admin": {
    "id": 12345,
    "username": "Charan",
    "pass": "hehehelol"
  },
  "rules": {
    "min_length": 4,
    "max_length": 6,
    "min_upper": 1,
    "min_lower": 1,
    "min_number": 1,
    "min_specialchar": 1
  },
  "Batch_size": 50,
  "Days_to_reset": "2"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
