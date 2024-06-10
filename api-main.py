from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from function.home import getHome
from function.auth import authLogin, authLogout

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/home/{oAuthToken}", status_code=200)
def home(response: Response, oAuthToken: str):
    return getHome(response, oAuthToken)




@app.get("/cart/{jwt}", status_code=200)
def getCart(response: Response, jwt: str = ""):
    user_db = {
        "ByhUAbsfybu12vb8fy13bfOF": {
            "cart": [
                {
                    "id": 1,
                    "name": "T-Shirt",
                    "icon": ""
                },
                {
                    "id": 2,
                    "name": "Jacket",
                    "icon": ""
                },
                {
                    "id": 3,
                    "name": "Tote-Bag",
                    "icon": ""
                },
                {
                    "id": 4,
                    "name": "Cap",
                    "icon": ""
                },
            ]
        }
    }
    if(jwt==""):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    else:
        return {
            "status": 200,
            "cart": user_db[jwt]["cart"]
        }




# AUTH
@app.get("/auth/login/{username}/{password}", status_code=200)
def login(response: Response, username: str = "", password: str = ""):
    return authLogin(username=username, password=password)

@app.get("/auth/logout/{oAuthToken}", status_code=200)
def login(response: Response, username: str = "", oAuthToken: str = ""):
    return authLogout(oAuthToken=oAuthToken)