from fastapi import FastAPI, Response, status
from function.database import runDB, DBtoDict
from function.auth import authCheck

def getHome(response: Response, oAuthToken: str):
    auth = authCheck(oAuthToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    # Get Showcase
    showcase_query, showcase_column = runDB("SELECT * FROM Home_Showcase")
    showcase = DBtoDict(showcase_query, showcase_column)

    # Get Product Categories
    product_query, product_column = runDB("SELECT Stock_Type.id, Stock_Type.`type` FROM Stock LEFT JOIN Stock_Type ON Stock.`type` = Stock_Type.id WHERE Stock.quantity > 0 GROUP BY Stock_Type.id, Stock_Type.`type` ORDER BY Stock_Type.id")
    product = DBtoDict(product_query, product_column)

    return {
        "status": 200,
        "session": {
            "userName": auth["userName"],
            "profileName": auth["profileName"],
        },
        "product": product,
        "showcase": showcase
    }