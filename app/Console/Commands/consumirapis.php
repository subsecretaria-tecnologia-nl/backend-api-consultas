<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use App\Http\Controllers\ServiciosExternosController;
class ConsumirApis extends Command
{
    
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'consumir:apis {tipo}';

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
        $tipo= $this->argument('tipo');
        $this->optionApis($tipo);
    }
    private function optionApis($tipo){
        try {
            Log::info("Consumir:apis " . $tipo );
            app(ServiciosExternosController::class)->findServicios($tipo);
        } catch (\Exception $e) {
            log::info("Error Schedule commmand@consumirapis" . $e);
        }
    }
}
