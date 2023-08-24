<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use App\Models\User;
use Exception;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Log;
use Carbon\Carbon;
class AuthController extends Controller
{
     
    public function createUser(Request $request)
    {
        try {
            $validateUser = Validator::make($request->all(), 
            [
                'name' => 'required',
                'email' => 'required|email|unique:users,email',
                'password' => 'required'
            ]);
            if($validateUser->fails()){
                return response()->json([
                    'status' => 400,
                    'message' => 'validacion error',
                    'errors' => $validateUser->errors()
                ], 401);
            }
            User::create([
                'name' => $request->name,
                'email' => $request->email,
                'password' => Hash::make($request->password),
                'status' => "1",
                'perfil' => "",
                'entidad' => json_encode(array()),
                'tramites' => json_encode(array())
            ]);

            return response()->json([
                'status' => 200,
                'message' => 'Usuerio creado correctamente!!'
            ], 200);

        } catch (\Throwable $th) {
            return response()->json([
                'status' => 400,
                'message' => $th->getMessage()
            ], 500);
        }
    }

    /**
     * Login The User
     * @param Request $request
     * @return User
     */
    public function loginUser(Request $request)
    {
        $minutes=env("TOKEN_EXPIRES_MINUTES");
        try {
            $validateUser = Validator::make($request->all(), 
            [
                'email' => 'required|email',
                'password' => 'required',
                'status'=>'1'
            ]);

            if($validateUser->fails()){
                return response()->json([
                    'status' => 400,
                    'message' => 'Error de validacion',
                    'errors' => $validateUser->errors()
                ], 401);
            }

            if(!Auth::attempt($request->only(['email', 'password']))){
                return response()->json([
                    'status' => 400,
                    'message' => 'Correo & Contraseña no coincide con nuestro registro.',
                ], 401);
            }

            $user = User::where('email', $request->email)->where('status',1)->first();
            if(!empty($user)){
                return response()->json([
                    'status' => true,
                    'message' => 'Usuario autenticado correctamente',
                    'token' => $user->createToken("API TOKEN",["*"],Carbon::now()->addMinutes($minutes))->plainTextToken
                ], 200);
            }else{
                return response()->json([
                    'status' => 400,
                    'message' => 'Error al autenticar',
                ], 401);
            }          

        } catch (\Throwable $th) {
            return response()->json([
                'status' => 400,
                'message' => $th->getMessage()
            ], 500);
        }
    }

    public function logoutUser(Request $request){
        try {
            auth()->user()->tokens()->delete();
            return [
                'status' => 200,
                'message' => 'Cerrar sesion correntamente'
            ];
        } catch (Exception $th) {
            return response()->json([
                'status' => 400,
                'message' => $th->getMessage()
            ], 500);
        }
    }
}
