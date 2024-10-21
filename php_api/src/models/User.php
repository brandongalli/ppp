<?php

class User {
    private $id;
    private $name;
    private $email;

    // Constructor to initialize the user object
    public function __construct($data) {
        $this->id = $data['id'] ?? null;
        $this->name = $data['name'] ?? '';
        $this->email = $data['email'] ?? '';
    }

    // Validation method for user data
    public static function validate($data) {
        $errors = [];

        if (empty($data['name'])) {
            $errors[] = 'Name is required';
        }
        if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
            $errors[] = 'Invalid email address';
        }

        return $errors;
    }

    // Method to serialize the user object into an array for JSON response
    public function serialize() {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email
        ];
    }

    // Static method to create an array of user objects from database results
    public static function fromDbRows($rows) {
        return array_map(function ($row) {
            return new self($row);
        }, $rows);
    }
}
