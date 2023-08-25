<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use App\Models\OperMetodosPago;
use App\Models\Transacciones;
use App\Models\OperPagos;
use App\Models\OperTramites;
use App\Models\OperProcessedregisters;

class OperacionPagos extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'operacion:pagos';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'llena la tabla de oper_pagos_api con las transacciones pagas';
    protected $list_mp;
    /**
     * Execute the console command.
     */
    public function __construct(){ 
        parent::__construct();
        $this->loadMetodosPago();
        
    }
    public function handle(){
        $this->updateTable();
    }
    public function updateTable(){
        try{
            $fechaInicio=Carbon::now()->addMonth(-15)->format("Y-m-d") . " 00:00:00";
            $fechaHoy=Carbon::now()->format("Y-m-d") . " 23:59:59";
            Log::info("[OperacionPagos@updateTable]-Command para actualizar la tabla de pagos" );                 
            $registros = Transacciones::select("oper_transacciones.*")
            ->leftjoin ("oper_pagos_api","oper_pagos_api.id_transaccion_motor","oper_transacciones.id_transaccion_motor")
            ->where('oper_transacciones.estatus',0)
            ->whereBetween("oper_transacciones.fecha_transaccion",[$fechaInicio,$fechaHoy])
            ->where("oper_pagos_api.id_transaccion_motor",NULL)
            ->take(1000)
            ->get();

            Log::info("[OperacionPagos@updateTable]-Registros a buscar " . $registros->count() );
            if($registros->count() > 0){
                foreach($registros as $reg){
                    $detalles=OperTramites::where("id_transaccion_motor",$reg->id_transaccion_motor)
                    ->with("servicios")
                    ->get();
                    $extras=array();                    
                    foreach ($detalles as $d) {
                        $auxiliar=$d->auxiliar_2;
                        #Log::Info("contains " . str_contains($auxiliar,"{"));
                        if(str_contains($auxiliar,"{")){
                            $auxiliar="";
                        }
                        $extras []=array(
                            "sub_folio"             =>$d->id_tramite_motor,
                            "clave_tramite"         =>$d["servicios"][0]["Tipo_Code"],
                            "descripcion_tramite"   =>$d["servicios"][0]["Tipo_Descripcion"],
                            "rfc"                   =>$d->rfc,
                            "curp"                  =>$d->curp,
                            "nombre_rs"             =>$d->nombre . " " . $d->apellido_paterno . " " . $d->apellido_materno . $d->razon_social,
                            "cuenta_estatal"        =>"",
                            "anio_ejercicio"        =>"",
                            "mes_ejercicio"         =>"",
                            "tipo_declaracion"      =>"",
                            "importe_tramite"       =>$d->importe_tramite,
                            "maquinas"              =>"",
                            "placa"                 =>$auxiliar,
                            "solicitud"             =>"",
                            "concesion"             =>"",
                            "licencia"              =>"",
                            "municipio"             =>"",
                            "expediente_catastral"  =>"",
                            "boleta"                =>"",
                            "credito"               =>"",
                            "convenio"              =>"",
                            "parcialidad"           =>"",
                            "adicional_1"           =>"",
                            "adicional_2"           =>"",
                            "adicional_3"           =>"",
                            "adicional_4"           =>"",
                            "adicional_5"           =>"",
                            "adicional_6"           =>""
                        );
                    }
                    $detalle=array(
                        "referencia_bancaria"   => $reg->referencia,
                        "folio"                 => $reg->id_transaccion_motor,
                        "origen_tramites"       => $reg->tipo_pago,
                        "origen_pago"           => "027",
                        "medio_pago"            => "",
                        "importe_pago"          => $reg->importe_transaccion,
                        "fecha_pago"            => Carbon::parse($reg->fecha_pago)->format("Ymd"),
                        "hora_pago"             => Carbon::parse($reg->fecha_pago)->format("His"),
                        "tramites"              => $extras
                    );
                    $info = array(
                        'id_transaccion_motor'  => $reg->id_transaccion_motor,
                        'id_transaccion'        => $reg->id_transaccion,
                        'estatus'               => $reg->estatus,
                        'entidad'               => $reg->entidad,
                        'referencia'            => $reg->referencia,
                        'Total'                 => $reg->importe_transaccion,
                        'MetododePago'          => $this->list_mp[$reg->metodo_pago_id],
                        'cve_Banco'             => $reg->tipo_pago,
                        'FechaTransaccion'      => $reg->fecha_transaccion,
                        'FechaPago'             => $reg->fecha_pago,
                        'FechaConciliacion'     => $this->obtenerfechaConciliacion($reg->referencia),
                        'procesado'             => 0,
                        'detalle'               => json_encode($detalle)
                    );
                    //Log::info("[Pagosas400@updateTable]-Insertar pago" );                    
                    if(OperPagos::where('id_transaccion_motor','=', $reg->id_transaccion_motor)->count() == 0){
                        OperPagos::create( $info );                    
                    }
                }              
            }else{
                Log::info("[OperacionPagos@updateTable]-No existen pagos sin procesar");
            }
    
        }catch(\Exception $e){
            Log::info("[OperacionPagos@updateTable]-ERROR-".$e->getMessage());
            dd($e->getMessage());
        }
        Log::info("[OperacionPagos@updateTable]-Proceso terminado");
    }
    private function obtenerfechaConciliacion($referencia)
    {   
        $info = OperProcessedregisters::where("referencia",$referencia)->get();
        if($info->count() > 0){
            foreach($info as $i){
                return $i->fecha_ejecucion;
            }
        }else{
            return "";
        }
    }
    private function loadMetodosPago(){        
        $res = array();
        $info = OperMetodosPago::all();

        foreach($info as $i){
            $res [$i->id]= $i->nombre;
        }
        $res [0]= "No Identificado";
        $this->list_mp = $res;
    }
}
