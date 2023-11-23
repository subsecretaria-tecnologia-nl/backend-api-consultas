<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperApiServicios extends Model
{
    use HasFactory;
    protected $connection = 'mysql';
    protected $fillable = [
        'id',
        'user_id',
        'url',
        'url_token',
        'tipo_parametros',
        'tipo',
        'autenticacion',
        'usuario',
        'password',
        'alias_usuario',
        'alias_password',
        'token_variable',
        'token_response',
        'token_operacion',
        'token',
        'xml_token',
        'parametro',
        'xml_servicio',
        'servicio_variable',
        'servicio_response',
        'servicio_operacion',
        'json',
        'bd_query',
        'tiempo',
        'created_at',
        'updated_at'
    ];

    protected $table = "api_servicios";
 
}
