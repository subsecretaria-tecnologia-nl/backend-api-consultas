<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Carbon\Carbon;
use App\Models\OperProcessedregisters;
use App\Models\OperPagos;

class PagosEstatusConciliado extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'pagos:conciliado';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Actualiza la fecha de conciliacion de las transacciones en oper_pagos_api';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $this->transccionesConciliadas();
    }
    private function transccionesConciliadas(){
        try {
            $registros = OperPagos::select("oper_processedregiters.*")
            ->join("oper_processedregiters","oper_processedregiters.referencia","oper_pagos_api.referencia")
            ->where("oper_pagos_api.entidad","<>","24")
            ->where("oper_pagos_api.fechaConciliacion","<>","")
            ->get();
            if($registros->count() > 0){
                foreach($registros as $reg){
                    OperPagos::where("referencia",$reg->referencia)->update(["fechaConciliacion"=>$reg->fecha_ejecucion]);
                    Log::info("[PagosEstatusConciliado@updateTable]-Command para actualizar la tabla de pagos referencia: " .  $reg->referencia); 
                }
            }
        } catch (\Exception $e) {
            Log::info("[PagosEstatusConciliado@updateTable]-Command error " .  $e); 
        }
    }
}
