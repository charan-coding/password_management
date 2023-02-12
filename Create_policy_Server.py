from flask import Flask, request
import mysql.connector
import requests
from Extra_Create_policy_Validation import authenticate, check_and_validate, write, sql
from Extra_Create_policy_batch_Generation import generate_password, leak_check, csv_file_psw
import Extra_Create_policy_Validation as c


app = Flask(__name__)
@app.route("/createpolicy", methods=["POST"])

def createpolicy():
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
        write(csv_dict)
    except IOError:
        return {"Error": "I/O"}

    try:
        sql(csv_dict)
    except mysql.connector.Error as err:
        return{"Error":str(err)}

    pass_list=[]
    while len(pass_list)<(policy["Batch_size"]):
        psw = generate_password(csv_dict["min_length"],csv_dict["max_length"],
                                csv_dict["min_specialchar"], csv_dict["min_upper"],
                                csv_dict["min_lower"],csv_dict["min_number"])
        try:
            flag = leak_check(psw)
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

    return{"Policy": "Created"}



if __name__ == '__main__':
    app.run(debug=True, port=5000)
