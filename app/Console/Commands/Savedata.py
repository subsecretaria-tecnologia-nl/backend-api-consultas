import mysql.connector
import json
from mysql.connector import Error
from dotenv import dotenv_values

config = dotenv_values(".env")

def inserta_data(d):
    response = {"error":1, "msg":"", "data":[]}
    data = list()

    for x in d:
        lista = list(x.values())
        data.append(lista)

    try:
        dbhost = config['DB_MYSQL_HOST']
        dbname = config['DB_MYSQL_DATABASE']
        dbuser = config['DB_MYSQL_USERNAME']
        dbpwd = config['DB_MYSQL_PASSWORD']

        saveconn = mysql.connector.connect(host=dbhost, database=dbname, user=dbuser, password=dbpwd)

        if saveconn.is_connected():
            while len(data) != 0:
                qry = """ INSERT INTO operacion.oper_pagos_api (
                    id_transaccion_motor,
                    id_transaccion,
                    estatus,
                    desc_estatus,
                    entidad,
                    referencia,
                    Total,
                    cve_Banco,
                    MetododePago,
                    FechaTransaccion,
                    FechaPago,
                    FechaConciliacion,
                    tipo_servicio,
                    desc_tipo_servicio,
                    created_at,
                    updated_at,
                    detalle,
                    corte,
                    procesado
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                savecursor = saveconn.cursor()
                savecursor.executemany(qry,data[:999])
                del data[:999]
                saveconn.commit()
    except Error as e:
        response["msg"] = "Error mientras se intento guardar los datos {}" . format(e)
        response["data"] = []
    finally:
        if saveconn.is_connected():
            savecursor.close()
            saveconn.close()
        print("Elementos insertados: ", len(d))
        return response