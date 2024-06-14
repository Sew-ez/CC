from fastapi import FastAPI, Response, Request, status
from function.database import runDB, DBtoDict
from function.auth import authCheck
from function.classes import OrderForm

def getCart(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    cart_query, cart_column = runDB("SELECT * FROM Home_Showcase")

def getOrderForm(request: Request, response: Response, productType: int):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    stock_query, stock_column = runDB("""
                                        SELECT 'color' AS attribute, id, value
                                        FROM (
                                            SELECT DISTINCT stock_color.id AS id, stock_color.color AS value
                                            FROM stock
                                            LEFT JOIN stock_color ON stock.color = stock_color.id
                                            WHERE stock.`type` = %s
                                        ) AS t1

                                        UNION ALL

                                        SELECT 'type' AS attribute, id, value
                                        FROM (
                                            SELECT DISTINCT stock_type.id AS id, stock_type.`type` AS value
                                            FROM stock
                                            LEFT JOIN stock_type ON stock.`type` = stock_type.id
                                            WHERE stock.`type` = %s
                                        ) AS t2

                                        UNION ALL

                                        SELECT 'size' AS attribute, id, value
                                        FROM (
                                            SELECT DISTINCT stock_size.id AS id, stock_size.size AS value
                                            FROM stock
                                            LEFT JOIN stock_size ON stock.size = stock_size.id
                                            WHERE stock.`type` = %s
                                        ) AS t3

                                        UNION ALL

                                        SELECT 'fabric' AS attribute, id, value
                                        FROM (
                                            SELECT DISTINCT stock_fabric.id AS id, stock_fabric.fabric AS value
                                            FROM stock
                                            LEFT JOIN stock_fabric ON stock.fabric = stock_fabric.id
                                            WHERE stock.`type` = %s
                                        ) AS t4
                                              """, (productType,productType,productType,productType))
    stock = DBtoDict(stock_query, stock_column)
    if len(stock)>0:
        orderFormData = {}
        for row in stock:
            if row['attribute'] not in orderFormData:
                orderFormData[row['attribute']] = []
            orderFormData[row['attribute']].append({
                row['id']:row['value']
            })
        orderFormData = {
            "error": False,
            "message": "Stock fetch successfully",
            "list":orderFormData
        }
        return orderFormData
    else:
        return {
            "error": True,
            "message": "No stock available"
        }

def pushOrder(request: Request, response: Response, orderForm: OrderForm):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
