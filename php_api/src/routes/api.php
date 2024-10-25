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
    /**
     * JWT Middleware to protect routes by validating the Authorization header.
     *
     * This middleware intercepts requests to check for a valid JWT in the Authorization header.
     * If a valid token is present, the request proceeds to the handler; otherwise, it returns a 401 Unauthorized response.
     *
     * @param Request $request The incoming HTTP request object.
     * @param callable $handler The next middleware or request handler.
     * 
     * @return Response Returns the response from the handler if the token is valid, or a 401 response if invalid/absent.
     */
    $authMiddleware = function (Request $request, $handler) use ($config) {
        $authHeader = $request->getHeader('Authorization');
        
        if ($authHeader && preg_match('/Bearer\s(\S+)/', $authHeader[0], $matches)) {
            try {
                // Decodes JWT using the secret key from configuration
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

    /**
     * Proxy route to fetch player data from FastAPI.
     *
     * This route forwards the request to the FastAPI '/players' endpoint, appending any query parameters.
     * It uses an authorization request with a JWT token for secure access to FastAPI data.
     *
     * @param Request $request The incoming HTTP request object with optional query parameters.
     * @param Response $response The HTTP response object.
     * 
     * @return Response Returns the data from FastAPI as JSON or an error message with status 500.
     */
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

    /**
     * Proxy route to fetch game data from FastAPI.
     *
     * This route retrieves game data by forwarding the request to FastAPI's '/games' endpoint with query parameters.
     * Access to this route requires valid JWT authorization.
     *
     * @param Request $request The incoming HTTP request object with query parameters.
     * @param Response $response The HTTP response object.
     * 
     * @return Response Returns the data from FastAPI as JSON or an error message with status 500 if there is an issue.
     */
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
    })->add($authMiddleware); // Apply JWT middleware to protect the route
};
