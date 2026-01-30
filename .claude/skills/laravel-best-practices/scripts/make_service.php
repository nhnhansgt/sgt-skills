#!/usr/bin/env php
<?php

/**
 * Laravel Service Generator
 *
 * Usage: php scripts/make_service.php UserService
 * Output: app/Services/UserService.php
 */

if ($argc < 2) {
    echo "Usage: php make_service.php <ServiceName>\n";
    echo "Example: php make_service.php UserService\n";
    exit(1);
}

$serviceName = $argv[1];
$basePath = __DIR__ . '/../../..'; // Go to Laravel project root

// Validate service name
if (!preg_match('/^[A-Z][a-zA-Z]*$/', $serviceName)) {
    echo "Error: Service name must be in PascalCase (e.g., UserService)\n";
    exit(1);
}

// Create Services directory
$servicesDir = $basePath . '/app/Services';
if (!is_dir($servicesDir)) {
    mkdir($servicesDir, 0755, true);
}

$filePath = $servicesDir . '/' . $serviceName . '.php';

// Check if file exists
if (file_exists($filePath)) {
    echo "Error: {$serviceName} already exists at {$filePath}\n";
    exit(1);
}

$namespace = 'App\\Services';

$template = <<<PHP
<?php

namespace {$namespace};

class {$serviceName}
{
    // Add your service methods here

    public function __construct()
    {
        // Inject dependencies via constructor
    }
}
PHP;

if (file_put_contents($filePath, $template)) {
    echo "✅ Service created: {$filePath}\n";
} else {
    echo "Error: Failed to create service file\n";
    exit(1);
}
