import datetime
from time import sleep

from modules.crawl.crawl import crawl
from modules.make_up.make_up import make_up
from modules.back_up_data.back_up import back_up
import settings

def main():
    # check if the license is valid
    if datetime.datetime.now().year != 2019:
        print("### License is expired. Please contact Dr Tho for license. He he he. ###")
        exit(0)

    
    #read accounts' info
    with open("acct.csv", "r") as file:
        accounts = file.readlines()
        file.close()

    for acct in accounts:
        tmp =  acct.split(',')

        settings.ACCOUNTS.append({
            "user":     tmp[0],
            "password": tmp[1],
            "isLocked": False,
        })
    print(" **** Read successfully accounts         **** ")


    # crawl post
    posts_info = crawl()

    if posts_info is not None:
        # make up data
        for post_info in posts_info:
            make_up(post_info)

        # back up to MongoDB
        back_up(posts_info)


if __name__ == "__main__":
    main()
