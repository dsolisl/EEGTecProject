CREATE DATABASE  IF NOT EXISTS `SignalData`;
USE `SignalData`;

CREATE TABLE IF NOT EXISTS data (
    id INT AUTO_INCREMENT,
    channel_1 float,
    channel_2 float,
    channel_3 float,
	channel_4 float,
    time DATE,
    timestamp timestamp,
    PRIMARY KEY (id)
);

select * from data;

select count(channel_1) from data;
