-- View all rows in genres
SELECT * FROM musiclibrarydb.genres;

-- View all rows in songs
SELECT * FROM musiclibrarydb.songs;

-- View all rows in accounts
SELECT * FROM musiclibrarydb.accounts;

-- View all rows in artists
SELECT * FROM musiclibrarydb.artists;

-- Join songs and artists to ensure songsartists links them correctly
SELECT sa.song_id, sa.artist_id, s.title AS song_title, a.name AS artist_name
FROM musiclibrarydb.songsartists sa
JOIN musiclibrarydb.songs s ON sa.song_id = s.song_id
JOIN musiclibrarydb.artists a ON sa.artist_id = a.artist_id;

-- View all rows in albums
SELECT * FROM musiclibrarydb.albums;

-- Join albums and songs to ensure albumssongs links them correctly
SELECT asg.album_id, asg.song_id, a.title AS album_title, s.title AS song_title
FROM musiclibrarydb.albumssongs asg
JOIN musiclibrarydb.albums a ON asg.album_id = a.album_id
JOIN musiclibrarydb.songs s ON asg.song_id = s.song_id;

-- Join albums and artists to ensure albumartist links them correctly
SELECT aa.album_id, aa.artist_id, a.title AS album_title, ar.name AS artist_name
FROM musiclibrarydb.albumartist aa
JOIN musiclibrarydb.albums a ON aa.album_id = a.album_id
JOIN musiclibrarydb.artists ar ON aa.artist_id = ar.artist_id;

-- Join playlists and songs to ensure playlistssongs links them correctly
SELECT ps.playlist_id, ps.song_id, p.name AS playlist_name, s.title AS song_title
FROM musiclibrarydb.playlistssongs ps
JOIN musiclibrarydb.playlist p ON ps.playlist_id = p.playlist_id
JOIN musiclibrarydb.songs s ON ps.song_id = s.song_id;

-- Join accounts and songs to ensure accountlikessong links them correctly
SELECT als.account_id, als.song_id, a.username AS account_name, s.title AS song_title
FROM musiclibrarydb.accountlikessong als
JOIN musiclibrarydb.accounts a ON als.account_id = a.account_id
JOIN musiclibrarydb.songs s ON als.song_id = s.song_id;

-- Join accounts and songs to ensure songhistory links them correctly
SELECT sh.account_id, sh.song_id, sh.date_played, a.username AS account_name, s.title AS song_title
FROM musiclibrarydb.songhistory sh
JOIN musiclibrarydb.accounts a ON sh.account_id = a.account_id
JOIN musiclibrarydb.songs s ON sh.song_id = s.song_id;
