<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('api_servicios', function (Blueprint $table) {
            $table->id();
            $table->string('user_id',50);
            $table->string('url_token',200);
            $table->string('url',200);
            $table->string('metodo',50);   
            $table->string('tipo',50);
            $table->string('autenticacion',50);
            $table->string('usuario',200); 
            $table->string('password',200);
            $table->string('alias_usuario',200); 
            $table->string('alias_password',200);
            $table->string('token',200);
            $table->string('parametro',100);
            $table->text('header_token'); 
            $table->text('footer_token');
            $table->text('header'); 
            $table->text('footer');
            $table->json('json'); 
            $table->json('bd_query'); 
            $table->string('tiempo',50);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('api_servicios');
    }
};
