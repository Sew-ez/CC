from fastapi import FastAPI, Response, Request, status
from function.database import runDB, DBtoDict
from function.auth import authCheck
import os

def getHome(response: Response, request: Request):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "error": True,
            "message": "Unauthorized"
        }
    
    # Get Showcase
    showcase_query, showcase_column = runDB("SELECT * FROM Home_Showcase ORDER BY id DESC")
    showcase = DBtoDict(showcase_query, showcase_column)

    # Get Product Categories
    product_query, product_column = runDB("SELECT Stock_Type.id, Stock_Type.`type` FROM Stock LEFT JOIN Stock_Type ON Stock.`type` = Stock_Type.id WHERE Stock.quantity > 0 GROUP BY Stock_Type.id, Stock_Type.`type` ORDER BY Stock_Type.id")
    product = DBtoDict(product_query, product_column)

    #Iterate and update image path for showcase
    for item in showcase:
        baseUrl = os.getenv("BASE_URL")
        item["image"] = f"{baseUrl}/static/showcase/{item['image']}"
    
    #Iterate and update image path for category
    for item in product:
        baseUrl = os.getenv("BASE_URL")
        item["image"] = f"{baseUrl}/static/category/{item['image']}"

    return {
        "error": False,
        "message": "Success",
        "session": {
            "name": auth["profileName"],
            "email": auth["email"],
            "profilePicture": auth["profilePicture"]
        },
        "product": product,
        "showcase": showcase
    }