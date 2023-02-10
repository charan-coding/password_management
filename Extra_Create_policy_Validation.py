from datetime import date
import csv
import os
import time
import mysql.connector
import pandas as pd
from Extra_Assign_users_Sql import *

def authenticate(id_no, psw):
    if id_no != 12345 or psw != "hehehelol":
        raise InvalidCredentials


def check_and_validate(policy):
    csv_dict = policy["rules"]
    csv_dict["Days_to_reset"] = policy["Days_to_reset"]
    today = date.today()
    csv_dict["updatedOn"] = today.strftime("%B %d, %Y")

    if "min_upper" not in csv_dict.keys():
        csv_dict["min_upper"] = 0
    if "min_lower" not in csv_dict.keys():
        csv_dict["min_lower"] = 0
    if "min_number" not in csv_dict.keys():
        csv_dict["min_number"] = 0
    if "min_specialchar" not in csv_dict.keys():
        csv_dict["min_specialchar"] = 0

    if int(csv_dict["min_upper"])<0:
        raise InvalidRange()
    if int(csv_dict["min_lower"])<0:
        raise InvalidRange()
    if int(csv_dict["min_number"])<0:
        raise InvalidRange()
    if int(csv_dict["min_specialchar"])<0:
        raise InvalidRange()

    total_chars = csv_dict["min_upper"] + csv_dict["min_lower"] + csv_dict["min_number"] + csv_dict["min_specialchar"]

    if int(csv_dict["min_length"]) < total_chars:
        raise InvalidRules1
    if int(csv_dict["max_length"]) > 20:
        raise InvalidRules3
    if csv_dict["max_length"] < total_chars:
        raise InvalidRules2

    try:
        if policy["Batch_size"]>50 or policy["Batch_size"]<1:
            raise BadSize
    except KeyError:
        raise MissingBatch
    return csv_dict

class InvalidRules1(Exception):
    pass


class InvalidRules2(Exception):
    pass


class InvalidRules3(Exception):
    pass


class InvalidCredentials(Exception):
    pass

class InvalidRange(Exception):
    pass

class MissingBatch(Exception):
    pass

class BadSize(Exception):
    pass

def write(csv_dict):
    df = pd.DataFrame([csv_dict])
    df.to_csv("policy.csv", index=False)


def up_write(csv_dict):
    df1 = pd.DataFrame([csv_dict])
    df1.to_csv("policy.csv", index=False)

def sql(csv_dict):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        autocommit=True
    )
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("CREATE DATABASE IF NOT EXISTS pms;")
    mycursor.execute("USE pms;")
    mycursor.execute("SHOW TABLES;")
    mycursor.execute("DROP TABLE IF EXISTS APP_PASSWORD;")
    mycursor.execute("DROP TABLE IF EXISTS MASTER_PASSWORD;")
    mycursor.execute(
        "CREATE TABLE app_password (USER_ID char(4) NOT NULL,App_name varchar(20),App_ID char(3) NOT NULL, password varchar(25));")
    mycursor.execute(
        "CREATE TABLE master_password(USER_ID char(4) NOT NULL Primary Key,user_name varchar(20), password varchar(128), state varchar(25), date DATE);")
    for x in mycursor:
        print(x)

def up_sql():
    # Connect to the database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hehehelol",
        database="pms",
        autocommit=True
    )
    cursor = cnx.cursor()

    # Update the value of the column "status" to "reset" in the table "master_password"
    update_master_password = "UPDATE master_password SET state = 'reset'"
    cursor.execute(update_master_password)
    cnx.commit()

    # Select all rows from the "app_password" table
    select_app_password = "SELECT * FROM app_password"
    cursor.execute(select_app_password)
    rows = cursor.fetchall()

    # Replace the value of the "password" column with a new random password for each row
    for row in rows:
        new_password = getrandom_pass()
        update_app_password = f"UPDATE app_password SET password = '{new_password}' WHERE USER_ID = '{row[0]}' and APP_name= '{row[1]}';"
        cursor.execute(update_app_password)

    # Close the cursor and connection
    cursor.close()
    cnx.close()