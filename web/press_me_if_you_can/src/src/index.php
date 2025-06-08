<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['submit'])) {
    if (!isset($_SERVER['HTTP_REFERER']) || (isset($_SERVER['HTTP_USER_AGENT']) && str_starts_with($_SERVER['HTTP_USER_AGENT'], "curl"))) {
        die("I saw that you did not press the button, did you? 🍋");
    }
    echo "<script>console.log('Well Done. You can validate this challenge with this flag : N0PS{W3l1_i7_w4S_Ju5T_F0r_Fun}');</script>";
}
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Press me if you can</title>
        <link href="https://fonts.googleapis.com/css2?family=Mouse+Memoirs&amp;display=swap" rel="stylesheet">
        <link rel="stylesheet" href="styles.css">
        <script src="script.js" defer></script>
    </head>
    <body>
    <div id="bg">    
    <div class="eyes-container">
        <div class="eye">
            <div class="pupil"></div>
            <div class="blink"></div>
        </div>
        <div class="eye">
            <div class="pupil"></div>
            <div class="blink"></div>
        </div>
        </div>
    </div>
    <form method="post">
        <button type="submit" name="submit">Press Me</button>
    </form>

    </body>

</html>