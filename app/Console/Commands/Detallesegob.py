import mysql.connector
import json
from mysql.connector import Error
from dotenv import dotenv_values
from Conceptosegob import *

config = dotenv_values(".env")

def obtDetalle(id,ts,cursor):

    response = {"error":1, "msg":"", "data":[]}

    try:

        t = {
            'sub_folio': "",
            'clave_tramite': "",
            'descripcion_tramite': "",
            'rfc': "",
            'curp': "",
            'cuenta_estatal': "",
            'anio_ejercicio': "",
            'mes_ejercicio': "",
            'tipo_declaracion': "",
            'importe_tramite': "",
            'maquinas': "",
            'placa': "",
            'solicitud': "",
            'concesion': "",
            'licencia': "",
            'municipio': "",
            'expediente_catastral': "",
            'boleta': "",
            'credito': "",
            'convenio': "",
            'parcialidad': "",
            'adicional_1': "",
            'adicional_2': "",
            'adicional_3': "",
            'adicional_4': "",
            'adicional_5': "",
            'adicional_6': ""
        }
        data = {
            'referencia_bancaria': "",
            'folio': "",
            'origen_tramites': "",
            'origen_pago': "",
            'medio_pago': "",
            'importe_pago': "",
            'fecha_pago': "",
            'hora_pago': "",
            'nombre_rs': "",
            'tramites': t
        }

        match ts:
            case 3:
                qry = """ SELECT 
                        IFNULL(R.Linea,'') AS referencia,
                        T.idTrans AS idTrans,
                        D.Folio AS folio,
                        IF(T.totaltramite = 0,0,IFNULL(T.tipopago,0)) AS origentramites,
                        T.totaltramite AS importe_pago,
                        T.NombreEnvio AS nombrerc,
                        IFNULL(CONCAT(D.rfcalf,D.rfcnum,D.rfchom),"") AS RFC,
                        D.cuenta AS cuenta,
                        D.anio AS anio,
                        D.mes AS mes,
                        D.tipo_declaracion AS tipo_declaracion,
                        D.total_cargo AS totalcargo,
                        D.municipio as municipio,
                        REPLACE(IFNULL(C.fecha_banco,'00000000'),'-','') as fechapago
                    FROM
                        contribuyente.detalle_isn D
                    LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                    LEFT JOIN 
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                    LEFT JOIN
                        conciliacion.conciliacion C ON C.idtrans = T.idTrans
                    WHERE
                        D.idTrans = """ + str(id)

        cursor.execute(qry)
        records = cursor.fetchall()
        if len(records) > 0:
            data['referencia_bancaria'] = records[0]['referencia']
            data['folio'] = records[0]['idTrans']
            data['origen_tramites'] = records[0]['origentramites']
            data['origen_pago'] = '015'
            data['importe_pago'] = records[0]['importe_pago']
            data['nombre_rs'] = records[0]['nombrerc']
            data['fecha_pago'] = records[0]['fechapago']
            tramites = list()
            for r in records:
                row = t
                row['sub_folio'] = r['folio']
                row['clave_tramite'] = '3'
                row['descripcion_tramite'] = "ISN 3%"
                row['rfc'] = r['RFC']
                row['cuenta_estatal'] = r['cuenta']
                row['anio_ejercicio'] = r['anio']
                row['mes_ejercicio'] = r['mes']
                row['tipo_declaracion'] = r['tipo_declaracion']
                row['importe_tramite'] = r['totalcargo']
                row['municipio'] = r['municipio']
                tramites.append(row)
            data['tramites'] = tramites
        response["error"] = 0
        response["msg"]  = "Consulta Exitosa"
        response["data"] = data
    except (Exception, mysql.connector.Error) as error:
        response["msg"] = "Error mientras se intento conectar {}" . format(error)
        response["data"] = data
    finally:
        return response
