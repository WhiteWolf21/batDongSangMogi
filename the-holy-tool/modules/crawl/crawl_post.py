# -*- coding: utf-8 -*-

from re import findall
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep
from datetime import datetime
from pymongo import MongoClient

import settings
from modules.PostInfo import PostInfo
from modules.miscellaneous import random_time
from modules.miscellaneous import check_isLock

re_group_member  = r"member_id="                        # regex string to find whether the post's owner is group member
re_post_owner_id = r"member_id=(\d+)"                   # regex string to find the id of post's owner

re_group_post_id = r"groups\/(.+)\/permalink\/(.+)\/"   #regex string to find the group name and post id

re_comm_user_id  = r"id=(.+)"


def crawl_post(signin_driver, links,len_links):
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

    while len(links) > len_links - 2:
        print("len links", len_links,len(links))
        sleep(random_time(5, 8))

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




        # # user_ajax = signin_driver.find_element_by_tag_name('h5').find_element_by_tag_name('a').get_attribute('ajaxify')
        # n_reset_link = 0
        # while True:
        #     try:
        #         user_ajax = signin_driver.find_element_by_xpath("//h5//a[1]").get_attribute("ajaxify")
        #         print("user: ", user_ajax)
        #         break
        #     except NoSuchElementException:
        #         if n_reset_link == 3:
        #             # if refresh the page 3 times and still error, then move to next link
        #             break
        #         else:
        #             # refresh the page
        #             n_reset_link += 1
        #             signin_driver.refresh()

        #             # check whether the account is locked
        #             if check_isLock(signin_driver) is False:
        #                 return None

        # # if refresh page 3 times, move to next link
        # if n_reset_link == 3:
        #     continue


        # if len(findall(re_group_member, user_ajax)) == 0:
        #     # the user is not group member
        #     continue

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
            print("Len: ", len(class_2_content))
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
                a_tag = signin_driver.find_element_by_xpath("//a[@class='_4sxc _42ft']")
                a_tag.click()
                sleep(0.75)
            except NoSuchElementException:
                break

        # assign comment for post
        #comments = signin_driver.find_elements_by_class_name('_72vr')
        comments_replies = signin_driver.find_elements_by_xpath("//div[@aria-label='Comment' or @aria-label='Comment reply']")        
      
        is_live_stream = False
        if len(comments_replies) > 0:
            # if post has comment(s)           
            

            # For comment or reply, we do:
            #   if the current is comment:
            #       append to post_info.post_comments if the current comment is not the first comment of the post
            #   then get owner id, tagged user and content of the current
            
            comm_count = 0
            flag_comment_reply = True                       # True: the current is comment, False: otherwise
            comm_replies = []

            
            for comment_reply in comments_replies:
                
                comm_count += 1

                # this is comment
                if comment_reply.get_attribute('aria-label') == "Comment":
                    # print("This is comment")
                    flag_comment_reply = True
                    # if this is not first comment
                    if comm_count > 1:
                        post_info.add_comment(comm_rep_user, comm_rep_content, comm_rep_tag, comm_replies)
                        comm_replies = []

                # this is reply of comment
                # else:
                    # print("This is reply")
              

                
                # extract data of reply or comment

                ## get comment's or reply's owner ID

                try:
                    tmp = comment_reply.find_element_by_class_name('_6qw4').get_attribute('data-hovercard')
                except NoSuchElementException:
                    # this is live stream
                    break


                comm_rep_user = findall(re_comm_user_id, tmp)[0]

                # print("Comm user id: ", comm_rep_user)
                
                
                ## get content and (or) tagged user of comment or reply
                comm_rep_content = ""
                comm_rep_tag     = []
                try:
                    comment_class = comment_reply.find_element_by_class_name('_3l3x')

                    # get text in comment
                    try:
                        comm_rep_content = comment_class.find_element_by_tag_name('span').text
                        # print("Text: ", comm_rep_content)
                    except NoSuchElementException:
                        pass

                    # get tag in comment
                    try:

                        tag = comment_class.find_element_by_tag_name('a').get_attribute('data-hovercard')

                        comm_rep_tag.append(findall(re_comm_user_id, tag)[0])

                        # print("Tag id: ", comm_rep_tag)
                    except NoSuchElementException:
                        pass
                    except TypeError:
                        pass
                
                except NoSuchElementException:
                    pass

                
                # if the current is reply, add reply to list comm_replies
                if flag_comment_reply is False:
                    comm_replies.append({
                        'reply_user'   : comm_rep_user,
                        'reply_comment': comm_rep_content,
                        'reply_tag'    : comm_rep_tag
                    })

            






        # append to posts_info        
        posts_info.append(post_info)
    
            
    signin_driver.quit()


    return posts_info


re_datetime = r"(\d{1,2})\/(\d{1,2})\/(\d{1,2}),\s(\d{1,2}):(\d{1,2})\s(AM|PM)"

def get_datetime(datetime_str):
    if datetime_str!='':
        split_datetime = datetime_str.split(' ')
        split_time = split_datetime[1].split(':')
        date_ = split_datetime[0].split('/')
        year = date_[2].split(',')[0]
        if int(date_[0]) < 10:
            date_[0] = '0' + date_[0]
        if int(year) < 2000:
            year = '20' + year + ","
        if datetime_str.split(' ')[-1]=='PM':
            # split_time = split_datetime[1].split(':')
            # datetime_str = split_datetime[0] + " " + str(int(split_time[0])+12) + \
            #                 ":" + split_time[1]
            datetime_str = date_[0] + "/" + date_[1] + "/" + year + \
                    " " + str(int(split_time[0])+12) + \
                            ":" + split_time[1]            
        else:
            # datetime_str = " ".join(split_datetime[:2])
            datetime_str = date_[0] + "/" + date_[1] + "/" + year + \
                    " " + ":".join(split_time[:2])
        print(datetime_str)
        return datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')

