import mysql.connector
import json
from mysql.connector import Error
from dotenv import dotenv_values
from Detallesegob import *
from Updateegob import *
import datetime

config = dotenv_values(".env")

def consulta_egob():

    # Inicializacion de respuesta
    response = {"error": 1, "msg": "", "data": []}

    try:
        # parametros de conexion
        dbhost = config['DB_MYSQL8_HOST']
        dbname = config['DB_MYSQL8_DATABASE']
        dbuser = config['DB_MYSQL8_USERNAME']
        dbpwd = config['DB_MYSQL8_PASSWORD']
        dbmonth = config['API_MES_MARGEN']

        connection = mysql.connector.connect(host=dbhost, database=dbname, user=dbuser, password=dbpwd)

        if connection.is_connected():

            # Consulta base de datos para tabla concentradora.
            qry = """SELECT
                T.idtrans AS 'id_transaccion_motor',
                T.idtrans AS 'id_transaccion',
                T.status AS 'estatus',
                IF(T.status = 0,IF(C.fecha_conciliacion = '','PAGADO-NC','PAGADO-CON'),'NO PAGADO') AS 'desc_estatus',
                24 AS 'entidad',
                IFNULL(R.LInea, 0) AS 'referencia',
                T.totaltramite AS 'total',
                IFNULL(T.TipoPago, 0) AS 'tipo_pago',
                UPPER(P.Descripcion) AS 'desc_tipo_pago',
                T.fechatramite AS 'fecha_transaccion',
                C.fecha_banco AS 'fecha_pago',
                C.fecha_conciliacion AS 'fecha_conciliacion',
                T.tipoServicio AS 'tipo_servicio',
                UPPER(S.Tipo_Descripcion) AS 'desc_tipo_servicio',
                '' as detalle,
                '' as corte
            FROM egobierno.transacciones T
            LEFT JOIN egobierno.referenciabancaria R ON R.idtrans = T.idTrans
            LEFT JOIN conciliacion.conciliacion C ON C.idTrans = T.idTrans
            LEFT JOIN egobierno.tipo_servicios S ON S.Tipo_Code = T.TipoServicio
            LEFT JOIN egobierno.tipopago P ON P.TipoPago = IFNULL(T.TipoPago,7)
            WHERE T.fechatramite >= DATE_SUB(NOW(), INTERVAL """ + dbmonth + """ MONTH)
            AND T.status IN (0,30) LIMIT 1 """

            cursor = connection.cursor(dictionary=True)
            cursor.execute(qry)
            records = cursor.fetchall()

            # Llenado de respuesta para envio
            response["error"] = 0
            response["msg"] = "Consulta Exitosa"
            response["data"] = records

            # Inicialización de lista para el atributo data
            data = list()

            for r in records:
                d = dict()
                d['id_transaccion_motor'] = r['id_transaccion_motor']
                d['id_transaccion'] = r['id_transaccion']
                d['estatus'] = r['estatus']
                d['desc_estatus'] = r['desc_estatus']
                d['entidad'] = r['entidad']
                d['referencia'] = r['referencia']
                d['total'] = r['total']
                d['tipo_pago'] = r['tipo_pago']
                d['desc_tipo_pago'] = r['desc_tipo_pago']
                d['fecha_transaccion'] = r['fecha_transaccion']
                d['fecha_pago'] = r['fecha_pago']
                d['fecha_conciliacion'] = r['fecha_conciliacion']
                d['tipo_servicio'] = r['tipo_servicio']
                d['desc_tipo_servicio'] = r['desc_tipo_servicio']
                d['created_at'] = '{:%Y-%m-%d %H:%M:%S}' . format(datetime.datetime.now())
                d['updated_at'] = '{:%Y-%m-%d %H:%M:%S}' . format(datetime.datetime.now())
                d['corte'] = ''
                d['procesado'] = 0

                # Obtención del JSON con detalle de los tramites.
                detalle = obtDetalle(r['id_transaccion'], r['tipo_servicio'],cursor,r['desc_tipo_servicio'])
                updateEgob(r['id_transaccion'], r['tipo_servicio'],cursor)
                if detalle['error'] != 0:
                    d['detalle'] = ''
                # Validación de contenido para integración a la respuesta general
                else:
                    d['detalle'] = json.dumps(detalle['data'], default=str)

                data.append(d)

            response["data"] = data

    except (Exception, mysql.connector.Error) as error:
        response["msg"] = "Error mientras se intento conectar {}".format(error)
        response["data"] = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return response