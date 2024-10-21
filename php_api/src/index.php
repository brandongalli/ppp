<?php
require __DIR__ . '/../vendor/autoload.php';

use Slim\Factory\AppFactory;

// Create the Slim app
$app = AppFactory::create();

// Load environment variables from Docker

$dbHost = getenv('DATABASE_HOST');
$dbName = getenv('DATABASE');
$dbUser = getenv('DATABASE_USERNAME');
$dbPassword = getenv('DATABASE_PASSWORD');

// Set up MySQL PDO connection
$dsn = "mysql:host=$dbHost;dbname=$dbName";
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
];
$pdo = new PDO($dsn, $dbUser, $dbPassword, $options);

// Include routes
(require __DIR__ . '/routes/auth.php')($app);
(require __DIR__ . '/routes/api.php')($app, $pdo);

// Run the Slim app
$app->run();
