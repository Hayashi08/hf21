DROP DATABASE IF EXISTS hf21_db;

CREATE database hf21_db DEFAULT CHARACTER SET = utf8;

USE hf21_db;

SET NAMES utf8;

CREATE TABLE user_tbl (
	user_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	user_name VARCHAR(32) NOT NULL UNIQUE, 
	password VARCHAR(32) NOT NULL,
	PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE session_tbl (
	session_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	user_id INTEGER UNSIGNED NOT NULL,
	company_name VARCHAR(64) DEFAULT '',
	company_stage VARCHAR(16) DEFAULT '',
	PRIMARY KEY (session_id),
	FOREIGN KEY (user_id) REFERENCES user_tbl (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE result_tbl (
	result_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	session_id INTEGER UNSIGNED NOT NULL,
	result_datetime DATETIME,
	result_time TIME DEFAULT '00:00:00',
	result_total_point TINYINT UNSIGNED DEFAULT 0,
	result_wasoku SMALLINT UNSIGNED DEFAULT 0,
	result_wasoku_point TINYINT UNSIGNED DEFAULT 0,
	result_posture_point TINYINT UNSIGNED DEFAULT 0,
	PRIMARY KEY (result_id),
	FOREIGN KEY (session_id) REFERENCES session_tbl (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE sentence_tbl (
	sentence_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	result_id INTEGER UNSIGNED NOT NULL,
	sentence_str VARCHAR(512),
	sentence_len TINYINT UNSIGNED DEFAULT 0,
	sentence_time TIME DEFAULT '00:00:00',
	sentence_wasoku TINYINT UNSIGNED DEFAULT 0,
	sentence_datetime DATETIME,
	PRIMARY KEY (sentence_id),
	FOREIGN KEY (result_id) REFERENCES result_tbl (result_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE image_tbl (
	image_id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	result_id INTEGER UNSIGNED NOT NULL,
	image_path VARCHAR(64) DEFAULT '',
	image_judge CHAR(1) DEFAULT '0',
	image_datetime DATETIME,
	PRIMARY KEY (image_id),
	FOREIGN KEY (result_id) REFERENCES result_tbl (result_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET NAMES cp932;
