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
        Schema::create('oper_pagos_api_historial', function (Blueprint $table) {
            $table->id();
            $table->string("id_transaccion_motor",11);
            $table->string("id_transaccion",100);
            $table->integer("estatus");
            $table->string("desc_estatus",100);
            $table->integer("entidad");
            $table->string("referencia",100);
            $table->string("Total",100);
            $table->string("MetododePago",100);
            $table->string("cve_Banco",100);
            $table->string("FechaTransaccion",100);
            $table->string("FechaPago",100);
            $table->string("FechaConciliacion",100);
            $table->integer("tipo_servicio");
            $table->string("desc_tipo_servicio",100);
            $table->json("detalle");
            $table->json("corte");
            $table->integer("procesado");
            $table->string("usuario_procesado",100);
            $table->timestamps();
        });
    }
    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('oper_pagos_historial');
    }
};
