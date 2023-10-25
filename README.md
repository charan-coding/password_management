# PMS-Charan

# Servers
This PMS project has 10 functionalities and each functionality has an associated server  and request with it:

    1.Create Policy 
    2.Assign Users 
    3.Add Batch 
    4.Update Policy 
    5.Login Master  
    6.Login App
    7.User Reset (Master)
    8.Admin Reset (Master)
    9.Admin Delete (Master and App)
    10.Password Leak Check

## Usage
The Work flow would go like this 
As an Admin:
	1. Run the Create_policy_Server
	2. Import Data into the policy of Create_policy_Request and change data and run Create_policy_Request
	3. Run Assign_users_Server
	4. Modify data in Assign_users_Request and Run it to update the user accounts
	5. Update Policy when required by running the Update_policy_Server
	6. Make a call to the server with the updated policy using Update_policy_Request
As a User:
	1. Run the Login_master_Server
	2. Use the Credentials stored in master_passwords and try to login using Login_master_Request
	3. Be met with an Error asking you to Reset Password
	4. Run the User reset Server
	5. User_reset_Request Update the password there using your own password
	6. Try to login using Login_master_Request again using your own password
	7. Retrieve Application Specific Passwords 
	8. Run the Login_app_Server
	9. Update details in the Login_app_Request like appID userID and Password.
	10. Run Login_app_Request and recieve authentication message back
Miscellaneous functions:
	1. Admin can run the Admin Delete Server and the Admin Delete Request in order to Delete User Records
	2. Admin or User can run the Check Leak Server and Check Leak Request in order to Check if their passwords have been leaked or not
	3. Acounts which have passed the reset mark will be disabled and Admin can run the Admin_Reset_Server and Admin_Reset_Request to set their state back to Reset.
	4. Admin can add to the batch generated password if he wishes

## Create Policy
The first serve request pair is created with Create policy. The server has the follwing functions:
	authenticate
	check_and_validate
	write
	sql
	generate_password
	leak_check

The functions are defined in files with the suffix Extra_create_policy. Function authenticate. This authenticate function takes two parameters id_no and psw. It checks if the provided id_no is equal to 12345 and the psw is equal to "hehehelol". If either of these conditions is not met, the function raises an exception InvalidCredentials.
Function check_and_validate. This check_and_validate function takes one parameter policy, which is a dictionary that contains several key-value pairs. The function performs the following tasks:

Updates the dictionary csv_dict by adding a new key-value pair Days_to_reset from the policy dictionary.
Adds today's date in the format of "Month day, Year" to the csv_dict dictionary as a new key-value pair updatedOn.
Adds default values to the csv_dict dictionary for the keys min_upper, min_lower, min_number, and min_specialchar if they do not already exist.
Checks if the values of min_upper, min_lower, min_number, and min_specialchar are all non-negative. If any of these values are negative, the function raises an exception InvalidRange.
Calculates the total number of characters from min_upper, min_lower, min_number, and min_specialchar.
Validates the policy rules by checking the following conditions:
    a. If the minimum length of the password is less than the total number of characters, the function raises an exception InvalidRules1.
    b. If the maximum length of the password is more than 20, the function raises an exception InvalidRules3.
    c. If the maximum length of the password is less than the total number of characters, the function raises an exception InvalidRules2.
Validates the batch size of the policy by checking if it exists and is within the range of 1 to 50. If the batch size is missing or outside the range, the function raises an exception MissingBatch or BadSize, respectively.
Returns the updated csv_dict dictionary.

Note: InvalidCredentials, InvalidRange, InvalidRules1, InvalidRules2, InvalidRules3, BadSize, and MissingBatch are all custom exceptions used in this code.

The generate_password function uses the random and string Python modules to generate a password with specified requirements. The function starts by defining the required characters for the password, including uppercase letters, lowercase letters, numeric characters, and special characters. The function then generates a random length for the password within the specified minimum and maximum length parameters. The function uses the random.sample method to select characters from the defined character set, combining them to form the password. The function also includes logic to ensure that the password meets the minimum requirements for each character type. If the length of the password is less than the specified minimum length, the function adds additional random characters to meet the requirement. If the length of the password is greater than the specified maximum length, the function truncates the password to meet the requirement.

