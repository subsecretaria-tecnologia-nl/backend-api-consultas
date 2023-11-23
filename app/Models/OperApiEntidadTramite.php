<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperApiEntidadTramite extends Model
{
    use HasFactory;
    protected $connection = 'mysql';
    protected $fillable = [
        'id',
        'entidad',
        'tramite',
        'user_id',
        'id_relacion',
        'created_at',
        'updated_at'
    ];

    protected $table = "api_entidad_tramite";
    public function entidadTramite() {
      return $this->hasMany("App\Models\OperEntidad", "id", "entidad");
    }
    
}
