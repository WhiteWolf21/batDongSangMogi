# -*- coding: utf-8 -*-

from re import findall, search
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from time import sleep
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import os
from urllib.request import urlopen

import settings
from modules.PostInfo import PostInfo
from modules.miscellaneous import random_time
from modules.miscellaneous import check_isLock

re_group_member  = r"member_id="                        # regex string to find whether the post's owner is group member
re_post_owner_id = r"group_id=(\d+)"                   # regex string to find the id of post's owner

re_group_post_id = r"groups\/(.+)\/permalink\/(.+)\/"   #regex string to find the group name and post id

re_comm_user_id  = r"id=(.+)"
re_img_id = r"[A-Z0-9]+\b"


def crawl_post(signin_driver, links):
    """Crawl post and its releavant information
    Additionally, crawl_post() removes each link in parameter links after crawling it

    :Args:
     - signin_driver - a Selenium driver
     - links - link of posts found
     - accounts - list of account get from db server

    :Returns:
     - posts_info - a list of instances of class PostInfo
     - None - if the account is locked
   """
    print("======================== CRAWL POST =========================")

    # this list contains info of posts
    posts_info = []
    

    # each account is used to crawl a fixed number of account
    N_max_post_each_acc = settings.MAX_POST_EACH    
    n_max = 0

    while len(links) > 0:
        sleep(random_time(2, 5))

        if n_max == N_max_post_each_acc:
            # this account reaches the upper bound
            break
        else:
            n_max += 1

        
        ############## start crawling ###############


        ################# TESTING MODULE ################
        print("No. links left: ", len(links))
        ################# TESTING MODULE ################


        link = links.pop()
        n_time_refresh = 0
        while True:
            try:
                signin_driver.get(link)
                break
            except TimeoutError:
                signin_driver.refresh()
                n_time_refresh += 1

                if n_time_refresh == 3:
                    break
        if n_time_refresh == 3:
            continue

        
        # check whether the account is locked
        if check_isLock(signin_driver) is False:
            return None


        # ############## TESTING MODULE ###############
        # print(signin_driver.page_source)
        # signin_driver.quit()
        # exit(1)
        # ############## TESTING MODULE ###############



        # check if this post is sharing another post which is not available
        try:
            signin_driver.find_element_by_xpath("//div[@class='mbs _6m6 _2cnj _5s6c']").text
            continue
        except NoSuchElementException:
            pass

        # check if the post shares another post or link
        # if post shares a link, ignore the post
        # if post share another post which is useful (the shared post has infomation extracted by API NLP)
        is_share = False
        try:
            check_share = signin_driver.find_element_by_xpath("//span[@class='fcg']").get_attribute('innerHTML')
            if len(findall(r"shared", check_share)) > 0:
                if len(findall(r"post", check_share)) > 0:
                    # this post is sharing another post
                    is_share = True
                else:
                    # this post shares nonsense thing
                    continue
        except NoSuchElementException:
            pass


        post_info = PostInfo()


        # ############### TESTING MODULE ###############
        # print(signin_driver.page_source)
        # signin_driver.quit()
        # exit(1)
        # ############### TESTING MODULE ###############


        # assign basic info for post
        tmp = findall(re_group_post_id, link)[0]
        user_ajax = signin_driver.find_element_by_xpath("//h5//a[1]").get_attribute("ajaxify")


        post_info.set_info("group", tmp[0])
        post_info.set_info("link", "https://facebook.com/groups/" + tmp[0] + "/permalink/" + tmp[1])
        post_info.set_info("post_id", tmp[1])
        post_info.set_info("crawled_date", datetime.now().isoformat())
        post_info.set_info("post_owner_id", findall(re_post_owner_id, user_ajax)[0])


        # download images if exists
        try:
            element = signin_driver.find_element_by_xpath("//a[@rel='theater' and @class='_5dec _xcx']")
            element.click()

            first_img_id = ""
            
            img_folder = "images/" + post_info.get_info("post_id")
            try:
                os.mkdir(img_folder)
            except FileExistsError:
                pass

            for i in range(30):
                print(i)
                sleep(2)
                tmp = signin_driver.find_element_by_class_name('spotlight')
                img_src = tmp.get_attribute("src")
                img_id = findall(re_img_id, img_src)
                if first_img_id == "":
                    first_img_id = img_id
                else:
                    if img_id == first_img_id:
                        element.send_keys(Keys.ESCAPE)
                        break


                image = urlopen(img_src)
                
                f = open( img_folder + '/' + str(i) + ".jpg", 'wb' )
                f.write( image.read() )
                f.close()


                element.send_keys(Keys.ARROW_RIGHT)
        except NoSuchElementException:
            # if no image exists, continue the task
            pass

        


        # assign date the post is published
        try:
            datetime_str = signin_driver.find_element_by_xpath("//a[@class='_5pcq']/abbr").get_attribute('title')
            post_info.set_info("post_date", get_datetime(datetime_str))
        except NoSuchElementException:
            pass



        # assign number of reactions, comments and shares of posts
        try:
            post_info.set_info("post_comment_num", (int(findall(r"\d{1,4}", signin_driver.find_element_by_xpath("//a[@class='_3hg- _42ft']").get_attribute("innerHTML"))[0])))
        except NoSuchElementException:
            pass
        try:
            post_info.set_info("post_reaction_num", (int(findall(r"\d{1,4}", signin_driver.find_element_by_xpath("//span[@class='_81hb']").get_attribute("innerHTML"))[0])))
        except NoSuchElementException:
            pass
        # try:
        #     post_info.set_post_share_num(int(signin_driver.find_element_by_xpath("//a[@class='_3rwx _42ft").get_attribute("innerHTML")))
        # except NoSuchElementException:
        #     pass
        post_info.set_info("score", post_info.get_info("post_comment_num") + post_info.get_info("post_reaction_num") + post_info.get_info("post_share_num"))



        # assign post content for post
        # there are in fact 3 cases of post content:
        #   - plain text enclosed in                    <p></p>
        #   - text decorated by a frame of Facebook: in <span class="_4a6n _a5_">
        #   - from a shared post

        # the first case of post content
        post_content = signin_driver.find_elements_by_tag_name('p')
        tmp = ''
        for element in post_content:
            tmp += element.text + " "

        price = ""
        location = ""
        try:
            price = signin_driver.find_element_by_xpath("//div[@class='_l57']").get_attribute("innerHTML")
        except NoSuchElementException:
            pass
        try:
            location = signin_driver.find_element_by_xpath("//div[@class='_l58']").get_attribute("innerHTML")
        except NoSuchElementException:
            pass

        tmp = tmp + " " + price + " " + location
        
        # this is a special case, which post content in embedded in div[@class="_2cuy _3dgx _2vxa"]
        # rather than in <p>
        try:
            class_2_content = signin_driver.find_elements_by_xpath("//div[@class='_2cuy _3dgx _2vxa']")            
            for content in class_2_content:
                tmp = tmp + " " + content.text
        except NoSuchElementException:
            pass



        # the second case of post content
        # in this case, there are 2 possible scenarios
        if tmp == '  ':
            # tmp = signin_driver.find_element_by_class_name("_4a6n _a5_").text
            # tmp = signin_driver.find_element_by_class_name("_4a6n").text
            try:
                # first scenario, content is embedded in span[@class='_4a6n _a5_']
                tmp = signin_driver.find_element_by_xpath("//span[@class='_4a6n _a5_']").get_attribute('innerHTML')
            except NoSuchElementException:
                try:
                    # first scenario, content is embedded in pan[@class='_7df8']/span[2]
                    # example: https://facebook.com/groups/mogivietnam/permalink/2328058160563227

                    # first, must click on "See more..." if it exists
                    try:
                        a_tag = signin_driver.find_element_by_xpath("//a[@class='_6tw8']")
                        a_tag.click()
                    except NoSuchElementException:
                        pass
                    
                    tmp = signin_driver.find_element_by_xpath("//span[@class='_7df8']").text
                except NoSuchElementException:
                    pass
                    

        # the third case of post content
        if tmp == '  ' and is_share is True:
            # if the post is sharing another post, take shared post's post content as the sharing one's content
            
            try:
                link_share = signin_driver.find_element_by_xpath("//span[@class='fcg']/a").get_attribute('href')
            except NoSuchElementException:
                # if this post is sharing another post but cannot detect that shared post, then ifnore this post and move to next link
                continue
            
            if len(findall(r"facebook.com", link_share)) == 0:
                link_share = settings.URL + link_share
            # get that shared post's link and crawl its content
            signin_driver.get(link_share)
            sleep(2)
            post_content = signin_driver.find_elements_by_tag_name('p')
            tmp = ''
            for element in post_content:
                tmp += element.text + " "


            # this is a special case, which post content in embedded in div[@class="_2cuy _3dgx _2vxa"]
            # rather than in <p>
            try:
                class_2_content = signin_driver.find_elements_by_class_name("_2cuy _3dgx _2vxa")
                for content in class_2_content:
                    tmp = tmp + " " + content.text
            except NoSuchElementException:
                pass


            price = ""
            location = ""
            try:
                price = signin_driver.find_element_by_xpath("//div[@class='_l57']").get_attribute("innerHTML")
            except NoSuchElementException:
                pass
            try:
                location = signin_driver.find_element_by_xpath("//div[@class='_l58']").get_attribute("innerHTML")
            except NoSuchElementException:
                pass

            tmp = tmp + " " + price + " " + location
            # back to the sharing post
            signin_driver.get(link)

        


        # if reaches this far and tmp == '', we can ignore this post
        if tmp == '':
            continue

        # try to extract price and location specified by user
        # some posts the owner has already specified the price and the location of the real estate
        price = ""
        location = ""
        try:
            price = signin_driver.find_element_by_xpath("//div[@class='_l57']").get_attribute("innerHTML")
        except NoSuchElementException:
            pass
        try:
            location = signin_driver.find_element_by_xpath("//div[@class='_l58']").get_attribute("innerHTML")
        except NoSuchElementException:
            pass

        tmp = tmp + " " + price + " " + location

        print("Content: ", tmp)

        print("nLike  = ", post_info.get_info("post_reaction_num"))
        print("nComm  = ", post_info.get_info("post_comment_num"))
        print("nShare = ", post_info.get_info("post_share_num"))

        post_info.set_info("message", tmp)




        # ************************************************** CRAWL COMMENT **************************************************


        # Show all comments and replies
        while True:
            try:
                # a[@class='_4sxc _42ft'] : "See more replies" button
                # a[@class='_5v47 fss'] : "Show more content" button

                a_tag = signin_driver.find_element_by_xpath("//a[@class='_4sxc _42ft' or @class='_5v47 fss']")
                a_tag.click()
                sleep(0.75)
            except (NoSuchElementException, ElementNotInteractableException):
                break

        comment = None        
        comments_replies = signin_driver.find_elements_by_xpath("//div[@aria-label='Comment' or @aria-label='Comment reply']")
        for comment_reply, i in zip(comments_replies, range(len(comments_replies))):            
            if comment_reply.get_attribute('aria-label') == "Comment":
                # this is comment

                if comment is not None:
                    post_info.add_comment(comment)

                comment = {}
                comment_extraction(comment, comment_reply)
                comment['comment_replies']  = []

            else:
                #this is reply

                reply = dict()
                comment_extraction(reply, comment_reply)

                comment['comment_replies'].append(reply)

            if i == len(comments_replies) - 1:
                post_info.add_comment(comment)


        # append to posts_info        
        posts_info.append(post_info)
    
            
    signin_driver.quit()


    return posts_info


