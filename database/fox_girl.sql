
CREATE TABLE `object` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `rating` tinytext NOT NULL,
  `md5_hash` char(32) NOT NULL
);


CREATE TABLE `obj_to_tag` (
  `tag` int,
  `object` int,
  PRIMARY KEY (`tag`, `object`)
);

CREATE TABLE `tag` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL
);



CREATE TABLE `time_file` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `time_file` timestamp UNIQUE NOT NULL
);

CREATE TABLE `file_url` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_object` int NOT NULL,
  `file_width` int NOT NULL,
  `file_height` int NOT NULL,
  `url` longTEXT NOT NULL,
  `hash_url` varchar(255) UNIQUE NOT NULL,
  `file_ext` char(8) NOT NULL
  `id_update_at` int NOT NULL,
  `id_create_at` int NOT NULL
);

ALTER TABLE object ADD UNIQUE (md5_hash);

ALTER TABLE tag ADD UNIQUE (name);

ALTER TABLE file_url ADD UNIQUE (hash_url);

ALTER TABLE time_file ADD UNIQUE (time_file);

ALTER TABLE `obj_to_tag` ADD FOREIGN KEY (`tag`) REFERENCES `tag` (`id`);

ALTER TABLE `obj_to_tag` ADD FOREIGN KEY (`object`) REFERENCES `object` (`id`);

ALTER TABLE `file_url` ADD FOREIGN KEY (`id_object`) REFERENCES `object` (`id`);


ALTER TABLE `file_url` ADD FOREIGN KEY (`id_update_at`) REFERENCES `time_file` (`id`);

ALTER TABLE `file_url` ADD FOREIGN KEY (`id_create_at`) REFERENCES `time_file` (`id`);