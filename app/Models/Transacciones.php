<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use SebastianBergmann\CodeCoverage\Node\Builder;
/**
 * Class Transacciones.
 *
 * @package namespace App\Entities;
 */
class Transacciones extends Model 
{
    use HasFactory;


   protected $connection = "mysql";

    protected $fillable = [
        'id_transaccion_motor',
        'estatus',
        'referencia',
        'importe_transaccion',
        'fecha_transaccion',
        'id_transaccion',
        'fecha_limite_referencia',
        'fecha_pago',
        'entidad',
        'tipo_pago',
        'id_transaccion',
        'email_referencia',
        'email_pago',
        'revisado'
    ];

    protected $table = "oper_transacciones";
    public $timestamps = true;
    public function tramites() {
		return $this->hasMany("App\Models\OperTramites", "id_transaccion_motor", "id_transaccion_motor");
	}
    public static function findTransaccionesFolio($entidad,$variable1,$variable2)
    {
        
        $data = Transacciones::select(
            'oper_transacciones.entidad AS entidad',
            'oper_transacciones.referencia AS referencia',
            'oper_transacciones.id_transaccion_motor AS id_transaccion_motor',
            'oper_transacciones.id_transaccion AS id_transaccion',
            'oper_transacciones.estatus AS estatus',
            'oper_transacciones.importe_transaccion  AS Total',
            'oper_metodopago.nombre AS MetododePago',
            'oper_transacciones.tipo_pago AS cve_Banco',
            'oper_transacciones.banco AS Banco',
            'oper_transacciones.fecha_transaccion AS FechaTransaccion',
            'oper_transacciones.fecha_pago AS FechaPago',
            'oper_processedregisters.fecha_ejecucion AS FechaConciliacion')
        ->leftjoin('oper_metodopago','oper_metodopago.id','=','oper_transacciones.metodo_pago_id')
        //->leftjoin('oper_banco','oper_banco.id','=','oper_transacciones.banco')
        ->leftjoin('oper_processedregisters','oper_processedregisters.referencia','=','oper_transacciones.referencia')
        #->leftjoin('oper_usuariobd_entidad','oper_usuariobd_entidad.id_entidad','=','oper_transacciones.entidad')
         #->leftjoin('oper_pagos_solicitud','oper_pagos_solicitud.id_transaccion_motor','=','oper_transacciones.id_transaccion_motor')
         ->whereIn("oper_transacciones.entidad",$entidad)
         #->where('oper_usuariobd_entidad.usuariobd' ,'=', $user)  
         ->whereIn($variable1,$variable2) 
        //->whereIn('oper_transacciones.entidad' ,$entidad)  
        //->Where('oper_pagos_solicitud.id_transaccion_motor','=',null)
        ->orderBy('oper_transacciones.id_transaccion_motor', 'DESC')
        ->get();
          return $data;
       
    }
    public static function findtransaccionesDetalle($referencia){
        $data=Transacciones::where('oper_transacciones.estatus','0')
            ->leftjoin("oper_tramites as tramites","tramites.id_transaccion_motor","oper_transacciones.id_transaccion_motor")
            ->leftjoin("oper_detalle_tramite as detalle","detalle.id_tramite_motor","tramites.id_tramite_motor")
            ->leftjoin("oper_processedregisters as concilia","concilia.referencia","oper_transacciones.referencia")
            ->where("oper_transacciones.referencia",$referencia)
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
                'oper_transacciones.referencia',
                'concilia.banco_id',
                'concilia.info_transacciones',
                'concilia.cuenta_banco',
                'concilia.cuenta_alias',
                'concilia.fecha_ejecucion',
                'concilia.day',
                'concilia.month',
                'concilia.year',
                'oper_transacciones.metodo_pago_id',
                'oper_transacciones.cuenta_deposito',
                'fecha_transaccion as fecha_tramite',
                'fecha_transaccion as hora_tramite',
                'tramites.id_tramite_motor as Folio',
                'tramites.id_tipo_servicio as tipo_servicio',
                'tramites.auxiliar_1',
                'tramites.auxiliar_2',
                'detalle.concepto',
                'detalle.importe_concepto',
                'detalle.partida',
                'oper_transacciones.id_transaccion_motor',
                'tramites.nombre',
                'tramites.apellido_paterno',
                'tramites.apellido_materno',
                'tramites.razon_social'
            )
            ->groupBy('detalle.id_detalle_tramite','oper_transacciones.referencia')
            ->orderBy('oper_transacciones.id_transaccion_motor','DESC')
            ->take(1000)
            ->get();
        return $data;
    }
    public static function findTransaccionesEstatus($entidad,$sign,$status,$variable){
        $data = Transacciones::select(
            'oper_transacciones.entidad AS entidad',
            'oper_transacciones.referencia AS referencia',
            'oper_transacciones.id_transaccion_motor AS id_transaccion_motor',
            'oper_transacciones.id_transaccion AS id_transaccion',
            'oper_transacciones.estatus AS estatus',
            'oper_transacciones.importe_transaccion  AS Total',
            'oper_metodopago.nombre AS MetododePago',
            'oper_transacciones.tipo_pago AS cve_Banco',
            'oper_transacciones.banco AS Banco',
            'oper_transacciones.fecha_transaccion AS FechaTransaccion',
            'oper_transacciones.fecha_pago AS FechaPago',
            'oper_processedregisters.fecha_ejecucion AS FechaConciliacion')
        ->leftjoin('oper_metodopago','oper_metodopago.id','=','oper_transacciones.metodo_pago_id')
        ->leftjoin('oper_processedregisters','oper_processedregisters.referencia','=','oper_transacciones.referencia')
         ->where("oper_transacciones.estatus",$sign,$status)
         ->whereIn("oper_transacciones.entidad",$entidad)
         ->whereBetween("oper_transacciones.fecha_transaccion",$variable) 
        ->orderBy('oper_transacciones.id_transaccion_motor', 'DESC')
        ->get();
        return $data;       
    }
    public static function findtransaccionesGeneral($variable,$folio,$entidad){
        $data=Transacciones::where("oper_transacciones.".$variable,$folio)
            ->leftjoin("oper_tramites as tramites","tramites.id_transaccion_motor","oper_transacciones.id_transaccion_motor")
            ->leftjoin("oper_processedregisters as concilia","concilia.referencia","oper_transacciones.referencia")            
            ->whereIn("oper_transacciones.entidad",$entidad)
            ->select(
                'oper_transacciones.referencia',
                'concilia.fecha_ejecucion as fecha_conciliacion',
                'oper_transacciones.metodo_pago_id',
                'oper_transacciones.cuenta_deposito',
                'oper_transacciones.fecha_transaccion as fecha_tramite',
                'oper_transacciones.id_transaccion_motor'
            )
            ->with(['tramites'=>function ($query) {
                $query->leftjoin("egobierno.tipo_servicios as serv","serv.Tipo_Code","id_tipo_servicio")
                ->select('id_transaccion_motor','id_tramite_motor','id_tipo_servicio', 'serv.Tipo_Descripcion');
            }])
            ->groupBy('tramites.id_tramite_motor','oper_transacciones.referencia')
            ->orderBy('oper_transacciones.id_transaccion_motor','DESC')
            ->get();
        return $data;
    }

}
