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





from typing import Union, Annotated
from fastapi import FastAPI, Response, Request, status, Header
from fastapi.staticfiles import StaticFiles
from function.home import getHome
from function.order import getCart, getOrderForm, pushCart, pushOrder
from function.auth import authLogin, authLogout, authRegister, authCheck
from function.classes import RegistrationForm, OrderForm, LoginForm, LogoutForm
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#################################################################
#                              AUTH                             #
#################################################################
@app.post("/auth/login", status_code=200)
def login(response: Response, loginForm: LoginForm):
    return authLogin(loginForm=loginForm)

@app.post("/auth/logout", status_code=200)
def logout(request: Request, response: Response):
    return authLogout(request=request, response=response)

@app.post("/auth/register", status_code=200)
def register(response: Response, registrationform: RegistrationForm):
    return authRegister(response=response, registrationForm=registrationform)

@app.post("/auth/check", status_code=200)
def checkSession(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    return authCheck(sessionToken)

#################################################################
#                           HOME PAGE                           #
#################################################################
@app.get("/home", status_code=200)
def home(request: Request, response: Response):
    return getHome(request=request, response=response)

#################################################################
#                            ORDERING                           #
#################################################################

@app.get("/cart", status_code=200)
def cart(request: Request, response: Response):
    return getCart(response=response, request=request)

@app.post("/cart", status_code=200)
def cart(request: Request, response: Response, orderForm: OrderForm = {}):
    return pushCart(request=request, response=response, orderForm=orderForm)

@app.get("/order", status_code=200)
def order(request: Request, response: Response, producttype: str = ""):
    return getOrderForm(request=request, response=response, productType=producttype)

@app.post("/order", status_code=200)
def cart(request: Request, response: Response, orderForm: OrderForm = {}):
    return pushOrder(request=request, response=response, orderForm=orderForm)

# @app.get("/orderoverview", status_code=200)


#################################################################
#                            ORDERING                           #
#################################################################
# @app.get("/payment", status_code=200)

import json
@app.get("/test")
def test(request: Request, response: Response, user_agent: Annotated[str | None, Header()] = None):
    return {
        1:request.headers
    }
