<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json; charset=utf-8');

$conn = new mysqli("localhost", "root", "", "taxi_dispatch");
$conn->set_charset("utf8");

if ($conn->connect_error) {
    die(json_encode(["error" => "Ошибка подключения: " . $conn->connect_error]));
}

// Получаем параметр status из запроса
$status = isset($_GET['status']) ? $_GET['status'] : 'new';

// Формируем запрос в зависимости от статуса
switch ($status) {
    case 'new':
        $sql = "SELECT r.id, r.start_address, r.end_address, r.status, r.created_at,
                       c.full_name as client_name, c.phone as client_phone,
                       NULL as driver_name, NULL as completed_at
                FROM rides r 
                JOIN clients c ON r.client_id = c.id 
                WHERE r.status = 'new' 
                ORDER BY r.id DESC";
        break;
        
    case 'assigned':
        $sql = "SELECT r.id, r.start_address, r.end_address, r.status, r.created_at,
                       c.full_name as client_name, c.phone as client_phone,
                       d.full_name as driver_name, NULL as completed_at
                FROM rides r 
                JOIN clients c ON r.client_id = c.id 
                LEFT JOIN drivers d ON r.driver_id = d.id 
                WHERE r.status = 'assigned' 
                ORDER BY r.id DESC";
        break;
        
    case 'in_progress':
        $sql = "SELECT r.id, r.start_address, r.end_address, r.status, r.created_at,
                       c.full_name as client_name, c.phone as client_phone,
                       d.full_name as driver_name, NULL as completed_at
                FROM rides r 
                JOIN clients c ON r.client_id = c.id 
                LEFT JOIN drivers d ON r.driver_id = d.id 
                WHERE r.status = 'in_progress' 
                ORDER BY r.id DESC";
        break;
        
    case 'completed':
        $sql = "SELECT r.id, r.start_address, r.end_address, r.status, r.created_at, r.completed_at,
                       c.full_name as client_name, c.phone as client_phone,
                       d.full_name as driver_name
                FROM rides r 
                JOIN clients c ON r.client_id = c.id 
                LEFT JOIN drivers d ON r.driver_id = d.id 
                WHERE r.status = 'completed' 
                ORDER BY r.completed_at DESC LIMIT 50";
        break;
        
    default:
        $sql = "SELECT r.id, r.start_address, r.end_address, r.status, r.created_at,
                       c.full_name as client_name, c.phone as client_phone,
                       NULL as driver_name, NULL as completed_at
                FROM rides r 
                JOIN clients c ON r.client_id = c.id 
                WHERE r.status = 'new' 
                ORDER BY r.id DESC";
}

$result = $conn->query($sql);
$data = [];

if ($result) {
    while($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

echo json_encode($data, JSON_UNESCAPED_UNICODE);
$conn->close();
?>