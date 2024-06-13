from function.classes import registrationForm
from fastapi import Response
from .database import runDB, DBtoDict
from uuid import uuid4
import bcrypt


def authRegister(response: Response, registrationForm: registrationForm):
    registrationFormData = registrationForm.model_dump()
    username = str(registrationFormData["username"])
    profileName = str(registrationFormData["profilename"])
    password = str(registrationFormData["password"])
    if(username == "" or profileName == "" or password == ""):
        response.status_code=400
        return{
            "status": 400,
            "message": "Please fill all required field"
        } 
    elif(" " in username):
        response.status_code=400
        return{
            "status": 400,
            "message": "Username contains illegal character"
        }   
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE username = %s", (username,))
    user = DBtoDict(user_query, user_column)
    print(user)
    if len(user) > 0:
        response.status_code=400
        return{
            "status": 400,
            "message": "Username already exist"
        }
    else:
        salt = bcrypt.gensalt()
        password_b = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_b, salt).decode('utf-8')
        runDB("INSERT INTO Auth_User (username, name, password) VALUES (%s, %s, %s)", (username, profileName, hashed))
        user_query, user_column = runDB("SELECT * FROM Auth_User WHERE username = %s", (username,))
        user = DBtoDict(user_query, user_column)
        if len(user) > 0:
            encrypted_passwd = user[0]['password']
            if bcrypt.checkpw(password.encode('utf-8'), encrypted_passwd.encode('utf-8')):
                return {
                    "status": 200,
                    "message": "Successfully registered"
                }
        else:
            return {
                "status": 500,
                "message": "Server side error! Contact Developer"
            }

def authLogin(username, password):
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE username = %s", (username,))
    user = DBtoDict(user_query, user_column)
    if len(user) > 0:
        encrypted_passwd = user[0]['password']
        if bcrypt.checkpw(password.encode('utf-8'), encrypted_passwd.encode('utf-8')):
            rand_token = str(uuid4())
            runDB("UPDATE Auth_User SET apiKey = %s WHERE username = %s", (rand_token, username))
            return {
                "login": True,
                "apiKey": rand_token,
                "username": user[0]['username'],
                "profileName": user[0]['name']
            }
        else:
            return {
                "login": False,
                "message": "Wrong Password"
            }
    else:
        return {
            "login": False,
            "message": "User Not Found"
        }
    
def authLogout(apiKey):
    runDB("UPDATE Auth_User SET apiKey = '' WHERE apiKey =  %s", (apiKey,))
    return {
        "logout": True
    }

def authCheck(apiKey):
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE apiKey = %s", (apiKey,))
    user = DBtoDict(user_query, user_column)
    if len(user) > 0:
        return {
            "login": True,
            "userName": user[0]['username'],
            "profileName": user[0]['name']
        }
    else:
        return {
            "login": False
        }