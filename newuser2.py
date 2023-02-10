import pandas as pd
import mysql.connector
import hashlib
from mysql.connector import errorcode


def getrandom_pass():
    df = pd.read_csv('passwords batch.csv')
    random_value = df['Password'].sample().values[0]
    df = df[df['Password'] != random_value]
    df.to_csv('passwords batch.csv', index=False)
    return random_value

def insertsql(response):
    Legacy_apps = {"001": "App1", "002": "App2","003": "App3", "004": "App4", "005": "App5", "006": "App6", "007": "App7"}
    appID = response["Access"]
    userID = response["UserID"]
    name=response["UserName"]

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )

    mycursor = mydb.cursor(buffered=True)
    for i in appID:
        try:
            #calls the getrandom_pass function in order to get a random password from the batch
            psw=getrandom_pass()
        except ValueError:
            #if the passwords in the file are exhausted it raises this error
            raise RanOutOfPsWs
        query="INSERT INTO app_password VALUES (\""+str(userID)+"\",\""+str(Legacy_apps[i])+"\",\""+str(i)+"\",\""+str(psw)+"\");"
        mycursor.execute(str(query))
    try:
        pas = getrandom_pass()
        # Hashing the input password using sha1 algorithm
        psw = hashlib.sha1(pas.encode()).hexdigest()
        # Converting the hashed password to uppercase
        psw =psw.upper()
    except ValueError:
        raise RanOutOfPsWs
    query=str(f"INSERT INTO master_password VALUES(\"{userID}\",\"{name}\",\"{psw}\", \"reset\", NOW());")
    mycursor.execute(query)


class RanOutOfPsWs(Exception):
    pass