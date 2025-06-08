<?php

$backend_host = "backend";

if (isset($_GET['blog'])) {
    # TODO: remove debug feature
    if (str_starts_with($_GET['blog'], 'http://')) {
        if (!str_starts_with($_GET['blog'], 'http://backend')) {
            header('HTTP/1.1 403 Unauthorized');
            echo "<pre><b>Warning</b>: Request should only be sent to <b>backend</b> host.</pre>";
            die();
        }
        $url = $_GET['blog'];
    } else {
        $url = $backend_host . "/" . $_GET['blog'];
    }
    #$url = $backend_host . "/" . $_GET['blog'];
    $ch = curl_init(); 
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_URL, $url);
    $result = curl_exec($ch);
    echo $result;
    curl_close($ch);
}

?>