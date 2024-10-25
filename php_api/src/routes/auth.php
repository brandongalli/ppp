<?php
use Slim\App;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Firebase\JWT\JWT;

return function (App $app) {
    /**
     * Route to generate a JWT token.
     * 
     * This endpoint generates a JWT token for authentication purposes. 
     * The token includes a user identifier and an expiration time set for 1 hour.
     *
     * @param Request $request The HTTP request object.
     * @param Response $response The HTTP response object.
     * 
     * @return Response Returns a JSON response with the generated JWT token.
     */
    $app->post('/token', function (Request $request, Response $response) {
        $secretKey = getenv('JWT_SECRET'); // Retrieve from environment variable

        $payload = [
            'user' => 'testuser',             // Identifier for the user (example: 'testuser')
            'exp' => time() + 3600            // Token expiration time (1 hour from current time)
        ];

        // Encode the payload as a JWT token using HS256 algorithm
        $jwt = JWT::encode($payload, $secretKey, 'HS256');
        
        // Write the token to the response body as JSON
        $response->getBody()->write(json_encode(['token' => $jwt]));
        return $response->withHeader('Content-Type', 'application/json');
    });
};
