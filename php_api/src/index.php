<?php
require __DIR__ . '/../vendor/autoload.php';

use Slim\Factory\AppFactory;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

$app = AppFactory::create();

// JWT Secret Key
$secretKey = "your_secret_key";

// Middleware to validate JWT
$authMiddleware = function (Request $request, $handler) use ($secretKey) {
    $authHeader = $request->getHeader('Authorization');
    if ($authHeader && preg_match('/Bearer\s(\S+)/', $authHeader[0], $matches)) {
        try {
            // Decode JWT and validate signature
            $decoded = JWT::decode($matches[1], new Key($secretKey, 'HS256'));

            // Continue request if valid
            return $handler->handle($request);
        } catch (Exception $e) {
            $response = new \Slim\Psr7\Response();
            $response->getBody()->write('Invalid Token: ' . $e->getMessage());
            return $response->withStatus(401);
        }
    }

    $response = new \Slim\Psr7\Response();
    $response->getBody()->write('Unauthorized');
    return $response->withStatus(401);
};

// Route to generate JWT token (public)
$app->post('/token', function (Request $request, Response $response) use ($secretKey) {
    $payload = [
        'user' => 'testuser',
        'exp' => time() + 3600 // 1 hour expiration
    ];

    $jwt = JWT::encode($payload, $secretKey, 'HS256');
    $response->getBody()->write(json_encode(['token' => $jwt]));
    return $response->withHeader('Content-Type', 'application/json');
});

// Protected route (requires valid JWT)
$app->get('/protected', function (Request $request, Response $response) {
    $response->getBody()->write('You are authorized!');
    return $response;
})->add($authMiddleware);

$app->run();
