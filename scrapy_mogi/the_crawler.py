import os
from pymongo import MongoClient
import time

import mogi_vn.settings as setting


os.chdir("mogi_vn")

province_list  = setting.PROVINCES


if province_list == 0:
    province_list = [x for x in range(1, 64, 1)]


os.system("scrapy crawl mogi")