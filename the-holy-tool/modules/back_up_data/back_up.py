from pymongo import MongoClient
import pandas as pd 

import settings


def back_up(posts_info):
    with open("result.txt", "w") as file:
        dict_posts, dict_comment, dict_reply = {}, {}, {}
        # Post results
        dict_posts['group_id'] = [post.get_info('group') for post in posts_info]
        dict_posts['post_id'] = [post.get_info('post_id') for post in posts_info]
        dict_posts['post_owner_id'] = [post.get_info('post_owner_id') for post in posts_info]
        dict_posts['post_content'] = [post.get_info('message') for post in posts_info]
        dict_posts['date_crawl'] = [post.get_info('crawled_date') for post in posts_info]
        dict_posts['date_post'] = [post.get_info('post_date') for post in posts_info]
        dict_posts['no. comments'] = [post.get_info('post_comment_num') for post in posts_info]
        dict_posts['no. reactions'] = [post.get_info('post_reaction_num') for post in posts_info]
        dict_posts['no. shares'] = [post.get_info('post_share_num') for post in posts_info]
        dict_posts['score'] = [post.get_info('score') for post in posts_info]
        
        # Comment results
        list_comment_owner_id, list_comment_content, list_comment_tags,list_comment_id = [], [], [], []
        list_reply_user, list_reply_comment, list_reply_tag,list_reply_id = [], [], [], []
        for post in posts_info:
            for comment in post.get_post_comments():
                list_comment_owner_id.extend(comment['comment_owner_id'])
                list_comment_content.extend(comment['comment_content'])
                # list_comment_tags.extend(comment['comment_tags'])
                # list_comment_id.extend(post.get_info('post_id'))
                for reply in comment['comment_replies']:
                    list_reply_user.extend(reply['reply_user'])
                    list_reply_comment.extend(reply['reply_comment'])
                    # list_reply_tag.extend(reply['reply_tag'])
                    # list_reply_id.extend(comment['comment_owner_id'])


        # Comment results
        dict_comment['comment_owner_id'] = list_comment_owner_id
        dict_comment['comment_content'] = list_comment_content
        dict_comment['comment_tags'] = list_comment_tags
        dict_comment['posts'] = list_comment_id        
        print("Comment",len(list_comment_owner_id),len(list_comment_content),len(list_comment_tags),len(list_comment_id))

        # Reply results
        dict_reply['reply_user'] = list_reply_user
        dict_reply['reply_comment'] = list_reply_comment
        dict_reply['reply_tag'] = list_reply_tag
        dict_reply['comment_owner_id'] = list_reply_id 
        print("Reply",len(list_reply_user),len(list_reply_comment),len(list_reply_tag),len(list_reply_id))

        writer1 = pd.ExcelWriter('b.xls', engine='xlsxwriter')
        pd.DataFrame(data=dict_posts).sort_values(by=['score'], ascending=False).to_excel(writer1,sheet_name="Posts")
        # pd.DataFrame(data=dict_comment).to_excel(writer1,sheet_name="Comment")
        # pd.DataFrame(data=dict_reply).to_excel(writer1,sheet_name="Reply")
        writer1.save()       

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
                file.write("    ------------")
                file.write("    comment_owner_id: "+ comment['comment_owner_id']+ "\n")
                file.write("    comment_content : "+ comment['comment_content']+ "\n")
                file.write("    comment_tags    : "+ str(comment['comment_tags']) + "\n")
                file.write("    comment_replies : "+ "\n")
                for reply in comment['comment_replies']:
                    file.write("      reply_user   :"+ reply['reply_user']+ "\n")
                    file.write("      reply_comment:"+ reply['reply_comment']+ "\n")
                    file.write("      reply_tag    :"+ str(reply['reply_tag'])+ "\n")
