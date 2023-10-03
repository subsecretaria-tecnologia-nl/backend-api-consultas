<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use App\Models\OperMetodosPago;
use App\Models\Transacciones;
use App\Models\OperPagos;
use App\Models\OperPagosHistorial;

class OperacionPagosHistorial extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'pagos:historial';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Pasar las transacciones de 3 meses anteriores ya procesadas para moverlas en la tabla de historial';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $this->moveTransacciones();
    }
    private function moveTransacciones(){
        try {
            $fecha_anterior=Carbon::now()->addMonth(-3)->format("Y-m-d");
            $ftrans=OperPagos::select('id_transaccion_motor',
            'id_transaccion',
            'estatus',
            'desc_estatus',
            'entidad',
            'referencia',
            'Total',
            'MetododePago',
            'cve_Banco',
            'FechaTransaccion',
            'FechaPago',
            'FechaConciliacion',
            'tipo_servicio',
            'desc_tipo_servicio',
            'detalle',
            'corte',
            'procesado',
            'usuario_procesado')
            ->where("FechaTransaccion","<",$fecha_anterior)
            ->where("procesado","1")
            ->take(1000)
            ->get();
            #log::info($ftrans);
            OperPagosHistorial::insert(json_decode($ftrans,true));
            foreach ($ftrans as $f) {
                #OperPagos::where('id',$f->id)->delete();
            }    
        } catch (\Exception $e) {
            Log::info("[OperacionPagosHistorial@moveTransacciones]-ERROR-".$e->getMessage());
        }
    }
}
