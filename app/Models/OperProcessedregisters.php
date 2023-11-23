<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperProcessedregisters extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $table = "oper_processedregisters";

    protected $fillable = ['id','transaccion_id','day','month','year','monto','status','filename','origen','referencia','cuenta_banco','cuenta_alias','banco_id','fecha_ejecucion','info_transacciones','archivo_corte','tipo_servicio','facturado','revisado'];
}
