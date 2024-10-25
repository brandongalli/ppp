<?php

class User {
    private $id;
    private $name;
    private $email;

    /**
     * Constructor to initialize the User object with provided data.
     *
     * @param array $data Associative array with 'id', 'name', and 'email' keys.
     *                    'id' defaults to null, 'name' to an empty string if not provided.
     */
    public function __construct($data) {
        $this->id = $data['id'] ?? null;
        $this->name = $data['name'] ?? '';
        $this->email = $data['email'] ?? '';
    }

    /**
     * Validates user data, checking for required fields and correct formats.
     *
     * @param array $data Associative array with 'name' and 'email' fields for validation.
     * 
     * @return array Returns an array of validation error messages. Empty if no errors.
     */
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

    /**
     * Serializes the User object into an associative array format for JSON responses.
     *
     * @return array Returns an array with 'id', 'name', and 'email' keys.
     */
    public function serialize() {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email
        ];
    }

    /**
     * Creates an array of User objects from database result rows.
     *
     * @param array $rows Array of associative arrays, each representing a user row from the database.
     * 
     * @return array Returns an array of User objects initialized with database row data.
     */
    public static function fromDbRows($rows) {
        return array_map(function ($row) {
            return new self($row);
        }, $rows);
    }
}
