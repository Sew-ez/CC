from function.classes import RegistrationForm, LoginForm, LogoutForm
from function.dataValidation import isValidEmail
from fastapi import Response, Request, status
from .database import runDB, DBtoDict
import os, bcrypt, string, random


def authRegister(response: Response, registrationForm: RegistrationForm):
    registrationFormData = registrationForm.model_dump()
    email = str(registrationFormData["email"])
    profileName = str(registrationFormData["name"])
    password = str(registrationFormData["password"])
    if(email == "" or profileName == "" or password == ""):
        response.status_code=400
        return{
            "error": True,
            "message": "Please fill all required field"
        } 
    elif(len(password)<8):
        response.status_code=400
        return{
            "error": True,
            "message": "Password must be at least 8 characters"
        }
    elif(not isValidEmail(email)):
        response.status_code=400
        return{
            "error": True,
            "message": "Email contains illegal character"
        }   
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE email = %s", (email,))
    user = DBtoDict(user_query, user_column)
    if len(user) > 0:
        response.status_code=400
        return{
            "status": True,
            "message": "Username already exist"
        }
    else:
        salt = bcrypt.gensalt()
        password_b = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_b, salt).decode('utf-8')
        uniQueId = randomGenerator(20)
        runDB("INSERT INTO Auth_User (email, name, password, uniqueId) VALUES (%s, %s, %s, %s)", (email, profileName, hashed, uniQueId))
        user_query, user_column = runDB("SELECT * FROM Auth_User WHERE email = %s", (email,))
        user = DBtoDict(user_query, user_column)
        if len(user) > 0:
            encrypted_passwd = user[0]['password']
            if bcrypt.checkpw(password.encode('utf-8'), encrypted_passwd.encode('utf-8')):
                return {
                    "error": False,
                    "message": "Successfully registered"
                }
        else:
            response.status_code=500
            return {
                "error": True,
                "message": "Server side error. Contact Developer!"
            }

def authLogin(loginForm: LoginForm):
    loginFormData = loginForm.model_dump()
    email = str(loginFormData["email"])
    password = str(loginFormData["password"])
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE email = %s", (email,))
    user = DBtoDict(user_query, user_column)
    if len(user) > 0:
        encrypted_passwd = user[0]['password']
        if bcrypt.checkpw(password.encode('utf-8'), encrypted_passwd.encode('utf-8')):
            rand_token = randomGenerator(100)
            runDB("UPDATE Auth_User SET sessionToken = %s WHERE email = %s", (rand_token, email))
            baseUrl = os.getenv("BASE_URL")
            userUniqueId = user[0]['uniqueId']
            profilePictureSource = user[0]['profilePicture']
            if profilePictureSource == 1:
                profilePicture = f"{baseUrl}/static/profile/{userUniqueId}.jpg"
            else:
                profilePicture = f"{baseUrl}/static/aseets/placeholder/placeholder_male.jpg"
            return {
                "error": False,
                "message": "Success",
                "loginResult": {
                    "userId": user[0]['uniqueId'],
                    "name": user[0]['name'],
                    "email": user[0]['email'],
                    "token": rand_token,
                    "picture": profilePicture
                }
            }
        else:
            return {
                "error": True,
                "message": "Wrong Password"
            }
    else:
        return {
            "error": True,
            "message": "User Not Found"
        }
    
def authLogout(request:Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        return {
            "login": False
        }
    if sessionToken == "" or not type(sessionToken)==str:
        return {
            "login": False
        }
    elif not "Bearer" in sessionToken:
        return {
            "login": False
        }
    sessionToken = str(sessionToken[len("Bearer "):])
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE sessionToken = %s", (sessionToken,))
    user = DBtoDict(user_query, user_column)
    if len(user) > 0:
        runDB("UPDATE Auth_User SET sessionToken = NULL WHERE sessionToken =  %s", (sessionToken,))
        return {
            "error": False,
            "message": "Successfully logged out"
        }
    else:
        return {
            "error": True,
            "message": "Session not found"
        }

def authCheck(sessionToken:str = ""):
    if sessionToken == "" or not type(sessionToken)==str:
        return {
            "login": False
        }
    elif not "Bearer" in sessionToken:
        return {
            "login": False
        }
    sessionToken = str(sessionToken[len("Bearer "):])
    user_query, user_column = runDB("SELECT * FROM Auth_User WHERE sessionToken = %s", (sessionToken,))
    user = DBtoDict(user_query, user_column)
    print(user)
    if len(user) > 0:
        baseUrl = os.getenv("BASE_URL")
        userUniqueId = user[0]['uniqueId']
        profilePictureSource = user[0]['profilePicture']
        if profilePictureSource == 1:
            profilePicture = f"{baseUrl}/static/profile/{userUniqueId}.jpg"
        else:
            profilePicture = f"{baseUrl}/static/aseets/placeholder/placeholder_male.jpg"
        return {
                "error": False,
                "message": "Success",
                "login": True,
                "loginResult": {
                    "userId": user[0]['uniqueId'],
                    "name": user[0]['name'],
                    "email": user[0]['email'],
                    "token": user[0]['sessionToken'],
                    "picture": profilePicture
                },
                "email": user[0]['email'],
                "profileName": user[0]['name'],
                "profilePicture": profilePicture,
                "sessionToken": user[0]['sessionToken']
        }
    else:
        return {
            "login": False
        }
        
def randomGenerator(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string