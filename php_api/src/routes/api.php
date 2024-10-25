<?php

use Slim\App;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

require __DIR__ . '/../../vendor/autoload.php';
$config = require __DIR__ . '/../config.php';
require __DIR__ . '/functions.php';

return function (App $app) use ($config) {
    // JWT Middleware for protected routes
    $authMiddleware = function (Request $request, $handler) use ($config) {
        $authHeader = $request->getHeader('Authorization');
        
        if ($authHeader && preg_match('/Bearer\s(\S+)/', $authHeader[0], $matches)) {
            try {
                // Corrected decode usage without a reference for the third parameter
                JWT::decode($matches[1], new Key($config['jwt_secret'], 'HS256'));
                return $handler->handle($request);
            } catch (Exception $e) {
                $response = new \Slim\Psr7\Response();
                $response->getBody()->write('Invalid Token');
                return $response->withStatus(401);
            }
        }

        $response = new \Slim\Psr7\Response();
        $response->getBody()->write('Unauthorized');
        return $response->withStatus(401);
    };

    // Proxy route to fetch players from FastAPI
    $app->get('/players', function (Request $request, Response $response) use ($config) {
        $query = $request->getUri()->getQuery();
        $fastapiUrl = $config['fastapi_url'] . '/players' . ($query ? "?$query" : '');

        try {
            $fastapiResponse = authorizedRequest($config, $fastapiUrl);
            $response->getBody()->write($fastapiResponse->getBody()->getContents());
            return $response->withHeader('Content-Type', 'application/json');
        } catch (Exception $e) {
            $response->getBody()->write(json_encode(['error' => 'Failed to fetch players']));
            return $response->withStatus(500)->withHeader('Content-Type', 'application/json');
        }
    });

    // Proxy route to fetch games from FastAPI
    $app->get('/games', function (Request $request, Response $response) use ($config) {
        $queryParams = $request->getQueryParams();
        $queryString = http_build_query($queryParams);
        $fastapiUrl = $config['fastapi_url'] . '/games' . ($queryString ? "?$queryString" : '');

        try {
            $fastapiResponse = authorizedRequest($config, $fastapiUrl);
            $response->getBody()->write($fastapiResponse->getBody()->getContents());
            return $response->withHeader('Content-Type', 'application/json');
        } catch (Exception $e) {
            $response->getBody()->write(json_encode(['error' => 'Failed to fetch games']));
            return $response->withStatus(500)->withHeader('Content-Type', 'application/json');
        }
    })->add($authMiddleware);
};
