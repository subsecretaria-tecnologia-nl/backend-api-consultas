<?php

namespace App\Http\Middleware\Api;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Illuminate\Support\Facades\Log;
class Authenticate
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        #obtner datos basicos para bitacora
        #ruta
        #usario
        #fecha
        #request
        $url =$request->url();
        $request=$request;
        $user=auth()->user();
        #log::info($user);
        return $next($request);
    }
}
