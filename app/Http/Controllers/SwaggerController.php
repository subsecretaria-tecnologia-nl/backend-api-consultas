<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class SwaggerController extends Controller
{
/**
 * @return \Illuminate\Http\JsonResponse
 * 
 * 
* @OA\Post(
* path="/api/auth/login",
* operationId="login",
* tags={"Token"},
* summary="TOKEN",
* description="User Login Token",
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
*      @OA\Response(
*     response=200,
*     description="Login Successfully",
*      @OA\JsonContent(
*        @OA\Property(property="status", type="string", example=true),
*        @OA\Property(property="message", type="string", example="User Logged In Successfully."),
*        @OA\Property(property="token", type="string", example="1|0JJCOd0QSTajchCUf5fYPex0ZKThSjLWefe3OfTb")
*        )
*      ),
*      @OA\Response(
*          response=400,
*          description="Login Unsuccessfully",
*          @OA\JsonContent()
*       )
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
*       @OA\Property(property="code", type="string", example=202),
*        @OA\Property(property="status", type="string", example="Guardado exitoso."),
*        @OA\Property(property="response", type="string", example="[]")
*      )
*   ),
*      @OA\Response(
*       response=400,
*       description="Unsuccessfully",
*       @OA\JsonContent(
*        @OA\Property(property="code", type="string", example=400),
*        @OA\Property(property="status", type="string", example="id_transaccion_motor requerido."),
*        @OA\Property(property="response", type="string", example="[]")
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
*      @OA\Property(property="code", type="string", example=202),
*        @OA\Property(property="status", type="string", example="Registros encontrados"),
*        @OA\Property(property="response", type="string", example="[]")
*      )
*   ),
*      @OA\Response(
*       response=400,
*       description="Unsuccessfully",
*       @OA\JsonContent(
*        @OA\Property(property="code", type="string", example=400),
*        @OA\Property(property="status", type="string", example="Sin Registros encontrado."),
*        @OA\Property(property="response", type="string", example="[]")
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
*      @OA\Property(property="status", type="string", example=true),
*        @OA\Property(property="message", type="string", example="Archivo disponible, descarga una vez, expira en 24hrs."),
*        @OA\Property(property="url", type="string", example="http://website.com")
*      )
*   ),
* 
* )
*/
    public function index(){
    	return true;
    }
}