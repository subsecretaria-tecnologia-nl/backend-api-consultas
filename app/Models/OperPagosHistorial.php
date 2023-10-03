<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperPagosHistorial extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $table = "oper_pagos_api_historial";

    protected $fillable = [
        'id',
        'id_transaccion_motor',
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
        'usuario_procesado',
        'created_at',
        'updated_at'
    ];
}
