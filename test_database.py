from database import *

clear()
setup()

db.execute("BEGIN;")
add_channel("Joe", 100000)
add_channel("Steve", 10000)
add_support("Steve", "Joe", 10000)
iterate()
db.execute("COMMIT;")