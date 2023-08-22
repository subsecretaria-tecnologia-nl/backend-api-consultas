<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    protected $commands=[
        Commands\ConsumirServicios::class,
        Commands\OperacionPagos::class,
        Commands\OperacionCancelados::class
    ];
    /**
     * Define the application's command schedule.
     */
    protected function schedule(Schedule $schedule): void
    {
        #command consume el servicio registrado en api_servicios cada cierto tiempo configurado
        #$schedule->command('consumir:apis 1')->everyFiveMinutes();       #cada 5  min
        $schedule->command('consumir:apis 2')->everyTenMinutes();        #cada 10 min
        $schedule->command('consumir:apis 3')->everyFifteenMinutes();    #cada 15 min 
        $schedule->command('consumir:apis 4')->everyThirtyMinutes();     #cada 30 min
        $schedule->command('consumir:apis 5')->hourly();                 #cada 1 hora
        $schedule->command('consumir:apis 6')->hourlyAt('03:00');        #todos los dias 03:00 am
        
        #command para el llenado de la tabla oper_pagos_api
        $schedule->command('operacion:pagos')->everyTenMinutes();
        #command actualiza el estatus en oper_pagos_api dependiendo de oper_transacciones
        $schedule->command('operacion:cancelados')->everyTenMinutes();
    }

    /**
     * Register the commands for the application.
     */
    protected function commands(): void
    {
        $this->load(__DIR__.'/Commands');

        require base_path('routes/console.php');
    }
}
