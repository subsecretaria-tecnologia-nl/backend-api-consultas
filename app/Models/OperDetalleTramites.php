<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperDetalleTramites extends Model
{
    use HasFactory;
    protected $connection = 'mysql';
    

    protected $fillable = [
    	'id_detalle_tramite',
    	'id_tramite_motor',
    	'concepto',
    	'importe_concepto',
    	'partida',
        'id_transaccion_motor'
    ];
    protected $table = "oper_detalle_tramite";
}
