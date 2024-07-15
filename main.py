import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import json
import datetime
import numpy as np
import skimage.draw
import cv2
import random
import math
import re
import time
import tensorflow as tf
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from runtime.logoDetector.mrcnn import utils
from runtime.logoDetector.mrcnn import visualize
from runtime.logoDetector.mrcnn.visualize import display_images
from runtime.logoDetector.mrcnn.visualize import display_instances
from runtime.logoDetector.mrcnn import model as modellib
from runtime.logoDetector.mrcnn.model import log
from runtime.logoDetector.mrcnn.config import Config
from runtime.logoDetector.mrcnn import model as modellib, utils
from typing import Union, Annotated
from fastapi import FastAPI, Response, Request, status, UploadFile, File, Header, Form
from fastapi.staticfiles import StaticFiles
from function.home import getHome
from function.order import getCart, getOrderForm, pushCart, pushOrder, getFabricTypeAll, getColorAll, addOrder, getLogoTypeAll
from function.auth import authLogin, authLogout, authRegister, authCheck, randomGenerator
from function.classes import RegistrationForm, OrderForm, LoginForm, LogoutForm, CartForm
from runtime.logoDetector.main import loadLogoDetector
from dotenv import load_dotenv
load_dotenv()

#################################################################
#                         LOAD MODEL                            #
#################################################################
model, dataset_val = loadLogoDetector()
#################################################################
#                         START API                             #
#################################################################
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#################################################################
#                           INTRO                               #
#################################################################
@app.get("/", status_code=200, response_description="Sae-sae Mawon")
def intro(request: Request, response: Response):
    headers = [f"Connection ID: {request.headers.get('cf-ray')}",
               f"- IP Address : {request.headers.get('cf-connecting-ip')}",
               f"- Country    : {request.headers.get('cf-ipcountry')}"]
    for i in range(len(headers)):
        if len(headers[i]) < 48:
            headers[i] += " " * (48 - len(headers[i]))
    return {
        "101":"███████╗███████╗██╗    ██╗      ███████╗███████╗",
        "102":"██╔════╝██╔════╝██║    ██║      ██╔════╝╚══███╔╝",
        "103":"███████╗█████╗  ██║ █╗ ██║█████╗█████╗    ███╔╝ ",
        "104":"╚════██║██╔══╝  ██║███╗██║╚════╝██╔══╝   ███╔╝  ",
        "105":"███████║███████╗╚███╔███╔╝      ███████╗███████╗",
        "106":"╚══════╝╚══════╝ ╚══╝╚══╝       ╚══════╝╚══════╝",
        "107":"                                                ",
        "108":"######### WELCOME TO SEWEZ BACKEND API #########",
        "109":"Server       : South East Asia                  ",
        "110":headers[0],
        "111":"Your Info                                       ",
        "112":headers[1],
        "113":headers[2],
    }

#################################################################
#                            AUTH                               #
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
    sessionToken = str(request.headers.get("Authorization"))
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

@app.get("/order/jenis-bahan", status_code=200)
def fabricType(request: Request, response: Response):
    return getFabricTypeAll(request=request, response=response)

@app.get("/order/jenis-bahan-logo", status_code=200)
def logoType(request: Request, response: Response):
    return getLogoTypeAll(request=request, response=response)

@app.get("/order/warna", status_code=200)
def fabricColor(request: Request, response: Response):
    return getColorAll(request=request, response=response)

@app.post("/order/submit", status_code=200)
async def submitOrder(request: Request, response: Response, jenisproduk: Annotated[int, Form()], jenisbahan: Annotated[int, Form()], warna: Annotated[int, Form()], jenislogo: Annotated[int, Form()], xxl:Annotated[int, Form()], xl: Annotated[int, Form()], l: Annotated[int, Form()], m: Annotated[int, Form()], s: Annotated[int, Form()], image: UploadFile = File(...)):
    apiData = addOrder(request=request, response=response, jenisproduk=jenisproduk, jenisbahan=jenisbahan, warna=warna, jenislogo=jenislogo, xxl=xxl, xl=xl, l=l, m=m, s=s, image=image, model=model, dataset_val=dataset_val)
    return apiData