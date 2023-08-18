<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperMetodosPago extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $fillable = ['id','nombre','abreviatura','created_at','update_at'];

    protected $table = "oper_metodopago";
}
