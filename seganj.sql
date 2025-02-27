-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Фев 27 2025 г., 05:50
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
-- База данных: `seganj`
--

-- --------------------------------------------------------

--
-- Структура таблицы `registrations`
--

CREATE TABLE `registrations` (
  `id` int(11) NOT NULL,
  `chat_id` bigint(20) NOT NULL,
  `car_number` varchar(50) NOT NULL,
  `car_category` varchar(50) DEFAULT NULL,
  `fuel_type` varchar(50) DEFAULT NULL,
  `truck_type` varchar(50) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `user_fuel_type` varchar(50) DEFAULT NULL,
  `card_or_app_status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `registrations`
--

INSERT INTO `registrations` (`id`, `chat_id`, `car_number`, `car_category`, `fuel_type`, `truck_type`, `phone_number`, `full_name`, `user_fuel_type`, `card_or_app_status`) VALUES
(4, 594439967, '4940FF02', 'Маршрутное такси', 'СУГ/ГАЗ', NULL, '927998090', 'Шавкат', 'Дизель', 'Установлено'),
(5, 594439967, '4940FF02', 'Легковое ТС', 'Дизель', NULL, '927998090', 'Шавкат', 'Дизель', 'Установлено'),
(6, 594439967, '4940FF02', 'Грузовое ТС', 'Дизель', 'Лабо', '927998090', 'Шавкат', 'Дизель', 'Установлено'),
(7, 594439967, '4778DO02', 'Маршрутное такси', 'Дизель', NULL, '111110069', 'Косим', 'Дизель', 'Установлено'),
(8, 594439967, '0777VZ01', 'Грузовое ТС', 'Дизель', 'Дулан', '7881316', 'Бекзод', 'Дизель', 'Карта'),
(9, 594439967, '0777VZ01', 'Маршрутное такси', 'Дизель', NULL, '7881316', 'Бекзод', 'Дизель', 'Карта'),
(10, 594439967, '4940FF02', 'Маршрутное такси', 'Дизель', NULL, '927998090', 'Шавкат', 'Дизель', 'Установлено'),
(11, 594439967, '4940FF02', 'Легковое ТС', 'СУГ/ГАЗ', NULL, '927998090', 'Шавкат', 'Дизель', 'Установлено');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `car_number` varchar(50) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `fuel_type` varchar(50) DEFAULT NULL,
  `card_or_app_status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `car_number`, `phone_number`, `full_name`, `fuel_type`, `card_or_app_status`) VALUES
(1, '4940FF02', '927998090', 'Шавкат', 'Дизель', 'Установлено'),
(2, '9030YO02', '929976707', 'Муродчон', 'Дизель', 'Карта'),
(3, '0777VZ01', '7881316', 'Бекзод', 'Дизель', 'Карта'),
(4, '4778DO02', '111110069', 'Косим', 'Дизель', 'Установлено');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `registrations`
--
ALTER TABLE `registrations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `car_number` (`car_number`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `car_number` (`car_number`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `registrations`
--
ALTER TABLE `registrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `registrations`
--
ALTER TABLE `registrations`
  ADD CONSTRAINT `registrations_ibfk_1` FOREIGN KEY (`car_number`) REFERENCES `users` (`car_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
