<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class TablacentralCron extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'tablacentral:cron';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command encargado de llenar la tabla central de operaciones pagadas en egobierno.';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $process = new Process(["python3", base_path() . "/app/Console/Commands/Cronegob.py"]);
        $process->setTimeout(240);
        $process->run();

        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }
        $data = $process->getOutput();
        dd($data);
    }
}
