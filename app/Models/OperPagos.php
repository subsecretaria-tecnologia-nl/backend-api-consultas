<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperPagos extends Model
{
    use HasFactory;
    protected $connection = "mysql";
    protected $fillable = ['transacciones_id','id_transaccion_motor','id_transaccion','estatus','entidad','referencia','Total','MetododePago','cve_Banco','FechaTransaccion','FechaPago','FechaConciliacion','tipo_servicio','desc_tipo_servicio','detalle','procesado'];

    protected $table = "oper_pagos_api";

    public static function findtransaccionesDetalle($date){
        $data=OperPagos::where('oper_pagos_api.estatus','0')
            ->leftjoin("oper_tramites as tramites","tramites.id_transaccion_motor","oper_pagos_api.id_transaccion_motor")
            ->leftjoin("oper_detalle_tramite as detalle","detalle.id_tramite_motor","tramites.id_tramite_motor")
            ->leftjoin("oper_processedregisters as concilia","concilia.referencia","oper_pagos_api.referencia")
            ->leftjoin("oper_transacciones as trans","trans.referencia","oper_pagos_api.referencia")
            ->whereBetween("oper_pagos_api.created_at",$date)
            ->where('detalle.partida','<>','53234')
            ->where(function ($q) {
                $q->orWhere('detalle.partida','<>','56754')
                ->orWhere('detalle.concepto' ,'LIKE', '%Normal%')
                ->orWhere('detalle.concepto','LIKE', '%Diferencia%');
            })
            ->select(
                'concilia.transaccion_id',
                'detalle.id_detalle_tramite',
                'concilia.id',
                'oper_pagos_api.referencia',
                'concilia.banco_id',
                'concilia.info_transacciones',
                'concilia.cuenta_banco',
                'concilia.cuenta_alias',
                'concilia.fecha_ejecucion',
                'concilia.day',
                'concilia.month',
                'concilia.year',
                'trans.metodo_pago_id',
                'trans.cuenta_deposito',
                'fecha_transaccion as fecha_tramite',
                'fecha_transaccion as hora_tramite',
                'tramites.id_tramite_motor as Folio',
                'tramites.id_tipo_servicio as tipo_servicio',
                'tramites.auxiliar_1',
                'tramites.auxiliar_2',
                'detalle.concepto',
                'detalle.importe_concepto',
                'detalle.partida',
                'trans.id_transaccion_motor',
                'tramites.nombre',
                'tramites.apellido_paterno',
                'tramites.apellido_materno',
                'tramites.razon_social'
            )
            ->groupBy('detalle.id_detalle_tramite','oper_pagos_api.referencia')
            ->orderBy('oper_pagos_api.id','DESC')
            ->take(1000)
            ->get();
        return $data;
    }
    public static function findTransaccionesFolio($entidad,$variable1,$variable2){
        $data = OperPagos::select("ent.nombre as entidad",
        "referencia",
        "id_transaccion_motor",
        "id_transaccion",
        "estatus",
        "Total",
        "MetododePago",
        "cve_Banco",
        "FechaTransaccion",
        "FechaPago",
        "FechaConciliacion")
        ->whereIn("entidad",$entidad)
        //->where("estatus",0)
        ->whereIn($variable1,$variable2)
        ->leftjoin("operacion.oper_entidad as ent","ent.id","entidad")
        ->get();
        return $data;
    }
}
