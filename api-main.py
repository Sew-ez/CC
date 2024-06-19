from typing import Union, Annotated
from fastapi import FastAPI, Response, Request, status, UploadFile, File, Header, Form
from fastapi.staticfiles import StaticFiles
from function.home import getHome
from function.order import getCart, getOrderForm, pushCart, pushOrder, getFabricTypeAll, getColorAll, addOrder
from function.auth import authLogin, authLogout, authRegister, authCheck, randomGenerator
from function.classes import RegistrationForm, OrderForm, LoginForm, LogoutForm, CartForm
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

@app.get("/auth/logout", status_code=200)
def logout(request: Request, response: Response):
    return authLogout(request=request, response=response)

@app.post("/auth/register", status_code=200)
def register(response: Response, registrationform: RegistrationForm):
    return authRegister(response=response, registrationForm=registrationform)

@app.get("/auth/check", status_code=200)
def checkSession(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    return authCheck(sessionToken)

#################################################################
#                           HOME PAGE                           #
#################################################################
@app.get("/home", status_code=200)
async def home(request: Request, response: Response):
    return await getHome(request=request, response=response)

#################################################################
#                            ORDERING                           #
#################################################################

@app.get("/order/jenis-bahan", status_code=200)
def order(request: Request, response: Response):
    return getFabricTypeAll(request=request, response=response)

@app.get("/order/warna", status_code=200)
def order(request: Request, response: Response):
    return getColorAll(request=request, response=response)

@app.post("/order/submit", status_code=200)
def submitOrder(request: Request, response: Response, jenisbahan: Annotated[int, Form()], warna: Annotated[int, Form()], xl: Annotated[int, Form()], l: Annotated[int, Form()], m: Annotated[int, Form()], s: Annotated[int, Form()], image: UploadFile = File(...)):
    return addOrder(request=request, response=response, jenisbahan=jenisbahan, warna=warna, xl=xl, l=l, m=m, s=s, image=image)

# @app.get("/cart", status_code=200)
# async def cart(request: Request, response: Response):
#     return await getCart(response=response, request=request)

# @app.post("/cart", status_code=200)
# async def cart(request: Request, response: Response, orderForm: OrderForm = {}):
#     return await pushCart(request=request, response=response, orderForm=orderForm)

# @app.get("/order", status_code=200)
# async def order(request: Request, response: Response, producttype: str = ""):
#     return await getOrderForm(request=request, response=response, productType=producttype)

# @app.post("/order", status_code=200)
# async def cart(request: Request, response: Response, cartForm: CartForm = {}):
#     return await pushOrder(request=request, response=response, cartForm=CartForm)
# @app.get("/orderoverview", status_code=200)


#################################################################
#                            ORDERING                           #
#################################################################
# @app.get("/payment", status_code=200)

import json
@app.get("/test")
async def test(request: Request, response: Response, user_agent: Annotated[str | None, Header()] = None):
    return await {
        1:request.headers
    }

@app.get("/test/random")
async def test(request: Request, response: Response):
    return {
        "data": randomGenerator(5)
    }

@app.post("/test/upload")
async def testUpload(request: Request, response: Response, file:UploadFile):
    file_path = os.getcwd()
    file_path = os.path.join(file_path, "test.txt")
    try:
        # Read the file and write it to the specified path
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_path": file_path
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    # return{
    #     "dataRead": await file.read(),
    #     "data": file
    # }
