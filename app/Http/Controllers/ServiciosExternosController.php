<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use App\Models\OperacionApiServicios;
use App\Models\OperacionPagosApi;


class ServiciosExternosController extends Controller
{
    private function apiLoginUser($request){
        try {
            $url = $request->url_;
            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request('POST',$url,[
                #'auth' => [ $this->userAuth,$this->passwordAuth ] ,
                'form_params' => [
                'email' => $request->api_user,
                'password' => $request->api_password
                ]
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);

            return $response;
        } catch (\Exception $e) {
            Log::Info('AdministrarApiController@apiLoginUser ' . $e);
        }
    }
    private function consumirApiJSON($url_,$method_,$body_,$request){
        try {
            $response_api=$this->apiLoginUser($request);
            
            if(!$response_api["status"]){
                Log::Info('AdministrarApiController@consumirApi Error autenticacion API: ' ); //$this->apiLoginUser());
            }
            $Token=$response_api["token"];
            $url =$url_;
            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request($method_,$url,[
                'headers' => [ 'Authorization' => 'Bearer ' . $Token ],
                'form_params' => $body_
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);
            return $response;
        } catch (\Exception $e) {
            Log::Info('AdministrarApiController@apiLoginUser ' . $e);
        }
    }
    public function findServicios(){
        try {
            $fServicios=OperacionApiServicios::where("tiempo","1")
            ->get();
            $response=array();
            foreach ($fServicios as $f) {
                $response=$this->findServiciosEntidad($f);
            }
            return $response;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findServicios] Error ' . $th->getMessage());
        }
    }
    public function findServiciosEntidad($f){
        try {
            $fUser=OperacionPagosApi::select(DB::raw($f->bd_query))
            ->leftjoin("api_entidad_tramite as entidadTr","entidadTr.entidad","oper_pagos_api.entidad")
            ->where("entidadTr.user_id",$f->user_id)
            ->groupBy("oper_pagos_api.id")
            ->get();  
            $response=$this->arrayFormat($f->json,$fUser);   
            return $response;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findServicios] Error ' . $th->getMessage());
        }
    }
    private function arrayFormat($format,$data){
        try {
            $format=json_decode($format,true);
            //dd($format);
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
}
