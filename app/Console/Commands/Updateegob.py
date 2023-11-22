import mysql.connector
import json
from mysql.connector import Error
from dotenv import dotenv_values


config = dotenv_values(".env")

def updateEgob(idTrans,cursor):
    try:
        response = {"error":1, "msg":"", "data":[]}
        #query para actualizar la transaccion enviada a la tablas de operacion.oper_pagos_api.
        qry = """ UPDATE egobierno.transacciones SET campos_nuevo=1 WHERE idTrans in (""" + idTrans + """)""" 
        cursor.execute(qry)
        cursor.commit()
    except (Exception, mysql.connector.Error) as error:
        response["msg"] = "Error mientras se intento conectar {}" . format(error)
        response["data folio"] = idTrans
    finally:
        return response
    
