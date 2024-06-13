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
from function.order import getCart, getOrderForm
from function.auth import authLogin, authLogout, authRegister
from function.classes import RegistrationForm, OrderForm
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
def logout(response: Response, apikey: str = ""):
    return authLogout(apiKey=apikey)

@app.post("/auth/register", status_code=200)
def register(response: Response, registrationform: RegistrationForm):
    return authRegister(response=response, registrationForm=registrationform)

#################################################################
#                           HOME PAGE                           #
#################################################################
@app.get("/home", status_code=200)
def home(response: Response, apikey: str):
    return getHome(response, apikey)

#################################################################
#                            ORDERING                           #
#################################################################

@app.get("/cart", status_code=200)
def cart(response: Response, apikey: str = ""):
    return getCart(response=response, apiKey=apikey)

@app.get("/order", status_code=200)
def order(response: Response, apikey: str = "", producttype: str = ""):
    return getOrderForm(response=response, apiKey=apikey, productType=producttype)

# @app.post("/order", status_code=200)
# def cart(response: Response, apiKey: str = "", orderForm: orderForm = {}):
#     return getCart(response=response, apiKey=apiKey, orderForm=orderForm)

# @app.get("/orderoverview", status_code=200)


#################################################################
#                            ORDERING                           #
#################################################################
# @app.get("/payment", status_code=200)


@app.get("/test")
def test(response: Response):
    print (response.raw_headers)
    return {
        1:response.raw_headers
    }
