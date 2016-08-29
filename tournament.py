#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect(database = "tournament")
    except:
        print("Connection failed")

@contextmanager
def GetCursor():
    """Helper function to get a psycopg2 cursor"""
    Database = connect()
    Cursor = Database.cursor()
    try:
        yield Cursor
    except:
        raise
    else:
        Database.commit()
    finally:
        Cursor.close()
        Database.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with GetCursor() as Cursor:
        Cursor.execute("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with GetCursor() as Cursor:
        Cursor.execute("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""
    with GetCursor() as Cursor:
        Cursor.execute("SELECT COUNT(ID) FROM players;")
        Result = Cursor.fetchone()
        Count = int(Result[0])

        return Count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    Command = "INSERT INTO players (NAME) VALUES (%s)"
    Data = (name, )

    with GetCursor() as Cursor:
        Cursor.execute(Command, Data)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    with GetCursor() as Cursor:
        Cursor.execute("SELECT * FROM standings")
        Result = Cursor.fetchall()

        return Result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    Command = "INSERT INTO matches (ID_WINNER, ID_LOSER) VALUES (%s, %s)"
    Data = (winner, loser, )

    with GetCursor() as Cursor:
        Cursor.execute(Command, Data)
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    Result = []
    Players = playerStandings()
    for Index in range(0, len(Players), 2):
        Result.append((Players[Index][0], Players[Index][1], Players[Index + 1][0], Players[Index + 1][1]))

    return Result

    


