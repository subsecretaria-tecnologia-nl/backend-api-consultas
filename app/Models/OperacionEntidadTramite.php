<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperacionEntidadTramite extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $fillable = [
        'id',
        'entidad_id',
        'tipo_servicios_id',
        'status',
        'create_at',
        'updated_at'
    ];

    protected $table = "oper_entidadtramite";
    public function servicios() {
      return $this->hasMany("App\Models\EgobiernoTipoServicios", "Tipo_Code", "tipo_servicios_id");
    }
}
