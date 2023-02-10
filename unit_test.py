import unittest
from create_policy import *
from batch_gen_pass import *
from unittest.mock import patch
from assign import *
import re


class maintest(unittest.TestCase):
    @patch('mysql.connector.connect')
    def test_insertsql(self, mock_connect):
        mock_cursor = mock_connect().cursor.return_value

        test_response = {"Access": ["001", "002"], "UserID": "0001", "UserName": "Test User"}

        insertsql(test_response)

        expected_queries = [
            "^INSERT INTO app_password VALUES \(\"0001\",\"App1\",\"001\",\".*\",\" reset\"\);$",
            "^INSERT INTO app_password VALUES \(\"0001\",\"App2\",\"002\",\".*\",\" reset\"\);$",
            "^INSERT INTO master_password VALUES\(\"0001\",\"Test User\",\".*\", \"reset\", NOW\(\)\);$"
        ]

        patterns = [re.compile(q) for q in expected_queries]

        matched = False
        for call in mock_cursor.execute.call_args_list:
            for pattern in patterns:
                if pattern.match(call[0][0]):
                    matched = True
                    break
            if matched:
                break
        self.assertTrue(matched)




    def test_authentication(self):
        id_no = 12345
        psw = "hehehelol"

        # testing the authenticate function with the correct id number and password
        authenticate(id_no, psw)

        # testing the authenticate function with the correct id number but wrong password
        self.assertRaises(c.InvalidCredentials, authenticate, 12345, "wrongpassword")

        # testing the authenticate function with the wrong id number and correct password
        self.assertRaises(c.InvalidCredentials, authenticate, 123, "hehehelol")

        # testing the authenticate function with the wrong id number and wrong password
        self.assertRaises(c.InvalidCredentials, authenticate, 123, "wrongpassword")

        # testing the authenticate function with invalid input types
        self.assertRaises(c.InvalidCredentials, authenticate, "hahah", 123.45)

    def test_generate_password(self):
        csv_dict = {
            'min_length': 9,
            'max_length': 15,
            'min_upper': 4,
            'min_lower': 2,
            'min_number': 1,
            'min_specialchar': 2} #policy
        Upper_count=Ucount(
            generate_password(csv_dict["min_length"], csv_dict["max_length"], csv_dict["min_specialchar"],
                          csv_dict["min_upper"], csv_dict["min_lower"], csv_dict["min_number"]))
        Lower_count = Lcount(
            generate_password(csv_dict["min_length"], csv_dict["max_length"], csv_dict["min_specialchar"],
                              csv_dict["min_upper"], csv_dict["min_lower"], csv_dict["min_number"]))
        Digit_count = Dcount(
            generate_password(csv_dict["min_length"], csv_dict["max_length"], csv_dict["min_specialchar"],
                              csv_dict["min_upper"], csv_dict["min_lower"], csv_dict["min_number"]))
        Special_count = Scount(
            generate_password(csv_dict["min_length"], csv_dict["max_length"], csv_dict["min_specialchar"],
                              csv_dict["min_upper"], csv_dict["min_lower"], csv_dict["min_number"]))
        Length=len(
            generate_password(csv_dict["min_length"], csv_dict["max_length"], csv_dict["min_specialchar"],
                              csv_dict["min_upper"], csv_dict["min_lower"], csv_dict["min_number"]))

        # Checking if the number of uppercase letters is greater than or equal to the minimum required
        self.assertGreaterEqual(Upper_count, csv_dict["min_upper"])
        # Checking if the number of lowercase letters is greater than or equal to the minimum required
        self.assertGreaterEqual(Lower_count, csv_dict["min_lower"])
        # Checking if the number of special characters is greater than or equal to the minimum required
        self.assertGreaterEqual(Special_count, csv_dict["min_specialchar"])
        # Checking if the number of digits is greater than or equal to the minimum required
        self.assertGreaterEqual(Digit_count, csv_dict["min_number"])
        # Checking if the length of the password is greater than or equal to the minimum length
        self.assertGreaterEqual(Length, csv_dict["min_length"])
        # Checking if the length of the password is less than or equal to the maximum length
        self.assertLessEqual(Length, csv_dict["max_length"])

    def testleak_check(self):
        # Testing the leak_check function with a password that has not been leaked
        self.assertEqual(leak_check("egrck2@"), 0)

        # Testing the leak_check function with a password that has been leaked
        self.assertEqual(leak_check("password"), 1)
        self.assertEqual(leak_check("admin"), 1)
        self.assertEqual(leak_check("123456789"), 1)

        # Testing the API response
        password = "password"
        hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = hashed_password[:5]
        suffix = hashed_password[5:]
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        # Checking the API response status code
        self.assertEqual(response.status_code, 200)
        # Checking if the API response has suffix part of the hash
        self.assertIn(suffix, response.text)

    def testcheck_and_validate(self):
        today = date.today()

        policy1 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#normal policy
        csv_dict1={
            'min_length': 9,
            'max_length': 15,
            'min_upper': 4,
            'min_lower': 2,
            'min_number': 1,
            'min_specialchar': 2,
            'Hours_to_reset': '36',
            'updatedOn': today.strftime("%B %d, %Y")}#expected csv_dict
        self.assertEqual(check_and_validate(policy1),csv_dict1)

        policy2 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#policy without certain parameters such as minimum required special characters
        csv_dict2 = {
            'min_length': 9,
            'max_length': 15,
            'min_upper': 0,
            'min_lower': 0,
            'min_number': 0,
            'min_specialchar': 0,
            'Hours_to_reset': '36',
            'updatedOn': today.strftime("%B %d, %Y")}#processed policy with empty data replaced by 0s
        self.assertEqual(check_and_validate(policy2), csv_dict2)

        policy3= {"Batch_size": 50, "Hours_to_reset": "36"}#policy without rules
        policy4 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
                "min_specialchar": 1
            },
            "Batch_size": 50,
            }#policy without hours_to_reset
        policy5 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Hours_to_reset": "36"}#policy without batch size
        self.assertRaises(KeyError,check_and_validate,policy3)
        self.assertRaises(KeyError, check_and_validate, policy4)
        self.assertRaises(c.MissingBatch, check_and_validate, policy5)

        policy6 = {
            "rules": {
                "min_length": 9,
                "max_length": "15",
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#policy with string instead of int
        policy7 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
                "min_upper": "41",
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#policy with string instead of int
        self.assertRaises(TypeError,check_and_validate,policy6)
        self.assertRaises(TypeError, check_and_validate, policy7)

        policy8 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
                "min_upper": 4,
                "min_lower": -2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#policy with negative rules minimum uppercase
        policy9 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": -1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#policy with negative rules minimum lowercase
        self.assertRaises(c.InvalidRange,check_and_validate,policy8)
        self.assertRaises(c.InvalidRange, check_and_validate, policy9)

        policy10 = {
            "rules": {
                "min_length": 2,
                "max_length": 15,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#very low min length
        policy11 = {
            "rules": {
                "min_length": -9,
                "max_length": 15,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#negative min length
        self.assertRaises(c.InvalidRules1, check_and_validate,policy10)
        self.assertRaises(c.InvalidRules1, check_and_validate,policy11)

        policy12 = {
            "rules": {
                "min_length": 9,
                "max_length": 21,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#max password length more than limit - corner
        policy13 = {
            "rules": {
                "min_length": 9,
                "max_length": 2000,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#max password length more than limit - extreme
        self.assertRaises(c.InvalidRules3,check_and_validate,policy12)
        self.assertRaises(c.InvalidRules3, check_and_validate, policy13)

        policy14 = {
            "rules": {
                "min_length": 9,
                "max_length": 2,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}#max password length lower than sum of other chars - corner
        policy15 = {
            "rules": {
                "min_length": 9,
                "max_length": -200,
                "min_upper": 4,
                "min_lower": 2,
                "min_number": 1,
                "min_specialchar": 2
            },
            "Batch_size": 50,
            "Hours_to_reset": "36"}# max password length lower than sum of other chars - extreme -negative
        self.assertRaises(c.InvalidRules2, check_and_validate,policy14)
        self.assertRaises(c.InvalidRules2, check_and_validate, policy15)

        policy16 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
            },
            "Batch_size": 200,
            "Hours_to_reset": "36"}#batch size extreme positive
        policy17 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
            },
            "Batch_size": 51,
            "Hours_to_reset": "36"}#batch size corner positive
        policy18 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
            },
            "Batch_size": -200,
            "Hours_to_reset": "36"}#batch size extreme negative
        policy19 = {
            "rules": {
                "min_length": 9,
                "max_length": 15,
            },
            "Batch_size": 0,
            "Hours_to_reset": "36"}#batchsize corner negative
        self.assertRaises(c.BadSize,check_and_validate,policy16)
        self.assertRaises(c.BadSize, check_and_validate, policy17)
        self.assertRaises(c.BadSize, check_and_validate, policy18)
        self.assertRaises(c.BadSize, check_and_validate, policy19)


if __name__ == "__main__":
    unittest.main()