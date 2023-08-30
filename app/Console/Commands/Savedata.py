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
        savecursor = saveconn.cursor()
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
                corte,
                procesado,
                detalle
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        if saveconn.is_connected():
            i = 0
            while i < len(data):
                savecursor.execute(qry,data[i])
                # del data[:999]
                saveconn.commit()
                i+=1

    # except Error as e:
    #     response["msg"] = "Error mientras se intento guardar los datos {}" . format(e)
    #     response["data"] = []
    except (Exception, mysql.connector.Error) as error:
        print("Error durante la conexión o consulta (Guardado):", error)
    finally:
        if saveconn.is_connected():
            saveconn.close()
        print("Elementos insertados: ", len(d))
        return response