from fastapi import FastAPI, Response, Request, status, UploadFile, File
from function.database import runDB, DBtoDict
from function.auth import authCheck, randomGenerator
from function.classes import OrderForm, CartForm
from runtime.logoDetector.main import calculateLogo
import json, os

def getCart(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "error": True,
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
            "error": True,
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
            "error": True,
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
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "error": True,
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
            "message": "No fabric type available"
        }

def getLogoTypeAll(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "error": True,
            "message": "Unauthorized"
        }
    fabric_type_query, fabric_type_column = runDB("SELECT * FROM logo_type")
    jenisData = DBtoDict(fabric_type_query, fabric_type_column)
    if len(jenisData)>0:
        listJenis = []
        for row in jenisData:
            listJenis.append({
                "id": row['id'],
                "type": row['type']
                })
        jenis = {
            "error": False,
            "message": "Logo type fetch successfully",
            "data":listJenis
        }
        return jenis
    else:
        return {
            "error": True,
            "message": "No logo type available"
        }

def getColorAll(request: Request, response: Response):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "error": True,
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
    
def addOrder(request: Request, response: Response, jenisproduk:int, jenisbahan:int, warna:int, jenislogo:int, xxl:int, xl:int, l:int, m:int, s:int, image: UploadFile, dataset_val, model):
    sessionToken = request.headers.get("Authorization")
    auth = authCheck(sessionToken)
    if not auth["login"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "error": True,
            "message": "Unauthorized"
        }
    if not image.content_type == "image/jpeg":
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {
            "error": True,
            "message": "Image type not supported"
        }
    
    #Generate Order ID
    orderId = randomGenerator(15)

    # Save image
    imageName = str(auth["loginResult"]["userId"] + "-" + orderId + ".jpg")
    imagePath = os.path.join(os.getcwd(), "static/uploads/order/", imageName)
    savePath = os.path.join(os.getcwd(), "static/generated/order/", imageName)
    try:
        # Read the file and write it to the specified path
        with open(imagePath, "wb") as f:
            f.write(image.file.read())
    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }
    
    # Detect logo
    detectionData = calculateLogo(imagePath=imagePath, savePath=savePath, model=model, dataset_val=dataset_val)
    if detectionData["error"]:
        return detectionData

    tshirtSizes = {}
    if(s>0):
        tshirtSizes["s"] = s
    if(m>0):
        tshirtSizes["m"] = m
    if(l>0):
        tshirtSizes["l"] = l
    if(xl>0):
        tshirtSizes["xl"] = xl
    if(xxl>0):
        tshirtSizes["xxl"] = xxl
    if len(tshirtSizes) == 0:
        return {
            "error": True,
            "message": "No size selected"
        }

    # Create new order
    order_query, order_column = runDB("""
                                        INSERT INTO `order` (uniqueId, `user`, mockup)
                                        VALUES (
                                            %s,
                                            (SELECT id FROM auth_user WHERE sessionToken = %s),
                                            %s
                                        )
                                    """, (orderId, auth["loginResult"]["token"], imageName))
    order_query, order_column = runDB("""
                                        SELECT * FROM `order` WHERE uniqueId = %s
                                    """, (orderId,))
    order = DBtoDict(order_query, order_column)
    if len(order) == 0:
        return {
            "error": True,
            "message": "Order not inserted"
        }

    # Create new logo order
    for logo in detectionData["data"]["logo"]:
        logoXLength = min(logo["x"], logo["y"])
        logoYLength = max(logo["x"], logo["y"])
        logo_query, logo_column = runDB("""
                                        INSERT INTO order_logo (`order`, logo)
                                        VALUES (
                                            (SELECT id FROM `order` WHERE uniqueId = %s),
                                            (SELECT logo.id AS id FROM logo
                                            LEFT JOIN logo_size ON logo.size = logo_size.id
                                            LEFT JOIN logo_type ON logo.`type` = logo_type.id
                                            WHERE Y >= %s AND X >= %s  AND logo.`type` = %s
                                            order BY Y ASC
                                            LIMIT 1)
                                        )
                                    """, (orderId, logoYLength, logoXLength, jenislogo))
        logo_query, logo_column = runDB("""
                                        SELECT * FROM order_logo WHERE `order` = (SELECT id FROM `order` WHERE uniqueId = %s)
                                    """, (orderId,))
        logo = DBtoDict(logo_query, logo_column)
        if len(logo) == 0:
            return {
                "error": True,
                "message": "Logo not inserted"
            }

    # iterate through sizes
    for size in tshirtSizes:
        # insert order item
        order_item_query, order_item_column = runDB("""
                                        INSERT INTO order_item (`order`, stock, quantity)
                                        VALUES (
                                            (SELECT id FROM `order` WHERE uniqueId = %s),
                                            (SELECT id FROM stock WHERE `type` = %s AND color = %s AND size = (SELECT id FROM stock_size WHERE size = %s) AND fabric = %s),
                                            %s
                                        )
                                    """, (orderId, jenisproduk, warna, size, jenisbahan, tshirtSizes[size]))
        # check if order item inserted
        order_item_query, order_item_column = runDB("""
                                                    SELECT * FROM order_item WHERE `order` = (SELECT id FROM `order` WHERE uniqueId = %s)
                                                    """, (orderId,))
        order_item = DBtoDict(order_item_query, order_item_column)
        if len(order_item) == 0:
            return {
                "error": True,
                "message": "Order item not inserted"
            }
        
    # calculate total price
    ## Fabric price
    fabric_query, fabric_column = runDB("""
                                                        SELECT 
                                                            `order`.id,
                                                            `order`.uniqueId,
                                                            order_item.quantity AS quantity,
                                                            stock_type.`type` AS fabricType,
                                                            stock_size.size AS fabricSize,
                                                            stock_color.color AS fabricColor,
                                                            stock_color.hexadecimal AS fabrichexColor,
                                                            stock.price AS fabricPrice
                                                        FROM order_item
                                                        LEFT JOIN `order` ON `order`.id = order_item.`order`
                                                        LEFT JOIN stock ON stock.id = order_item.stock
                                                        LEFT JOIN stock_color ON stock_color.id = stock.color
                                                        LEFT JOIN stock_type ON stock_type.id = stock.`type`
                                                        LEFT JOIN stock_size ON stock_size.id = stock.size
                                                        LEFT JOIN stock_fabric ON stock_fabric.id = stock.fabric
                                                        WHERE `order`.uniqueId = %s;
                                                    """, (orderId,))
    fabricData = DBtoDict(fabric_query, fabric_column)
    totalFabricQty = 0
    totalFabricPrice = 0
    for fabric in fabricData:
        totalFabricQty += fabric["quantity"]
        totalFabricPrice += fabric["quantity"] * fabric["fabricPrice"]
    
    ## Logo price
    logo_query, logo_column = runDB("""
                                                    SELECT 
                                                        `order`.id,
                                                        `order`.uniqueId,
                                                        order_logo.logo AS logoId,
                                                        logo_size.size AS logoSize,
                                                        logo_type.type AS logoType,
                                                        logo.price AS logoPrice
                                                    FROM order_logo
                                                    LEFT JOIN `order` ON `order`.id = order_logo.`order`
                                                    LEFT JOIN logo ON logo.id = order_logo.logo
                                                    LEFT JOIN logo_size ON logo_size.id = logo.size
                                                    LEFT JOIN logo_type ON logo_type.id = logo.`type`
                                                    WHERE `order`.uniqueId = %s;
                                                """, (orderId,))
    logoData = DBtoDict(logo_query, logo_column)
    totalLogoQty = 0
    totalLogoPrice = 0
    for logo in logoData:
        totalLogoQty += 1
        totalLogoPrice += logo["logoPrice"] * totalFabricQty

    # imagePath
    imagePath = os.path.join(str(os.getenv("BASE_URL")), "static/generated/order/", imageName)

    return {
        "error": False,
        "message": "Order added successfully",
        "data": {
            "jenisbahan": fabricData[0]["fabricType"],
            "warna": fabricData[0]["fabricColor"],
            "jenislogo": logoData[0]["logoType"],
            "xxl": xxl,
            "xl": xl,
            "l": l,
            "m": m,
            "s": s,
            "totalFabricPrice": totalFabricPrice,
            "totalLogoPrice": totalLogoPrice,
            "totalPrice": totalFabricPrice + totalLogoPrice,
            "image": imagePath,
        }
    }