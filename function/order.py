from fastapi import FastAPI, Response, status
from function.database import runDB, DBtoDict
from function.auth import authCheck
from function.classes import OrderForm

def getCart(response: Response, apiKey: str):
    auth = authCheck(apiKey)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    cart_query, cart_column = runDB("SELECT * FROM Home_Showcase")

def getOrderForm(response: Response, apiKey: str, productType: int):
    auth = authCheck(apiKey)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    stock_query, stock_column = runDB("""
                                        SELECT 'color' AS attribute, color AS value
                                        FROM (
                                            SELECT DISTINCT stock_color.color AS color
                                            FROM stock
                                            LEFT JOIN stock_color ON stock.color = stock_color.id
                                            WHERE stock.`type` = %s
                                        ) AS t1

                                        UNION ALL

                                        SELECT 'type' AS attribute, `type` AS value
                                        FROM (
                                            SELECT DISTINCT stock_type.`type` AS `type`
                                            FROM stock
                                            LEFT JOIN stock_type ON stock.`type` = stock_type.id
                                            WHERE stock.`type` = %s
                                        ) AS t2

                                        UNION ALL

                                        SELECT 'size' AS attribute, size AS value
                                        FROM (
                                            SELECT DISTINCT stock_size.size AS size
                                            FROM stock
                                            LEFT JOIN stock_size ON stock.size = stock_size.id
                                            WHERE stock.`type` = %s
                                        ) AS t3

                                        UNION ALL

                                        SELECT 'fabric' AS attribute, fabric AS value
                                        FROM (
                                            SELECT DISTINCT stock_fabric.fabric AS fabric
                                            FROM stock
                                            LEFT JOIN stock_fabric ON stock.fabric = stock_fabric.id
                                            WHERE stock.`type` = %s
                                        ) AS t4;
                                              """, (productType,productType,productType,productType))
    stock = DBtoDict(stock_query, stock_column)
    print(stock)
    orderFormData = {}
    for row in stock:
        if row['attribute'] not in orderFormData:
            orderFormData[row['attribute']] = []
        orderFormData[row['attribute']].append(row['value'])
    return orderFormData


def pushOrder(response: Response, orderForm: OrderForm):
    return {
            "status": 401,
            "message": "Unauthorized"
        }