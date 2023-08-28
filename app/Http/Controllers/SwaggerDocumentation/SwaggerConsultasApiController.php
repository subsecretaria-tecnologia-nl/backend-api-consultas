<?php

namespace App\Http\Controllers\SwaggerDocumentation;

use App\Http\Controllers\Controller;

use Illuminate\Http\Request;
use L5Swagger\Http\Controllers\SwaggerAssetController;

class SwaggerConsultasApiController extends Controller
{
/**
 * @return \Illuminate\Http\JsonResponse
 * 
 * 
* @OA\Post(
* path="/api/auth/login",
* operationId="login",
* tags={"Token"},
* summary="Token",
* description="Api para obtener el token y usarlo en cada peticion",
*      @OA\RequestBody(
*         @OA\JsonContent(),
*         @OA\MediaType(
*            mediaType="multipart/form-data",
*            @OA\Schema(
*               type="object",
*               required={"email", "password"},
*               @OA\Property(property="email", type="email"),
*               @OA\Property(property="password", type="password")
*            ),
*        ),
*    ),
*    @OA\Response(
*     response=200,
*     description="Login Successfully",
*      @OA\JsonContent(
*        @OA\Property(property="status", type="string", example="integer"),
*        @OA\Property(property="message", type="string", example="string"),
*        @OA\Property(property="token", type="string", example="string")
*        )
*      ),
*    @OA\Response(
*         response=400,
*         description="string",
*        @OA\JsonContent(
*           @OA\Property(property="status", type="string", example="integer"),
*           @OA\Property(property="message", type="string", example="string"),
*           @OA\Property(property="token", type="string", example="string")
*        )
*     )
* )
*
 * @OA\Get(
 * path="/api/consulta-pagos",
 * summary="Consulta de transacciones",
 * description="Consulta de transacciones pagadas por entidad",
 * tags={"Consultas"},
 * security={{"bearerAuth":{}}},
*     @OA\Response(
*     response=200,
*     description="Successfully",
*      @OA\JsonContent(
*        @OA\Property(property="status", type="string", example="integer"),
*        @OA\Property(property="message", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*      )
*    )
* )
*
* @OA\Post(
* path="/api/verifica-pagos",
* operationId="verifica_pagos",
* tags={"Consultas"},
* summary="Verifica pagos",
* description="Verificacion de transacciones consultadas",
* security={{"bearerAuth":{}}},
*      @OA\RequestBody(
*         @OA\JsonContent(
*               @OA\Property(
*                   property="id_transaccion_motor", type="object",
*                   collectionFormat="multi",
*                   example="[2000000000]",    
*            ),
*        ),
*    ),     
*  @OA\Response(
*     response=202,
*     description="Successfully",
*      @OA\JsonContent(
*       @OA\Property(property="status", type="string", example="integer"),
*        @OA\Property(property="message", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*      )
*   ),
*      @OA\Response(
*       response=400,
*       description="Unsuccessfully",
*       @OA\JsonContent(
*        @OA\Property(property="code", type="string",  example="integer"),
*        @OA\Property(property="status", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*       )
*    )
* )
* @OA\Post(
* path="/api/consulta-folios",
* operationId="consulta_folios",
* tags={"Consultas"},
* summary="Consulta de folios",
* description="consulta de folios",
* security={{"bearerAuth":{}}},
*      @OA\RequestBody(
*         @OA\JsonContent(
*               @OA\Property(
*                   property="id_transaccion_motor", type="object",
*                   collectionFormat="multi",
*                   example="[2000000000]",    
*            ),
*        ),
*    ),     
*  @OA\Response(
*     response=202,
*     description="Successfully",
*      @OA\JsonContent(
*      @OA\Property(property="code", type="string", example="integer"),
*        @OA\Property(property="status", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*      )
*   ),
*      @OA\Response(
*       response=400,
*       description="Unsuccessfully",
*       @OA\JsonContent(
*        @OA\Property(property="code", type="string", example="integer"),
*        @OA\Property(property="status", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*       )
*    )
* ),
* @OA\Get(
* path="/api/consulta-folio/{tipo}/{transaccion}",
* operationId="consulta_tipo_folio",
* tags={"Consultas"},
* summary="Consulta de folios",
* description="consulta por tipo id_transaccion_motor/referencia/id_transaccion",
* security={{"bearerAuth":{}}},
*     @OA\Parameter(
 *    in="path",
 *    name="tipo",
 *    required=true
 *  ), 
 * @OA\Parameter(
 *    in="path",
 *    name="transaccion",
 *    required=true
 *  ), 
*  @OA\Response(
*     response=202,
*     description="Successfully",
*      @OA\JsonContent(
*      @OA\Property(property="code", type="string", example="integer"),
*        @OA\Property(property="status", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*      )
*   ),
*      @OA\Response(
*       response=400,
*       description="Unsuccessfully",
*       @OA\JsonContent(
*        @OA\Property(property="code", type="string", example="integer"),
*        @OA\Property(property="status", type="string", example="string"),
*        @OA\Property(property="response", type="string", example="array")
*       )
*    )
* ),
* @OA\Post(
* path="/api/consulta-archivos",
* operationId="consulta_archivos",
* tags={"Consultas"},
* summary="Consulta archivos",
* description="consulta por fecha y genera una url de descarga de archivo en txt",
* security={{"bearerAuth":{}}},
*      @OA\RequestBody(
*         @OA\JsonContent(
*               @OA\Property(
*                   property="fecha_registro", type="object",
*                   collectionFormat="multi",
*                   example="2021-02-22",    
*            ),
*        ),
*    ),     
*  @OA\Response(
*     response=202,
*     description="Successfully",
*      @OA\JsonContent(
*      @OA\Property(property="status", type="string", example="integer"),
*        @OA\Property(property="message", type="string", example="string"),
*        @OA\Property(property="url", type="string", example="string")
*      )
*   ),
* 
* )
*/
    public function index(){
    	return true;
    }
}