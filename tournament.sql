-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;

CREATE DATABASE tournament;

\c tournament

DROP TABLE players CASCADE;
DROP TABLE matches CASCADE;

-- Create table for players
CREATE TABLE players(
   ID SERIAL,
   NAME TEXT,
   PRIMARY KEY( ID )
);

-- Create table for matches
CREATE TABLE matches(
    ID_MATCH SERIAL,
    ID_WINNER INTEGER NULL REFERENCES players(ID),
    ID_LOSER INTEGER NULL REFERENCES players(ID),
    PRIMARY KEY (ID_MATCH)
);

-- Create a view to count all the wins of one player
CREATE VIEW countwins AS
    SELECT players.ID AS ID, players.NAME AS NAME, COUNT(matches.ID_WINNER) AS RECORD
    FROM players LEFT JOIN matches ON players.ID = matches.ID_WINNER
    GROUP BY players.ID;

-- Create a view of all the matches a player has played
CREATE VIEW countmatches AS
    SELECT players.ID AS ID, players.NAME AS NAME, COUNT(matches.ID_MATCH) AS PLAYS
    FROM players LEFT JOIN matches ON players.ID = matches.ID_WINNER OR players.ID = matches.ID_LOSER
    GROUP BY players.ID;

-- Create a view of standings of all players
 CREATE VIEW standings AS
    SELECT countmatches.ID AS PLAYER_ID, countmatches.NAME AS PLAYER_NAME,
    countwins.RECORD AS WINS, countmatches.PLAYS AS MATCHES_PLAYED
    FROM countmatches 
    LEFT JOIN countwins
    ON countwins.ID = countmatches.ID
    ORDER BY WINS DESC;

-- Create a view of a swiss pairing
-- CREATE VIEW swisspairing AS
--     SELECT DISTINCT PAIR_ONE.PLAYER_ID AS PLAYER_ONE_ID, PAIR_ONE.PLAYER_NAME AS PLAYER_ONE_NAME, 
--     PAIR_TWO.PLAYER_ID AS PLAYER_TWO_ID, PAIR_TWO.PLAYER_NAME AS PLAYER_TWO_NAME
--     FROM standings PAIR_ONE INNER JOIN standings PAIR_TWO 
--     ON PAIR_ONE.PLAYER_ID != PAIR_TWO.PLAYER_ID AND PAIR_ONE.WINS >= PAIR_TWO.WINS
--     WHERE PAIR_ONE.WINS >= PAIR_TWO.WINS;