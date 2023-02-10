from flask import Flask, request
import mysql.connector
import requests
from create2 import authenticate, check_and_validate, write, sql
from batch_gen_pass import generate_password, leak_check, csv_file_psw
import create2 as c
from newuser2 import *
import batch_gen_pass as b

app = Flask(__name__)
@app.route("/updatepolicy", methods=["POST"])

def updatepolicy():
    policy = request.get_json()
    try:
        authenticate(policy["Admin"]["id"], policy["Admin"]["pass"])

    except KeyError:
        return{"BadAuthError": "Missing authentication info"}

    except c.InvalidCredentials:
        return {"BadAuthError": "Invalid Creds"}

    try:
        csv_dict = dict(check_and_validate(policy))

    except KeyError:
        return {"MissingDataError": "Missing critical information for policy (rules or time to reset)"}
    except TypeError:
        return{"TypeError":"Input data type is not right"}
    except c.InvalidRange:
        return{"InvalidRange":"Please recheck input"}
    except c.InvalidRules1:
        return {
            "InvalidRulesError": "Invalid Policy Parameters, minimum length of password is lesser than total required characters"}
    except c.InvalidRules2:
        return {
            "InvalidRulesError": "Invalid Policy Parameters, maximum length of password is lesser than total required characters"}
    except c.InvalidRules3:
        return {"InvalidRulesError": "Invalid Policy Parameters, maximum length of password is greater than 20 characters"}
    except c.BadSize:
        return {"InvalidBatchError": "Batch Size is not valid (Choose a number between 1 and 50)"}
    except c.MissingBatch:
        return {"InvalidBatchError": "Batch Size is not specified"}

    try:
        c.up_write(csv_dict)
    except IOError:
        return {"Error": "I/O"}

    try:
        c.up_sql()
    except mysql.connector.Error as err:
        return{"Error":str(err).split(':')[1]}

    pass_list=[]
    while len(pass_list)<(policy["Batch_size"]):
        psw = generate_password(csv_dict["min_length"],csv_dict["max_length"],csv_dict["min_specialchar"], csv_dict["min_upper"],csv_dict["min_lower"],csv_dict["min_number"])
        try:
            flag=leak_check(psw)
        except requests.exceptions.HTTPError as errh:
            return{"Http Error": str(errh)}
        except requests.exceptions.ConnectionError as errc:
            return {"Connection Error": str(errc)}
        except requests.exceptions.Timeout as errt:
            return {"Timeout Error": str(errt)}
        except requests.exceptions.RequestException as err:
            return {"Undefined API Error": str(err)}
        if flag==0:
            pass_list.append(psw)

    csv_file_psw(pass_list)

    return{"Policy": "Updated"}



if __name__ == '__main__':
    app.run(debug=True, port=5002)