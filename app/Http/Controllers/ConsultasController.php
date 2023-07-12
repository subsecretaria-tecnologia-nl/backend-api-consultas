<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Model\OperPagos;
use Model\Transacciones;


class ConsultasController extends Controller
{
    public function consultaPagos(Request $request)
    { 
        //log::info($request);
        $responseJson=array();
        $response=array();
        
        try
        {
            $user = ( isset($request->user) ) ? $request->user : "user400";
            
            // $entidad= $this->checkEntity($user);

            if($entidad == 0)
            {
                $responseJson= $this->reponseVerf('400','user requerido',[]);
                
                return response()->json($responseJson);

            }else{
                
                // obtener todos los registros que ya se arrojaron
               $registros = OperPagos::where(
                    [
                        "entidad"   => $entidad,
                        "procesado" => 0
                    ]
                )->get();

               if($registros->count() > 0)
                {
                    $temp = array();
                    foreach($registros as $r)
                    {   
                        $temp[]= array(
                            "usuario"               => $user,
                            "entidad"               => $entidad,
                            "referencia"            => $r->referencia,
                            "id_transaccion_motor"  => $r->id_transaccion_motor,
                            "id_transaccion"        => $r->id_transaccion,
                            "estatus"               => $r->estatus,
                            "Total"                 => $r->Total,
                            "MetododePago"          => $r->MetododePago,
                            "cve_Banco"             => $r->cve_Banco,
                            "FechaTransaccion"      => $r->FechaTransaccion,
                            "FechaPago"             => $r->FechaPago,
                            "FechaConciliacion"     => $r->FechaConciliacion,
                        );
                        
                    }

                    $responseJson= $this->reponseVerf('202','',$temp);
                }else{
                    $responseJson= $this->reponseVerf('202','Sin registros',array());
                }
            }
        }catch (\Exception $e) {
            log::info('consultaPagos ' . $e->getMessage());
            $responseJson= $this->reponseVerf('400','ocurrio un error',[]);     
          return  response()->json($responseJson);            
        }
        return response()->json($responseJson);

    }
    public function consultaEntidadFolios(Request $request)
    { 
        $responseJson=array();
        $select=array();
        try{            
            $insolicitud=array();            
            $folios=$request->id_transaccion_motor;
            $entidad=$request->entidad;
            $user=$request->user;
            if($user==null){
                $responseJson= $this->reponseVerf('400','user requerido',[]);
                return response()->json($responseJson);
            }
            if($entidad==null && $folios==null){
                $responseJson= $this->reponseVerf('400','entidad / id_transaccion_motor requerido',[]);
                return response()->json($responseJson);
            }
            if($entidad==null)
            {
                $select=Transacciones::findTransaccionesFolio($user,'oper_transacciones.id_transaccion_motor',$folios);
            }else{
                $select=Transacciones::findTransaccionesEntidad($user,'oper_transacciones.entidad',$entidad);
            }           
                   
            $responseJson= $this->reponseVerf('202','',$select);  
         }catch (\Exception $e) {
            $responseJson=$this->reponseVerf('400','ocurrio un error',[]);
            log::info('PagosVerificados insert' . $e->getMessage());
          return  response()->json($responseJson);            
        }
        return response()->json($responseJson);

    }

}
