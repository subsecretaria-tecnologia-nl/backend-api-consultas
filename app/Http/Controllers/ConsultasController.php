<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\OperPagos;
use App\Models\OperacionApiEntidadTramite;
use App\Models\Transacciones;
use Illuminate\Support\Facades\Log;

class ConsultasController extends Controller
{
    public function consultaPagos(Request $request){         
        try{
            $user=auth()->user();
            $entidad = OperacionApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
            #dd($entidad);
            $registros = OperPagos::where("procesado",0)
            ->whereIn("entidad",$entidad)
            ->where("estatus",0)
            ->leftjoin("operacion.oper_entidad as ent","ent.id","oper_pagos_api.entidad")
            ->select("oper_pagos_api.*","ent.nombre as entidad")
            ->get();

            if($registros->count() > 0)
            {
                $temp = array();
                foreach($registros as $r)
                {   
                    $temp[]= array(
                        #"usuario"               => $request->user,
                        "entidad"               => $r->entidad,
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
                    'usuario' => 'Registros encontrados', 
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
    public function consultaEntidadFolios(Request $request){ 
        try{   
            $user=auth()->user();
            $entidad = OperacionApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();     
            
            if(!empty($request->id_transaccion_motor)){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.id_transaccion_motor',$request->id_transaccion_motor);
            }else if(!empty($request->referencia)){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.referencia',$request->referencia);
            }else if(!empty($request->id_transaccion)){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.id_transaccion',$request->id_transaccion);
            }else{
                return response()->json([
                    'status' => false,
                    'message' => 'Sin Registros encontrados', 
                    'datos'=>[]
                ], 200); 
            }           
            return response()->json([
                'status' => true,
                'message' => 'Registros encontrados', 
                'datos'=>$datos
            ], 200); 
           
         }catch (\Exception $e) {
            log::info('Error folios entidad' . $e->getMessage());
            return response()->json([
                'status' => false,
                'message' => 'Error folios entidad: ' .$e->getMessage()
            ], 400);                       
        }
    }

}
