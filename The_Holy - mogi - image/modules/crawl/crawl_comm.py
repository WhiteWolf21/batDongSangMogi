# -*- coding: utf-8 -*-

from re import findall
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
import os
from selenium.webdriver.common.keys import Keys

from modules.PostInfo import PostInfo
from modules.data_backup.store_data import store_data

import urllib.parse
from urllib.request import urlopen

re_group_member  = r"member_id="                        # regex string to find whether the post's owner is group member
re_post_owner_id = r"member_id=(\d+)"                   # regex string to find the id of post's owner

re_group_post_id = r"groups\/(.+)\/permalink\/(.+)\/"   #regex string to find the group name and post id

re_comm_user_id  = r"id=(.+)"
re_img_id = r"[A-Z0-9]+\b"


def crawl_comm(signin_driver, links):
    """Crawl users' post and comment

    :Args:
     - links - link of posts found

    :Returns:
   """

    # this list contains info of posts
    posts_info = []


    for link in links:       
        signin_driver.get(link)

        post_info = PostInfo()
        post_info.set_post_id(link)


        tmp = findall(re_group_post_id, link)[0]
        post_id = tmp[1]
        #get user post id

        try:
            user_ajax = signin_driver.find_element_by_xpath("//h5//a[1]").get_attribute("ajaxify")

        except NoSuchElementException:
            continue

        if len(findall(re_group_member, user_ajax)) == 0:
            # the user is not group member
            continue
        post_info.set_post_owner_id(findall(re_post_owner_id, user_ajax)[0])


        #make folder

        path = 'images/'
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        try:
            test_element = signin_driver.find_element_by_xpath("//a[@rel='theater' and (@data-render-location='group_permalink' or @data-render-location='group' or @passthroughprops='[object Object]')]")
            try:
                os.makedirs(os.path.join('images', post_id))
            except FileExistsError:
                pass
            try:
                element = signin_driver.find_element_by_xpath("//a[@rel='theater' and (@data-render-location='group_permalink' or @data-render-location='group')]")
                element.click()

                first_img_id = ""

                for i in range(30):
                    print(i)
                    sleep(5)
                    tmp = signin_driver.find_element_by_class_name('spotlight')
                    img_src = tmp.get_attribute("src")
                    img_id = findall(re_img_id, img_src)
                    if first_img_id == "":
                        first_img_id = img_id
                    else:
                        if img_id == first_img_id:
                            break

                    image = urlopen(img_src)

                    f = open("images/"+post_id+"/" + str(i) + ".jpg", 'wb')
                    f.write(image.read())
                    f.close()

                    element.send_keys(Keys.ARROW_RIGHT)
            except NoSuchElementException:
                print("No pic post")
                pass

            try:
                first_img_id = ""
                cmt_image = signin_driver.find_elements_by_xpath("//a[@passthroughprops='[object Object]' and @rel='theater']")
                if cmt_image != []:
                    i = 1
                    for cmt in cmt_image:
                        img_src = cmt.find_element_by_tag_name('img').get_attribute('src')
                        img_id = findall(re_img_id, img_src)
                        if first_img_id == "":
                            first_img_id = img_id
                        else:
                            if img_id == first_img_id:
                                break
                        image = urlopen(img_src)
                        f = open("images/"+post_id+"/cmt" + str(i) + ".jpg", 'wb')
                        f.write(image.read())
                        f.close()
                        i += 1

            except NoSuchElementException:
                print("No pic cmt")
                pass
        except NoSuchElementException:
            # if no image exists, continue the task
            print("no pic")
            pass

        posts_info.append(post_info)


    store_data(posts_info)

    signin_driver.quit()


