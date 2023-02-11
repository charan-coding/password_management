from Extra_Create_policy_batch_Generation import leak_check
from flask import Flask, request
import requests

app = Flask(__name__)
@app.route("/checkleak", methods=["POST"])

def checkleak():
  response = request.get_json()
  password=response["password"]
  try:
    flag = leak_check(password)
  except requests.exceptions.HTTPError as errh:
    return {"Http Error": str(errh)}
  except requests.exceptions.ConnectionError as errc:
    return {"Connection Error": str(errc)}
  except requests.exceptions.Timeout as errt:
    return {"Timeout Error": str(errt)}
  except requests.exceptions.RequestException as err:
    return {"Undefined API Error": str(err)}
  if flag == 0:
    return{"Password":"Not Leaked Yet"}
  else:
    return {"Password": "Leaked"}

if __name__ == '__main__':
    app.run(debug=True, port=5009)
