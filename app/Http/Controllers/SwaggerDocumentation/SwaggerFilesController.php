<?php

namespace App\Http\Controllers\SwaggerDocumentation;

use App\Http\Controllers\Controller;

use Illuminate\Http\Request;
use L5Swagger\Http\Controllers\SwaggerAssetController;

class SwaggerFilesController extends Controller
{
  /**
 * @return \Illuminate\Http\JsonResponse
 * 
 * 
* @OA\Post(
* path="/api/alfresco/folder",
* operationId="folder",
* tags={"Centralizacion de archivos"},
* summary="Crear folder",
* security={{"bearerAuth":{}}},
* description="Crear la carpeta para almacenar los archivos, response->id es el identificador de la carpeta para usarse en el siguiente api.",
*      @OA\RequestBody(
*         @OA\JsonContent(),
*         @OA\MediaType(
*            mediaType="multipart/form-data",
*            @OA\Schema(
*               type="object",
*               required={"name"},
*               @OA\Property(property="name", type="string")
*            ),
*        ),
*    ),
*    @OA\Response(
*     response=200,
*     description="Carpeta creada",
*      @OA\JsonContent(
*        @OA\Property(property="status", type="string", example="integer"),
*        @OA\Property(property="message", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*        )
*      )
* ),
*
* @OA\Post(
* path="/api/alfresco/file",
* operationId="file",
* tags={"Centralizacion de archivos"},
* summary="Guardar archivo",
* security={{"bearerAuth":{}}},
* description="usar el id anterior para adjuntar el archivo para subirse",
*      @OA\RequestBody(
*         @OA\JsonContent(),
*         @OA\MediaType(
*            mediaType="multipart/form-data",
*            @OA\Schema(
*               type="object",
*               required={"id","file"},
*               @OA\Property(property="id", type="string"),
*               @OA\Property(property="file",type="file",
*                      @OA\Schema(
*                          type="string",
*                          format="binary"
*                      )
*                  ),
*            ),
*        ),
*    ),
*    @OA\Response(
*     response=200,
*     description="Carpeta creada",
*      @OA\JsonContent(
*        @OA\Property(property="status", type="string", example="integer"),
*        @OA\Property(property="message", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*        )
*      )
* ),
* 
*@OA\Get(
* path="/api/alfresco/download/{id}/{type}",
* summary="descarga de arhivo",
* description="Descarga de archivo con el id de la anterior respuesta de la api, especificar si es un archivo comprimido 'zip' o arhivo 'file' ",
* tags={"Centralizacion de archivos"},
 *   @OA\Parameter(
 *    description="id",
 *    in="path",
 *    name="id",
 *    required=true,
 *    example="21"
 *  ), 
 * @OA\Parameter(
 *    description="type",
 *    in="path",
 *    name="type",
 *    required=true,
 *    example="file"
 *  ),
*     @OA\Response(
*     response=200,
*     description="File"      
*    )
* )
*
*/
    public function index(){
        return true;
    }
}
