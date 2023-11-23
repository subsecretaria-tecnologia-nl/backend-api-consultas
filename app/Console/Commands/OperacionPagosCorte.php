<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use App\Models\OperPagos;
use App\Models\Transacciones;

class OperacionPagosCorte extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'operacion:pagoscorte';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'actualiza el campo en la tabla de oper_pagos_api en json de la estrura del corte';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $this->findTransacciones();
    }
    public function findTransacciones(){
        try {
            $fechaInicio=Carbon::now()->addMonth(-2)->format("Y-m-d") . " 00:00:00";
            $fechaHoy=Carbon::now()->format("Y-m-d") . " 23:59:59";
            $data=OperPagos::where('oper_pagos_api.estatus','0')
            ->where("oper_pagos_api.corte","")
            ->where("oper_pagos_api.entidad","<>","24")
            ->leftjoin("oper_processedregisters as concilia","concilia.referencia","oper_pagos_api.referencia")
            ->whereBetween("oper_pagos_api.created_at",[$fechaInicio,$fechaHoy])
            ->select("oper_pagos_api.*","concilia.banco_id")
            ->get();
            //log::info($data);
           $this->gJsonCorte($data);

        } catch (\Exception $e) {
            log::info('Error OperacionPagosCorte@findTransacciones' . $e->getMessage());
        }
    }
    private function gJsonCorte($data){
        try {
            $array_corte=array();
            foreach($data as $d){
                $findDetalle=Transacciones::findtransaccionesDetalle($d->referencia);
                $detalle=array();
                foreach($findDetalle as $detalle){
                    $auxiliar_2=$detalle->auxiliar_2;
                        if(strpos($auxiliar_2,"{") || strpos($auxiliar_2,"}")){$auxiliar_2="";}
                    $RowNombreRazonS=$detalle->razon_social;
                    if($detalle->nombre!=null){
                        $RowNombreRazonS=$detalle->nombre . " " . $detalle->apellido_paterno . " " . $detalle->apellido_materno;
                    }
                    $detalle []=array(
                        "clave_tramite"=> '025001',                    
                        "fecha_dispocision"=>Carbon::parse($detalle->fecha_ejecucion)->format('Ymd') ,
                        "hora_disposicion"=>  Carbon::parse($detalle->fecha_ejecucion)->format('His'),
                        "fecha_pago"=> Carbon::parse($detalle->year . '-' . $detalle->month . '-' . $detalle->day)->format('Ymd'),
                        "hora_pago"=> Carbon::parse($detalle->year . '-' . $detalle->month . '-' . $detalle->day)->format('his'),
                        "cuenta_pago"=>  $detalle->cuenta_banco,
                        "alias"=>  $detalle->cuenta_alias,
                        "dato_adicional_1"=>  $detalle->id_transaccion_motor,
                        "dato_adicional_2"=> $auxiliar_2,
                        "nombre_razonSocial"=>  $RowNombreRazonS,
                        "partida"=>  $detalle->partida,
                        "consepto"=>  $detalle->concepto
                    );
                }
                $array_corte=array(
                    "referencia"=> $d->referencia,
                    "folio"=> $d->id_transaccion_motor,
                    "origen"=> "027",
                    "medio_pago"=> $d->banco_id,
                    "total_apgo"=> $d->Total,
                    "detalle"=>$detalle
                );
                OperPagos::where("id",$d->id)->update(["corte"=>json_encode($array_corte)]);
            }
            
        } catch (\Exception $e) {
            log::info('Error OperacionPagosCorte@gJsonCorte' . $e->getMessage());
        }
    }
}
