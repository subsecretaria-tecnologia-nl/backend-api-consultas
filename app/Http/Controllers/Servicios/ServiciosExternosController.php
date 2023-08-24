<?php

namespace App\Http\Controllers\Servicios;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use App\Models\OperApiServicios;
use App\Models\OperPagos;
use SimpleXMLElement;
use SoapClient;
use Artisaninweb\SoapWrapper\SoapWrapper;
class ServiciosExternosController extends Controller
{
    public function __construct(){
        $this->middleware('authsanctum');
    }
    private function apiLoginUser($request){
        try {
            $v_token=$request->token_variable;
            $v_funcion=$request->token_operacion;
            $v_response=$request->token_response;
            $responseToken="";
            $alias_user_="usuario";
            $alias_password_="password";
            if($request->alias_usuario!=""  &&  $request->alias_password!=""){
                $alias_user_=$request->alias_usuario;
                $alias_password_=$request->alias_password;
            }
            $parameters=[
                $alias_user_=>$request->usuario,
                $alias_password_=>$request->password
            ];
            
            $url_ = $request->url_token;
            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request('POST',$url_,[
                'form_params' => $parameters
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);          
            if($v_response==NULL){
                $responseToken =$response[$v_token];   #obtiene el token de la variable
            }else{
                $responseToken =$response[$v_response][$v_token];  #obtiene el token de la variable dentro de nodo.
            }
            #dd($responseToken);
            return $responseToken;
        } catch (\Exception $e) {
            Log::Info('AdministrarApiController@apiLoginUser ' . $e);
        }
    }
    private function consumirApiJSON($request,$data){
        try {
            $v_variable=$request->servicio_variable;
            $v_response=$request->servicio_response;
            $headers_=[];
            $basicAuth_=[];
            if($request->autenticacion=="TOKEN_AUTH"){
                $token_=$this->apiLoginUser($request);
                $headers_=[ 'Authorization' => 'Bearer ' . $token_ ];
            }else if($request->autenticacion=="TOKEN"){
               $headers_=  [ 'Authorization' => 'Bearer ' . $request->Token ];
            }else if($request->autenticacion=="BASIC_AUTH"){
                $basicAuth_=[ $request->usuario,$request->password];
            }           
            $url =$request->url;
           # $parametro_=json_encode($data);
            $parametro_=json_encode(["name"=>"Carpeta T6",
            "nodeType"=>"cm:folder"]);
            if($request->parametro!=""){
                $parametro_=[$request->parametro=>$data];;
            }
            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request('POST',$url,[
                'headers'=> $headers_,
                'auth' => $basicAuth_,
                $request->tipo_parametro=>$parametro_
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);
            if($v_response==NULL){
                $response =$response[$v_variable];   #obtiene el token de la variable
            }else{
                $response =$response[$v_response][$v_variable];  #obtiene el token de la variable dentro de nodo.
            }         
            return $response;
        } catch (\Exception $e) {
            Log::Info('AdministrarApiController@apiLoginUser ' . $e);
        }
    }
    private function apiLoginUserXML($request){
        try {
            #log::info($request);
            $v_token=$request->token_variable;
            $v_funcion=$request->token_operacion;
            $v_response=$request->token_response;
            $alias_user_="usuario";
            $alias_password_="password";
            if($request->alias_usuario!=""  &&  $request->alias_password!=""){
                $alias_user_=$request->alias_usuario;
                $alias_password_=$request->alias_password;
            }
            $parameters=[
                $alias_user_=>$request->usuario,
                $alias_password_=>$request->password
            ];
            $url=$request->url;
            $server = new SoapClient($url,[
                'encoding' => 'UTF-8'
            ]);
            if($v_response==""){
                $responseXML =$server->$v_funcion($parameters)->$v_token;   #obtiene el token de la variable
            }else{
                $responseXML =$server->$v_funcion($parameters)->$v_response->$v_token;  #obtiene el token de la variable dentro de nodo.
            }
            $token=(string)$responseXML;
            return $token;
        } catch (\Exception $e) {
            Log::Info('AdministrarApiController@apiLoginUser ' . $e);
        }
    }
    private function consumirApiXML($request,$data){
        try {
            $v_variable=$request->servicio_variable;
            $v_funcion=$request->servicio_operacion;
            $v_response=$request->servicio_response;
            $parametro_="data";
            $headers_=[];
            $basicAuth_=[];
            if($request->autenticacion=="TOKEN_AUTH"){
                $token_=$this->apiLoginUserXML($request);
                $headers_=[ 'Authorization' => 'Bearer ' . $token_ ];
            }else if($request->autenticacion=="TOKEN"){
               $headers_=  [ 'Authorization' => 'Bearer ' . $request->Token ];
            }else if($request->autenticacion=="BASIC_AUTH"){
                $basicAuth_=[ $request->usuario,$request->password];
            }           
            $url =$request->url;
            $parametro_="data";
            if($request->parametro!=""){
                $parametro_=$request->parametro;
            }
            $parameters=[
                $parametro_=>$data
            ];
            $server = new SoapClient($url,[
                'headers'=>$headers_,
                'auth' => $basicAuth_
            ]);
            $responseXML =$server->$v_funcion($parameters)->$v_response;

            if($v_response==""){
                $responseXML =$server->$v_funcion($parameters)->$v_variable;   #obtiene el token de la variable
            }else{
              $responseXML =$server->$v_funcion($parameters)->$v_response->$v_variable;  #obtiene el token de la variable dentro de nodo.
            }       
            return $responseXML;
        } catch (\Exception $e) {
            Log::Info('AdministrarApiController@apiLoginUser ' . $e);
        }
    }
    public function findServicios($tipo){
        try {
            $fServicios=OperApiServicios::where("tiempo",$tipo)
            ->where("status","0")
            ->get();
            $response=array();
            foreach ($fServicios as $f) {
                OperApiServicios::where("id",$f->id)->update(["status"=>"2"]);
            }
            foreach ($fServicios as $f) {
                $response=$this->findServiciosEntidad($f);
                if($f->tipo=="XML"){
                    $response =$this->consumirApiXML($f,$response); 
                }else{
                    $response= $this->consumirApiJSON($f,$response); 
                }
                OperApiServicios::where("id",$f->id)->update(["status"=>"1"]);
            }
            return $response;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findServicios] Error ' . $th->getMessage());
        }
    }
    public function findServiciosEntidad($f){
        try {
            $fUser=OperPagos::select(DB::raw("oper_pagos_api.*"))
            ->leftjoin("api_entidad_tramite as entidadTr","entidadTr.entidad","oper_pagos_api.entidad")
            ->where("entidadTr.user_id",$f->user_id)
            ->where("oper_pagos_api.procesado","0")
            ->groupBy("oper_pagos_api.id")
            ->get();  
            //$response=$this->arrayFormat($f->json,$fUser);   
            return $fUser;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findServicios] Error ' . $th->getMessage());
        }
    }
    private function arrayFormat($format,$data){
        try {
            $format=json_decode($format,true);
            $response=array();
            foreach ($data as $d) {                
                $array_=array();
              foreach($format as $f=>$h){
                $array_=array_merge($array_,array($f=>$d[$h]));
              } 
              $response []=$array_;
            }
            //log::info($response);
            return $response;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@arrayFormat] Error ' . $th->getMessage());
        }
    }
    private function loadXmlStringAsArray($xml)
    {
    	$array=(array)@simplexml_load_string($xml);
    	if(!$array)
    	{
    		$array=(array)json_decode($xml,true);
    	}else{
    		$array=(array)json_decode(json_encode($array),true);
    	}
    	return $array;
    }
}
