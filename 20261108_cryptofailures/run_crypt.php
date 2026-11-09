<?php
// crypt.php

function cryptstring($what, $SALT) {
    return crypt($what, $SALT);
}

if ($argc < 3) {
    fwrite(STDERR, "Gebruik: php crypt.php <input> <salt>\n");
    exit(1);
}

$input = $argv[1];
$salt  = $argv[2];

echo cryptstring($input, $salt), PHP_EOL;
