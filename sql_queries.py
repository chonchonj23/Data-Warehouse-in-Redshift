import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN = config.get("IAM_ROLE","ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    EventLog_id INT IDENTITY,
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender VARCHAR,
    iteminSession INTEGER,
    lastName VARCHAR,
    length DOUBLE PRECISION,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    sessionID BIGINT,
    song VARCHAR,
    status INTEGER,
    ts VARCHAR,
    userAgent VARCHAR,
    userID VARCHAR,
    PRIMARY KEY (EventLog_id))
""")


staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    artist_id VARCHAR,
    artist_latitude DOUBLE PRECISION,
    artist_location VARCHAR,
    artist_longitude DOUBLE PRECISION,
    artist_name VARCHAR,
    duration DOUBLE PRECISION,
    num_songs INTEGER,
    song_id VARCHAR,
    title VARCHAR,
    year INTEGER )
""")


songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INT IDENTITY, 
    start_time TIMESTAMP NOT NULL, 
    user_id varchar NOT NULL, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int NOT NULL, 
    location varchar, 
    user_agent varchar,
    PRIMARY KEY (songplay_id) )
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id varchar PRIMARY KEY, 
    first_name varchar, 
    last_name varchar, 
    gender varchar,
    level varchar )
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY, 
    title varchar, 
    artist_id varchar, 
    year int, 
    duration float )
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY,  
    name varchar, 
    location varchar, 
    latitude float, 
    longitude float )
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
    start_time TIMESTAMP PRIMARY KEY, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int )
""")



# STAGING TABLES

staging_events_copy = ("""
copy staging_events from 's3://udacity-dend/log_data' 
credentials 'aws_iam_role={}'
json 's3://udacity-dend/log_json_path.json';
""").format(ARN)


staging_songs_copy = ("""
copy staging_songs from 's3://udacity-dend/song_data' 
credentials 'aws_iam_role={}'
json 'auto'
;
""").format(ARN)


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
SELECT  
    timestamp 'epoch' + se.ts/1000 * interval '1 second',
    se.userID, 
    se.level, 
    ss.song_id,
    ss.artist_id, 
    se.sessionID,
    se.location, 
    se.userAgent
FROM staging_events se, staging_songs ss
WHERE se.page = 'NextSong' 
AND se.artist = ss.artist_name 
AND se.song = ss.title 
AND se.length = ss.duration
""")


user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT userId, firstName, lastName, gender, level
FROM staging_events   
""")


song_table_insert = ("""
INSERT INTO SONGS (song_id, title, artist_id, year, duration)
SELECT song_id, title, artist_id, year, duration
FROM staging_songs
""")


artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs
""")


time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
SELECT start_time, 
    extract(hour from start_time),
    extract(day from start_time),
    extract(week from start_time), 
    extract(month from start_time),
    extract(year from start_time), 
    extract(dayofweek from start_time)
FROM songplays
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
