from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep
from random import shuffle

import settings
from modules.crawl.get_link import get_link
from modules.miscellaneous import check_isLock
from modules.miscellaneous import random_time

    

def sign_in(user, password):
    ''' Sign in to Facebook.

    :Args:
    - user - user name
    - password - password of user

    :Returns:
    - signin_driver - a driver that has been already logged in
    - None - if the account is locked
    '''

    print("========================= SIGN IN ===========================")

    # FOR CHROME
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.default_content_setting_values.notifications": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(settings.DRIVER, chrome_options=chrome_options)

    # FOR FIREFOX
    # firefox_options = webdriver.FirefoxOptions()
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("dom.webnotifications.enabled", False)
    # driver = webdriver.Firefox(executable_path=settings.DRIVER, firefox_options=firefox_options, firefox_profile=profile)
    # driver.maximize_window()
    
    #FOR CHROME 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=settings.DRIVER, options=chrome_options)

    driver.get(settings.URL)
    sleep(3)

    # type user name and password to TextField
    driver.find_element_by_id('email').send_keys(user)
    sleep(3)
    driver.find_element_by_id('pass').send_keys(password)
    sleep(3)
    

    driver.find_element_by_id('loginbutton').click()
    # check whether the account is locked
    if check_isLock(driver) is False:
        driver.quit()
        return None
    else:
        return driver