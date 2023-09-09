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
            'nombre_rs': "",
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
            case 1:
                qry = """ SELECT 
                        F.folio AS sub_folio,
                        IFNULL(F.CartKey3,'') AS RFC,
                        '' AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        F.CartImporte AS totalcargo,
                        '' AS maquinas,
                        IFNULL(F.CartKey1,'') AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        '' AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                    --     egobierno.contveh D
                    --         LEFT JOIN
                        egobierno.transacciones T
                            LEFT JOIN
                        egobierno.folios F ON T.idTrans = F.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "1"
                desc = "CONTROL VEHICULAR"
            case 3:
                qry = """ SELECT 
                        D.Folio AS sub_folio,
                        IFNULL(CONCAT(D.rfcalf,D.rfcnum,D.rfchom),"") AS RFC,
                        '' AS CURP,
                        D.cuenta AS cuenta,
                        D.anio AS anio,
                        D.mes AS mes,
                        D.tipo_declaracion AS tipo_declaracion,
                        D.total_cargo AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        D.municipio as municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea,'') AS referencia,
                        IF(T.totaltramite = 0,0,IFNULL(T.tipopago,0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        D.nombre_razonS AS nombretr,
                        T.totaltramite AS importe_pago,
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
                cve = "3"
                desc = "IMPUESTO SOBRE NOMINA"
            case 8:
                qry = """ SELECT 
                        D.id_tramite AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_tramite AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, IFNULL(D.razon_social, ''), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.paterno, ''),' ',IFNULL(D.materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.tramites D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "8"
                desc = "INVORMATIVO VALOR CATASTRAL"
            case 20:
                qry = """ SELECT 
                        D.Folio AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.monto AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IFNULL(D.nombre_razonS,'') AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        servicios.detalle_servicios D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "20"
                desc = "SERVICIOS GENERALES"
            case 21:
                qry = """ SELECT 
                        F.folio AS sub_folio,
                        IFNULL(D.rfc,"") AS RFC,
                        IFNULL(D.curp,"") AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' as municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,    
                        IFNULL(R.Linea,'') AS referencia,
                        IF(T.totaltramite = 0,0,IFNULL(T.tipopago,0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.apaterno, ''),' ',IFNULL(D.amaterno, '')) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco,'00000000'),'-','') AS fechapago
                    FROM
                        egobierno.folios F
                    LEFT JOIN
                        gobmx.registrocivilgmx D ON F.CartKey2 = D.folioSeguimiento
                    LEFT JOIN
                        egobierno.transacciones T ON F.idTrans = T.idTrans
                    LEFT JOIN 
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                    LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "21"
                desc = "REGISTRO CIVIL GOBMX"
            case 23:
                qry = """ SELECT 
                        D.Folio AS sub_folio,
                        IFNULL(CONCAT(D.rfcalfa,D.rfcnum,D.rfchom), '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        IFNULL(D.cuenta, '') AS cuenta,
                        IFNULL(D.anio, '') AS anio,
                        IFNULL(D.mes, '') AS mes,
                        IFNULL(UPPER(D.tipo_declaracion), '') AS tipo_declaracion,
                        D.total_pagar AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        D.nombre_razonS AS nombretr
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        contribuyente.detalle_isn_prestadora D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idtrans = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "23"
                desc = "IMPUESTO SOBRE NÓMINA (PRESTADORA DE SERVICIOS)"
            case 28:
                qry = """ SELECT 
                        D.folio AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_total AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, '')), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.detalle_agilgob D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "28"
                desc = "COPIA DE ACTA CERTIFICADA DE MATRIMONIOS"
            case 32:
                qry =""" SELECT 
                        F.Folio AS sub_folio,
                        IFNULL(D.RFC, '') AS RFC,
                        IFNULL(D.CURP, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.monto AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        CONCAT(TRIM(IFNULL(D.Nombre,'')),' ',TRIM(IFNULL(Appaterno,'')),' ',TRIM(IFNULL(D.Apmaterno,''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        cninhabilitacion.detalle_cni D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                            LEFT JOIN
                        egobierno.folios F ON T.idTrans = F.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "32"
                desc = "CARTA DE NO INHABILITACIÓN"
            case 90:
                qry = """ SELECT 
                    D.id_tramite AS sub_folio,
                    IFNULL(D.rfc, '') AS RFC,
                    IFNULL(D.curp, '') AS CURP,
                    '' AS cuenta,
                    '' AS anio,
                    '' AS mes,
                    '' AS tipo_declaracion,
                    D.importe_tramite AS totalcargo,
                    '' AS maquinas,
                    '' AS placa,
                    '' AS solicitud,
                    '' AS concesion,
                    '' AS licencia,
                    '' AS municipio,
                    '' AS expcat,
                    '' AS boleta,
                    '' AS credito,
                    '' AS convenio,
                    '' AS parcialidad,
                    '' AS adicional_1,
                    '' AS adicional_2,
                    '' AS adicional_3,
                    '' AS adicional_4,
                    '' AS adicional_5,
                    '' AS adicional_6,
                    IFNULL(R.Linea, '') AS referencia,
                    IF(T.totaltramite = 0,
                        0,
                        IFNULL(T.tipopago, 0)) AS origentramites,
                    T.idTrans AS idTrans,
                    T.NombreEnvio AS nombrerc,
                    IF(LENGTH(D.rfc) = 12, IFNULL(D.razon_social, ''), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.paterno, ''),' ',IFNULL(D.materno, ''))) AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    egobierno.tramites D
                        LEFT JOIN
                    egobierno.transacciones T ON D.id_transaccion = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idTrans = T.idTrans
                WHERE
                    T.idTrans = """ + str(id)
                cve = "90"
                desc = "DUPLICADOS DE ESTUDIOS DE EDUCACION SECUNDARIA"
            case 106:
                qry = """ SELECT 
                    D.id_tramite AS sub_folio,
                    IFNULL(D.rfc, '') AS RFC,
                    IFNULL(D.curp, '') AS CURP,
                    '' AS cuenta,
                    '' AS anio,
                    '' AS mes,
                    '' AS tipo_declaracion,
                    D.importe_tramite AS totalcargo,
                    '' AS maquinas,
                    '' AS placa,
                    '' AS solicitud,
                    '' AS concesion,
                    '' AS licencia,
                    '' AS municipio,
                    '' AS expcat,
                    '' AS boleta,
                    '' AS credito,
                    '' AS convenio,
                    '' AS parcialidad,
                    '' AS adicional_1,
                    '' AS adicional_2,
                    '' AS adicional_3,
                    '' AS adicional_4,
                    '' AS adicional_5,
                    '' AS adicional_6,
                    IFNULL(R.Linea, '') AS referencia,
                    IF(T.totaltramite = 0,
                        0,
                        IFNULL(T.tipopago, 0)) AS origentramites,
                    T.idTrans AS idTrans,
                    T.NombreEnvio AS nombrerc,
                    IF(LENGTH(D.rfc) = 12, IFNULL(D.razon_social, ''), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.paterno, ''),' ',IFNULL(D.materno, ''))) AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    egobierno.tramites D
                        LEFT JOIN
                    egobierno.transacciones T ON D.id_transaccion = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idTrans = T.idTrans
                WHERE
                    T.idTrans = """ + str(id)
                cve = "106"
                desc = "AVISO PRE-PREVENTIVO"
            case 107:
                qry = """ SELECT 
                        D.id_tramite AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_tramite AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, IFNULL(D.razon_social, ''), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.paterno, ''),' ',IFNULL(D.materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.tramites D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "107"
                desc = "AVISO PREVENTIVO"
            case 112:
                qry = """ SELECT 
                        D.id_tramite AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_tramite AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, IFNULL(D.razon_social, ''), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.paterno, ''),' ',IFNULL(D.materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.tramites D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "112"
                desc = "CANCELACION DE HIPOTECA"
            case 137:
                qry = """ SELECT 
                        D.id_tramite AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_tramite AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, IFNULL(D.razon_social, ''), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.paterno, ''),' ',IFNULL(D.materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.tramites D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "137"
                desc = "COMPR-VENTA TRASL D/DOMINIO PGO EN LiNEA"
            case 161:
                qry = """ SELECT 
                        D.folio AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_total AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, '')), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.detalle_agilgob D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "161"
                desc = "COPIA CERTIFICADA DE DEFUNCIÓN"
            case 520:
                qry = """ SELECT 
                        D.folio AS sub_folio,
                        IFNULL(D.rfc, '') AS RFC,
                        IFNULL(D.curp, '') AS CURP,
                        '' AS cuenta,
                        '' AS anio,
                        '' AS mes,
                        '' AS tipo_declaracion,
                        D.importe_total AS totalcargo,
                        '' AS maquinas,
                        '' AS placa,
                        '' AS solicitud,
                        '' AS concesion,
                        '' AS licencia,
                        '' AS municipio,
                        '' AS expcat,
                        '' AS boleta,
                        '' AS credito,
                        '' AS convenio,
                        '' AS parcialidad,
                        '' AS adicional_1,
                        '' AS adicional_2,
                        '' AS adicional_3,
                        '' AS adicional_4,
                        '' AS adicional_5,
                        '' AS adicional_6,
                        IFNULL(R.Linea, '') AS referencia,
                        IF(T.totaltramite = 0,
                            0,
                            IFNULL(T.tipopago, 0)) AS origentramites,
                        T.idTrans AS idTrans,
                        T.NombreEnvio AS nombrerc,
                        IF(LENGTH(D.rfc) = 12, CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, '')), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, ''))) AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        egobierno.detalle_agilgob D
                            LEFT JOIN
                        egobierno.transacciones T ON D.id_transaccion = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "520"
                desc = "COPIA CERTIFICADA DE ACTA DE NACIMIENTO"
            case 521:
                qry = """ SELECT 
                            D.folio AS sub_folio,
                            IFNULL(D.rfc, '') AS RFC,
                            IFNULL(D.curp, '') AS CURP,
                            '' AS cuenta,
                            '' AS anio,
                            '' AS mes,
                            '' AS tipo_declaracion,
                            D.importe_total AS totalcargo,
                            '' AS maquinas,
                            '' AS placa,
                            '' AS solicitud,
                            '' AS concesion,
                            '' AS licencia,
                            '' AS municipio,
                            '' AS expcat,
                            '' AS boleta,
                            '' AS credito,
                            '' AS convenio,
                            '' AS parcialidad,
                            '' AS adicional_1,
                            '' AS adicional_2,
                            '' AS adicional_3,
                            '' AS adicional_4,
                            '' AS adicional_5,
                            '' AS adicional_6,
                            IFNULL(R.Linea, '') AS referencia,
                            IF(T.totaltramite = 0,
                                0,
                                IFNULL(T.tipopago, 0)) AS origentramites,
                            T.idTrans AS idTrans,
                            T.NombreEnvio AS nombrerc,
                            IF(LENGTH(D.rfc) = 12, CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, '')), CONCAT(IFNULL(D.nombre, ''),' ',IFNULL(D.ap_paterno, ''),' ',IFNULL(D.ap_materno, ''))) AS nombretr,
                            T.totaltramite AS importe_pago,
                            REPLACE(IFNULL(C.fecha_banco, '00000000'),
                                '-',
                                '') AS fechapago
                        FROM
                            egobierno.detalle_agilgob D
                                LEFT JOIN
                            egobierno.transacciones T ON D.id_transaccion = T.idTrans
                                LEFT JOIN
                            egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                                LEFT JOIN
                            conciliacion.conciliacion C ON C.idTrans = T.idTrans
                        WHERE
                            T.idTrans = """ + str(id)
                cve = "521"
                desc = "COPIA CERTIFICADA DE ACTA DE DIVORCIO"

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
                row = dict()
                row['sub_folio'] = r['sub_folio']
                row['clave_tramite'] = cve
                row['descripcion_tramite'] = desc
                row['rfc'] = r['RFC']
                row['curp'] = r['CURP']
                row['nombre_rs'] = r['nombretr']
                row['cuenta_estatal'] = r['cuenta']
                row['anio_ejercicio'] = r['anio']
                row['mes_ejercicio'] = r['mes']
                row['tipo_declaracion'] = r['tipo_declaracion']
                row['importe_tramite'] = r['totalcargo']
                row['maquinas'] = r['maquinas']
                row['placa'] = r['placa']
                row['solicitud'] = r['solicitud']
                row['concesion'] = r['concesion']
                row['licencia'] = r['licencia']
                row['municipio'] = r['municipio']
                row['expediente_catastral'] = r['expcat']
                row['boleta'] = r['boleta']
                row['credito'] = r['credito']
                row['convenio'] = r['convenio']
                row['parcialidad'] = r['parcialidad']
                row['adicional_1'] = r['adicional_1']
                row['adicional_2'] = r['adicional_2']
                row['adicional_3'] = r['adicional_3']
                row['adicional_4'] = r['adicional_4']
                row['adicional_5'] = r['adicional_5']
                row['adicional_6'] = r['adicional_6']
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
