import apsw
from soften import *

conn = apsw.Connection("channel_scores.db")
db = conn.cursor()

def setup():
    """
    Create the tables and so on.
    """
    db.execute("PRAGMA FOREIGN_KEYS = ON;")
    db.execute("PRAGMA JOURNAL_MODE = WAL;")
    db.execute("PRAGMA SYNCHRONOUS = 0;")

    db.execute("BEGIN;")

    db.execute("""CREATE TABLE IF NOT EXISTS channels
(claim_hash        BLOB NOT NULL PRIMARY KEY,
 total_deweys      INTEGER NOT NULL)
WITHOUT ROWID;""")

    # Supports ALSO INCLUDES THE BID, which is treated as a self-support.
    db.execute("""CREATE TABLE IF NOT EXISTS supports
(id           INTEGER NOT NULL PRIMARY KEY,
 from_channel BLOB REFERENCES channels (claim_hash),
 to_channel   BLOB NOT NULL REFERENCES channels (claim_hash),
 deweys       INTEGER NOT NULL);""")

    db.execute("COMMIT;")


def clear():
    db.execute("DROP TABLE IF EXISTS supports;")
    db.execute("DROP TABLE IF EXISTS channels;")


def add_channel(claim_hash, bid_deweys):

    # Create the channel
    db.execute("INSERT INTO channels VALUES (?, ?);",
               (claim_hash, bid_deweys))

    # Add the self-support
    add_support(claim_hash, claim_hash, bid_deweys)


def add_support(from_channel, to_channel, deweys):

    # Add the support
    db.execute("INSERT INTO supports (from_channel, to_channel, deweys)\
                VALUES (?, ?, ?);",
               (from_channel, to_channel, deweys))

    # Update total deweys
    db.execute("UPDATE channels SET total_deweys = total_deweys + ?\
                WHERE claim_hash = ?;", (deweys, to_channel))


def top_supporters(to_channel):
    return db.execute("""
            SELECT from_channel AS supporter, 1E-8*SUM(deweys) AS lbc
            FROM supports
            WHERE to_channel = ? AND from_channel <> to_channel
            GROUP BY from_channel
            ORDER BY lbc DESC
            LIMIT 5;""", (to_channel, )).fetchall()

