from flask import Flask,request
from batch_gen_pass import *

app = Flask(__name__)
@app.route("/addbatch", methods=["POST"])

def addbatch():
    number=request.get_json()
    num=int(number["number"])
    policy= pd.read_csv("policy.csv")

    pass_list = []
    while len(pass_list) < 10:
        psw = generate_password(int(policy["min_length"]), int(policy["max_length"]), int(policy["min_specialchar"]),
                                int(policy["min_upper"]), int(policy["min_lower"]), int(policy["min_number"]))
        try:
            flag = leak_check(psw)
        except requests.exceptions.HTTPError as errh:
            return {"Http Error": str(errh)}
        except requests.exceptions.ConnectionError as errc:
            return {"Connection Error": str(errc)}
        except requests.exceptions.Timeout as errt:
            return {"Timeout Error": str(errt)}
        except requests.exceptions.RequestException as err:
            return {"Undefined API Error": str(err)}
        if flag == 0:
            pass_list.append(psw)

    df = pd.DataFrame({'Password': pass_list})
    df['Upper_case_chars'] = df['Password'].apply(Ucount)
    df['Lower_case_chars'] = df['Password'].apply(Lcount)
    df['Special_chars'] = df['Password'].apply(Scount)
    df['Digits'] = df['Password'].apply(Dcount)
    df1= pd.read_csv("passwords batch.csv")
    df2 = pd.concat([df, df1], axis=0)
    print(df2)
    df2.to_csv('passwords batch.csv', index=False)



    return{(str(num)+" passwords" ): "Created"}

if __name__ == '__main__':
    app.run(debug=True, port=5004)