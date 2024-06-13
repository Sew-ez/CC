##################################################################################################
# MYSQL ORM
#
# Example usage for SELECT:
# select_query = "SELECT * FROM users WHERE username = %s"
# params = ("some_username",)
# result, columns = runDB(select_query, params)
#
# Example usage for INSERT:
# insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
# params = ("new_user", "hashed_password")
# runDB(insert_query, params)
#
# Example usage for UPDATE:
# update_query = "UPDATE users SET password = %s WHERE username = %s"
# params = ("new_hashed_password", "existing_user")
# runDB(update_query, params)
#
##################################################################################################
import mysql.connector
import os

def runDB(query: str, parameters: tuple = ()):
    mydb = mysql.connector.connect(
        host=os.getenv("DB_Host"),
        user=os.getenv("DB_User"),
        password=os.getenv("DB_Password"),
        database=os.getenv("DB_Name")
    )
    mycursor = mydb.cursor()

    myresult = []
    column_names = []

    try:
        mycursor.execute(query, parameters)
        
        if query.strip().upper().startswith(("UPDATE", "INSERT", "DELETE")):
            mydb.commit()
        else:
            myresult = mycursor.fetchall()
            if mycursor.description is not None:
                column_names = [column[0] for column in mycursor.description]
    except Exception as e:
        mydb.rollback()
        raise e
    finally:
        mycursor.close()
        mydb.close()

    return (myresult, column_names)

def DBtoDict(runDBResult, runDBColumn):
    data = [] 
    for row in runDBResult:
        if len(row)<1:
            break
        row_dict = dict(zip(runDBColumn, row))
        data.append(row_dict)
    return data

# def runDB(query: str):
#     mydb = mysql.connector.connect(
#         host=os.getenv("DB_Host"),
#         user=os.getenv("DB_User"),
#         password=os.getenv("DB_Password"),
#         database=os.getenv("DB_Name")
#     )
#     mycursor = mydb.cursor()

#     try:
#         mycursor.execute(query)
#         if query.strip().upper().startswith(("UPDATE", "INSERT", "DELETE")):
#             mydb.commit()
        
#         myresult = mycursor.fetchall()
#         column_names = []
#         if mycursor.description is not None:
#             column_names = [column[0] for column in mycursor.description]
#     except Exception as e:
#         mydb.rollback()
#         raise e
#     finally:
#         mycursor.close()
#         mydb.close()
        
#     return (myresult, column_names)