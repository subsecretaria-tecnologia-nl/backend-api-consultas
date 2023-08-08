<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\OperPagos;
use App\Models\OperacionApiEntidadTramite;
use App\Models\Transacciones;
use Illuminate\Support\Facades\Log;
use Carbon\Carbon;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
class ConsultasController extends Controller
{
    /**
     * @return \Illuminate\Http\JsonResponse
     * 
     * 
 * @OA\Get(
 * path="/api/consulta-pagos",
 * summary="Consulta de transacciones",
 * description="Consulta de transacciones",
 * tags={"Consultas"},
 * security={{"bearerAuth":{}}},
*     @OA\Response(
*     response=200,
*     description="Successfully",
*      @OA\JsonContent(
*        @OA\Property(property="status", type="string", example=true),
*        @OA\Property(property="message", type="string", example="Registros encontrados"),
*        @OA\Property(
*              property="datos",
*              type="array",
*              collectionFormat="multi",
*              @OA\Items()
*        )
*      )
*    )
* )
*/
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
    public function PagosVerificados(Request $request){ 
        $user=auth()->user();
        $entidad = OperacionApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
        $responseJson=array();
        $noInsert=array();
        //log::info($request->request);

        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] USER " . $user->email);
        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] FOLIOS " . json_encode($request->id_transaccion_motor));
        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] NOW " . date("Y-m-d H:i:s"));
        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] ALL " . json_encode($request->all()));

        try
        {
            $folios=$request->id_transaccion_motor;
            $user = ( isset($request->user) ) ? $request->user : "user400";
            
            $entidad= $this->checkEntity($user);

            if($entidad == 0){
                $responseJson= $this->reponseVerf('400','user requerido',[]);                
                return response()->json($responseJson);
            }else{
                if(empty($folios)){
                    $responseJson= $this->reponseVerf('400','id_transaccion_motor requerido',$noInsert);
                    return response()->json($responseJson);
                }else{
                    OperPagos::whereIn('id_transaccion_motor',$folios)->update(['procesado' => 1]);
                    $responseJson= $this->reponseVerf('202','Guardado exitoso',$noInsert);

                }
            }        
         }catch (\Exception $e) {
            $responseJson=$this->reponseVerf('400','ocurrio un error',[]);
            log::info('PagosVerificados insert' . $e->getMessage());
          return  response()->json($responseJson);            
        }
        return response()->json($responseJson);

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
    private function reponseVerf($status,$error,$responseJ){
        $response=array();
        $response= array(
            'code' => $status,
            'status' => $error,
            'response' => $responseJ,
        );
        return $response;
    }
    public function findTransacciones(Request $request){
        try {
            $data=array();
            $data=OperPagos::select("*");
            $fecha="fechaTransaccion";
            $fecha_hoy=Carbon::now()->format('Y-m-d');
            if(!empty($request->fecha) ){
                $fecha=$request->fecha;
            }
            if(!empty($request->fecha_inicio) && !empty($request->fecha_fin)){
                $data=$data->whereBetween($fecha,[$request->fecha_inicio,$request->fecha_fin]);
            }else{
                $data=$data->whereBetween($fecha,[$fecha_hoy.' 00:00:00',$fecha_hoy.'23:59:59']);
            }
            if(!empty($request->status)){
                $data=$data->where('status',$request->status);
            }
            $data=$data->get();
            $name='entidad_'.Carbon::now()->format('YmdHHmmss');
            $path=storage_path('app/ConsultasTXT/'.$name.'.txt');
            if (!File::exists($path)){File::put($path,'');}
           $createFile=$this->gArchivo_Generico_Oper($path,$data);
           if($createFile==0){
                #File::delete($path);
                return response()->json([
                    'status' => false,
                    'message' => 'Sin Registros'
                ], 400);
           }else{
                $url = URL::temporarySignedRoute('api/download-file', Carbon::now()->addDays(1), ['name' => $name]);
                return response()->json([
                    'status' => true,
                    'message' => 'Archivo disponible, descarga una vez, expira en 24hrs.',
                    'url'=>$url
                ], 200);
               
           }           
        } catch (\Exception $e) {
            log::info('Error findTransacciones' . $e->getMessage());
        }
    }
    private function gArchivo_Generico_Oper($path,$data){
        $cadena='';        
        
        if(count($data)>0){     
            foreach ($data as $d) {
                #log::info($d->id);
                $RowReferencia=str_pad($d->referencia,30,"0",STR_PAD_LEFT);
                $RowFolio=str_pad($d->id_transaccion_motor,20,"0",STR_PAD_LEFT);
                $RowTransaccion=str_pad($d->id_transaccion,20,"0",STR_PAD_LEFT);
                $RowOrigen=str_pad("027",3,"0",STR_PAD_LEFT);
                $RowMedio_pago=str_pad(mb_convert_encoding(substr($d->MetododePago,0,50), "Windows-1252", "UTF-8"),50); 
                $RowIdtramite=str_pad($d->tipo_servicio,6,"0",STR_PAD_LEFT);
                $RowFechaDis=str_pad(Carbon::parse($d->fecha_ejecucion)->format('Ymd'),8);
                $RowHoraDis=str_pad(Carbon::parse($d->fecha_ejecucion)->format('Hms'),6);          
                $RowFechapago=str_pad(Carbon::parse($d->fechaPago)->format('Ymd'),8);
                $RowHorapago=str_pad(Carbon::parse($d->fechaPago)->format('hms'),6);
                $RowPartida=str_pad($d->partida,5,"0",STR_PAD_LEFT);
                #$RowConsepto=str_pad(mb_convert_encoding(substr($d->concepto,0,120), "Windows-1252", "UTF-8"),120);
                $RowTotalTramite=str_pad(str_replace(".", "",$d->Total),11,"0",STR_PAD_LEFT);
                $RowCuentaPago=str_pad($d->cuenta_banco,30,"0",STR_PAD_LEFT);
                $RowAlias=str_pad($d->cuenta_alias,6,"0",STR_PAD_LEFT); 
                #$RowNombreRazonS=str_pad(mb_convert_encoding(substr($RowNombreRazonS,0,250), "Windows-1252", "UTF-8"),250);
                $RowDatoAdicional1=str_pad("",30,"0",STR_PAD_LEFT);

                $cadena=$RowReferencia.$RowFolio.$RowTransaccion.$RowOrigen.$RowTotalTramite.$RowMedio_pago.$RowIdtramite.$RowPartida.$RowFechaDis.$RowHoraDis.$RowFechapago.$RowHorapago.$RowCuentaPago.$RowAlias.$RowDatoAdicional1;
                File::append($path,$cadena."\r\n");
                        
            }
            return $path;
        }
        return 0;
    }
    public function downloadFile(Request $request){
        
        if ($request->hasValidSignature()) {
            $name = $request->get('name');
            $path=storage_path('app/ConsultasTXT/'.$name.'.txt');
            if (File::exists($path)){
                return response()->download($path)->deleteFileAfterSend(true);
            }else{
                return "<br><br><rh><center><h3>Archivo no encontrado</h3></center><hr>";
            }
            return $path;
        }else{
            return "<br><br><rh><center><h3>URL Expirado</h3></center><hr>";
        }
    }

}
