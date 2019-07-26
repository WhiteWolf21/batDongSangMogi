import urllib.parse

URL           = "https://www.facebook.com/"
# DRIVER        = "drivers/chromedriver"
# DRIVER        = "drivers/geckodriver"
DRIVER        = "drivers/chromedriver"


GROUPS        = [
    "mogivietnam",
    "vinhomesmarket"
]

SCROLLS       = 1
WAITING_TIME  = 30
ACCOUNTS      = []
MAX_POST_EACH = 2                   # max posts each account crawls before logging out
MONGO_LINK 	  = "mongodb://localhost:27017"
MONGO_DATA 	  = "posts"
MONGO_DB      = "cool_db"