from flask import Flask, request
import mysql.connector
import hashlib
import pandas as pd
import datetime

app = Flask(__name__)
@app.route("/loginmaster", methods=["POST"])

def loginmaster():
    creds=request.get_json()
    username=creds["username"]
    password=creds["password"]
    # Hashing the input password using sha1 algorithm
    psw = hashlib.sha1(password.encode()).hexdigest()
    # Converting the hashed password to uppercase
    psw = psw.upper()
    if is_expired(username):
        return{"Reset Password":"Required"}
    try:
        out=validate_username_password(username, psw)
        if out!=0:
            if out == "reset":
                return{"Reset Password":"Required"}
            return retrieve_app_passwords(out)

        else:
            return{"Access":"Denied"}

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
    query = "SELECT USER_ID, State, date  FROM master_password WHERE user_name = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        return 0
    elif result[1] != 'enabled':
        return 'reset'
    else:
        return result[0]

def retrieve_app_passwords(userID):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hehehelol",
            database="pms",
            autocommit=True
        )
        cursor = conn.cursor()
        query = "SELECT App_ID, password FROM app_password WHERE USER_ID = %s"
        cursor.execute(query, (userID,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        out = {}
        for app_id, password in result:
            out[app_id] = password
        return out

def is_expired(username):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hehehelol",
            database="pms",
            autocommit=True
        )
        cursor = conn.cursor()
        query = "SELECT date FROM master_password WHERE user_name = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()


        if result is None:
            return False

        last_update = result[0]
        print(last_update)
        print(datetime.datetime.now().date())
        time_diff = datetime.datetime.now().date() - last_update
        print(time_diff)
        df = pd.read_csv('policy.csv')

        if time_diff.days >= int(df["Days_to_reset"]):
            update_query = "UPDATE master_password SET state = 'disabled' WHERE user_name = %s"
            cursor = conn.cursor()
            cursor.execute(update_query, (username,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            return False


if __name__ == '__main__':
    app.run(debug=True, port=5005)
