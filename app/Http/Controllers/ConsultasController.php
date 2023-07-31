<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Model\OperPagos;
use Model\OperacionEntidad;
use Model\Transacciones;


class ConsultasController extends Controller
{
    public function consultaPagos(Request $request)
    { 
        
        try
        {
                $entidad = OperacionEntidad::find($request->entidad);
                $registros = OperPagos::where(
                    [
                        "entidad"   => $request->entidad,
                        "procesado" => 0
                    ]
                )->get();

               if($registros->count() > 0)
                {
                    $temp = array();
                    foreach($registros as $r)
                    {   
                        $temp[]= array(
                            "usuario"               => $request->user,
                            "entidad"               => $entidad->nombre,
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

                    return response()->json([
                        'status' => true,
                        'message' => 'Registros encontrados', 
                        'datos'=>$temp
                    ], 200);
                }else{
                    return response()->json([
                        'status' => false,
                        'message' => 'No se encontraronr egistros'
                    ], 400);
                }

            
    
        }catch (\Exception $e) {
            log::info('consultaPagos ' . $e->getMessage());
            return response()->json([
                'status' => false,
                'message' => 'Error: ' .$e->getMessage()
            ], 400);              
        }

    }
    public function consultaEntidadFolios(Request $request)
    { 
        try{                    
            $folios=$request->id_transaccion_motor;
            $entidad=$request->entidad;
            $user=$request->user;
          
        
            if($entidad==null)
            {
                $datos=Transacciones::findTransaccionesFolio($user,'oper_transacciones.id_transaccion_motor',$folios);
            }else{
                $datos=Transacciones::findTransaccionesEntidad($user,'oper_transacciones.entidad',$entidad);
            }           
            return response()->json([
                'status' => true,
                'message' => 'Registros encontrados', 
                'datos'=>$datos
            ], 200); 
           
         }catch (\Exception $e) {
            return response()->json([
                'status' => false,
                'message' => 'Error folios entidad: ' .$e->getMessage()
            ], 400); 
            log::info('Error folios entidad' . $e->getMessage());
          return  response()->json($responseJson);            
        }
        return response()->json($responseJson);

    }

}
