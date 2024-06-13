from fastapi import FastAPI, Response, status
from function.database import runDB, DBtoDict
from function.auth import authCheck
from function.classes import orderForm

def getCart(response: Response, apiKey: str):
    auth = authCheck(apiKey)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    cart_query, cart_column = runDB("SELECT * FROM Home_Showcase")

def pushOrder(response: Response, orderForm: orderForm):
    return {
            "status": 401,
            "message": "Unauthorized"
        }