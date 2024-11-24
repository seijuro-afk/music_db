INSERT INTO `musiclibrarydb`.`genres` (`genre_alias`, `genre_name`) VALUES
('kpop', 'K-Pop'),
('none', 'None');

SELECT * FROM `musiclibrarydb`.`genres`;

INSERT INTO `musiclibrarydb`.`accounts` (`username`, `email`, `password`, `created_at`) VALUES
('loona_official', 'loona@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('ateez_official', 'ateez@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('triples_official', 'triples@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('newjeans_ador', 'newjeans@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('aespa_official', 'aespa@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('seventeen_official', 'seventeen@gmail.com', 'securepassword123', CURRENT_TIMESTAMP);

INSERT INTO `musiclibrarydb`.`artists` (`email`, `name`) VALUES
('loona@gmail.com', 'LOONA'),
('ateez@gmail.com', 'ATEEZ'),
('triples@gmail.com', 'tripleS'),
('newjeans@gmail.com', 'NewJeans'),
('aespa@gmail.com', 'aespa'),
('seventeen@gmail.com', 'SEVENTEEN');

INSERT INTO `musiclibrarydb`.`albums` (`album_id`, `title`, `album_type`, `album_duration`, `created_at`) VALUES
(1, '++', 'Mini Album', '00:23:45', CURRENT_TIMESTAMP),
(2, '[12:00]', 'Full Album', '00:38:56', CURRENT_TIMESTAMP),
(3, 'TREASURE EP.1', 'Mini Album', '00:25:15', CURRENT_TIMESTAMP),
(4, 'ZERO: FEVER Part.2', 'Mini Album', '00:28:30', CURRENT_TIMESTAMP),
(5, 'ASSEMBLE', 'Mini Album', '00:22:10', CURRENT_TIMESTAMP),
(6, 'OMG', 'Single', '00:10:12', CURRENT_TIMESTAMP),
(7, 'Girls', 'Mini Album', '00:20:45', CURRENT_TIMESTAMP),
(8, 'Sector 17', 'Repackage Album', '00:31:25', CURRENT_TIMESTAMP);

INSERT INTO `musiclibrarydb`.`songs` (`song_id`, `title`, `song_duration`, `genre`, `created_at`, `song_likes`, `song_streams`) VALUES
-- LOONA
(1, 'Hi High', '00:03:18', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(2, 'Favorite', '00:03:14', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(3, 'Why Not?', '00:03:25', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(4, 'Voice', '00:03:40', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- ATEEZ
(5, 'Pirate King', '00:03:15', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(6, 'Treasure', '00:03:23', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(7, 'Fireworks (I’m The One)', '00:03:33', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(8, 'Celebrate', '00:03:50', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- tripleS
(9, 'Rising', '00:03:22', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(10, 'Beam', '00:03:18', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- NewJeans
(11, 'Attention', '00:03:13', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(12, 'Hype Boy', '00:03:04', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(13, 'Ditto', '00:03:01', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- aespa
(14, 'Black Mamba', '00:03:20', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(15, 'Savage', '00:03:58', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(16, 'Illusion', '00:03:30', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- SEVENTEEN
(17, 'HOT', '00:03:15', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(18, '_World', '00:03:21', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(19, 'Darl+ing', '00:03:45', 'kpop', CURRENT_TIMESTAMP, 0, 0);

INSERT INTO `musiclibrarydb`.`albumssongs` (`song_id`, `album_id`) VALUES
-- LOONA
(1, 1),
(2, 1),
(3, 2),
(4, 2),

-- ATEEZ
(5, 3),
(6, 3),
(7, 4),
(8, 4),

-- tripleS
(9, 5),
(10, 5),

-- NewJeans
(11, 6),
(12, 6),
(13, 6),

-- aespa
(14, 7),
(15, 7),
(16, 7),

-- SEVENTEEN
(17, 8),
(18, 8),
(19, 8);

INSERT INTO `musiclibrarydb`.`songsartists` (`song_id`, `artist_id`) VALUES
-- LOONA
(1, 1),
(2, 1),
(3, 1),
(4, 1),

-- ATEEZ
(5, 2),
(6, 2),
(7, 2),
(8, 2),

-- tripleS
(9, 3),
(10, 3),

-- NewJeans
(11, 4),
(12, 4),
(13, 4),

-- aespa
(14, 5),
(15, 5),
(16, 5),

-- SEVENTEEN
(17, 6),
(18, 6),
(19, 6);

INSERT INTO `musiclibrarydb`.`albumartist` (`artist_id`, `album_id`) VALUES
-- LOONA
(1, 1),  -- LOONA -> ++
(1, 2),  -- LOONA -> [12:00]

-- ATEEZ
(2, 3),  -- ATEEZ -> TREASURE EP.1
(2, 4),  -- ATEEZ -> ZERO: FEVER Part.2

-- tripleS
(3, 5),  -- tripleS -> ASSEMBLE

-- NewJeans
(4, 6),  -- NewJeans -> OMG

-- aespa
(5, 7),  -- aespa -> Girls

-- SEVENTEEN
(6, 8);  -- SEVENTEEN -> Sector 17
