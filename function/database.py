import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os

def runDB(query: str):
    mydb = mysql.connector.connect(
        host=os.getenv("DB_host"),
        user=os.getenv("DB_user"),
        password=os.getenv("DB_password"),
        database=os.getenv("DB_Name")
    )
    mycursor = mydb.cursor()

    try:
        mycursor.execute(query)
        if query.strip().upper().startswith(("UPDATE", "INSERT", "DELETE")):
            mydb.commit()
        
        myresult = mycursor.fetchall()
        column_names = []
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