<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ExtenoEgobFolios extends Model
{
    use HasFactory;
    
    protected $connection = 'mysql8';
    protected $fillable = [
        'Folio',
        'idTrans',
        'CartCantidad',
        'CartKey1',
        'CartKey2',
        'CartImporte',
        'CartTipo',
        'CartDescripcion',
        'CartKey3',
        'idgestor'
    ];
    protected $table = 'folios';
}
