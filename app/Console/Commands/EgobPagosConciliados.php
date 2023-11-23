<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use App\Models\ExternoConcConciliacion;
use App\Models\OperPagos;

class EgobPagosConciliados extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'egob:conciliados';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Actualizar la fecha de conciliacion de las transacciones de egobierno';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $this->findUpdate();
    }
    private function findUpdate(){
        try {
            $registros = OperPagos::where("oper_pagos_api.entidad","=","24")
            ->where(function ($q) {
                $q->orWhere("FechaConciliacion","=",null)
                ->orWhere("FechaConciliacion","=","");
            })
            ->take(1000)
            ->orderBy("id","ASC")
            ->get();
            if($registros->count() > 0){                
                foreach($registros as $reg){
                    $findConciliacion=ExternoConcConciliacion::where("idTrans",$reg->id_transaccion_motor)->get();
                    if(count($findConciliacion)>0){
                        OperPagos::where("id_transaccion_motor",$reg->id_transaccion_motor)->update(["FechaConciliacion"=>$findConciliacion[0]["archivo"]]);
                        if($reg->FechaPago=="" || $reg->FechaPago==null){
                            OperPagos::where("id_transaccion_motor",$reg->id_transaccion_motor)->update(["FechaPago"=>$findConciliacion[0]["fecha_banco"]]);
                        }
                        Log::info("[EgobPagosConciliados@findUpdate]-Command para actualizar la tabla de pagos referencia: " .  $reg->referencia); 
                    }                    
                }
            }
        } catch (\Exception $e) {
            log::info('Error EgobPagosConciliados@findUpdate' . $e->getMessage());
        }
    }
}
