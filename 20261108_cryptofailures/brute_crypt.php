<?php
// brute_crypt.php
// Gebruik: php brute_crypt.php <salt> <hash1> [hash2] ...
// Voorbeeld: php brute_crypt.php MA MAQ55hx59Xoc6 MAB0vELZMxT12

if ($argc < 3) {
    fwrite(STDERR, "Gebruik: php brute_crypt.php <salt> <hash1> [hash2] ...\n");
    exit(1);
}

$salt = $argv[1];
$targets = array_slice($argv, 2);

// Characterset zoals opgegeven
$charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}";
$len = strlen($charset);

// Maak een set van targets voor snelle lookup (array_flip is O(1) lookup)
$targetSet = array_flip($targets);

// We zoeken maximaal 8 tekens.
// Om multicore te gebruiken, splitsen we de zoekruimte in chunks.
// Elke worker krijgt een "start index" en een "chunk size".
// De totale ruimte is: sum(len^i for i=1..8) = len + len^2 + ... + len^8

// Bereken totale ruimte (kan groot zijn, maar we gebruiken 64-bit integers)
$totalSpace = 0;
$power = $len;
for ($i = 1; $i <= 8; $i++) {
    $totalSpace += $power;
    if ($i < 8) {
        // Voorkom overflow, maar voor dit characterset (64 chars) is len^8 = 2^48, prima in 64-bit
        $power *= $len;
    }
}

// Bepaal aantal cores. Probeer sys_getloadavg of nproc via shell_exec als fallback.
$cores = 1;
if (function_exists('shell_exec')) {
    // Probeer nproc (Linux)
    $nproc = trim(shell_exec('nproc 2>/dev/null'));
    if ($nproc && is_numeric($nproc)) {
        $cores = (int)$nproc;
    } else {
        // Fallback: sys_getloadavg geeft load average, niet cores. Gebruik 4 als default.
        $cores = 4;
    }
}

// Zorg dat we niet te veel processen starten
$cores = max(1, min($cores, 32));

echo "Salt: $salt\n";
echo "Targets: " . implode(', ', $targets) . "\n";
echo "Characterset lengte: $len\n";
echo "Totale zoekruimte (max 8 tekens): $totalSpace\n";
echo "Aantal cores/workers: $cores\n\n";

// Splits de totale ruimte in chunks voor elke worker
$chunkSize = intdiv($totalSpace, $cores);
if ($chunkSize < 1) {
    $chunkSize = 1;
}

// Start workers via pcntl_fork als beschikbaar, anders sequentieel
if (function_exists('pcntl_fork')) {
    $pids = [];
    
    for ($workerId = 0; $workerId < $cores; $workerId++) {
        // Bereken start en einde voor deze worker
        $start = $workerId * $chunkSize;
        $end = ($workerId === $cores - 1) ? $totalSpace : ($start + $chunkSize);
        
        if ($start >= $totalSpace) break;
        
        $pid = pcntl_fork();
        
        if ($pid == -1) {
            fwrite(STDERR, "Fout bij fork voor worker $workerId\n");
            exit(1);
        } elseif ($pid == 0) {
            // Kind process: doe het werk
            bruteForceChunk($salt, $targetSet, $charset, $len, $start, $end, $workerId);
            exit(0);
        } else {
            $pids[] = $pid;
        }
    }
    
    // Wacht op alle children
    foreach ($pids as $pid) {
        pcntl_wait($status, 0, $pid);
    }
} else {
    // Fallback: sequentieel (geen multicore)
    echo "pcntl niet beschikbaar, draait sequentieel...\n";
    bruteForceChunk($salt, $targetSet, $charset, $len, 0, $totalSpace, 0);
}

echo "\nKlaar.\n";

function bruteForceChunk(string $salt, array $targetSet, string $charset, int $len, int $start, int $end, int $workerId): void {
    // We genereren strings van lengte 1 tot 8.
    // De "index" in de totale ruimte is een gemengd getal: eerst alle lengte-1, dan lengte-2, etc.
    
    // Eerst berekenen hoeveel er per lengte zijn
    $counts = [];
    $totalSoFar = 0;
    for ($l = 1; $l <= 8; $l++) {
        $count = pow($len, $l);
        $counts[$l] = $count;
        $totalSoFar += $count;
    }
    
    // Bepaal welke lengtes binnen [start, end) vallen
    // We kunnen per lengte bepalen of er overlap is
    
    for ($l = 1; $l <= 8; $l++) {
        $countForLen = (int)$counts[$l];
        
        // Bereken het bereik voor deze lengte in de globale index
        // Eerst alle kortere lengtes
        $offsetBefore = 0;
        for ($i = 1; $i < $l; $i++) {
            $offsetBefore += (int)$counts[$i];
        }
        
        $rangeStart = $offsetBefore;
        $rangeEnd = $offsetBefore + $countForLen;
        
        // Overlap met [start, end)?
        $overlapStart = max($start, $rangeStart);
        $overlapEnd = min($end, $rangeEnd);
        
        if ($overlapStart >= $overlapEnd) {
            continue; // Geen overlap voor deze lengte
        }
        
        // Lokale indices binnen deze lengte
        $localStart = $overlapStart - $rangeStart;
        $localEnd = $overlapEnd - $rangeStart;
        
        // Genereer alle strings van lengte $l met index in [$localStart, $localEnd)
        for ($idx = $localStart; $idx < $localEnd; $idx++) {
            // Converteer index naar string van lengte $l over characterset
            $str = '';
            $tempIdx = $idx;
            for ($pos = 0; $pos < $l; $pos++) {
                $charIndex = $tempIdx % $len;
                $str = $charset[$charIndex] . $str; // prepend
                $tempIdx = intdiv($tempIdx, $len);
            }
            
            // Test crypt
            $hash = crypt($str, $salt);
            if (isset($targetSet[$hash])) {
                echo "[Worker $workerId] GEVONDEN: input='$str' hash='$hash'\n";
                exit(0);
            }
        }
    }
}
