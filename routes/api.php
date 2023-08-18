<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers;
use App\Http\Controllers\Api;

use App\Http\Controllers\ServiciosExternosController;
use App\Http\Controllers\ConsultasController;
use App\Http\Controllers\SwaggerController;
use App\Http\Controllers\AlfrescoController;

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


Route::post('/auth/login', [Api\AuthController::class, 'loginUser']);
Route::get('/download-file',[ConsultasController::class, 'downloadFile'])->name("api/download-file");
Route::middleware('auth:sanctum')->group(function (){

    #Route::post('/auth/logout', [Api\AuthController::class, 'logoutUser']);
    Route::get('/swagger/home', [Api\SwaggerController::class, 'index']);
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
    Route::get('/admin/servicios-ws/{user_id?}', [Api\AdministrarUsuariosController::class, 'findWs']);
    Route::post('/admin/servicios-ws', [Api\AdministrarUsuariosController::class, 'insertServicioWs']);
    Route::post('/admin/servicios-ws/{id_registro?}', [Api\AdministrarUsuariosController::class, 'updateServicioWs']);
    Route::get('/cron/servicios', [ServiciosExternosController::class, 'findServicios']);

    #CONSULTA TRANSACCIONES
    Route::get('/consulta-pagos',[ConsultasController::class, 'consultaPagos']);
    Route::post('/verifica-pagos',[ConsultasController::class, 'PagosVerificados']);
    Route::post('/consulta-folios',[ConsultasController::class, 'consultaEntidadFolios']);
    Route::post('/consulta-archivos',[ConsultasController::class, 'findTransacciones']);

    #API ALFRESCO SERVICIO concentracion de archivos
    Route::post('/folder',[AlfrescoController::class, 'createfolder']);
    Route::post('/verifica-pagos',[AlfrescoController::class, 'PagosVerificados']);

});
