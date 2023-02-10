from flask import Flask, request
import mysql.connector
import hashlib
from Extra_Create_policy_Validation import *


app = Flask(__name__)
@app.route("/adminreset", methods=["POST"])

def adminreset():
    creds = request.get_json()
    try:
        authenticate(creds["Admin"]["id"], creds["Admin"]["pass"])

    except KeyError:
        return{"BadAuthError": "Missing authentication info"}

    except InvalidCredentials:
        return {"BadAuthError": "Invalid Creds"}

    username=creds["username"]
    reset_state(username)
    return{"State":"Updated"}

def reset_state(username):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = conn.cursor()
    update_query = "UPDATE master_password SET state = 'reset' WHERE user_name = %s"
    cursor.execute(update_query, (username,))
    conn.commit()
    cursor.close()
    conn.close()





if __name__ == '__main__':
    app.run(debug=True, port=5006)