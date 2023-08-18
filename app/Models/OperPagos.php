<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperPagos extends Model
{
    use HasFactory;
    protected $connection = "mysql";
    protected $fillable = ['transacciones_id','id_transaccion_motor','id_transaccion','estatus','entidad','referencia','Total','MetododePago','cve_Banco','FechaTransaccion','FechaPago','FechaConciliacion','tipo_servicio','desc_tipo_servicio','detalle','procesado'];

    protected $table = "oper_pagos_api";
}
