from flask import Flask, request
import mysql.connector
from mysql.connector import errorcode
from Extra_Assign_users_Sql import *
app = Flask(__name__)


@app.route("/assignpass", methods=["POST"])

def assignpass():
  response = request.get_json()
  try:
    if response["Type"] == "new":
      try:
        insertsql(response)
      except mysql.connector.Error as err:
        return{"Error":str(err).split(':')[1]}
      except RanOutOfPsWs:
        return{"Error":"Ran out of passwords, please generate more"}
  except KeyError:
    return{"KeyError":"Missing Type of user"}

  return{"Database":"Updated"}

if __name__ == '__main__':
    app.run(debug=True, port=5001)
