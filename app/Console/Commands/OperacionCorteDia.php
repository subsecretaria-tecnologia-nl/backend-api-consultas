<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use App\Models\OperPagos;

class OperacionCorteDia extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'operacion:cortedia';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $fs=rand(1,28);
        echo($fs);
        //$this->findTransacciones();
       
    }
    public function findTransacciones(){
        try {
            $date=Carbon::now()->format('Y-m-d');
            $data=OperPagos::select("*")
            ->whereBetween("fechaPago",[$date . ' 00:00:00',$date.'23:59:59'])
            ->where('status','0')
            ->get();

            $name='corte_'.Carbon::now()->format('YmdHHmmss');
            $path=storage_path('app/ConsultasTXT/'.$name.'.txt');
            if (!File::exists($path)){File::put($path,'');}
           $createFile=$this->gArchivo_Generico_Oper($path,$data);

        } catch (\Exception $e) {
            log::info('Error findTransacciones' . $e->getMessage());
        }
    }
    private function gArchivo_Generico_Oper($path,$data){
        $cadena='';        
        
        if(count($data)>0){     
            foreach ($data as $d) {
                #log::info($d->id);
                $RowReferencia=str_pad($d->referencia,30,"0",STR_PAD_LEFT);
                $RowFolio=str_pad($d->id_transaccion_motor,20,"0",STR_PAD_LEFT);
                $RowTransaccion=str_pad($d->id_transaccion,20,"0",STR_PAD_LEFT);
                $RowOrigen=str_pad("027",3,"0",STR_PAD_LEFT);
                $RowMedio_pago=str_pad(mb_convert_encoding(substr($d->MetododePago,0,50), "Windows-1252", "UTF-8"),50); 
                $RowIdtramite=str_pad($d->tipo_servicio,6,"0",STR_PAD_LEFT);
                $RowFechaDis=str_pad(Carbon::parse($d->fecha_ejecucion)->format('Ymd'),8);
                $RowHoraDis=str_pad(Carbon::parse($d->fecha_ejecucion)->format('Hms'),6);          
                $RowFechapago=str_pad(Carbon::parse($d->fechaPago)->format('Ymd'),8);
                $RowHorapago=str_pad(Carbon::parse($d->fechaPago)->format('hms'),6);
                $RowPartida=str_pad($d->partida,5,"0",STR_PAD_LEFT);
                #$RowConsepto=str_pad(mb_convert_encoding(substr($d->concepto,0,120), "Windows-1252", "UTF-8"),120);
                $RowTotalTramite=str_pad(str_replace(".", "",$d->Total),11,"0",STR_PAD_LEFT);
                $RowCuentaPago=str_pad($d->cuenta_banco,30,"0",STR_PAD_LEFT);
                $RowAlias=str_pad($d->cuenta_alias,6,"0",STR_PAD_LEFT); 
                #$RowNombreRazonS=str_pad(mb_convert_encoding(substr($RowNombreRazonS,0,250), "Windows-1252", "UTF-8"),250);
                $RowDatoAdicional1=str_pad("",30,"0",STR_PAD_LEFT);

                $cadena=$RowReferencia.$RowFolio.$RowTransaccion.$RowOrigen.$RowTotalTramite.$RowMedio_pago.$RowIdtramite.$RowPartida.$RowFechaDis.$RowHoraDis.$RowFechapago.$RowHorapago.$RowCuentaPago.$RowAlias.$RowDatoAdicional1;
                File::append($path,$cadena."\r\n");
                        
            }
            return $path;
        }
        return 0;
    }
}
