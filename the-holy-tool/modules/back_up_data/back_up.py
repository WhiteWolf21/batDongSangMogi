from pymongo import MongoClient

import settings


def back_up(posts_info):
    with open("result.txt", "w") as file:
        for post in posts_info:
            file.write("*********************************************\n")
            file.write("group_id     : " + post.get_info("group")+ "\n")
            file.write("post_id      : " + post.get_info("post_id")+ "\n")
            file.write("post_owner_id: " + post.get_info("post_owner_id")+ "\n")
            file.write("post_content : " + post.get_info("message")+ "\n")
            file.write("date_crawl   : " + post.get_info("crawled_date")+ "\n")
            file.write("date_post    : " + post.get_info("post_date")+ "\n")
            file.write("no. comments : " + str(post.get_info("post_comment_num")) + "\n")
            file.write("no. reactions: " + str(post.get_info("post_reaction_num")) + "\n")
            file.write("no. shares   : " + str(post.get_info("post_share_num")) + "\n")
            file.write("score        : " + str(post.get_info("score")) + "\n")
            file.write("post_comments: " + "\n")
            for comment in post.get_post_comments():
                file.write("    ------------" + "\n")
                file.write("    comment_owner_id: "+ comment['comment_owner_id']+ "\n")
                file.write("    comment_content : "+ comment['comment_content']+ "\n")
                file.write("    comment_tags    : "+ str(comment['comment_tags']) + "\n")
                file.write("    comment_replies : "+ "\n")
                for reply in comment['comment_replies']:
                    file.write("      reply_user   :"+ reply['reply_user']+ "\n")
                    file.write("      reply_comment:"+ reply['reply_comment']+ "\n")
                    file.write("      reply_tag    :"+ str(reply['reply_tag'])+ "\n")
