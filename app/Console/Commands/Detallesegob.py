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
                desc = "INFORMATIVO VALOR CATASTRAL"
            case 13:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    IFNULL(D.curp, '') AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio_1, '') AS anio,
                    IFNULL(D.mes_1, '') AS mes,
                    IFNULL(D.tipo_declaracion, '') AS tipo_declaracion,
                    IFNULL(D.total_cargo, '') AS totalcargo,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.detalle_isan D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "13"
                desc = "ISAN"
            case 14:
                qry = """ SELECT 
                        D.Folio AS sub_folio,
                        IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                        IFNULL(D.curp,'') AS CURP,
                        IFNULL(D.cuenta,'') AS cuenta,
                        IFNULL(D.anio,'') AS anio,
                        IFNULL(D.mes,'') AS mes,
                        IFNULL(D.tipo_declaracion,'') AS tipo_declaracion,
                        IFNULL(D.total_cargo,'') AS totalcargo,
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
                        D.nombre_razonS AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        contribuyente.detalle_ish D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idtrans = T.idTrans
                    WHERE
                        D.idTrans = """ +str(id)
                cve = "14"
                desc = "ISH"
            case 15:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    IFNULL(D.curp, '') AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    IFNULL(D.mes, '') AS mes,
                    '' AS tipo_declaracion,
                    IFNULL(D.total_contribuciones, '') AS totalcargo,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.detalle_isop D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "15"
                desc = "ISOP"
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
            case 24:
                qry = """ SELECT 
                        D.folio AS sub_folio,
                        CONCAT(IFNULL(D.rfcalfa,''),IFNULL(D.rfcnum,''),IFNULL(D.rfchom,'')) AS RFC,
                        IFNULL(D.curp,'') AS CURP,
                        IFNULL(D.cuenta,'') AS cuenta,
                        IFNULL(D.anio,'') AS anio,
                        IFNULL(D.mes,'') AS mes,
                        IFNULL(D.tipo_declaracion,'') AS tipo_declaracion,
                        D.total AS totalcargo,
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
                        '' AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        contribuyente.detalle_isn_retenedor D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idTrans = T.idTrans
                    WHERE
                        T.idTrans = """ + str(id)
                cve = "24"
                desc = "RETENCIÓN DE IMPUESTO SOBRE NÓMINA"
            case 25:
                qry = """ SELECT 
                    D.folio AS sub_folio,
                    CONCAT(IFNULL(D.rfcalf, ''),
                            IFNULL(D.rfcnum, ''),
                            IFNULL(D.rfchom, '')) AS RFC,
                    IFNULL(D.curp, '') AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    IFNULL(D.mes, '') AS mes,
                    IFNULL(D.tipo_dec, '') AS tipo_declaracion,
                    D.ttl_cont_isop AS totalcargo,
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
                    '' AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.det_imp_isop D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idTrans = T.idTrans
                WHERE
                    T.idTrans = """ + str(id)
                cve = "25"
                desc = "IMPUESTO POR JUEGOS CON APUESTAS Y OBTENCIÓN DE PREMIOS"
            case 26:
                qry = """ SELECT 
                    D.folio AS sub_folio,
                    '' AS RFC,
                    '' AS CURP,
                    '' AS cuenta,
                    IFNULL(D.ejercicio_fiscal, '') AS anio,
                    '' AS mes,
                    '' AS tipo_declaracion,
                    D.monto_retencion AS totalcargo,
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
                    UPPER(IFNULL(T.NombreEnvio,'')) AS nombrerc,
                    '' AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    servicios.detalle_aportacion D
                        LEFT JOIN
                    egobierno.transacciones T ON D.id_transaccion = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idTrans = T.idTrans
                WHERE
                    T.idTrans """ + str(id)
                cve = "26"
                desc = "APORTACIONES AL MILLAR"
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
                qry = """ SELECT 
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
            case 43:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    '' AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    IFNULL(D.mes, '') AS mes,
                    IFNULL(D.tipo_declaracion, '') AS tipo_declaracion,
                    IFNULL(D.total_cargo, '') AS totalcargo,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.det_imp_emi_conatmosfera D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "43"
                desc = "IMPUESTO AMBIENTAL POR CONTAMINACIÓN EN LA EXTRACCIÓN DE MATERIALES PÉTREOS"
            case 44:
                qry = """ SELECT 
                        D.Folio AS sub_folio,
                        IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                        '' AS CURP,
                        IFNULL(D.cuenta,'') AS cuenta,
                        IFNULL(D.anio,'') AS anio,
                        IFNULL(D.mes,'') AS mes,
                        IFNULL(D.tipo_declaracion,'') AS tipo_declaracion,
                        IFNULL(D.total_cargo,'') AS totalcargo,
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
                        D.nombre_razonS AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        contribuyente.det_imp_emi_conatmosfera D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idtrans = T.idTrans
                    WHERE
                        D.idTrans = """ + str(id)
                cve = "44"
                desc = "IMPUESTO POR LA EMISIÓN DE CONTAMINANTES A LA ATMÓSFERA"
            case 45:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    '' AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    IFNULL(D.mes, '') AS mes,
                    IFNULL(D.tipo_declaracion, '') AS tipo_declaracion,
                    IFNULL(D.total_cargo, '') AS totalcargo,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.detalle_iec_agua D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "45"
                desc = "IMPUESTO POR LA EMISIÓN DE CONTAMINANTES EN EL AGUA"
            case 46:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    '' AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    IFNULL(D.mes, '') AS mes,
                    IFNULL(D.tipo_declaracion, '') AS tipo_declaracion,
                    IFNULL(D.total_cargo, '') AS totalcargo,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.detalle_iec_subsu D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "46"
                desc = "IMPUESTO POR LA EMISIÓN DE CONTAMINANTES EN EL SUBSUELO Y/O SUELO"
            case 65:
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "65"
                desc = "DUPLICADOS DE ESTUDIOS DE EDUCACIÓN PRIMARIA"
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
            case 91:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "91"
                desc = "DUPLICADOS DE ESTUDIOS DE EDUCACIÓN PREESCOLAR"
            case 100:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "101"
                desc = "ACTA ACLARATORIA"
            case 101:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "101"
                desc = "ADJUDICACIÓN POR HERENCIA"
            case 102:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "102"
                desc = "ADJUDICACIÓN POR REMATE"
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
            case 108:
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
                cve = "108"
                desc = "CANCELACIÓN DE EMBARGO "
            case 109:
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
                cve = "109"
                desc = "CANCELACIÓN AVISO PRE-PREVENTIVO"
            case 111:
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
                cve = ""
                desc = "CANCELACIÓN DE GRAVAMEN "
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
            case 113:
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
                cve = "113"
                desc = "CANCELACIÓN DE HIPOTECA PARCIAL "
            case 116:
                qry  = """ SELECT 
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
                cve = "116"
                desc = "CÉDULA HIPOTECARIA"
            case 117:
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
                cve = "117"
                desc = "CERTIFICADO DE GRAVAMEN "
            case 118:
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
                cve = "118"
                desc = "CERTIFICADO DE LIBERTAD DE GRAVAMEN"
            case 119:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "119"
                desc = "COMPR-VENTA RESERVA DOMINIO"
            case 121:
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "121"
                desc = "CONVENIO MODIFICATORIO DE GRAVAMEN "
            case 122:
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "122"
                desc = "DACIÓN EN PAGO "
            case 123:
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "123"
                desc = "DISOLUCIÓN COPROPIEDAD Y APLICACIÓN DE BIENES "
            case 124:
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
                cve = "124"
                desc = "DISOLUCIÓN DE SOCIEDAD CONYUGAL "
            case 125:
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
                cve = "125"
                desc = "FIDEICOMISO "
            case 127:
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
                cve = "127"
                desc = "HIPOTECA O GRAVAMEN"
            case 133:
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
                cve = "133"
                desc = "PERMUTA"
            case 135:
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
                        T.idTrans = """
                cve = "135"
                desc = "RECTIFICACIÓN DE MEDIDASRECTIFICACIÓN DE MEDIDAS"
            case 136:
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
                cve = "136"
                desc = "CESIÓN DE DERECHOS"
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
            case 163:
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
                    IFNULL(D.auxiliar_1, '') AS expcat,
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "163"
                desc = "CANCELACIÓN DE AVISO PREVENTIVO"
            case 168:
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
                    IFNULL(D.auxiliar_1, '') AS expcat,
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "168"
                desc = "LICENCIA DE CAZA DEPORTIVA"
            case 169:
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
                        IFNULL(D.auxiliar_1,'') AS expcat,
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "169"
                desc = "PAGO DE IMPUESTO PREDIAL"
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
            case 552:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "552"
                desc = "PAGO DE EQUIVALENCIAS DE PREPARATORIA "
            case 553:
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "553"
                desc = "PAGO DE EQUIVALENCIAS DE LICENCIATURA"
            case 561:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "561"
                desc = "PAGO DE LEGALIZACIONES DE PREPARATORIA"
            case 562:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "562"
                desc = "PAGO DE LEGALIZACIONES DE LICENCIATURA"
            case 563:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "563"
                desc = "PAGO DE LEGALIZACIONES DE MAESTRÍA"
            case 564:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "564"
                desc = "PAGO DE VISTO BUENO O CONSTANCIA DE ESTUDIOS"
            case 566:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "566"
                desc = "PAGO DE LEGALIZACIONES DE CERTIFICADO DE ENFERMERÍA"
            case 567:
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "567"
                desc = "PAGO DE ELABORACIÓN DE CERTIFICADO DE NORMAL"
            case 572:
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
                cve = "572"
                desc = "PAGO DE LEGALIZACIÓN DE CERTIFICADO DE NORMALES"
            case 573:
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
                cve = "573"
                desc = "PAGO DE LEGALIZACIÓN DE ACTA DE EXAMEN"
            case 587:
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
                    IFNULL(D.auxiliar_1, '') AS expcat,
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
                    IF(LENGTH(D.rfc) = 12,
                        IFNULL(D.razon_social, ''),
                        CONCAT(IFNULL(D.nombre, ''),
                                ' ',
                                IFNULL(D.paterno, ''),
                                ' ',
                                IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "587"
                desc = "PAGO DE LEGALIZACIÓN DE TÍTULOS DE EDUCACIÓN SUPERIOR Y TÉCNICO SUPERIOR PROFESIONAL"
            case 588:
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
                       IFNULL(D.auxiliar_1, '') AS expcat,
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
                       IF(LENGTH(D.rfc) = 12,
                           IFNULL(D.razon_social, ''),
                           CONCAT(IFNULL(D.nombre, ''),
                                   ' ',
                                   IFNULL(D.paterno, ''),
                                   ' ',
                                   IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "588"
                desc = "PAGO DE LEGALIZACIÓN DE TÍTULOS DE ENFERMERÍA"
            case 597:
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
                        IF(LENGTH(D.rfc) = 12,
                            IFNULL(D.razon_social, ''),
                            CONCAT(IFNULL(D.nombre, ''),
                                    ' ',
                                    IFNULL(D.paterno, ''),
                                    ' ',
                                    IFNULL(D.materno, ''))) AS nombretr,
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
                cve = "597"
                desc = "PAGO DE VALIDACIÓN DE CERTIFICADOS DE ESTUDIOS"
            case 598:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    '' AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    '' AS mes,
                    IFNULL(D.tipo_declaracion, '') AS tipo_declaracion,
                    IFNULL(D.total_cargo, '') AS totalcargo,
                    IFNULL(D.cant_maquinas,'') AS maquinas,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.det_pago_derechos D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "598"
                desc = "ALTA DE MAQUINAS DE JUEGOS Y APUESTAS (100, 200 Y 300 CUOTAS)"
            case 599:
                qry = """ SELECT 
                    D.Folio AS sub_folio,
                    IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                    '' AS CURP,
                    IFNULL(D.cuenta, '') AS cuenta,
                    IFNULL(D.anio, '') AS anio,
                    '' AS mes,
                    IFNULL(D.tipo_declaracion, '') AS tipo_declaracion,
                    IFNULL(D.total_cargo, '') AS totalcargo,
                    IFNULL(D.cant_maquinas,'') AS maquinas,
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
                    D.nombre_razonS AS nombretr,
                    T.totaltramite AS importe_pago,
                    REPLACE(IFNULL(C.fecha_banco, '00000000'),
                        '-',
                        '') AS fechapago
                FROM
                    contribuyente.det_pago_derechos D
                        LEFT JOIN
                    egobierno.transacciones T ON D.idTrans = T.idTrans
                        LEFT JOIN
                    egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                        LEFT JOIN
                    conciliacion.conciliacion C ON C.idtrans = T.idTrans
                WHERE
                    D.idTrans = """ + str(id)
                cve = "599"
                desc = "PAGO DE DERECHOS POR LOS SERVICIOS DE SUPERVISION, CONTROL Y EXPEDICION DE CONSTANCIAS DE INGRESO A LA BD DE MAQUINAS DE JUEGOS Y APUESTAS (200 CUOTAS)"
            case 600:
                qry = """ SELECT 
                        D.Folio AS sub_folio,
                        IFNULL(CONCAT(D.rfcalf, D.rfcnum, D.rfchom), '') AS RFC,
                        IFNULL(D.curp,'') AS CURP,
                        IFNULL(D.cuenta,'') AS cuenta,
                        IFNULL(D.anio,'') AS anio,
                        IFNULL(D.mes,'') AS mes,
                        IFNULL(D.tipo_declaracion,'') AS tipo_declaracion,
                        IFNULL(D.total_cargo,'') AS totalcargo,
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
                        D.nombre_razonS AS nombretr,
                        T.totaltramite AS importe_pago,
                        REPLACE(IFNULL(C.fecha_banco, '00000000'),
                            '-',
                            '') AS fechapago
                    FROM
                        contribuyente.detalle_ish D
                            LEFT JOIN
                        egobierno.transacciones T ON D.idTrans = T.idTrans
                            LEFT JOIN
                        egobierno.referenciabancaria R ON R.idTrans = T.idTrans
                            LEFT JOIN
                        conciliacion.conciliacion C ON C.idtrans = T.idTrans
                    WHERE
                        D.idTrans = """ + str(id)
                cve = "600"
                desc = "IMPUESTO SOBRE HOSPEDAJE EN SU CARACTER DE INTERMEDIARIO O FACILITADOR"


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
