import requests
import json

url = "http://127.0.0.1:5000/createpolicy"

payload = json.dumps({
  "Admin": {
    "id": 12345,
    "username": "Charan",
    "pass": "hehehelol"
  },
  "rules": {
    "min_length": 9,
    "max_length": 15,
    "min_upper": 4,
    "min_lower": 2,
    "min_number": 1,
    "min_specialchar": 2
  },
  "Batch_size": 50,
  "Hours_to_reset": "36"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)