-- MySQL Script generated by MySQL Workbench
-- Fri Nov 22 23:29:30 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema musiclibrarydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema musiclibrarydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `musiclibrarydb` DEFAULT CHARACTER SET utf8 ;
USE `musiclibrarydb` ;

-- -----------------------------------------------------
-- Table `musiclibrarydb`.`genre`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`genres` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`genres` (
  `genre_alias` VARCHAR(10) NOT NULL,
  `genre_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`genre_alias`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`songs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`songs` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`songs` (
  `song_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL DEFAULT 'untitled',
  `song_duration` TIME NOT NULL DEFAULT '00:00:00',
  `genre` VARCHAR(10) NOT NULL DEFAULT 'none',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `song_likes` INT NOT NULL DEFAULT 0,
  `song_streams` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`song_id`),
  INDEX `fk_songs_genre1_idx` (`genre` ASC) VISIBLE,
  CONSTRAINT `fk_songs_genre1`
    FOREIGN KEY (`genre`)
    REFERENCES `musiclibrarydb`.`genres` (`genre_alias`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`account`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`accounts` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`accounts` (
  `account_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`artists`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`artists` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`artists` (
  `artist_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(200) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`artist_id`),
  INDEX `fk_artists_account1_idx` (`email` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) INVISIBLE,
  CONSTRAINT `fk_artists_account1`
    FOREIGN KEY (`email`)
    REFERENCES `musiclibrarydb`.`accounts` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`songsartists`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`songsartists` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`songsartists` (
  `song_id` INT NOT NULL,
  `artist_id` INT NOT NULL,
  PRIMARY KEY (`song_id`, `artist_id`),
  INDEX `fk_songsartists_artists1_idx` (`artist_id` ASC) VISIBLE,
  CONSTRAINT `fk_songsartists_songs`
    FOREIGN KEY (`song_id`)
    REFERENCES `musiclibrarydb`.`songs` (`song_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_songsartists_artists1`
    FOREIGN KEY (`artist_id`)
    REFERENCES `musiclibrarydb`.`artists` (`artist_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`albums`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`albums` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`albums` (
  `album_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL DEFAULT 'untitled',
  `album_type` VARCHAR(45) NOT NULL DEFAULT 'none',
  `album_duration` TIME NOT NULL DEFAULT '00:00:00',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`album_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`albumssongs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`albumssongs` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`albumssongs` (
  `song_id` INT NOT NULL,
  `album_id` INT NOT NULL,
  PRIMARY KEY (`song_id`, `album_id`),
  INDEX `fk_albumssongs_album1_idx` (`album_id` ASC) VISIBLE,
  CONSTRAINT `fk_albumssongs_songs1`
    FOREIGN KEY (`song_id`)
    REFERENCES `musiclibrarydb`.`songs` (`song_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_albumssongs_album1`
    FOREIGN KEY (`album_id`)
    REFERENCES `musiclibrarydb`.`albums` (`album_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`albumartist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`albumartist` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`albumartist` (
  `artist_id` INT NOT NULL,
  `album_id` INT NOT NULL,
  PRIMARY KEY (`artist_id`, `album_id`),
  INDEX `fk_albumartist_album1_idx` (`album_id` ASC) VISIBLE,
  CONSTRAINT `fk_albumartist_artists1`
    FOREIGN KEY (`artist_id`)
    REFERENCES `musiclibrarydb`.`artists` (`artist_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_albumartist_album1`
    FOREIGN KEY (`album_id`)
    REFERENCES `musiclibrarydb`.`albums` (`album_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`playlist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`playlist` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`playlist` (
  `playlist_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL DEFAULT 'untitled',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` VARCHAR(200) NOT NULL,
  `playlist_views` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`playlist_id`),
  INDEX `fk_playlist_account1_idx` (`email` ASC) VISIBLE,
  CONSTRAINT `fk_playlist_account1`
    FOREIGN KEY (`email`)
    REFERENCES `musiclibrarydb`.`accounts` (`email`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`playlistssongs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`playlistssongs` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`playlistssongs` (
  `playlist_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`playlist_id`, `song_id`),
  INDEX `fk_playlistssongs_songs1_idx` (`song_id` ASC) VISIBLE,
  CONSTRAINT `fk_playlistssongs_playlist1`
    FOREIGN KEY (`playlist_id`)
    REFERENCES `musiclibrarydb`.`playlist` (`playlist_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_playlistssongs_songs1`
    FOREIGN KEY (`song_id`)
    REFERENCES `musiclibrarydb`.`songs` (`song_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`accountlikessong`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`accountlikessong` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`accountlikessong` (
  `account_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`account_id`, `song_id`),
  INDEX `fk_accountlikessong_songs1_idx` (`song_id` ASC) VISIBLE,
  CONSTRAINT `fk_accountlikessong_account1`
    FOREIGN KEY (`account_id`)
    REFERENCES `musiclibrarydb`.`accounts` (`account_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_accountlikessong_songs1`
    FOREIGN KEY (`song_id`)
    REFERENCES `musiclibrarydb`.`songs` (`song_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musiclibrarydb`.`songhistory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `musiclibrarydb`.`songhistory` ;

CREATE TABLE IF NOT EXISTS `musiclibrarydb`.`songhistory` (
  `account_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  `date_played` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`, `song_id`, `date_played`),
  INDEX `fk_songhistory_songs1_idx` (`song_id` ASC) VISIBLE,
  CONSTRAINT `fk_songhistory_account1`
    FOREIGN KEY (`account_id`)
    REFERENCES `musiclibrarydb`.`accounts` (`account_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_songhistory_songs1`
    FOREIGN KEY (`song_id`)
    REFERENCES `musiclibrarydb`.`songs` (`song_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


DELIMITER //

CREATE TRIGGER update_album_duration_after_insert
AFTER INSERT ON albumssongs
FOR EACH ROW
BEGIN
    DECLARE total_duration TIME;

    -- Calculate the total duration of all songs in the album
    SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(song_duration)))
    INTO total_duration
    FROM albumssongs
    JOIN songs ON albumssongs.song_id = songs.song_id
    WHERE albumssongs.album_id = NEW.album_id;

    -- Update the album's duration in the albums table
    UPDATE albums
    SET album_duration = total_duration
    WHERE album_id = NEW.album_id;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER update_album_duration_after_update
AFTER UPDATE ON albumssongs
FOR EACH ROW
BEGIN
    DECLARE total_duration TIME;

    -- Calculate the total duration of all songs in the album
    SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(song_duration)))
    INTO total_duration
    FROM albumssongs
    JOIN songs ON albumssongs.song_id = songs.song_id
    WHERE albumssongs.album_id = NEW.album_id;

    -- Update the album's duration in the albums table
    UPDATE albums
    SET album_duration = total_duration
    WHERE album_id = NEW.album_id;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER update_album_duration_after_delete
AFTER DELETE ON albumssongs
FOR EACH ROW
BEGIN
    DECLARE total_duration TIME;

    -- Calculate the total duration of all songs in the album
    SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(song_duration)))
    INTO total_duration
    FROM albumssongs
    JOIN songs ON albumssongs.song_id = songs.song_id
    WHERE albumssongs.album_id = OLD.album_id;

    -- Update the album's duration in the albums table
    UPDATE albums
    SET album_duration = total_duration
    WHERE album_id = OLD.album_id;
END;
//

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO `musiclibrarydb`.`accounts` (`account_id`, `username`, `email`, `password`) VALUES
(99, 'guest', 'guest@gmail.com', '1234');
