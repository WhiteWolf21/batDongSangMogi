from selenium import webdriver
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


username = 'tommyle133@gmail.com'
password = '(lock133)'

url = 'https://www.facebook.com/'


def get_link(scrolls = 500):
    driver = webdriver.Chrome("drivers/chromedriver")

    
    try:
        driver.get(url)

        driver.find_element_by_id('email').send_keys(username)
        driver.find_element_by_id('pass').send_keys(password)
        driver.find_element_by_id('loginbutton').click()

        driver.get("https://www.facebook.com/groups/mogivietnam")

        body = driver.find_element_by_tag_name('body')

        for i in range(10):
            body.send_keys(Keys.ESCAPE)
            driver.implicitly_wait(1)

        
        for i in range(scrolls):
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.ESCAPE)
            driver.implicitly_wait(1)

        posts =[]

        classes = driver.find_elements_by_xpath('//*[@class="_5pcq"]')

    except TimeoutException:
        driver.close()
        return False

 
    #get all link in one day


    #get n post recently

    for c in classes:
        posts.append(c.get_attribute('href'))

    with open("report/output_fl5.csv", "w") as file:
        for post in posts:
            file.write(post+"\n")
        file.close()

    driver.close()

    return True

