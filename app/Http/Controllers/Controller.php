<?php

namespace App\Http\Controllers;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

/**
 * @OA\Info(
 *    title="Your super  ApplicationAPI",
 *    version="1.0.0",
 * )
 * * @OA\Server(url="http://localhost/backend-api-consultas/public")
*/
class Controller extends BaseController
{

    use AuthorizesRequests, ValidatesRequests;
}
