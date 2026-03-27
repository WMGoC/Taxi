<?php
header('Content-Type: application/json');

$conn = new mysqli("localhost", "root", "", "taxi_dispatch");

if ($conn->connect_error) {
    die(json_encode(["error" => "Ошибка подключения: " . $conn->connect_error]));
}

// Получаем данные из POST запроса
$ride_id = isset($_POST['ride_id']) ? (int)$_POST['ride_id'] : 0;
$driver_id = isset($_POST['driver_id']) ? (int)$_POST['driver_id'] : 0;

if ($ride_id > 0 && $driver_id > 0) {
    // Обновляем статус заказа и назначаем водителя
    $sql = "UPDATE rides SET driver_id = $driver_id, status = 'assigned' WHERE id = $ride_id";
    
    if ($conn->query($sql) === TRUE) {
        echo json_encode(["success" => true, "message" => "Заказ принят"]);
    } else {
        echo json_encode(["success" => false, "error" => $conn->error]);
    }
} else {
    echo json_encode(["success" => false, "error" => "Неверные параметры"]);
}

$conn->close();
?>