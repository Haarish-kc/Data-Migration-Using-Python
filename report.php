<?php
$total_records = 0;
$success_count = 0;
$fail_count = 0;

$filename = "result.txt";

if (file_exists($filename)) {
    $lines = file($filename, FILE_IGNORE_NEW_LINES);
    
    foreach ($lines as $line) {
        list($key, $value) = explode("=", $line);
        if ($key == "total_records") $total_records = (int)$value;
        if ($key == "success_count") $success_count = (int)$value;
        if ($key == "fail_count") $fail_count = (int)$value;
    }
    
    unlink($filename);
}
?>

<html>
<head>
    <title>Automation Results</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .container { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; box-shadow: 0px 0px 10px #ccc; }
        h1 { color: #333; }
        .success { color: green; }
        .fail { color: red; }
    </style>
</head>
<body>

<div class="container">
    <h1>Automation Results</h1>
    <p><strong>Total Records Processed:</strong> <?php echo $total_records; ?></p>
    <p class="success"><strong>Successful Inserts:</strong> <?php echo $success_count; ?></p>
    <p class="fail"><strong>Failed Inserts:</strong> <?php echo $fail_count; ?></p>
    
</div>

</body>
</html>
