<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class AlfrescoDownload extends Model
{
    use HasFactory;
    protected $connection = "mysql";

    protected $fillable = ['id','id_download','expires','status','json_response','created_at','updated_at'];    

    protected $table = "alfresco_download";
}
