<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\User;
use App\Models\OperEntidadTramite;
use App\Models\OperApiEntidadTramite;
use App\Models\OperApiServicios;
use App\Models\EgobTipoServicios;
use App\Models\OperEntidad;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Log;
class AdministrarUsuariosController extends Controller
{
    public function __construct(){
        $this->middleware('authsanctum');

    }
    public function findUsers($id_){
        try {
            if($id_==0 || $id_==""){
                $fUser=User::all();
            }else{
                $fUser=User::where('id',$id_)->get();
            }            
            return $fUser;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findUsers] Error ' . $th->getMessage());
        }
    }
    public function updateUser(Request $request){
        try {
            $user = User::where("id",$request->id)->update([
                'entidad' => $request->status,
                'tramites' => $request->perfil
            ]);
            return response()->json([
                'status' => true,
                'message' => 'Usuario Actualizado',
                #'token' => $user->createToken("API TOKEN")->plainTextToken
            ], 200);

        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@updateUser] Error ' . $th->getMessage());
        }
    }
    public function updateStatus(Request $request){
        try {
            $updat=User::where("id",$request->id)->update(["status"=>$request->status]);
            if($request->status=="0"){
                $descripcion="Usuario Desactivado";
            }else{
                $descripcion="Usuario Activado";
            }
            return response()->json([
                "Code" => "200",
                "Message" =>$descripcion,
            ]);
        } catch (\Exception $e) {
            return response()->json([
                "Code" => "400",
                "Message" => "Error al obtener activar/desactivar ",
            ]);
        }
    }
    ############## MANEJO DE ENTIDADES

    public function findEntidadTramite(Request $request){
        try {
            //$user=auth()->user();
            $user_id=$request->user_id;
            $response=array();
            $arrayPermiso=OperApiEntidadTramite::where("user_id",$user_id)->pluck("id_relacion")->toArray();
            $fEntidadD=OperEntidad::all();
            foreach($fEntidadD as $e){
                $findTramite=OperEntidadTramite::from("oper_entidadtramite as rel")->where("entidad_id",$e->id)
                ->leftjoin("egobierno.tipo_servicios as tramite","tramite.Tipo_Code","rel.tipo_servicios_id")
                ->select("rel.id as id_relacion","tramite.Tipo_Code as id_servicio","tramite.Tipo_Descripcion as servicio")->whereNotIn("rel.id",$arrayPermiso)->get();  
                if(count($findTramite)>0){
                    $response []=array(
                        "id"=>$e->id,
                        "entidad"=>$e->nombre,
                        "tramites"=> $findTramite
                    );
                }
            }
            return $response;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findEntidad] Error ' . $th->getMessage());
        }
    }
    public function findEntidadTramiteUser(Request $request){
        try {
            $user_id=$request->user_id;
            $response=array();
            $fEntidadD=OperEntidad::all();
            foreach($fEntidadD as $e){
                $findTramite=OperApiEntidadTramite::from("api_entidad_tramite as rel")
                ->where("user_id",$user_id)
                ->where("rel.entidad",$e->id)
                ->leftjoin("egobierno.tipo_servicios as tramite","tramite.Tipo_Code","rel.tramite")
                ->select("rel.id as id_relacion","tramite.Tipo_Code as id_servicio","tramite.Tipo_Descripcion as servicio")->get();  
                if(count($findTramite)>0){
                    $response []=array(
                        "id"=>$e->id,
                        "entidad"=>$e->nombre,
                        "tramites"=> $findTramite
                    );
                }
            }
            return $response;
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findEntidadTramiteUser] Error ' . $th->getMessage());
        }
    }
    public function insertEntidadTramite(Request $request){
        try {
            $user_id=$request->user_id;
            if($request->var==1){
                $findTramite=OperApiEntidadTramite::where("user_id",$user_id)
                ->where("entidad",$request->entidad)
                ->where("tramite",$request->tramite)
                ->get();
                if(count($findTramite)==0){
                    $findTramite=OperApiEntidadTramite::create([
                        "user_id"=>$user_id,
                        "id_relacion"=>$request->id_relacion,
                        "entidad"=>$request->entidad,
                        "tramite"=>$request->tramite
                    ]);
                }
            }else{
                $fEntidadD=OperEntidadTramite::where("entidad_id",$request->entidad)->get();
                foreach ($fEntidadD as $e) {
                    $findTramiteE=OperApiEntidadTramite::where("user_id",$user_id)
                    ->where("entidad",$e->entidad_id)
                    ->where("tramite",$e->tipo_servicios_id)
                    ->get();
                    if(count($findTramiteE)==0){
                        $findTramite=OperApiEntidadTramite::create([
                            "user_id"=>$user_id,
                            "id_relacion"=>$e->id,
                            "entidad"=>$e->entidad_id,
                            "tramite"=>$e->tipo_servicios_id
                        ]);
                    }
                }
            }            
            return response()->json([
                'status' => true,
                'message' => 'tramites agragados'
            ], 200);
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@insertEntidadTramite] Error ' . $th->getMessage());
        }
    }
    public function deletedEntidadTramite(Request $request){
        try {
            $user_id=$request->user_id;

            $findTramite=OperApiEntidadTramite::where("user_id",$user_id)
                ->where("entidad",$request->entidad);
            if($request->var==1){
                $findTramite->where("tramite",$request->tramite);                
            }
            $findTramite->delete();            
            return response()->json([
                'status' => true,
                'message' => 'tramites elminados'
            ], 200);
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@insertEntidadTramite] Error ' . $th->getMessage());
        }
    }
    ###########MANEJO DE CONFIGURACION DE WS EXTERNAS
    public function findWs($user_id){
        try {
            if(empty($user_id)){
                return response()->json([
                    'status' => false,
                    'message' => 'parametro requerido',
                    'data'=>array()
                ], 400);    
            }
            $findWs=OperApiServicios::where("user_id",$user_id)->get();
            return response()->json([
                'status' => true,
                'message' => 'registros',
                'data'=>$findWs
            ], 200);
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@findWs] Error ' . $th->getMessage());
        }
    }
    public function insertServicioWs(Request $request){
        try {
            $data=$request->all();
            OperApiServicios::create($data);            
                       
            return response()->json([
                'status' => true,
                'message' => 'tramites agragados'
            ], 200);
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@insertServicioWs] Error ' . $th->getMessage());
        }
    }
    public function updateServicioWs($id_regitro,Request $request){
        try {
            $data=$request->all();
            OperApiServicios::where("id",$id_regitro)->update($data);           
                       
            return response()->json([
                'status' => true,
                'message' => 'tramites agragados'
            ], 200);
        } catch (\Exception $th) {
            Log::info('[AdministrarUsuariosController@updateServicioWs] Error ' . $th->getMessage());
        }
    }
}
