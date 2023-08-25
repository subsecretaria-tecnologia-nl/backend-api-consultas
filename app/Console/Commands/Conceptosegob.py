import mysql.connector
import json
from mysql.connector import Error
from dotenv import dotenv_values

config = dotenv_values(".env")

def obtConceptos(id,f,ts):
    response = {"error":1, "msg":"", "data":[]}
    dbhost = config['DB_MYSQL8_HOST']
    dbname = config['DB_MYSQL8_DATABASE']
    dbuser = config['DB_MYSQL8_USERNAME']
    dbpwd = config['DB_MYSQL8_PASSWORD']
    conn3 = mysql.connector.connect(host=dbhost, database=dbname, user=dbuser, password=dbpwd)
    try:
        data = []
        if conn3.is_connected():
            match ts :
                case 1:
                    qry = """ SELECT * FROM egobierno.contveh WHERE idtran = """ + str(id) + """ AND folio = """ + str(f)
                    cursor = conn3.cursor(dictionary=True)
                    cursor.execute(qry)
                    records = cursor.fetchall()
#                     for r in records:
#                         d = {}
#                         d['idtran'] = r['idtran']
#                         d['folio'] = r['folio']
#                         d['placaa'] = r['placaa']
#                         d['placaa'] = r['placaa']
#                         d['placan'] = r['placan']
#                         d['concepto'] = r['concepto']
#                         d['rezago'] = r['rezago']
#                         d['guid'] = r['guid']
#                         d['referencia'] = r['referencia']
#                         d['partida'] = r['partida']
#                         d['descripcion'] = r['descripcion']
#                         d['anio'] = r['anio']
#                         data.append(d)
                    data = list(records)
                case 3:
                    qry = """ SELECT * FROM contribuyente.detalle_isn WHERE idTrans = """ + str(id) + """ AND Folio = """ + str(f)
                    cursor = conn3.cursor(dictionary=True)
                    records = cursor.fetchall()
#                     for r in records:
#                         d = {}
#                         d[''] = r['']
#                         d[''] = r['']
                    data = list(records)
                case _:
                    response['msg'] = "No se encuentra conceptos para el tramite"
#                     return response
            response["error"] = 0
            response["msg"]  = "Consulta Exitosa"
            response["data"] = data
            return response

    except Error as e:
        response["msg"] = "Error mientras se intento conectar {}" . format(e)
        response["data"] = []
#         return response
    finally:
        if conn3.is_connected():
            conn3.close()
        return response