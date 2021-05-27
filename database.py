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
 boost_factor         REAL NOT NULL,
 boosted_total_deweys REAL NOT NULL)
WITHOUT ROWID;""")

    # Supports ALSO INCLUDES THE BID, which is treated as a self- or
    # anonymous- support.
    db.execute("""
CREATE TABLE IF NOT EXISTS supports
(deweys          INTEGER NOT NULL,
 signing_channel BLOB REFERENCES channels (claim_hash),
 boosted_deweys  REAL NOT NULL,
 PRIMARY KEY (deweys, signing_channel));""")

    db.execute("COMMIT;")


def add_channel(claim_hash, bid_deweys):

    # Create the channel
    db.execute("INSERT INTO channels VALUES (?, ?, ?, ?);",
               (claim_hash, bid_deweys, 1.0, bid_deweys))

    # Create the self-support
    db.execute("INSERT INTO supports VALUES (?, ?, ?);",
               (bid_deweys, claim_hash, bid_deweys))


setup()

