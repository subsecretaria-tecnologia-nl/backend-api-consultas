<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperacionApiServicios extends Model
{
    use HasFactory;
    protected $connection = 'mysql';
    protected $fillable = [
        'id',
        'user_id',
        'url',
        'url_token',
        'metodo',
        'tipo',
        'autenticacion',
        'usuario',
        'password',
        'alias_usuario',
        'alias_password',
        'token',
        'header_token',
        'footer_token',
        'parametro',
        'header',
        'footer',
        'json',
        'bd_query',
        'tiempo',
        'created_at',
        'updated_at'
    ];

    protected $table = "api_servicios";
 
}
