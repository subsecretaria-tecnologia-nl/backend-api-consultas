<?php

namespace App\Http\Controllers\Servicios;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\File;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\ClientException;
use App\Models\AlfrescoDirectory;
use App\Models\AlfrescoDownload;
use App\Models\AlfrescoFiles;
use Stringable;

class AlfrescoController extends Controller
{
    protected $url_alfresco;
    protected $userAuth; 
    protected $passwordAuth;

    public function __construct(){
        $this->url_alfresco=env('ALFRESCO_URL');
        $this->userAuth=env('ALFRESCO_USER');
        $this->passwordAuth=env('ALFRESCO_PASSWORD');
    }
    public function index(){
        return view("other/administrararchivos");
    }
    public function createfolder(Request $request){
        try {
            $url = $this->url_alfresco ."/-default-/public/alfresco/versions/1/nodes/-my-/children";
            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request('POST',$url,[
                'auth' => [ $this->userAuth,$this->passwordAuth ] ,
                'body' => json_encode([
                'name' => $request->name,
                'nodeType' => "cm:folder"
                ])
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);
            $insert=array();
            if(isset($response["entry"])){
                $insert=AlfrescoDirectory::create([
                    "name_folder"=>$request->name,
                    "id_folder"=>$response["entry"]["id"],
                    "status"=>1,
                    "node_type"=>$response["entry"]["nodeType"],
                    "parent_id"=>$response["entry"]["parentId"],
                    "json_response"=>json_encode( $response),
                ]);
                return response()->json([
                    "status" => 200,
                    "message" => "Carpeta creada.",
                    "response"=> array(
                        "id"=> $insert["id"],
                        "name_folder"=>$request->name,
                        "id_folder"=>$response["entry"]["id"],
                        "status"=>1,
                        "node_type"=>$response["entry"]["nodeType"],
                        "parent_id"=>$response["entry"]["parentId"],
                        "json_response"=> $response["entry"]
                        )
                ]);
            }else{
                return response()->json([
                    "status" => 400,
                    "message" => "Error al crear la carpeta",
                    "response"=>[]
                ]);
            }            
        } catch (\Exception $e) {
            log::info("AlfrescoController@createfolder: ".$e);
            return response()->json(["status" => 400,"message"=>"Error al crear la carpeta","response"=>[] ]);
        }
    }
    public function findAllResgistros(){
        try {
            $find=AlfrescoDirectory::All(); 
            return response()->json([
                "status" => 200,
                "message" => "registros encontrados",
                "response"=>$find
            ]);
        } catch (\Exception $e) {
            log::info("AlfrescoController@findAllResgistros: ".$e);
        }
    }
    public function saveFileAlfresco($request,$directoryTemp){
        try {
            //Log::info($request);
            $url = $this->url_alfresco ."/-default-/public/alfresco/versions/1/nodes/".$request["id_folder"]."/children";
            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request('POST',$url,[

                'auth' => [ $this->userAuth,$this->passwordAuth ],
                'multipart' => [
                    [
                        'name'     => "filedata",
                        'contents' => file_get_contents(storage_path('app/uploadTemporal/' . $directoryTemp)),
                        'filename'=>$request["name_file"]
                    ],
                    [
                        'name'     => "name",
                        'contents'=>$request["name_file"]
                    ],
                    [
                        'name'     => "relativePath",
                        'contents'=>$request["name_folder"]
                    ],
                    [
                        'name'     => "nodeType",
                        'contents'=>'cm:content'
                    ]
                ]
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);
            $insert=array();
            if(isset($response["entry"])){
                $insert=AlfrescoFiles::create([
                    "id_directory"=>$request["id"],
                    "name_file"=>$request["name_file"],
                    "name_original"=>$request["name_original"],
                    "id_file"=>$response["entry"]["id"],
                    "status"=>1,
                    "type_file"=>$response["entry"]["content"]["mimeTypeName"],
                    "node_type"=>$response["entry"]["nodeType"],
                    "parent_id"=>$response["entry"]["parentId"],
                    "json_response"=>json_encode( $response),
                ]);
                Storage::delete('uploadTemporal/'.$request["name_file"]);
                return response()->json([
                    "status" => 200,
                    "message" => "Archivo guardado.",
                    "response"=> array(
                        "id"=>$insert["id"],
                        "id_directory"=>$request["id"],
                        "name_file"=>$request["name_file"],
                        "name_original"=>$request["name_original"],
                        "id_file"=>$response["entry"]["id"],
                        "status"=>1,
                        "type_file"=>$response["entry"]["content"]["mimeTypeName"],
                        "node_type"=>$response["entry"]["nodeType"],
                        "parent_id"=>$response["entry"]["parentId"],
                        "json_response"=> $response
                        )
                ]);
            }
        } catch (\Exception $e) {
            log::info("AlfrescoController@saveFile: ".$e);
            return response()->json(["status" => 400, "message" => "Error al guardar el archivo." ]);
        }
    }
    public function saveFile(Request $request){
        try {
            $file=$request->file;
            $id=$request->id;
            $return=0;
            $date_=Carbon::now()->format("YmdHms");
            $array_=array();
            $extension = $file->getClientOriginalExtension();
            $filename = pathinfo($file->getClientOriginalName(), PATHINFO_FILENAME);
            $findFolder=AlfrescoDirectory::where("id",$id)->get();
            $fname=$filename . "-" .  $date_ . "." . $extension;
            Storage::disk('local')->put("uploadTemporal/".$fname,  File::get($file));
            if($findFolder->count()>0){
                $array_=array("id"=>$findFolder[0]["id"],
                    "id_folder"=>$findFolder[0]["id_folder"],
                    "name_folder"=>$findFolder[0]["name_folder"],
                    "name_file"=>$fname,
                    "name_original"=>$filename . "." . $extension
                );
                $return=$this->saveFileAlfresco($array_,$fname);
            }
            return $return;
        } catch (\Exception $e) {
            log::info("AlfrescoController@saveFile: ".$e);
            return 0;
        }
    }
    public function saveFileExample(Request $request){
        try {            
            $this->saveFile($request->file,"3"); //id del registro de la carpeta en tabla operacion.alfresco_directory
        } catch (\Exception $e) {
            log::info("AlfrescoController@saveFile: ".$e);
        }
    }
    public function findFiles(Request $request){
        try {
            $find=AlfrescoFiles::findWhere(["id_directory"=>$request->id]);
            return response()->json([
                "status" => 200,
                "message" => "registros encontrados",
                "response"=>$find
            ]);
        } catch (\Exception $e) {
            log::info("AlfrescoController@findFiles: ".$e);
            return response()->json(["status" => 400, "message" => "Error al buscar." ]);
        }
    }
    public function downloadFile($id,$type){
        try {
            if($type=="file"){
                $findF=AlfrescoFiles::findWhere(["id"=>$id]);
                $idFile=$findF[0]["id_file"];
                $fName=$findF[0]["name_original"];
            }else{
                $findF=AlfrescoDownload::findWhere(["id"=>$id]);
                $idFile=$findF[0]["id_download"];
                $fName="archive.zip";
            }           

            $url = $this->url_alfresco ."/-default-/public/alfresco/versions/1/nodes/".$idFile."/content";

            $client = new \GuzzleHttp\Client();     
            $request_body = $client->request('GET',$url,[
                'auth' => [ $this->userAuth,$this->passwordAuth ]
            ]);
            $response = $request_body->getBody()->getContents();
            Storage::disk('local')->put("uploadTemporal/".$fName, $response);
            return response()->download(storage_path("app/uploadTemporal")."/".$fName)->deleteFileAfterSend(true);
        } catch (\Exception $e) {
            log::info("AlfrescoController@downloadfile: ".$e);
            return response()->json(["status" => 400, "message" => "Error al descargar el archivo." ]);
        }
    }
    public function findResgistros(Request $request){
        try {
            $fInicio=Carbon::parse($request->fecha_inicio)->format("Y-m-d") . " 00:00:00";
            $fFin=Carbon::parse($request->fecha_fin)->format("Y-m-d") . " 23:59:59";
            $find=AlfrescoFiles::whereBetween("created_at",[$fInicio,$fFin])
            ->where("id_directory",$request->id)
            ->get(); 
            return response()->json([
                "status" => 200,
                "message" => "Registros encontrados.",
                "response"=> $find
            ]);
        } catch (\Exception $e) {
            log::info("AlfrescoController@findAllResgistros: ".$e);
        }
    }
    public function createDownloadExample(Request $request){
        try {
            $fInicio=Carbon::parse($request->fecha_inicio)->format("Y-m-d") . " 00:00:00";
            $fFin=Carbon::parse($request->fecha_fin)->format("Y-m-d") . " 23:59:59";
            $fIdsFiles=AlfrescoFiles::whereBetween("created_at",[$fInicio,$fFin])
            ->where("id_directory",$request->id)
            ->pluck("id_file")
            ->toArray();
            $response=$this->createDownload($fIdsFiles,3);
            if($response==null){
                return response()->json([
                    "status" => 400,
                    "message" => "Carpeta creada.",
                    "response"=>[]
                ]);
            }else{
                return response()->json([
                    "status" => 200,
                    "message" => "Descarga disponible.",
                    "response"=>$response
                ]);
            }
        } catch (\Exception $e) {
            log::info("AlfrescoController@createDownloadExample: ".$e);
        }
    }
    public function createDownload($ids,$expires){
        try {
            $dateExp=Carbon::now()->addDays($expires)->format("Y-m-d");
            $url = $this->url_alfresco ."/-default-/public/alfresco/versions/1/downloads";
            $client = new \GuzzleHttp\Client();  
            $request_body = $client->request('POST',$url,[
                'auth' => [ $this->userAuth,$this->passwordAuth ] ,
                'body' => json_encode([
                'nodeIds' =>$ids //array ids
                ])
            ]);
            $response = $request_body->getBody()->getContents();
            $response=json_decode($response,true);
            if(isset($response["entry"])){
                AlfrescoDownload::create([
                    "id_download"=>$response["entry"]["id"],
                    "status"=>1,
                    "expires"=>$dateExp,
                    "json_response"=>json_encode($response),
                ]);
                
            }   
            return response()->json([
                "status" => 200,
                "message" => "zip creado.",
                "response"=> array(
                    "id_download"=>$response["entry"]["id"],
                    "status"=>1,
                    "expires"=>$dateExp,
                    "json_response"=>$response
                )
            ]);
        } catch (\Exception $e) {
            log::info("AlfrescoController@createDownload: ".$e);
            return 0;
        }
    }
}