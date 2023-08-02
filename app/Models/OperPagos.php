<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperPagos extends Model
{
    use HasFactory;
    protected $connection = 'mysql';
    protected $fillable = [
        '*'
    ];

    protected $table = "oper_pagos_api";
}
