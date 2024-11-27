INSERT INTO `musiclibrarydb`.`genres` (`genre_alias`, `genre_name`) VALUES
('kpop', 'K-Pop');

INSERT INTO `musiclibrarydb`.`accounts` (`username`, `email`, `password`, `created_at`) VALUES
('loona_official', 'loona@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('ateez_official', 'ateez@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('triples_official', 'triples@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('newjeans_ador', 'newjeans@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('aespa_official', 'aespa@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('seventeen_official', 'seventeen@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('bts_official', 'bts@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('blackpink_official', 'blackpink@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('twice_official', 'twice@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('redvelvet_official', 'redvelvet@gmail.com', 'securepassword123', CURRENT_TIMESTAMP),
('got7_official', 'got7@gmail.com', 'securepassword123', CURRENT_TIMESTAMP);

INSERT INTO `musiclibrarydb`.`artists` (`artist_id`, `email`, `name`, `created_at`) VALUES
(1, 'loona@gmail.com', 'LOONA', CURRENT_TIMESTAMP),
(2, 'ateez@gmail.com', 'ATEEZ', CURRENT_TIMESTAMP),
(3, 'triples@gmail.com', 'tripleS', CURRENT_TIMESTAMP),
(4, 'newjeans@gmail.com', 'NewJeans', CURRENT_TIMESTAMP),
(5, 'aespa@gmail.com', 'aespa', CURRENT_TIMESTAMP),
(6, 'seventeen@gmail.com', 'SEVENTEEN', CURRENT_TIMESTAMP),
(7, 'bts@gmail.com', 'BTS', CURRENT_TIMESTAMP),
(8, 'blackpink@gmail.com', 'BLACKPINK', CURRENT_TIMESTAMP),
(9, 'twice@gmail.com', 'TWICE', CURRENT_TIMESTAMP),
(10, 'redvelvet@gmail.com', 'Red Velvet', CURRENT_TIMESTAMP),
(11, 'got7@gmail.com', 'GOT7', CURRENT_TIMESTAMP);


INSERT INTO `musiclibrarydb`.`albums` (`album_id`, `title`, `album_type`, `album_duration`, `created_at`) VALUES
(1, '++', 'Mini Album', '00:23:45', CURRENT_TIMESTAMP),
(2, '[12:00]', 'Full Album', '00:38:56', CURRENT_TIMESTAMP),
(3, 'TREASURE EP.1', 'Mini Album', '00:25:15', CURRENT_TIMESTAMP),
(4, 'ZERO: FEVER Part.2', 'Mini Album', '00:28:30', CURRENT_TIMESTAMP),
(5, 'ASSEMBLE', 'Mini Album', '00:22:10', CURRENT_TIMESTAMP),
(6, 'OMG', 'Single', '00:10:12', CURRENT_TIMESTAMP),
(7, 'Girls', 'Mini Album', '00:20:45', CURRENT_TIMESTAMP),
(8, 'Sector 17', 'Repackage Album', '00:31:25', CURRENT_TIMESTAMP),
(9, 'Wings', 'Full Album', '00:43:28', CURRENT_TIMESTAMP),       -- BTS
(10, 'The Album', 'Full Album', '00:34:50', CURRENT_TIMESTAMP), -- BLACKPINK
(11, 'Formula of Love', 'Full Album', '00:46:33', CURRENT_TIMESTAMP), -- TWICE
(12, 'The ReVe Festival Finale', 'Full Album', '00:36:12', CURRENT_TIMESTAMP), -- Red Velvet
(13, 'Present: YOU', 'Full Album', '00:42:17', CURRENT_TIMESTAMP); -- GOT7


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
(19, 'Darl+ing', '00:03:45', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- BTS
(20, 'Blood Sweat & Tears', '00:03:37', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(21, 'Spring Day', '00:04:35', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- BLACKPINK
(22, 'How You Like That', '00:03:01', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(23, 'Lovesick Girls', '00:03:12', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- TWICE
(24, 'Scientist', '00:03:14', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(25, 'The Feels', '00:03:19', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- Red Velvet
(26, 'Psycho', '00:03:32', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(27, 'Zimzalabim', '00:03:10', 'kpop', CURRENT_TIMESTAMP, 0, 0),

-- GOT7
(28, 'Lullaby', '00:03:34', 'kpop', CURRENT_TIMESTAMP, 0, 0),
(29, 'You Calling My Name', '00:03:28', 'kpop', CURRENT_TIMESTAMP, 0, 0);

INSERT INTO musiclibrarydb.albumssongs (song_id, album_id) VALUES
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
(19, 8),

-- BTS
(20, 9), -- Blood Sweat & Tears -> Wings
(21, 9), -- Spring Day -> Wings

-- BLACKPINK
(22, 10), -- How You Like That -> The Album
(23, 10), -- Lovesick Girls -> The Album

-- TWICE
(24, 11), -- Scientist -> Formula of Love
(25, 11), -- The Feels -> Formula of Love

-- Red Velvet
(26, 12), -- Psycho -> The ReVe Festival Finale
(27, 12), -- Zimzalabim -> The ReVe Festival Finale

-- GOT7
(28, 13), -- Lullaby -> Present: YOU
(29, 13); -- You Calling My Name -> Present: YOU

INSERT INTO musiclibrarydb.songsartists (song_id, artist_id) VALUES
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
(19, 6),

-- BTS
(20, 7), -- Blood Sweat & Tears -> BTS
(21, 7), -- Spring Day -> BTS

-- BLACKPINK
(22, 8), -- How You Like That -> BLACKPINK
(23, 8), -- Lovesick Girls -> BLACKPINK

-- TWICE
(24, 9), -- Scientist -> TWICE
(25, 9), -- The Feels -> TWICE

-- Red Velvet
(26, 10), -- Psycho -> Red Velvet
(27, 10), -- Zimzalabim -> Red Velvet

-- GOT7
(28, 11), -- Lullaby -> GOT7
(29, 11); -- You Calling My Name -> GOT7

INSERT INTO musiclibrarydb.albumsartists (artist_id, album_id) VALUES
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
(6, 8),  -- SEVENTEEN -> Sector 17

(7, 9),  -- BTS -> Wings
(8, 10), -- BLACKPINK -> The Album
(9, 11), -- TWICE -> Formula of Love
(10, 12), -- Red Velvet -> The ReVe Festival Finale
(11, 13); -- GOT7 -> Present: YOU

INSERT INTO `musiclibrarydb`.`playlists` (`playlist_id`, `name`, `created_at`, `email`, `playlist_views`) VALUES
(1, 'K-Pop Hits', CURRENT_TIMESTAMP, 'guest@gmail.com', 1200),
(2, '3rd Gen Favorites', CURRENT_TIMESTAMP, 'guest@gmail.com', 800),
(3, 'Chill Vibes', CURRENT_TIMESTAMP, 'guest@gmail.com', 600);


INSERT INTO `musiclibrarydb`.`playlistssongs` (`playlist_id`, `song_id`) VALUES
-- K-Pop Hits
(1, 1), -- Hi High
(1, 5), -- Pirate King
(1, 22), -- How You Like That
(1, 20), -- Blood Sweat & Tears

-- 3rd Gen Favorites
(2, 23), -- Lovesick Girls
(2, 24), -- Scientist
(2, 26), -- Psycho
(2, 28), -- Lullaby

-- Chill Vibes
(3, 13), -- Ditto
(3, 15), -- Savage
(3, 21), -- Spring Day
(3, 29); -- You Calling My Name



