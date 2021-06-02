from database import *

clear()
setup()

db.execute("BEGIN;")
add_channel("John", 0.1E8)
add_channel("Jane", 0.1E8)
add_channel("Steve", 1000E8)
add_support(None, "John", 100E8)
add_support("Steve", "John", 100E8)
db.execute("COMMIT;")

for i in range(15):
    update_ratings()

