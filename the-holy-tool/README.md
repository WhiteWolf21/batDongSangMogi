# The Holy
### v1.5

#### Created by
 - *Mai Pham*
 - *Tommy*
 - *Huy Duc*
 - *The whole team Real Estate - OISP*

### 1. Prerequsite
 - use `python 3`
 - install the following libraries by `pip` or `anaconda`: `selenium` `pandas`
 - Before running the following command, change the user name and password of **Facebook** account in file `acct.csv`
 - We strongly suggest using **Firefox** instead of f*kin **Chrome**. If you 
 - Please remove all stuffs in folder `images` before running command

### 2. Run

- In parent directory **The Holy** run: 

> python the_crawler.py

### 3. Features
 - Retrieve post content (current post or the post is shared)
 - Retrieve post owner's ID
 - Retrieve number of likes, post
 - Retrieve datetime (post day and crawl day)
 - Retrieve images attached in the post
 - Data retrieved is processed
 - Comment: comment owner's ID, replying comment, post owner's ID of the replying comment

 ----------------------------------------------------------------------------------------------------
## CHANGELOG
#### v1.6 
##### $ in development $
 - Configuring setting is much easier and convienient

#### v1.5
##### July 1, 2019
 - Add *Save image* feature: the pictures are now stored in folder `images` in parent directory
 - Data is processed after crawling: if you want to show more attributes than ones showed, modify `modules/back_up_data/back_up.py`
 - Result is stored in file `result.txt`
 - Config is now set in `settings.py`
 - Crawl many pages in one running time
##### v1.4
 - Enhance the crawling post content mechanism
##### v1.3.1
 - Fix datetime error as `12 PM` or `12 AM`
