import apsw

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

    db.execute("""
CREATE TABLE IF NOT EXISTS channels
(claim_hash           BLOB NOT NULL PRIMARY KEY,
 total_deweys         INTEGER NOT NULL,
 boost_factor         REAL NOT NULL DEFAULT 1.0,
 boosted_total_deweys REAL NOT NULL)
WITHOUT ROWID;""")

    db.execute("""
CREATE TABLE IF NOT EXISTS supports
(txo_hash        BLOB NOT NULL PRIMARY KEY,
 deweys          INTEGER NOT NULL,
 signing_channel BLOB REFERENCES channels (claim_hash)
 boosted_deweys  REAL NOT NULL)
WITHOUT ROWID;""")

    db.execute("COMMIT;")







setup()

