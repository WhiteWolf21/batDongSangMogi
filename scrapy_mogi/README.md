# Scrapy Crawler

This crawler bases on **scrapy** and can crawl only page **mogi.vn**


# Prerequisite

The crawler runs on Python 3.
Install the following libraries:
* pymongo
* scrapy
* timeout_decorator

If you want to run in *local machine*, please do as follows:
* Install *MongoDB*
* Start service mongodb.service in Linux, I don't think Windows user have to do this step

# Configuration
### settings.py
The configurations are set in `settings.py` in `mogi_vn\settings.py`
Below lists the settings you can change in project:
|                |Role                                                            |Default value    |
|----------------|----------------------------------------------------------------|-----------------|
|`MONGO_LINK`    |Link of Mongo server                                            |"localhost:27017"|
|`MONGO_DB`      |Database to store crawled data                                  |"mogi"           |
|`MONGO_DATA`    |Collection to store crawled data                                |"marker"         |
|`PROVINCES`     |A list containing IDs of provinces to crawl                     |[30]             |
|`MAX_SCROLL`    |Indicate how many pages the crawler searches in each category*  |20               |
*category: is the dict `BASE_URLS` is file `mogi_vn/spider/mogi.py`

**IMPORTANT**
Those configurations are read **once time only** in the first run. If you want to change it, stop the running program.
### Province list
In `settings.py`, `PROVINCES` specifies the id of the province crawled. Please read the list in `settings.py` also to know the corresponding id of provinces.

# Execute

In parent directory, execute:
> python the_crawler.py

# Result
## Images
Images of corresponding posts are stored in folder `mogi_vn/images`

## Crawled data
Stored in MongoDB, localhost:27017
