<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperEntidad extends Model
{
    use HasFactory;
    protected $connection = 'mysql';
    protected $fillable = [
        'id',
        'nombre',
        'clave',
        'created_at',
        'updated_at'
    ];

    protected $table = "oper_entidad";
 
    public function entidadTramite() {
		return $this->hasMany("App\Models\OperEntidadTramite", "entidad_id", "id");
	}
    
}
