CREATE DATABASE PRUEBA_INGESTA;
USE PRUEBA_INGESTA;

-- get the folder that has permissions to ingest data in csv format
SELECT @@global.secure_file_priv;
SHOW VARIABLES LIKE "secure_file_priv";


/*importing the tables*/

-- Table 'drivers' 
DROP TABLE IF EXISTS `drivers`;
CREATE TABLE IF NOT EXISTS `drivers` (
  	`driverId` 		INTEGER NOT NULL,
  	`code` 			VARCHAR(10),
  	`year` 			INTEGER,
    `nationality`	VARCHAR(30),
    `date_race` 	DATE,
    `Name_driver` 	VARCHAR(30),
  	`Number` 		DECIMAL(10,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;	

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\drivers_mydb.csv'
INTO TABLE `drivers` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- 

-- Table 'csontructors'
DROP TABLE IF EXISTS `constructors`;
CREATE TABLE IF NOT EXISTS `constructors` (
  	`constructorsId` 			INTEGER NOT NULL,
  	`name_constructor` 			VARCHAR(30),
    `nationality`				VARCHAR(30)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;	

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\constructors_mydb.csv'
INTO TABLE `constructors` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- 

-- Table 'pits'
DROP TABLE IF EXISTS `pits`;
CREATE TABLE `pits` (
  `pitsId` 			INTEGER,
  `raceId` 			INTEGER,
  `driverId` 		INTEGER,
  `stop` 			INTEGER,
  `lap` 			INTEGER,
  `time` 			time,
  `duration` 		time,
  `milliseconds`	INTEGER
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\pits_mydb.csv'
INTO TABLE `pits` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
--

-- Table 'circuits'
DROP TABLE IF EXISTS `circuits`;
CREATE TABLE `circuits` (
  `circuitsId` 			INTEGER NOT NULL,
  `name` 				VARCHAR(40),
  `location` 			VARCHAR(30),
  `country` 			VARCHAR(30),
  `latitude` 			DECIMAL(15,6),
  `length` 				DECIMAL(15,6),
  `altitude` 			INTEGER
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\circuits_mydb.csv'
INTO TABLE `circuits` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- 

-- Table 'circuits'
DROP TABLE IF EXISTS `races`;
CREATE TABLE `races` (
  `raceId` 				INTEGER NOT NULL,
  `year_race` 			INTEGER,
  `round` 				INTEGER,
  `circuitId` 			INTEGER,
  `name_race` 			VARCHAR(40),
  `date_race` 			DATE,
  `time_race` 			TIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\races_mydb.csv'
INTO TABLE `races` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- 

-- Table 'results'
DROP TABLE IF EXISTS `results`;
CREATE TABLE `results` (
  `General_Index` 		INTEGER NOT NULL,
  `constructorId` 		INTEGER,
  `driverId` 			INTEGER,
  `fastestLap` 			INTEGER,
  `fastestLapSpeed` 	DECIMAL(7,3),
  `fastestLapTime` 		TIME,
  `grid` 				INTEGER,
  `laps` 				INTEGER,
  `milliseconds` 		INTEGER,
  `number` 				DECIMAL(7,3),
  `Points` 				INTEGER,
  `Position` 			INTEGER,
  `PositionOrder` 		INTEGER,
  `PositionText` 		VARCHAR(10),
  `raceId`		 		INTEGER,
  `rank` 				INTEGER,
  `resultId` 			INTEGER,
  `status` 				INTEGER,
  `time_lap` 			text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\results_mydb.csv'
INTO TABLE `results` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- 

-- Table 'qualifying'
DROP TABLE IF EXISTS `qualifying`;
CREATE TABLE `qualifying` (
  `qualifyId`		INTEGER NOT NULL,
  `raceId` 			INTEGER,
  `driverId` 		INTEGER,
  `ConstructorId` 	INTEGER,
  `number` 			INTEGER,
  `position` 		INTEGER,
  `q1` 				time,
  `q2` 				time,
  `q3` 				time
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\qualifying_mydb.csv'
INTO TABLE `qualifying` 
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- 

/* Queries for the API */

-- 1. Year with the most races
SELECT 	count(*) 	as Cantidad_Carreras,
		year_race	as Año
FROM races
group by year_race
order by Cantidad_Carreras desc
LIMIT 1;

-- 2. Driver with the most first places
SELECT 	count(*) as Cantidad_Carreras, 
		r.driverId,
        d.Name_driver
FROM results as r 
JOIN drivers as d	ON (r.driverId = d.driverId)
WHERE PositionOrder = 1
GROUP BY driverId
ORDER BY Cantidad_Carreras DESC
limit 1;

-- 3. Name of the most traveled circuit
SELECT 	count(*) as Cantidad_Veces,
		r.circuitId,
        c.name,
        c.location,
        c.country
FROM races as r
JOIN circuits as c ON (r.circuitId = c.circuitsId)
GROUP BY circuitId
ORDER BY Cantidad_Veces DESC
LIMIT 1;

-- Driver with the highest number of points in total, whose constructor 
-- is of American or British nationality
SELECT 	sum(r.points) as Puntos,
		r.driverId,
        c.constructorsId,
        c.nationality,
        c.name_constructor,
        d.Name_driver
FROM results as r
JOIN constructors as c 	ON (r.constructorId = c.constructorsId)
JOIN drivers as d 	ON (r.driverId = d.driverId)
WHERE c.nationality = "American" or c.nationality = "British"
GROUP BY r.driverId
ORDER BY Puntos DESC
LIMIT 1;
