<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api;
/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/
#Route::apiResource('posts', PostController::class)->middleware('auth:sanctum');
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('/consulta-pagos','ConsultasController@consultaPagos');
Route::get('/verifica-pagos','ConsultasController@PagosVerificados');
Route::get('/consulta-folios','ConsultasController@consultaEntidadFolios');
Route::post('/auth/login', [Api\AuthController::class, 'loginUser']);

Route::middleware('auth:sanctum')->group(function (){

    #Route::post('/auth/logout', [Api\AuthController::class, 'logoutUser']);
    Route::post('/auth/register', [Api\AuthController::class, 'createUser']);
    #API_USUARIOS para consultar usurios | administrar
    Route::get('/admin/users/{id_?}', [Api\AdministrarUsuariosController::class, 'findUsers']);
    Route::post('/admin/status', [Api\AdministrarUsuariosController::class, 'updateStatus']);    
    Route::put('/admin/users/{id_?}', [Api\AdministrarUsuariosController::class, 'updateUsers']);
    Route::post('/admin/entidad', [Api\AdministrarUsuariosController::class, 'findEntidad']);
    Route::post('/admin/entidad-tramite', [Api\AdministrarUsuariosController::class, 'findEntidadTramite']);
    Route::post('/admin/entidad-tramite-user', [Api\AdministrarUsuariosController::class, 'findEntidadTramiteUser']);
    Route::put('/admin/entidad-tramite-user', [Api\AdministrarUsuariosController::class, 'insertEntidadTramite']);
    Route::delete('/admin/entidad-tramite-user', [Api\AdministrarUsuariosController::class, 'deletedEntidadTramite']);
    Route::get('/admin/configuracion-ws', [Api\AdministrarUsuariosController::class, 'deletedEntidadTramite']);
    #CONSULTAS APIS
});
