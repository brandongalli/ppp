<?php

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

function getJwtToken($config) {
    $client = new Client();

    try {
        // Request to get the JWT token from FastAPI
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

function authorizedRequest($config, $url, $method = 'GET', $options = []) {
    $token = getJwtToken($config);

    if (!$token) {
        throw new Exception("Failed to retrieve authorization token.");
    }

    $client = new Client();
    $options['headers']['Authorization'] = "Bearer {$token}";

    return $client->request($method, $url, $options);
}
