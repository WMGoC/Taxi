<?php
header('Content-Type: application/json');

// Подключение к базе данных
$conn = new mysqli("localhost", "root", "", "taxi_dispatch");

// Проверка подключения
if ($conn->connect_error) {
    die(json_encode(["error" => "Ошибка подключения: " . $conn->connect_error]));
}

// Запрос к базе данных
$result = $conn->query("SELECT id, full_name, car_number FROM drivers");

$data = [];
while($row = $result->fetch_assoc()) {
    $data[] = $row;
}

// Возвращаем данные в формате JSON
echo json_encode($data);

// Закрываем соединение
$conn->close();
?>