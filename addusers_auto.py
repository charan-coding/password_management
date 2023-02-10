import requests
import json

url = "http://127.0.0.1:5001/assignpass"

payload = json.dumps({
  "Type": "new",
  "Admin": {
    "id": 12345,
    "username": "Charan",
    "pass": "hehehelol"
  },
  "UserID": "0001",
  "UserName": "Jane doe",
  "Access": [
    "001",
    "002",
    "003"
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
payload = json.dumps({
  "Type": "new",
  "Admin": {
    "id": 12345,
    "username": "Charan",
    "pass": "hehehelol"
  },
  "UserID": "0002",
  "UserName": "John doe",
  "Access": [
    "001",
    "002"
  ]
})
response = requests.request("POST", url, headers=headers, data=payload)
payload = json.dumps({
  "Type": "new",
  "Admin": {
    "id": 12345,
    "username": "Charan",
    "pass": "hehehelol"
  },
  "UserID": "0003",
  "UserName": "Janis doe",
  "Access": [
    "001",
    "002",
    "004"
  ]
})
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)