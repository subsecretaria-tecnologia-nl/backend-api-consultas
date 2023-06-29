<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

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
            
            $entidad= $this->checkEntity($user);

            if($entidad == 0)
            {
                $responseJson= $this->reponseVerf('400','user requerido',[]);
                
                return response()->json($responseJson);

            }else{
                
                // obtener todos los registros que ya se arrojaron
               $registros = $this->pagosapi->findWhere(
                    [
                        "entidad"   => $entidad,
                        "procesado" => 0
                    ]
                );

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

}
