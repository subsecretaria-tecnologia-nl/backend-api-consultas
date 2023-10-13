<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ExternoEgobTransacciones extends Model
{
    use HasFactory;
    protected $connection = 'mysql8';
    protected $fillable = [
        'idTrans',
        'Sesion',
        'Status',
        'NombreEnvio',
        'fechatramite',
        'HoraTramite',
        'PaisEnvio',
        'EstadoEnvio',
        'MunicipioEnvio',
        'DomicilioEnvio',
        'NumExteriorEnvio',
        'ColoniaEnvio',
        'NumeroInteriorEnvio',
        'EntreCallesEnvio',
        'CPEnvio',
        'Email',
        'TotalTramite',
        'CostoMensajeria',
        'TitularTC',
        'TitularDiaNac',
        'TitularMesNac',
        'TitularAnoNac',
        'TitularTelefonoCasa',
        'TitularTelOficina',
        'TitularDomicilio',
        'TitularColonia',
        'TitularCiudad',
        'TitularEstado',
        'TitularPais',
        'PayworksAuthCode',
        'PayworksCcErrCode',
        'PayworksCcReturnMsg',
        'PayworksProcReturnCode',
        'PayworksProcReturnMsg',
        'PayworksMaxSev',
        'PayworksText',
        'PayworksTimeIn',
        'PayworksTimeOut',
        'PayworksStatus',
        'mensajeria_status',
        'mensajeria_auth',
        'mensajeria_ccerrcode',
        'mensajeria_ccreturnmsg',
        'mensajeria_procreturncode',
        'mensajeria_timein',
        'mensajeria_timeout',
        'mensajeria_maxsev',
        'mensajeria_text',
        'tordernum',
        'mordernum',
        'tcanio',
        'tcmes',
        'tcbanco',
        'tccvv2',
        'TipoServicio',
        'Telefono_Referencia',
        'Email_Referencia',
        'TipoPago',
        'Usuario',
        'Clabe_TipoPago',
        'Clabe_FechaDisp',
        'Clabe_FechaVenc',
        'Clabe_TipoProm',
        'ProcClabe_Hora',
        'ProcClabe_Fecha',
        'Clabe_Referencia',
        'Referencia',
        'BancoSeleccion',
        'fuente',
        'IFE',
        'NIS',
        'Donativo',
        'efectivo',
        'idgestor'        
    ];

    protected $table = "transacciones";
    public function tramites() {
		return $this->hasMany("App\Models\ExtenoEgobFolios", "idTrans", "folio");
	}
    public static function findTransaccionesFolio($id_transaccion){        
        $data = ExternoEgobTransacciones::select(
            'ref.Linea as referencia',
            'transacciones.idTrans as folio',           
            'transacciones.fechatramite as fecha_tramite',
            'conc.archivo as fecha_conciliacion',
            'transacciones.Status as estatus',
            'transacciones.TotalTramite as monto'
        )
        ->with(['tramites'=>function ($query) {
            $query->leftjoin("transacciones AS tr","tr.idTrans","folios.idTrans")
            ->leftjoin("tipo_servicios as serv","serv.Tipo_Code","tr.TipoServicio")            
            ->select('folios.idTrans','folios.Folio as folio_tramite','folios.CartImporte as monto','serv.Tipo_Code as id_tipo_servicio', 'serv.Tipo_Descripcion  as servicio');
        }]) 
        ->leftjoin('conciliacion.conciliacion AS conc','conc.idTrans','=','transacciones.idTrans')
        ->leftjoin('referenciabancaria AS ref','ref.idTrans','=','transacciones.idTrans')
        ->where("transacciones.idTrans",$id_transaccion)
        ->get();
          return $data;
       
    }
}
