<?php
use Slim\App;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Firebase\JWT\JWT;

return function (App $app) {
    // Public route to generate JWT token
    $app->post('/token', function (Request $request, Response $response) {
        $secretKey = getenv('JWT_SECRET'); // Retrieve from environment variable

        $payload = [
            'user' => 'testuser',
            'exp' => time() + 3600 // 1-hour expiration
        ];
        $jwt = JWT::encode($payload, $secretKey, 'HS256');
        $response->getBody()->write(json_encode(['token' => $jwt]));
        return $response->withHeader('Content-Type', 'application/json');
    });
};