re_datetime = r"(\d{1,2})\/(\d{1,2})\/(\d{1,2}),\s(\d{1,2}):(\d{1,2})\s(AM|PM)"

def get_datetime(datetime_str):
    result = findall(re_datetime, datetime_str)
    if result[0][5] == "AM":
        return datetime(int(result[0][2]) + 2000, int(result[0][0]), int(result[0][1]), int(result[0][3]), int(result[0][4])).isoformat()
    else:
        hour = int(result[0][3])
        if hour != 12:
            hour += 12
        return datetime(int(result[0][2]) + 2000, int(result[0][0]), int(result[0][1]), hour, int(result[0][4])).isoformat()


def comment_extraction(comment, element):
    '''Try to extract owner id, content and tagged user
    '''

    comment['comment_owner_id'] = findall(r"id=(\d+)", element.find_element_by_xpath(".//a[@class=' _3mf5 _3mg0' or @class=' _3mf5 _3mg1']").get_attribute("data-hovercard"))[0]

    # there are 2 cases for this:
    # - the content is short enough, so there is not button "See more": in this case, the element containing the content is span[@class='_3l3x']/span
    # - the content is long, so there is a button "See more"          : in this case, the elements containing the content are span[@class='_3l3x _1n4g']/span

    try:
        comment['comment_content']  = element.find_element_by_xpath(".//span[@class='_3l3x']/span").text
    except NoSuchElementException:
        comment['comment_content']  = ""
        tmp                     = element.find_elements_by_xpath(".//span[@class='_3l3x _1n4g']/span")
        for element in tmp:
            comment['comment_content'] = comment['comment_content'] + ' ' + element.text

    comment['comment_tags'] = []
    for tagged_user in element.find_elements_by_xpath(".//span[@class='_3l3x' or @class='_3l3x _1n4g']/a"):
        tagged_user_id = tagged_user.get_attribute('data-hovercard')
        

        if tagged_user_id is not None:
            if search(r"photo", tagged_user_id) is None:
                # if this is not 
                comment['comment_tags'].append(findall(re_comm_user_id, tagged_user_id)[0])
