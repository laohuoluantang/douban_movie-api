CREATE TABLE IF NOT EXISTS `movie_messages`(
   `movie_id` BIGINT UNSIGNED AUTO_INCREMENT,
   `title` VARCHAR(100),
   `imageurl` VARCHAR(100),
   `rate` VARCHAR(20),
   `report` text,
   `looked` BIGINT UNSIGNED,
   `wantlook` BIGINT UNSIGNED,
   PRIMARY KEY ( `movie_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;