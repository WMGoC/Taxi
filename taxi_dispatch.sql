-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Мар 23 2026 г., 12:35
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `taxi_dispatch`
--

-- --------------------------------------------------------

--
-- Структура таблицы `clients`
--

CREATE TABLE `clients` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `clients`
--

INSERT INTO `clients` (`id`, `full_name`, `phone`) VALUES
(1, 'Александрова Анна', '+7-903-111-11-11'),
(2, 'Борисов Борис', '+7-903-222-22-22'),
(3, 'Владимирова Елена', '+7-903-333-33-33'),
(4, 'Григорьев Григорий', '+7-903-444-44-44'),
(5, 'Дмитриева Мария', '+7-903-555-55-55'),
(6, 'Егоров Егор', '+7-903-666-66-66'),
(7, 'Жукова Наталья', '+7-903-777-77-77'),
(8, 'Зверев Олег', '+7-903-888-88-88');

-- --------------------------------------------------------

--
-- Структура таблицы `dispatchers`
--

CREATE TABLE `dispatchers` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `dispatchers`
--

INSERT INTO `dispatchers` (`id`, `full_name`, `login`, `password`) VALUES
(1, 'Админ Админович', 'admin', '123'),
(2, 'Смирнова Ольга', 'olga', '123');

-- --------------------------------------------------------

--
-- Структура таблицы `drivers`
--

CREATE TABLE `drivers` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `car_model` varchar(100) DEFAULT NULL,
  `car_number` varchar(10) DEFAULT NULL,
  `status` enum('available','on_shift','busy') DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `drivers`
--

INSERT INTO `drivers` (`id`, `full_name`, `phone`, `car_model`, `car_number`, `status`) VALUES
(1, 'Иванов Иван', '+7-916-111-22-33', 'Kia Rio', 'А111АА77', 'available'),
(2, 'Петров Петр', '+7-916-222-33-44', 'Hyundai Solaris', 'В222ВВ77', 'available'),
(3, 'Сидоров Сидор', '+7-916-333-44-55', 'Skoda Rapid', 'С333СС77', 'available'),
(4, 'Кузнецов Александр', '+7-916-444-55-66', 'Volkswagen Polo', 'К444КК77', 'on_shift'),
(5, 'Соколов Денис', '+7-915-111-22-33', 'Kia Optima', 'А888АА77', 'busy');

-- --------------------------------------------------------

--
-- Структура таблицы `rides`
--

CREATE TABLE `rides` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `driver_id` int(11) DEFAULT NULL,
  `dispatcher_id` int(11) NOT NULL,
  `tariff_id` int(11) NOT NULL,
  `start_address` varchar(255) NOT NULL,
  `end_address` varchar(255) NOT NULL,
  `distance_km` decimal(10,2) DEFAULT NULL,
  `total_cost` decimal(10,2) DEFAULT NULL,
  `status` enum('new','assigned','in_progress','completed','cancelled') DEFAULT 'new',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `completed_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `rides`
--

INSERT INTO `rides` (`id`, `client_id`, `driver_id`, `dispatcher_id`, `tariff_id`, `start_address`, `end_address`, `distance_km`, `total_cost`, `status`, `created_at`, `completed_at`) VALUES
(1, 1, NULL, 1, 1, 'ул. Тверская, д. 15', 'Ленинградский вокзал', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(2, 2, NULL, 1, 2, 'Кутузовский пр-т, д. 30', 'Аэропорт Шереметьево', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(3, 3, NULL, 2, 1, 'Ленинский пр-т, д. 45', 'Парк Горького', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(4, 4, NULL, 1, 3, 'Новый Арбат, д. 20', 'Москва-Сити', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(5, 5, NULL, 2, 2, 'Пр-т Мира, д. 50', 'ВДНХ', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(6, 6, NULL, 1, 1, 'ул. Покровка, д. 10', 'Курский вокзал', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(7, 7, NULL, 2, 4, 'Рублевское шоссе, д. 25', 'Сбербанк Арена', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(8, 8, NULL, 1, 3, 'ул. Арбат, д. 35', 'Киевский вокзал', NULL, NULL, 'new', '2026-03-23 11:34:31', NULL),
(9, 5, 1, 1, 2, 'ул. Б. Дмитровка, д. 10', 'Большой театр', NULL, NULL, 'assigned', '2026-03-23 11:34:31', NULL),
(10, 6, 2, 2, 1, 'пр-т Вернадского, д. 70', 'МГУ', NULL, NULL, 'assigned', '2026-03-23 11:34:31', NULL),
(11, 7, 3, 1, 4, 'ул. Профсоюзная, д. 120', 'ТРЦ Калужский', NULL, NULL, 'assigned', '2026-03-23 11:34:31', NULL),
(12, 1, 4, 1, 1, 'ул. Академика Королева, д. 15', 'Останкино', NULL, NULL, 'completed', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(13, 2, 5, 2, 2, 'Ленинградское ш., д. 45', 'Речной вокзал', NULL, NULL, 'completed', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(14, 3, 4, 1, 3, 'ул. 1905 года, д. 10', 'Краснопресненская', NULL, NULL, 'completed', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(15, 4, 5, 2, 1, 'Каширское ш., д. 60', 'Коломенское', NULL, NULL, 'completed', '0000-00-00 00:00:00', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Структура таблицы `tariffs`
--

CREATE TABLE `tariffs` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price_per_km` decimal(10,2) NOT NULL,
  `price_per_minute` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `tariffs`
--

INSERT INTO `tariffs` (`id`, `name`, `price_per_km`, `price_per_minute`) VALUES
(1, 'Эконом', 15.00, 5.00),
(2, 'Комфорт', 25.00, 8.00),
(3, 'Бизнес', 40.00, 12.00),
(4, 'Минивэн', 35.00, 10.00);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `dispatchers`
--
ALTER TABLE `dispatchers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`);

--
-- Индексы таблицы `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `car_number` (`car_number`);

--
-- Индексы таблицы `rides`
--
ALTER TABLE `rides`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `driver_id` (`driver_id`),
  ADD KEY `dispatcher_id` (`dispatcher_id`),
  ADD KEY `tariff_id` (`tariff_id`);

--
-- Индексы таблицы `tariffs`
--
ALTER TABLE `tariffs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `dispatchers`
--
ALTER TABLE `dispatchers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `drivers`
--
ALTER TABLE `drivers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `rides`
--
ALTER TABLE `rides`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT для таблицы `tariffs`
--
ALTER TABLE `tariffs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `rides`
--
ALTER TABLE `rides`
  ADD CONSTRAINT `rides_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`),
  ADD CONSTRAINT `rides_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`),
  ADD CONSTRAINT `rides_ibfk_3` FOREIGN KEY (`dispatcher_id`) REFERENCES `dispatchers` (`id`),
  ADD CONSTRAINT `rides_ibfk_4` FOREIGN KEY (`tariff_id`) REFERENCES `tariffs` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
