from flask import Flask, request
import mysql.connector
import hashlib
from batch_gen_pass  import *
import requests


app = Flask(__name__)
@app.route("/resetmaster", methods=["POST"])

def resetmaster():
    creds=request.get_json()
    username=creds["username"]
    oldpassword = creds["oldpassword"]
    newpassword = creds["newpassword"]

    if leak_check(newpassword)==1:
        return{"Can't use password": "It has been leaked"}
    psw1 = hashlib.sha1(newpassword.encode()).hexdigest()
    # Converting the hashed password to uppercase
    psw1 = psw1.upper()
    # Hashing the input password using sha1 algorithm
    psw = hashlib.sha1(oldpassword.encode()).hexdigest()
    # Converting the hashed password to uppercase
    psw = psw.upper()
    try:
        out=validate_username_password(username, psw)
        if out==2:
            return{"Account":"Disabled"}
        if out==1:
            update_password(username, psw1)
            return{"Password":"Updated"}
        else:
            return{"Wrong":"Old Password"}

    except mysql.connector.Error as error:
        return{"Error":format(error)}

def validate_username_password(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = conn.cursor()
    query = "SELECT USER_ID, State FROM master_password WHERE user_name = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        return 0
    if result[1]=="disabled":
        return 2
    else:
        return 1


def update_password(username, new_password):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = conn.cursor()
    query = "UPDATE master_password SET password = %s, state= 'enabled' WHERE user_name = %s"
    cursor.execute(query, (new_password, username))
    conn.commit()
    cursor.close()
    conn.close()





if __name__ == '__main__':
    app.run(debug=True, port=5003)
