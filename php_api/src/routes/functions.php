<?php

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

/**
 * Retrieves a JWT token from FastAPI.
 *
 * @param array $config Configuration array containing 'fastapi_url', 'fastapi_email', and 'fastapi_password'.
 * 
 * @return string|null Returns the JWT token as a string if successful, or null on failure.
 */
function getJwtToken($config) {
    $client = new Client();

    try {
        $response = $client->post($config['fastapi_url'] . '/token', [
            'json' => [
                'email' => $config['fastapi_email'],
                'password' => $config['fastapi_password']
            ]
        ]);

        $data = json_decode($response->getBody(), true);
        return $data['access_token'] ?? null;
    } catch (RequestException $e) {
        error_log('Error fetching JWT: ' . $e->getMessage());
        return null;
    }
}

/**
 * Sends an HTTP request to a specified URL with JWT authorization.
 *
 * @param array $config Configuration array, requiring FastAPI credentials and URL.
 * @param string $url The target URL for the request.
 * @param string $method HTTP method to use, defaults to 'GET'.
 * @param array $options Optional additional request options (e.g., query parameters, body).
 * 
 * @return \Psr\Http\Message\ResponseInterface The HTTP response object from the request.
 * 
 * @throws Exception Throws an exception if the JWT token cannot be retrieved.
 */
function authorizedRequest($config, $url, $method = 'GET', $options = []) {
    $token = getJwtToken($config);

    if (!$token) {
        throw new Exception("Failed to retrieve authorization token.");
    }

    $client = new Client();
    $options['headers']['Authorization'] = "Bearer {$token}";

    return $client->request($method, $url, $options);
}
