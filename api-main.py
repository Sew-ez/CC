#############################################################################
#
#   [AUTH]
#   GET /auth/login?username={your_username}&password={your_password}
#   GET /auth/logout?apikey={your_api_key}
#   POST /auth/register
#       [Body]
#       {
#         "profilename"="{your_name}",
#         "username"="{your_username}"",
#         "password"="{your_password}",
#       }
# 
#   [HOME]
#   GET /home?apikey={your_api_key}
#
#   [ORDER]
#   
#
#





from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from function.home import getHome
from function.order import getCart
from function.auth import authLogin, authLogout, authRegister
from function.classes import registrationForm, orderForm
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#################################################################
#                              AUTH                             #
#################################################################
@app.get("/auth/login", status_code=200)
def login(response: Response, username: str = "", password: str = ""):
    return authLogin(username=username, password=password)

@app.get("/auth/logout", status_code=200)
def logout(response: Response, username: str = "", apiKey: str = ""):
    return authLogout(apiKey=apiKey)

@app.post("/auth/register", status_code=200)
def register(response: Response, registrationForm: registrationForm):
    return authRegister(response=response, registrationForm=registrationForm)

#################################################################
#                           HOME PAGE                           #
#################################################################
@app.get("/home", status_code=200)
def home(response: Response, apiKey: str):
    return getHome(response, apiKey)

#################################################################
#                            ORDERING                           #
#################################################################

@app.get("/cart", status_code=200)
def cart(response: Response, apiKey: str = ""):
    return getCart(response=response, apiKey=apiKey)

@app.get("/order", status_code=200)
def order(response: Response, apiKey: str = ""):
    return getOrder()

@app.post("/order", status_code=200)
def cart(response: Response, apiKey: str = "", orderForm: orderForm = {}):
    return getCart(response=response, apiKey=apiKey, orderForm=orderForm)

@app.get("/orderoverview", status_code=200)


#################################################################
#                            ORDERING                           #
#################################################################
@app.get("/payment", status_code=200)