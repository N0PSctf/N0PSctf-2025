<?php

header("Content-Type: application/json");

$mysql_pass = "6bba23db7f6df87eb215120d86e8ebd8001a695dabafcf8d6ac4b437ab06b716";
$mysql_user = "root";
$mysql_host = "mysql";
$mysql_db = 'blog_db';
$conn = new mysqli($mysql_host, $mysql_user, $mysql_pass, $mysql_db);

$url = parse_url($_SERVER['REQUEST_URI']);
$url = explode('/', trim($url['path'], '/'));
$id = $url[0];

if ($id === 'all') {
    $query = "SELECT blog_posts.id, blog_posts.title, users.username AS name FROM blog_posts JOIN users ON blog_posts.user_id = users.id;";
    $result = $conn->query($query);
    $rows = [];
    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    echo json_encode($rows);
} else if (!is_numeric($id)) {
    echo json_encode(["error" => "Invalid ID"]);
    exit();
} else {
    $stmt = $conn->prepare("SELECT blog_posts.id, blog_posts.title, blog_posts.content, users.username AS name FROM blog_posts JOIN users ON blog_posts.user_id = users.id WHERE blog_posts.id = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    echo json_encode($row);
}

?>