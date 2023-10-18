<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers;
use App\Http\Controllers\Api;

use App\Http\Controllers\Servicios;

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
Route::get('/download-file',[Servicios\ConsultasController::class, 'downloadFile'])->name("api/download-file");
Route::get('/alfresco/download/{id?}/{type?}',[Servicios\AlfrescoController::class, 'downloadFile']);
Route::middleware('auth:sanctum')->group(function (){

    #Route::post('/auth/logout', [Api\AuthController::class, 'logoutUser']);

    #API_USUARIOS para consultar usurios | administrar 
    Route::post('/auth/register', [Api\AuthController::class, 'createUser']);
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
    Route::get('/cron/servicios', [Servicios\ServiciosExternosController::class, 'findServicios']);

    #CONSULTA TRANSACCIONES
    Route::get('/consulta-pagos',[Servicios\ConsultasController::class, 'consultaPagos']);
    Route::get('/consulta-cancelados',[Servicios\ConsultasController::class, 'findCancelados']);
    Route::post('/verifica-pagos',[Servicios\ConsultasController::class, 'PagosVerificados']);
    Route::post('/consulta-folios',[Servicios\ConsultasController::class, 'consultaEntidadFolios']);
    Route::get('/consulta-folio/{tipo?}/{transaccion?}',[Servicios\ConsultasController::class, 'consultaTransacciones']);
    Route::post('/consulta-archivos',[Servicios\ConsultasController::class, 'findTransacciones']);
    Route::post('/consulta-general',[Servicios\ConsultasController::class, 'consultaGeneral']);
    Route::post('/consulta-historico',[Servicios\ConsultasController::class, 'consultaTransaccionesHistorico']);

    #API ALFRESCO SERVICIO concentracion de archivos
    Route::post('/alfresco/folder',[Servicios\AlfrescoController::class, 'createfolder']);
    Route::post('/alfresco/file',[Servicios\AlfrescoController::class, 'saveFile']);    
    Route::get('/alfresco/all-folder',[Servicios\AlfrescoController::class, 'findAllResgistros']);
    Route::post('/alfresco/folder-file',[Servicios\AlfrescoController::class, 'findFiles']);
    Route::post('/alfresco/date-file',[Servicios\AlfrescoController::class, 'findResgistros']);
    Route::post('/alfresco/create-zip',[Servicios\AlfrescoController::class, 'createDownloadExample']);


});
