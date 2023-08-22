<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OperTramites extends Model
{
    use HasFactory;
    protected $table = "oper_tramites";
    protected $fillable = [
    	'id_tramite_motor',
    	'id_transaccion_motor',
    	'id_tipo_servicio',
    	'id_seguimiento',
    	'id_tramite',
    	'nombre',
    	'apellido_paterno',
    	'apellido_materno',
    	'razon_social',
    	'rfc',
    	'curp',
    	'email',
    	'calle',
    	'colonia',
    	'numexterior',
    	'numinterior',
    	'municipio',
    	'codigopostal',
    	'importe_tramite',
        'auxiliar_1',
        'auxiliar_2',
        'auxiliar_3',
    	'nombre_factura',
    	'apellido_paterno_factura',
    	'apellido_materno_factura',
    	'razon_social_factura',
    	'rfc_factura',
    	'curp_factura',
    	'email_factura',
    	'calle_factura',
    	'colonia_factura',
    	'numexteior_factura',
    	'numinterior_factura',
    	'municipio_factura',
    	'codigopostal_factura'
    ];

    public $timestamps = false;
    public function servicios() {
		return $this->hasMany("App\Models\EgobTipoServicios", "Tipo_Code", "id_tipo_servicio");
	}
}
