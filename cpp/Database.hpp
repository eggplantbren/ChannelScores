#ifndef ChannelScores_Database_hpp
#define ChannelScores_Database_hpp

#include "sqlite_modern_cpp/hdr/sqlite_modern_cpp.h"

namespace ChannelScores
{

class Database
{
    private:
        sqlite::database db;

        void create_tables();
        void drop_tables();
        void pragmas();

    public:
        Database();


};


/* IMPLEMENTATIONS FOLLOW */

Database::Database()
:db("channel_scores.db")
{
    pragmas();
    drop_tables();
    create_tables();
}

void Database::create_tables()
{
    db << "CREATE TABLE IF NOT EXISTS channels\
(claim_hash   BLOB NOT NULL PRIMARY KEY,\
 total_deweys INTEGER NOT NULL,\
 rating       REAL NOT NULL)\
WITHOUT ROWID;";

    db << "INSERT OR IGNORE INTO channels VALUES ('anon', 0, 1.0);";

    // Supports ALSO INCLUDES THE BID, which is treated as a self-support.
    db << "CREATE TABLE IF NOT EXISTS supports\
(id           INTEGER NOT NULL PRIMARY KEY,\
 from_channel BLOB NOT NULL REFERENCES channels (claim_hash),\
 to_channel   BLOB NOT NULL REFERENCES channels (claim_hash),\
 from_rating  REAL NOT NULL,\
 deweys       INTEGER NOT NULL);";

    db << "CREATE INDEX IF NOT EXISTS top_supporter_idx\
                ON supports (from_channel, to_channel, deweys);";
}

void Database::drop_tables()
{
    db << "DROP TABLE IF EXISTS supports;";
    db << "DROP TABLE IF EXISTS channels;";
}

void Database::pragmas()
{
    db << "PRAGMA SYNCHRONOUS = 0;";
    db << "PRAGMA JOURNAL_MODE = WAL;";
}


} // namespace

#endif
