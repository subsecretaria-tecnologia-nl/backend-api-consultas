<?php

use Illuminate\Support\Str;

return [

    /*
    |--------------------------------------------------------------------------
    | Default Database Connection Name
    |--------------------------------------------------------------------------
    |
    | Here you may specify which of the database connections below you wish
    | to use as your default connection for all database work. Of course
    | you may use many connections at once using the Database library.
    |
    */

    'default' => env('DB_CONNECTION', 'mysql'),

    /*
    |--------------------------------------------------------------------------
    | Database Connections
    |--------------------------------------------------------------------------
    |
    | Here are each of the database connections setup for your application.
    | Of course, examples of configuring each database platform that is
    | supported by Laravel is shown below to make development simple.
    |
    |
    | All database work in Laravel is done through the PHP PDO facilities
    | so make sure you have the driver for your particular database of
    | choice installed on your machine before you begin development.
    |
    */

    'connections' => [

        'sqlite' => [
            'driver' => 'sqlite',
            'url' => env('DATABASE_URL'),
            'database' => env('DB_DATABASE', database_path('database.sqlite')),
            'prefix' => '',
            'foreign_key_constraints' => env('DB_FOREIGN_KEYS', true),
        ],

        'mysql' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL_DATABASE'),
			'username' => env('DB_MYSQL_USERNAME'),
			'password' => env('DB_MYSQL_PASSWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'mysql2' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL2_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL2_DATABASE'),
			'username' => env('DB_MYSQL2_USERNAME'),
			'password' => env('DB_MYSQL2_PASSWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'mysql3' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL3_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL3_DATABASE'),
			'username' => env('DB_MYSQL3_USERNAME'),
			'password' => env('DB_MYSQL3_PASSWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'mysql4' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL4_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL6_DA4ABASE'),
			'username' => env('DB_MYSQL6_US4RNAME'),
			'password' => env('DB_MYSQL6_PA4SWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'mysql6' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL6_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL6_DATABASE'),
			'username' => env('DB_MYSQL6_USERNAME'),
			'password' => env('DB_MYSQL6_PASSWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'mysql7' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL7_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL7_DATABASE'),
			'username' => env('DB_MYSQL7_USERNAME'),
			'password' => env('DB_MYSQL7_PASSWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'mysql8' => [
			'driver' => 'mysql',
			'url' => env('DATABASE_URL'),
			'host' => env('DB_MYSQL8_HOST'),
			'port' => env('DB_PORT', '3306'),
			'database' => env('DB_MYSQL8_DATABASE'),
			'username' => env('DB_MYSQL8_USERNAME'),
			'password' => env('DB_MYSQL8_PASSWORD'),
			'unix_socket' => env('DB_SOCKET', ''),
			'charset' => 'utf8',
			'collation' => 'utf8_unicode_ci',
			'prefix' => '',
			'prefix_indexes' => true,
			'strict' => false,
			'engine' => null,
			'options' => extension_loaded('pdo_mysql') ? array_filter([
				PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
			]) : [],
		],
		'oracle' => [
			'driver' => 'oracle',
			'host' => getenv('DB_ORACLE_HOST'),
			'port' => '1521',
			'database' => getenv('DB_ORACLE_DATABASE'),
			'service_name' => getenv('DB_ORACLE_SERVICE_NAME'),
			'username' => getenv('DB_ORACLE_USERNAME'),
			'password' => getenv('DB_ORACLE_PASSWORD'),
			'charset' => 'UTF8',
			'prefix' => '',
		],

        'pgsql' => [
            'driver' => 'pgsql',
            'url' => env('DATABASE_URL'),
            'host' => env('DB_HOST', '127.0.0.1'),
            'port' => env('DB_PORT', '5432'),
            'database' => env('DB_DATABASE', 'forge'),
            'username' => env('DB_USERNAME', 'forge'),
            'password' => env('DB_PASSWORD', ''),
            'charset' => 'utf8',
            'prefix' => '',
            'prefix_indexes' => true,
            'search_path' => 'public',
            'sslmode' => 'prefer',
        ],

        'sqlsrv' => [
            'driver' => 'sqlsrv',
            'url' => env('DATABASE_URL'),
            'host' => env('DB_HOST', 'localhost'),
            'port' => env('DB_PORT', '1433'),
            'database' => env('DB_DATABASE', 'forge'),
            'username' => env('DB_USERNAME', 'forge'),
            'password' => env('DB_PASSWORD', ''),
            'charset' => 'utf8',
            'prefix' => '',
            'prefix_indexes' => true,
            // 'encrypt' => env('DB_ENCRYPT', 'yes'),
            // 'trust_server_certificate' => env('DB_TRUST_SERVER_CERTIFICATE', 'false'),
        ],

    ],

    /*
    |--------------------------------------------------------------------------
    | Migration Repository Table
    |--------------------------------------------------------------------------
    |
    | This table keeps track of all the migrations that have already run for
    | your application. Using this information, we can determine which of
    | the migrations on disk haven't actually been run in the database.
    |
    */

    'migrations' => 'migrations',

    /*
    |--------------------------------------------------------------------------
    | Redis Databases
    |--------------------------------------------------------------------------
    |
    | Redis is an open source, fast, and advanced key-value store that also
    | provides a richer body of commands than a typical key-value system
    | such as APC or Memcached. Laravel makes it easy to dig right in.
    |
    */

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
            'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        ],

        'default' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_DB', '0'),
        ],

        'cache' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_CACHE_DB', '1'),
        ],

    ],

];
