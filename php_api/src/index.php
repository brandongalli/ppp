<?php
require __DIR__ . '/../vendor/autoload.php'; // Autoload dependencies

use Slim\Factory\AppFactory;

$app = AppFactory::create(); // Create Slim app instance

// CORS Middleware
$app->add(function ($request, $handler) {
    $response = $handler->handle($request);
    return $response
        ->withHeader('Access-Control-Allow-Origin', '*') // Allow all origins; replace '*' with specific origin if needed
        ->withHeader('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, Origin, Authorization')
        ->withHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
});

// Handle preflight OPTIONS requests
$app->options('/{routes:.+}', function ($request, $response) {
    return $response;
});

// Retrieve database configuration from environment variables
$dbHost = getenv('DATABASE_HOST');
$dbName = getenv('DATABASE');
$dbUser = getenv('DATABASE_USERNAME');
$dbPassword = getenv('DATABASE_PASSWORD');

// Set up MySQL PDO connection with error and fetch mode configurations
$dsn = "mysql:host=$dbHost;dbname=$dbName";
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,   // Enable exception handling for PDO errors
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // Set default fetch mode to associative array
];
$pdo = new PDO($dsn, $dbUser, $dbPassword, $options); // Initialize PDO connection

// Load route definitions, injecting dependencies as required
(require __DIR__ . '/routes/auth.php')($app);       // Register authentication routes
(require __DIR__ . '/routes/api.php')($app, $pdo);   // Register API routes with database access

$app->run(); // Run the Slim app
