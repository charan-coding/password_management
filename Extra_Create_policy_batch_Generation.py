import random
import string
import requests
import hashlib
import pandas as pd
from datetime import date


def generate_password(min_length: int, max_length: int, min_special_chars: int, min_uppercase: int, min_lowercase: int, min_number: int) -> str:
    characters = ""
    characters += "".join(random.choice(string.ascii_uppercase) for _ in range(min_uppercase))
    characters += "".join(random.choice(string.ascii_lowercase) for _ in range(min_lowercase))
    characters += "".join(random.choice(string.digits) for _ in range(min_number))
    randlen = random.randint(min_length, max_length)

    temp = random.randrange(0, len(characters))

    password = str(characters[temp])
    characters = characters.replace(password, '')

    special_chars = "!#$%&()*+,-./?@^_~]"
    characters += "".join(random.choice(special_chars) for _ in range(min_special_chars))

    lol = random.sample(characters, len(characters))
    lol = ''.join(lol)
    password = password + lol

    if len(password) < randlen:
        password += ''.join(random.choice(string.ascii_letters + string.digits))
        password += ''.join(random.choice(string.ascii_letters + string.digits + special_chars) for _ in range(randlen - len(password)-1))

    elif len(password) > randlen:
        password = password[:randlen]

    return password


def leak_check(pass1):
    # Hashing the input password using sha1 algorithm
    sha = hashlib.sha1(pass1.encode()).hexdigest()
    # Converting the hashed password to uppercase
    sha = sha.upper()
    # Extracting the splitting the hashed password
    query = sha[0:5]
    lastbit = sha[5:]

    # Requesting the data from the pwnedpassword api
    url = "https://api.pwnedpasswords.com/range/"
    url = url + query
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    # Split the received data into a list
    out_list = response.text.split('\r\n')
    # Creating a dictionary with the received data
    out_dict = {}
    for i in out_list:
        rem_hash = i.split(':')[0]
        leak_num = i.split(':')[1]
        out_dict[rem_hash] = leak_num

    # Checking if the last 5 characters of the password's hash in the out_dict
    if lastbit in out_dict.keys():
        return 1
    else:
        return 0


def Ucount(password):
    uppercase_count = 0
    for char in password:
        if char.isupper():
            uppercase_count += 1
    return uppercase_count

def Lcount(password):
    lowercase_count = 0
    for char in password:
        if char.islower():
            lowercase_count += 1
    return lowercase_count

def Dcount(password):
    digit_count = 0
    for char in password:
        if char.isdigit():
            digit_count += 1
    return digit_count

def Scount(password):
    special_count = 0
    for char in password:
       if not char.isalnum():
            special_count += 1
    return special_count

def csv_file_psw(pass_list):
    df = pd.DataFrame({'Password': pass_list})
    df['Upper_case_chars'] = df['Password'].apply(Ucount)
    df['Lower_case_chars'] = df['Password'].apply(Lcount)
    df['Special_chars'] = df['Password'].apply(Scount)
    df['Digits'] = df['Password'].apply(Dcount)
    df.to_csv('passwords batch.csv', index=False)
    print(df)