<?php

namespace App\Http\Controllers\Servicios;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Carbon\Carbon;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use App\Models\OperPagos;
use App\Models\OperApiEntidadTramite;
use App\Models\Transacciones;
use App\Models\ExternoEgobReferenciabancaria;
use App\Models\ExternoEgobTransacciones;
use App\Models\OperPagosHistorial;
class ConsultasController extends Controller
{
    public function __construct(){
        $this->middleware('authsanctum');
    }
    public function consultaPagos(Request $request){         
        try{
            $user=auth()->user();
            $entidad = OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
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
                    'status' => 200,
                    'message' => 'Registros encontrados', 
                    'respose'=>$temp
                ], 200);
            }else{
                return response()->json([
                    'status' => 400,
                    'message' => 'No se encontraronr registros'
                ], 400);
            }
    
        }catch (\Exception $e) {
            log::info('consultaPagos ' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error: ' .$e->getMessage()
            ], 400);              
        }

    }
    public function PagosVerificados(Request $request){ 
        $user=auth()->user();
        $entidad = OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
        $responseJson=array();
        $noInsert=array();
        //log::info($request->request);

        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] USER " . $user->email);
        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] FOLIOS " . json_encode($request->id_transaccion_motor));
        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] NOW " . date("Y-m-d H:i:s"));
        Log::stack(['pagos-verificados'])->info("[ConsultasController@PagosVerificados] ALL " . json_encode($request->all()));

        try{            
            $folios=$request->id_transaccion_motor;
            //$user = ( isset($request->user) ) ? $request->user : "user400";
            //$entidad= $this->checkEntity($user);
           /* if($entidad == 0){
                $responseJson= $this->reponseVerf('400','user requerido',[]);                
                return response()->json($responseJson);
            }else{*/
                if(empty($folios)){
                    $responseJson= $this->reponseVerf('400','id_transaccion_motor requerido',$noInsert);
                    return response()->json($responseJson);
                }else{
                    OperPagos::whereIn('id_transaccion_motor',$folios)->update(['procesado' => 1]);
                    $responseJson= $this->reponseVerf('200','Guardado exitoso',$noInsert);

                }
                log::info($folios);           // }        
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
            $entidad = OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();     
            
            if(!empty($request->id_transaccion_motor)){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.id_transaccion_motor',$request->id_transaccion_motor);
            }else if(!empty($request->referencia)){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.referencia',$request->referencia);
            }else if(!empty($request->id_transaccion)){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.id_transaccion',$request->id_transaccion);
            }else{
                return response()->json([
                    'status' => 400,
                    'message' => 'referencia/id_transaccion_motor/id_transaccion requirido', 
                    'response'=>[]
                ], 200); 
            }
            if(count($datos)==0){
                return response()->json([
                    'status' => 200,
                    'message' => 'Sin Registros encontrados', 
                    'response'=>[]
                ], 200);   
            }           
            return response()->json([
                'status' => 200,
                'message' => 'Registros encontrados', 
                'response'=>$datos
            ], 200); 
           
         }catch (\Exception $e) {
            log::info('Error folios entidad' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error folios entidad: ' .$e->getMessage(), 
                'response'=>[]
            ], 400);                       
        }
    }
    public function consultaTransacciones($tipo=null,$transaccion=null){ 
        try{   
            $user=auth()->user();
            $entidad=OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();     
            if(empty($transaccion)){
                return response()->json([
                    'status' => 400,
                    'message' => 'transaccion requerido', 
                    'response'=>[]
                ], 400);
            }else if($tipo=="id_transaccion_motor"){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.id_transaccion_motor',[$transaccion]);
            }else if($tipo=="referencia"){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.referencia',[$transaccion]);
            }else if($tipo=="id_transaccion"){
                $datos=Transacciones::findTransaccionesFolio($entidad,'oper_transacciones.id_transaccion',[$transaccion]);
            }else{
                return response()->json([
                    'status' => 400,
                    'message' => 'Sin Registros encontrados', 
                    'response'=>[]
                ], 400); 
            }
            if(count($datos)==0){
                return response()->json([
                    'status' => 200,
                    'message' => 'Sin Registros encontrados', 
                    'response'=>[]
                ], 400);   
            }           
            return response()->json([
                'status' => 200,
                'message' => 'Registros encontrados', 
                'response'=>$datos
            ], 200); 
           
         }catch (\Exception $e) {
            log::info('Error folios entidad' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error folios entidad: ' .$e->getMessage(), 
                'response'=>[]
            ], 400);                       
        }
    }
    private function reponseVerf($status,$error,$responseJ){
        $response=array();
        $response= array(
            'status' => $status,
            'message' => $error,
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
            if(!empty($request->fecha_tipo) ){
                $fecha=$request->fecha_tipo;
            }
            if(!empty($request->fecha_registro)){
                $date=Carbon::parse($request->fecha_registro)->format('Y-m-d');
                $data=$data->whereBetween($fecha,[$date . ' 00:00:00',$fecha_hoy.'23:59:59']);
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
                    'status' => 400,
                    'message' => 'Sin Registros'
                ], 400);
           }else{
                $url = URL::temporarySignedRoute('api/download-file', Carbon::now()->addDays(1), ['name' => $name]);
                return response()->json([
                    'status' => 200,
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
                $RowReferencia=$d->referencia;
                $RowFolio=$d->id_transaccion_motor;
                $RowTransaccion=$d->id_transaccion;
                $RowOrigen="027";
                $RowMedio_pago=mb_convert_encoding(substr($d->MetododePago,0,50), "Windows-1252", "UTF-8"); 
                $RowIdtramite=$d->tipo_servicio;
                $RowFechaDis=Carbon::parse($d->fecha_ejecucion)->format('Ymd');
                $RowHoraDis=Carbon::parse($d->fecha_ejecucion)->format('Hms');          
                $RowFechapago=Carbon::parse($d->fechaPago)->format('Ymd');
                $RowHorapago=Carbon::parse($d->fechaPago)->format('hms');
                $RowPartida=$d->partida;
                #$RowConsepto=str_pad(mb_convert_encoding(substr($d->concepto,0,120), "Windows-1252", "UTF-8"),120);
                $RowTotalTramite=str_replace(".", "",$d->Total);
                $RowCuentaPago=$d->cuenta_banco;
                $RowAlias=$d->cuenta_alias; 
                #$RowNombreRazonS=str_pad(mb_convert_encoding(substr($RowNombreRazonS,0,250), "Windows-1252", "UTF-8"),250);
                $RowDatoAdicional1=" ";
                $cadena=$RowReferencia  . "|" . $RowFolio . "|" . $RowTransaccion . "|" . $RowOrigen . "|" . $RowTotalTramite . "|" . $RowMedio_pago . "|" . $RowIdtramite . "|" . $RowPartida . "|" . $RowFechaDis . "|" . $RowHoraDis . "|" . $RowFechapago . "|" . $RowHorapago . "|" . $RowCuentaPago . "|" . $RowAlias . "|" . $RowDatoAdicional1;
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
    /*public function findCancelados(){
        try {
            $user=auth()->user();
            $entidad = OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
            $registros = OperPagos::where("procesado",0)
            ->whereIn("entidad",$entidad)
            ->where("estatus","<>",0)
            ->leftjoin("operacion.oper_entidad as ent","ent.id","oper_pagos_api.entidad")
            ->select("oper_pagos_api.*","ent.nombre as entidad")
            ->get();

            if($registros->count() > 0){
                $temp = array();
                foreach($registros as $r){   
                    $temp[]= array(
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
                    'status' => 200,
                    'message' => 'Registros encontrados', 
                    'respose'=>$temp
                ], 200);
            }else{
                return response()->json([
                    'status' => 400,
                    'message' => 'No se encontraronr registros'
                ], 400);
            }    
        }catch (\Exception $e) {
            log::info('Error ConsultasController@findCancelados ' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error: ' .$e->getMessage()
            ], 400);              
        }
    }*/
    public function findCancelados(){
        try{
            $user=auth()->user();
            $entidad=OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
            #log::info($entidad);
            $fechaInicio=Carbon::now()->addMonth(-3)->format("Y-m-d") . " 00:00:00";
            $fechaHoy=Carbon::now()->format("Y-m-d") . " 23:59:59";     
            $datos=Transacciones::findTransaccionesEstatus($entidad,"<>","0",[$fechaInicio,$fechaHoy]);
            if(count($datos)==0){
                return response()->json([
                    'status' => 200,
                    'message' => 'Sin Registros encontrados', 
                    'response'=>[]
                ], 400);   
            }           
            return response()->json([
                'status' => 200,
                'message' => 'Registros encontrados', 
                'response'=>$datos
            ], 200);
        }catch (\Exception $e) {
            log::info('Error ConsultasController@findCancelados ' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error: ' .$e->getMessage()
            ], 400);              
        }
    }
    public function consultaGeneral(Request $request){
        try {
            $user=auth()->user();
            $referencia="";
            $id_transaccion="";
            $response=array();
            Log::info(!empty($request->referencia));
            $entidad=OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray(); 
            if(!empty($request->referencia)){
                $referencia=substr($request->referencia,0,2);
            }else if(!empty($request->id_transaccion_motor)){
                $id_transaccion=$request->id_transaccion_motor;
            }else if(!empty($request->id_transaccion)){
                $id_transaccion=$request->id_transaccion;
            }else{ 
                return response()->json([
                    'status' => 400,
                    'message' => 'Parametro requeridos, referencia|id_transaccion_motor|id_transaccion'
                ], 400);
            }
            if($referencia=="01"){
                $response=ExternoEgobReferenciabancaria::findTransaccionesReferencia($request->referencia);
            }else if(strlen($referencia)==2 &&  $referencia!="01"){
                $response=Transacciones::findtransaccionesGeneral("referencia",$request->referencia,$entidad);
            }else{
                $response=ExternoEgobTransacciones::findTransaccionesFolio($id_transaccion);
                if(count($response)==0){
                    log::info("opcion: id_transaccion_motor");
                    $response=Transacciones::findtransaccionesGeneral("id_transaccion_motor",$id_transaccion,$entidad);
                    if(count($response)==0){
                        if(count($response)==0){
                            log::info("opcion: id_transaccion 2");
                            $response=Transacciones::findtransaccionesGeneral("id_transaccion",$id_transaccion,$entidad);
                        }
                    }
                }                
            }
            if(count($response)==0){
                return response()->json([
                    'status' => 400,
                    'message' => 'Sin registros',
                    'response'=> []
                ], 400);
            }
            return response()->json([
                'status' => 200,
                'message' => 'Registros encontrados',
                'response'=> $response
            ], 200);
        } catch (\Exception $e) {
            log::info('Error ConsultasController@consultaGeneral ' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error: ' .$e->getMessage()
            ], 400);
        }
    }
    public function consultaTransaccionesHistorico(Request $request){ 
        try{   
            $user=auth()->user();
            $datos=array();
            $entidad = OperApiEntidadTramite::where("user_id",$user->id)->groupBy("entidad")->pluck("entidad")->toArray();
            if(!empty($request->id_transaccion_motor)){
                $datos=OperPagosHistorial::findTransaccionesFolio($entidad,'id_transaccion_motor',$request->id_transaccion_motor);
            }else if(!empty($request->referencia)){
                $datos=OperPagosHistorial::findTransaccionesFolio($entidad,'referencia',$request->referencia);
            }else if(!empty($request->id_transaccion)){
                $datos=OperPagosHistorial::findTransaccionesFolio($entidad,'id_transaccion',$request->id_transaccion);
            }else{
                return response()->json([
                    'status' => 400,
                    'message' => 'referencia/id_transaccion_motor/id_transaccion requeridos', 
                    'response'=>[]
                ], 200); 
            }
            if(count($datos)>0){
                return response()->json([
                    'status' => 200,
                    'message' => 'Sin registros', 
                    'response'=>[]
                ], 200);   
            }         
            return response()->json([
                'status' => 200,
                'message' => 'Registros encontrados', 
                'response'=>$datos
            ], 200); 
           
         }catch (\Exception $e) {
            log::info('Error ConsultasController@consultaTransaccionesHistorico entidad' . $e->getMessage());
            return response()->json([
                'status' => 400,
                'message' => 'Error folios entidad: ' .$e->getMessage(), 
                'response'=>[]
            ], 400);                       
        }
    }
}
