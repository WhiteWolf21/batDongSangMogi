from selenium.webdriver.common.keys import Keys
from re import findall
from time import sleep
from selenium.common.exceptions import NoSuchElementException

import settings
from modules.miscellaneous import random_time
from modules.miscellaneous import check_isLock
from pymongo import MongoClient


# re_id    = r"\/(\d+)"
re_id    = r"permalink\/(\d+)"

def get_link(signin_driver):
    '''Get link of posts in homepage of group.

    :Args:
     - signin_driver - Selenium driver which has successfully logged in
     
    :Returns:
     - posts_link - a list of links of post
     - None - if the account is locked
    '''

    print("========================= GET LINK ==========================")

    posts_link = []

    # the reason for this 3-time loop is: during getting post's links, if there is a problem with the account or some thing else
    # the getting link processing is restart
    # if it restarts 3 times, the account is actually getting problem
    for i in range(3):
        try :
            for group in settings.GROUPS:
                print("*** Find links in group: ", group)

                # loop every groups in list
                re_group = group + "/permalink/"

                signin_driver.get(settings.URL + "/groups/" + group)
                body = signin_driver.find_element_by_tag_name('body')       

                # scroll the home page
                for j in range(settings.SCROLLS):
                    body.send_keys(Keys.PAGE_DOWN)
                    body.send_keys(Keys.ESCAPE)
                    if j % 5 == 0:
                        sleep(random_time(2, 4))        
                    
                classes = signin_driver.find_elements_by_xpath('//*[@class="_5pcq"]')
                for c in classes:
                    link = c.get_attribute('href')
                    
                    # check whether this is post link
                    if len(findall(pattern=re_group, string=link)) == 0:
                        continue
                    else:
                        # posts_link.append(link)
                    
                        # #if link available

                        # # check whether the post is crawled by check its ID in database
                        id = findall(pattern=re_id, string=link)[0]

                        print("id : ", id)
                        ## check whether the post is already crawled by checking ID
                        if check_old_ID(id):
                            # no post in database has this ID
                            posts_link.append(link)                            
                        else:
                            print("This link has already crawled.")
                            

            signin_driver.quit()            
            return posts_link
        except NoSuchElementException:
            # if this exception is thrown, it means that there is a problem with account
            if check_isLock(signin_driver) is False:
                return None
            else:
                # the problem is not due to the account
                # check if how many times trying without successful
                if i == 2:
                    # the reason of not crawling link successfully may not be due to the account, but still return None
                    return None
                else:
                    continue

    
def check_old_ID(id):
    """Check if the id is already in database

    :Args:
    id - an ID of post 
       
    :Return:
    True - there is no post having given ID
    False - otherwise
    """
    client = MongoClient(settings.MONGO_LINK)
    records = list(client[settings.MONGO_DB][settings.MONGO_DATA].find({"post_id" : id}))
    client.close()

    if len(records) == 0:
        # no post has that ID
        return True
    else:
        return False

