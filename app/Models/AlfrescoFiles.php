<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class AlfrescoFiles extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $fillable = ['id','id_directory','name_original','name_file','id_file','status','type_file','node_type','parent_id','json_response','created_at','updated_at'];    

    protected $table = "alfresco_files";
}
