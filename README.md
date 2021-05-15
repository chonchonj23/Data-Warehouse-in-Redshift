#### Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which are JSON data residing inside AWS S3 buckets; data contain logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project, we would perform the role of a data engineer, and create a data warehouse for storing those music data within AWS Redshift cluster.



#### Database Design

The database has a star scheme with one fact table and four dimension tables.

* Fact table: 
1. songplays - records in log data associated with song plays i.e. records with page NextSong
   songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent


* Dimension Tables
1. users - users in the app
   columns in users: user_id, first_name, last_name, gender, level

2. songs - songs in music database
   columns in songs song_id, title, artist_id, year, duration

3. artists - artists in music database
   columns in artists: artist_id, name, location, latitude, longitude

4. time - timestamps of records in songplays broken down into specific units
   columns in time: start_time, hour, day, week, month, year, weekday


Due to relately simple data structure of song data (i.e. no or limited many-to-many relationships within data), star schema (instead of snowflake schema) has been chosen for this project.



#### ETL Pipeline Methodology

The challenge of this project is to load two sources of JSON formatted data into the PostgreSQL database within AWS Redshift. 

To do that, we have to perform several steps:

1. Sign up an AWS account
2. Create an AWS user for this project (as it is not a good idea to use root user directly)
3. Launch a Redshift Cluster (either manually or programmatically via Boto3)
4. Grant the Redshift CLuster a role for accessing S3 buckets
5. Create the 5 tables described above (1 fact and 4 dimension tables) as well as two staging tables (one for log and the other for song data) within the PostgreSQL database of Redshift cluster
6. Copy the log and song data from S3 into the two staging tables in Redshift
7. Copy data from the two staging tables into the fact and dimension tables



#### Python programs structure

create_tables.py: this code provides the code structure (i.e. another piece of code would do the actual work) for creating the 5 main tables as well as 2 staging tables; note that this program would first drop all related tables (so that we don't need to worry about what have been down in the past).

sql_queries.py: this code is actually the unsung hero in this project, because it does all the key works for both create_tables.py and etl.py. As an anology, sql_queries.py would do all the hard work without drawing attention, whereas create_tables.py and etl.py would ask direct help from it; in other words, it's like create_tables.py and etl.py are presenting the glorioius results and claiming all credits in meetings, whereas in effect it is sql_queries.py doing all the major works.

sql_queries.py contains all the codes for dropping tables, creating tables, copying data from S3 into staging tables, as well as copying data from staging tables into the 5 main tables.

etl.py: this code provides the code structure for extracting, transforming and loading JSON data for the project; again, it is sql_queries.py that actually does the hard work behind the scene.



#### Software Requirements

Below softwares have been used in this project:

* Python version 3.6.3 
* Psycopg2 verion 2.7.4 
* Boto3 version 1.9.7
