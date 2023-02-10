from flask import Flask, request
import mysql.connector

app = Flask(__name__)
@app.route("/loginapp", methods=["POST"])

def loginapp():
    creds = request.get_json()
    userID = creds["UserID"]
    password = creds["Password"]
    AppID = creds["AppID"]
    try:
        out = validate_app(userID, password,AppID)
        if out == 0:
            return {"Auth": "Failed"}
        return {"Auth": "Success"}

    except mysql.connector.Error as error:
        return {"Error": format(error)}


def validate_app(userID, password,appID):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = conn.cursor()
    query = "SELECT *  FROM app_password WHERE USER_ID = %s AND password = %s AND App_ID = %s"
    cursor.execute(query, (userID, password, appID))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        return 0
    else:
        return 1


if __name__ == '__main__':
    app.run(debug=True, port=5007)
