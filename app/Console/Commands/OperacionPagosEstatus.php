<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use App\Models\Transacciones;
use App\Models\OperPagos;
use App\Models\OperProcessedregisters;

class OperacionPagosEstatus extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'pagos:estatus';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'buscar las transacciones que esten cancelados para actualizarlo en oper_pagos_api';

    /**
     * Execute the console command.
     */
    public function handle()
    {
       $this->transaccionesCancelados();
    }
    private function transaccionesCancelados(){
        try {
            $fechaInicio=Carbon::now()->addMonth(-2)->format("Y-m-d") . " 00:00:00";
            $fechaHoy=Carbon::now()->format("Y-m-d") . " 23:59:59";
            $registros = Transacciones::select("oper_transacciones.*")
            ->join("oper_pagos_api","oper_pagos_api.id_transaccion_motor","oper_transacciones.id_transaccion_motor")
            ->whereBetween("oper_transacciones.fecha_transaccion",[$fechaInicio,$fechaHoy])
            ->whereRaw('oper_transacciones.estatus <> oper_pagos_api.estatus')
            ->get();
            if($registros->count() > 0){
                foreach($registros as $reg){
                    OperPagos::where("id_transaccion_motor",$reg->id_transaccion_motor)->update(["estatus"=>$reg->estatus]);
                    Log::info("[OperacionCancelados@updateTable]-Command para actualizar la tabla de pagos folio: " .  $reg->id_transaccion_motor); 
                }
            }
        } catch (\Exception $e) {
            log::info("[OperacionCancelados@updateTable]-Command error: " . $e);
        }
    }
}
