from random import shuffle
import settings

from modules.crawl.sign_in import sign_in
from modules.crawl.get_link import get_link
from modules.crawl.crawl_post import crawl_post

def crawl():
    '''Get link of posts and crawl theme
    :Returns:
    - posts_info - a list of instances of class PostInfo, those instances are not yet made up
    - None - if every accouns are locked
    '''

    account_list = settings.ACCOUNTS
    # begin the proccess

    posts_link = None
    posts_info = []

    # sign in and get link
    while True:
        account = pick_account(account_list)
        # if every accounts are blocked
        if account is None:
            print("** No account available")
            return None

        
        
        # sign in
        signin_driver = sign_in(account['user'], account['password'])
        if signin_driver is None:
            # this account is locked
            account['isLocked'] =  True
            continue
                
    
        # get link
        posts_link = get_link(signin_driver)
        if posts_link is None:
            # this account is locked
            account['isLocked'] =  True
            print("** Account: \'", account['user'], "\' is blocked")
            continue
        else:
            break
            

    print("Links after crawling: ")
    for link in posts_link:
        print(link)

        
    # sign in and crawl post
    while True:
        account = pick_account(account_list)
        # if every accounts are blocked
        if account is None:
            print("** No account available")
            return None

        # sign in
        signin_driver = sign_in(account['user'], account['password'])
        if signin_driver is None:
            # this account is locked
            account['isLocked'] =  True
            print("** Account: \'", account['user'], "\' is blocked")
            continue
                     
        # crawl post
        tmp = crawl_post(signin_driver, posts_link)        
        if tmp is not None:
            posts_info = posts_info + tmp
        else:
            # this account is locked
            account['isLocked'] =  True
            print("** Account: \'", account['user'], "\' is blocked")

        # check if whether continue crawling or not
        if len(posts_link) == 0:
            # if there is no more link to crawl
            break
    
    return posts_info

def pick_account(account_list):
    """Pick randomly an unblocked account in the list

    :Args:
    - account_list - account list

    :Returns:
    - account - if there is available account
    - None - otherwise
    """
    shuffle(account_list)
    for account in account_list:
        if account['isLocked'] is True:
            continue
        else:
            return account

    return None