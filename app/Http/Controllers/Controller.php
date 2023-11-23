<?php

namespace App\Http\Controllers;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

/**
 * @OA\Info(
 *    title="API's Consultas de transacciones",
 *    version="1.0.1",
 * )
 * * @OA\Server(url="http://localhost/backend-api-consultas/public")
*/
class Controller extends BaseController
{

    use AuthorizesRequests, ValidatesRequests;
}
