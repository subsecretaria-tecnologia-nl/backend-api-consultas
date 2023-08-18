<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    protected $commands=[
        Commands\ConsumirApis::class
    ];
    /**
     * Define the application's command schedule.
     */
    protected function schedule(Schedule $schedule): void
    {
        // $schedule->command('inspire')->hourly();
        #$schedule->command('consumir:apis 1')->everyFiveMinutes();       #cada 5  min
        $schedule->command('consumir:apis 2')->everyTenMinutes();        #cada 10 min
        $schedule->command('consumir:apis 3')->everyFifteenMinutes();    #cada 15 min 
        $schedule->command('consumir:apis 4')->everyThirtyMinutes();     #cada 30 min
        $schedule->command('consumir:apis 5')->hourly();                 #cada 1 hora
        $schedule->command('consumir:apis 6')->hourlyAt('03:00');        #todos los dias 03:00 am
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
