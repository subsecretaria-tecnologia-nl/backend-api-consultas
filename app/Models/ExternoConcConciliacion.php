<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ExternoConcConciliacion extends Model
{
    use HasFactory;

    protected $connection = 'mysql8';
    protected $fillable = [
        'american',
        'anomalia',
        'conciliacion',
        'conciliacionanomalia',
        'conciliacioncancelada',
        'layout','otrostipopago',
        'layoutcampos'
    ];
    protected $table = 'conciliacion.conciliacion';
}
