<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ExtenoEgobTipoServicios extends Model
{
    use HasFactory;
    protected $connection = 'mysql8';
    protected $fillable = [
        'Tipo_Code',
        'Tipo_Descripcion',
        'Origen_URL',
        'GpoTrans_Num',
        'id_gpm',
        'descripcion_gpm',
        'descripcion_gpm',
        'tiporeferencia_id',
        'limitereferencia_id'
    ];
    protected $table = 'tipo_servicios';
}