## Assign Users 
    Imports the pandas library for reading data from a csv file and the mysql library for connecting to a MySQL database.
    The getrandom_pass() function reads data from a csv file 'passwords batch.csv', selects a random password from the 'Password' column, and removes it from the csv file. The function then returns the selected random password.
    The insertsql(response) function takes a dictionary response as an input and performs the following operations:
        Defines a dictionary Legacy_apps that maps app IDs to app names.
        Connects to a MySQL database and creates a cursor.
        Loops over the IDs of the apps in response["Access"] and for each ID:
            Calls the getrandom_pass() function to get a random password from the 'passwords batch.csv' file. If there are no more passwords left in the file, it raises a RanOutOfPsWs error.
            Inserts a record in the 'app_password' table of the database, with columns for user ID, app name, app ID, and the random password obtained.
        Calls the getrandom_pass() function again to get another random password. If there are no more passwords left in the file, it raises a RanOutOfPsWs error.
        Inserts a record in the 'master_password' table of the database, with columns for user ID, username, hashed password, password status, and current date and time. The password is hashed using the SHA1 algorithm and converted to uppercase before being inserted.

It is worth noting that the code does not handle the RanOutOfPsWs error, and it is unclear what the desired behavior should be in that case. Additionally, the code does not sanitize user input or handle exceptions when interacting with the database, which could result in security vulnerabilities.

## The code you've shared implements a password management system (PMS). It has several functions that perform different operations such as validating the username and password, checking if a password has expired, and retrieving passwords for different applications.

The loginmaster function is the main entry point for the PMS. It first retrieves the username and password from a JSON request and hashes the password using the sha1 algorithm. It then calls the is_expired function to check if the password is expired. If the password has expired, the function returns a response indicating that a password reset is required.

If the password has not expired, the function calls the validate_username_password function to validate the username and password against the master password table in a MySQL database. If the username and password match, the function calls the retrieve_app_passwords function to retrieve the passwords for the different applications associated with the user. The function returns the retrieved passwords.

If the username and password do not match, the function returns a response indicating that access is denied.

The validate_username_password function establishes a connection to the MySQL database, retrieves the user ID, state, and date from the master password table, and returns the user ID if the username and password match. If the password has not been reset, the function returns a response indicating that a password reset is required.

The retrieve_app_passwords function establishes a connection to the MySQL database, retrieves the app ID and password from the app password table, and returns a dictionary containing the app ID and password.

The is_expired function establishes a connection to the MySQL database, retrieves the date of the last password update for a user, and checks if the password has expired based on the policy specified in a CSV file. If the password has expired, the function updates the state of the password in the master password table and returns True. If the password has not expired, the function returns False.

## Reset 
This code is a part of a password reset API. It contains three functions: resetmaster(), validate_username_password(), and update_password().

The resetmaster() function receives a JSON object containing the username, old password, and new password. It first checks if the new password has been leaked or not using the leak_check() function (not provided in the code). If the password has been leaked, it returns an error message indicating that the password can't be used.

The new password and old password are hashed using the sha1 algorithm and converted to uppercase. The validate_username_password() function is then called to verify the username and old password. If the username and password match, the state of the account is checked. If the state is disabled, the function returns an error message. If the state is enabled, the update_password() function is called to update the password in the database. If the username and password don't match, the function returns an error message indicating the old password is wrong.

The validate_username_password() function establishes a connection to a MySQL database using the provided credentials, and queries the master_password table to check if the provided username and password match. If a match is found, it returns the user ID and state.

The update_password() function establishes a connection to the MySQL database, updates the password in the master_password table for the provided username, and sets the state to "enabled".

## Authors and acknowledgment
Thanks to Jeet and Melvin for helping with the GIT push and pull.
