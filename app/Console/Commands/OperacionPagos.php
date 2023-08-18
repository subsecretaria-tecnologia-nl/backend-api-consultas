<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use App\Models\OperMetodosPago;
use App\Models\Transacciones;
use App\Models\OperPagos;
use App\Models\OperTramites;

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
            $fechaInicio=Carbon::now()->addMonth(-2)->format("Y-m-s") . " 00:00:00";
            $fechaHoy=Carbon::now()->format("Y-m-s") . " 23:59:59";
            Log::info("[Pagosas400@updateTable]-Command para actualizar la tabla de pagos" );                 
            $registros = Transacciones::where('estatus',0)
                ->whereBetween("fecha_transaccion",[$fechaInicio,$fechaHoy])
                ->get();

            Log::info("[Pagosas400@updateTable]-Registros a buscar " . $registros->count() );

            if($registros->count() > 0){
                foreach($registros as $reg){
                    $detalles=OperTramites::where("id_transaccion_motor",$reg->id_transaccion_motor)->get();
                    $extras=array();
                    foreach ($detalles as $d) {
                        $extras []=array(
                            "sub_folio"=>$d->id_tramite_motor,
                            "clave_tramite"=>"",
                            "descripcion_tramite"=>"",
                            "rfc"=>$d->rfc,
                            "curp"=>$d->curp,
                            "cuenta_estatal"=>"",
                            "anio_ejercicio"=>"",
                            "mes_ejercicio"=>"",
                            "tipo_declaracion"=>"",
                            "importe_tramite"=>"",
                            "maquinas"=>"",
                            "placa"=>$d->auxiliar_2,
                            "solicitud"=>"",
                            "concecion"=>"",
                            "licencia"=>"",
                            "municipio"=>"",
                            "expediente_catastral"=>"",
                            "boleta"=>"",
                            "credito"=>"",
                            "convenio"=>"",
                            "parcialidad"=>"",
                            "adicional_1"=>"",
                            "adicional_2"=>"",
                            "adicional_3"=>"",
                            "adicional_4"=>"",
                            "adicional_5"=>"",
                            "adicional_6"=>""
                        );
                    }
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
                        'detalle'               => json_encode($extras)
                    );
                    //Log::info("[Pagosas400@updateTable]-Insertar pago" );                    
                    if(OperPagos::where('id_transaccion_motor','=', $reg->id_transaccion_motor)->count() == 0){
                        OperPagos::create( $info );                    
                    }
                }              
            }else{
                Log::info("[Pagosas400@updateTable]-No existen pagos sin procesar");
            }
    
        }catch(\Exception $e){
            Log::info("[Pagosas400@updateTable]-ERROR-".$e->getMessage());
            dd($e->getMessage());
        }
        Log::info("[Pagosas400@updateTable]-Proceso terminado");
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
