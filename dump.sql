CREATE TABLE `flights` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `iata_from` varchar(64) NOT NULL, // код ап отправления
  `iata_to` varchar(64) NOT NULL,
  `line` varchar(255) NOT NULL, // рейс
  `day_1` int(1) NOT NULL DEFAULT 1, // флаги курсирования по дням недели
  `day_2` int(1) NOT NULL DEFAULT 1,
  `day_3` int(1) NOT NULL DEFAULT 1,
  `day_4` int(1) NOT NULL DEFAULT 1,
  `day_5` int(1) NOT NULL DEFAULT 1,
  `day_6` int(1) NOT NULL DEFAULT 1,
  `day_7` int(1) NOT NULL DEFAULT 1,
  `valid_from` datetime NOT NULL, // когда это расписание актуально
  `valid_to` datetime NOT NULL,
  `departure_loc` int(11) NOT NULL, // время отправления в минутах в часовом поясе места отправления
  `arrival_loc` int(11) NOT NULL,
  `departure` int(11) NOT NULL,
  `arrival` int(11) NOT NULL,
  `departure_gdelta` int(11) NOT NULL, // часовой пояс в минутах
  `arrival_gdelta` int(11) NOT NULL,
  `duration` int(11) NOT NULL, // время в пути в минутах
  `codeshares` varchar(255) NOT NULL DEFAULT '""',
  `aircraft_type` varchar(255) NOT NULL DEFAULT '""',
  `source` varchar(255) NOT NULL, // источник расписания, например 'OAG'
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
