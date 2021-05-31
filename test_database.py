from database import *

clear()
setup()

db.execute("BEGIN;")
add_channel("Joe", 100000)
add_channel("Steve", 10000)
add_channel("Jane", 10000)
add_support("Steve", "Steve", 10000)
add_support("Steve", "Joe", 10000)
add_support("Jane", "Joe", 20000)
add_support(None, "Jane", 100000000)
db.execute("COMMIT;")

for i in range(5):
    update_ratings()

