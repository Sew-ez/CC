from .database import runDB, DBtoDict
from uuid import uuid4
import bcrypt

def authLogin(username, password):
    print(username)
    user_query, user_column = runDB(f"SELECT * FROM Auth_User WHERE username = '{username}'")
    user = DBtoDict(user_query, user_column)
    if len(user) > 0:
        encrypted_passwd = user[0]['password']
        if bcrypt.checkpw(password.encode('utf-8'), encrypted_passwd.encode('utf-8')):
            rand_token = uuid4()
            runDB(f"UPDATE Auth_User SET oAuthToken = '{rand_token}' WHERE username = '{username}'")
            return {
                "login": True,
                "oAuth": rand_token,
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
    
def authLogout(oAuthToken):
    runDB(f"UPDATE Auth_User SET oAuthToken = '' WHERE oAuthToken = '{oAuthToken}'")
    return {
        "logout": True
    }

def authCheck(oAuthToken):
    user_query, user_column = runDB(f"SELECT * FROM Auth_User WHERE oAuthToken = '{oAuthToken}'")
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