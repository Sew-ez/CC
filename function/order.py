from fastapi import FastAPI, Response, Request, status, UploadFile, File
from function.database import runDB, DBtoDict
from function.auth import authCheck
from function.classes import OrderForm, CartForm
import json, os

def getCart(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    print(auth)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    cart_query, cart_column = runDB("""
                                        SELECT 
                                            order_cart.id,
                                            stock_type.`type` AS product_type,
                                            stock_fabric.fabric AS product_fabric,
                                            stock_color.color  AS product_color,
                                            stock_size.size	 AS product_size,
                                            order_cart.quantity AS quantity,
                                            order_cart.createdAt AS created_at,
                                            order_cart.price
                                        FROM order_cart 
                                        LEFT JOIN auth_user ON order_cart.user = auth_user.id
                                        LEFT JOIN stock ON order_cart.stock = stock.id
                                        LEFT JOIN stock_size ON stock.size = stock_size.id
                                        LEFT JOIN stock_type ON stock.`type` = stock_type.id
                                        LEFT JOIN stock_color ON stock.color = stock_color.id
                                        LEFT JOIN stock_fabric ON stock.fabric = stock_fabric.id
                                        WHERE auth_user.sessionToken = %s
                                    """, (auth["sessionToken"],))
    cartData = DBtoDict(cart_query, cart_column)
    if len(cartData)>0:
        cart = {}
        for row in cartData:
            cart[row['id']] = {
                "product_type": row['product_type'],
                "product_fabric": row['product_fabric'],
                "product_color": row['product_color'],
                "product_size": row['product_size'],
                "quantity": row['quantity'],
                "created_at": row['created_at'],
                "price": json.loads(row['price'])
            }
        cart = {
            "error": False,
            "message": "Cart fetch successfully",
            "cart":cart
        }
        return cart
    else:
        return {
            "error": True,
            "message": "No item in cart"
        }

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
                                            ORDER BY value ASC
                                        ) AS t1
                                      
                                        UNION ALL

                                        SELECT 'type' AS attribute, id, value
                                        FROM (
                                            SELECT DISTINCT stock_type.id AS id, stock_type.`type` AS value
                                            FROM stock
                                            LEFT JOIN stock_type ON stock.`type` = stock_type.id
                                            WHERE stock.`type` = %s
                                            ORDER BY value ASC
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
                                            ORDER BY value ASC
                                        ) AS t4
                                              """, (productType,productType,productType,productType))
    stock = DBtoDict(stock_query, stock_column)
    if len(stock)>0:
        orderFormData = {}
        for row in stock:
            if row['attribute'] not in orderFormData and row['attribute'] :
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

def pushCart(request: Request, response: Response, cartForm: CartForm):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    sessionToken = auth["sessionToken"]
    stock = cartForm[""]
    ##############################################################################
    #                           SOON TO BE ML FUNCTION                           #
    ##############################################################################
    order_query, order_column = runDB("""
                                        INSERT INTO order_cart (user, stock, quantity, price)
                                        VALUES (
                                            (SELECT id FROM auth_user WHERE sessionToken = %s),
                                            (SELECT id FROM stock WHERE `type` = %s AND color = %s AND size = %s AND fabric = %s),
                                            %s,
                                            %s
                                        )
                                    """, (auth["sessionToken"], orderForm.product_type, orderForm.product_color, orderForm.product_size, orderForm.product_fabric, orderForm.quantity, json.dumps(orderForm.price)))

def pushOrder(request: Request, response: Response, orderForm: OrderForm):
    pass

def getFabricTypeAll(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    print(auth)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    fabric_type_query, fabric_type_column = runDB("SELECT * FROM stock_fabric")
    jenisData = DBtoDict(fabric_type_query, fabric_type_column)
    if len(jenisData)>0:
        listJenis = []
        for row in jenisData:
            listJenis.append({
                "id": row['id'],
                "type": row['fabric']
                })
        jenis = {
            "error": False,
            "message": "Fabric type fetch successfully",
            "data":listJenis
        }
        return jenis
    else:
        return {
            "error": True,
            "message": "No jenis available"
        }
    
def getColorAll(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    print(auth)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    color_query, color_column = runDB("SELECT * FROM stock_color")
    colorData = DBtoDict(color_query, color_column)
    if len(colorData)>0:
        listColor = []
        for row in colorData:
            listColor.append({
                "id": row['id'],
                "color": row['color'],
                "hex": row["hexadecimal"]
                })
        color = {
            "error": False,
            "message": "Color fetch successfully",
            "data":listColor
        }
        return color
    else:
        return {
            "error": True,
            "message": "No color available"
        }
    
def addOrder(request: Request, response: Response, jenisbahan:int, warna:int, xl:int, l:int, m:int, s:int, image: UploadFile = File(...)):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": 401,
            "message": "Unauthorized"
        }
    order_query, order_column = runDB("""
                                        INSERT INTO order_cart (user, stock, quantity, price)
                                        VALUES (
                                            (SELECT id FROM auth_user WHERE sessionToken = %s),
                                            (SELECT id FROM stock WHERE `type` = %s AND color = %s AND size = %s AND fabric = %s),
                                            %s,
                                            %s
                                        )
                                    """, (auth["sessionToken"], jenisbahan, warna, xl, l, m, s, image))
    return {
        "error": False,
        "message": "Order added successfully"
    }

# {
#     "jenisbahan": 1,
#     "warna": 1,
#     "xl": 0,
#     "l": 0,
#     "m": 0,
#     "s": 10,
#     "image": FILE
# }