<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ExternoEgobReferenciabancaria extends Model
{
    use HasFactory;
    protected $connection = 'mysql8';
    protected $fillable = [
        'idTrans',
        'Linea',
        'FechaLimite',
        'BancoPago',
        'FechaCanc',
        'TipoServicio'    
    ];

    protected $table = "referenciabancaria";
    public function tiposervicios() {
		return $this->hasMany("App\Models\ExtenoEgobTipoServicios", "Tipo_Servicio", "TipoServicio");
	}
    public function tramites() {
		return $this->hasMany("App\Models\ExtenoEgobFolios", "idTrans", "folio");
	}
    public static function findTransaccionesReferencia($referencia){        
        $data = ExternoEgobReferenciabancaria::select(
            'referenciabancaria.Linea as referencia',
            'trans.idTrans as folio',           
            'trans.fechatramite as fecha_tramite',
            'conc.archivo as fecha_conciliacion',
            'trans.Status as estatus',
            'trans.TotalTramite as monto'
        )
        ->with(['tramites'=>function ($query) {
            $query->leftjoin("transacciones AS tr","tr.idTrans","folios.idTrans")
            ->leftjoin("tipo_servicios as serv","serv.Tipo_Code","tr.TipoServicio")            
            ->select('folios.idTrans','folios.Folio as folio_tramite','folios.CartImporte as monto','serv.Tipo_Code as id_tipo_servicio', 'serv.Tipo_Descripcion as servicio');
        }])   
        ->leftjoin('transacciones AS trans','referenciabancaria.idTrans','=','trans.idTrans')
        ->leftjoin('conciliacion.conciliacion AS conc','conc.idTrans','=','trans.idTrans')
        ->where("referenciabancaria.Linea",$referencia)
        ->get();
          return $data;
       
    }
}
