<?php
use Slim\App;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Firebase\JWT\JWT;

return function (App $app, PDO $pdo) {
    // JWT Middleware to authenticate protected routes
    $authMiddleware = function (Request $request, $handler) {
        $secretKey = getenv('JWT_SECRET');
        $authHeader = $request->getHeader('Authorization');

        if ($authHeader && preg_match('/Bearer\s(\S+)/', $authHeader[0], $matches)) {
            try {
                JWT::decode($matches[1], $secretKey, array('HS256'));
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

    // Protected route to fetch data from the database
    $app->get('/players', function (Request $request, Response $response) use ($pdo) {
        // Query the database
        $stmt = $pdo->query('SELECT * FROM users');
        $users = $stmt->fetchAll();

        // Serialize data into JSON
        $serializedData = json_encode($users);
        $response->getBody()->write($serializedData);

        return $response->withHeader('Content-Type', 'application/json');
    });

    // Additional private route (Example)
    $app->get('/games', function (Request $request, Response $response) use ($pdo) {
        // Fetch additional private data from the database
        $stmt = $pdo->query('SELECT name, email FROM users');
        $users = $stmt->fetchAll();

        // Serialize data into JSON
        $serializedData = json_encode($users);
        $response->getBody()->write($serializedData);

        return $response->withHeader('Content-Type', 'application/json');
    })->add($authMiddleware);
};
