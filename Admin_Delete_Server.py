from flask import Flask, request
import mysql.connector
import hashlib
from Extra_Create_policy_Validation import *


app = Flask(__name__)
@app.route("/admindelete", methods=["POST"])

def admindelete():
    creds = request.get_json()
    try:
        authenticate(creds["Admin"]["id"], creds["Admin"]["pass"])

    except KeyError:
        return{"BadAuthError": "Missing authentication info"}

    except InvalidCredentials:
        return {"BadAuthError": "Invalid Creds"}

    userID=creds["userID"]
    try:
        if notexists(userID):
            return{"User":"Does not exist"}
    except mysql.connector.Error as error:
        return {"MYSQL 1 Error:": format(error)}

    try:
        revoke(userID)
    except mysql.connector.Error as error:
        return{"MYSQL 2 Error:":format(error)}

    return{"User":"Deleted"}

def revoke(user_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = conn.cursor()
    delete_query1 = "DELETE FROM master_password WHERE user_id = %s"
    cursor.execute(delete_query1, (user_id,))
    delete_query2 = "DELETE FROM app_password WHERE user_id = %s"
    cursor.execute(delete_query2, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def notexists(user_id):
    conn = conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = conn.cursor()
    select_query1 = "SELECT * FROM master_password WHERE user_id = %s"
    cursor.execute(select_query1, (user_id,))
    master_result = cursor.fetchone()
    cursor.close()
    conn.close()
    if master_result is not None:
        return False
    else:
        return True

if __name__ == '__main__':
    app.run(debug=True, port=5008)