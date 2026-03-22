<?php

declare(strict_types=1);

/**
 * Demo API endpoint for AI assistant workflows.
 *
 * Run locally:
 * php -S localhost:8080 -t src
 *
 * Example:
 * curl "http://localhost:8080/index.php?user_id=2"
 */

header('Content-Type: application/json; charset=utf-8');

$users = [
    1 => ['id' => 1, 'name' => 'Ada Lovelace', 'email' => 'ada@example.com', 'role' => 'admin'],
    2 => ['id' => 2, 'name' => 'Linus Torvalds', 'email' => 'linus@example.com', 'role' => 'maintainer'],
    3 => ['id' => 3, 'name' => 'Margaret Hamilton', 'email' => 'margaret@example.com', 'role' => 'reviewer'],
];

$requestedUserId = filter_input(INPUT_GET, 'user_id', FILTER_VALIDATE_INT);

if ($requestedUserId !== null && $requestedUserId !== false) {
    if (!array_key_exists($requestedUserId, $users)) {
        http_response_code(404);
        echo json_encode([
            'ok' => false,
            'error' => 'User not found',
        ], JSON_PRETTY_PRINT);
        exit;
    }

    echo json_encode([
        'ok' => true,
        'data' => $users[$requestedUserId],
    ], JSON_PRETTY_PRINT);
    exit;
}

echo json_encode([
    'ok' => true,
    'data' => array_values($users),
], JSON_PRETTY_PRINT);
