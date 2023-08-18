<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class AlfrescoDirectory extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $fillable = ['id','name_folder','id_folder','node_type','parent_id','status','json_response','created_at','updated_at'];    

    protected $table = "alfresco_directory";
}
