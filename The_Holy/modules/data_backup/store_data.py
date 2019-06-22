import pandas as pd
import settings

# def store_data(posts_info):
#     df_dict = {
#         'Link': [],
#         'Contents': [],
#         'User': [],
#         'Type': [],
#         'Intent': [],
#         'PIC': [],
#     }
    
#     for post_info in posts_info:        
#         for comment in post_info.get_post_comments():
#             df_dict['Link'].append(settings.GROUP + "permalink/" + post_info.get_post_id())
#             df_dict['Contents'].append(comment['comment_content'])
#             df_dict['User'].append(settings.URL + comment['comment_owner_id'])
#             df_dict['Type'].append("comment")
#             df_dict['Intent'].append("")
#             df_dict['PIC'].append("")

#     df = pd.DataFrame(df_dict)
#     writer = pd.ExcelWriter('result1.xlsx', engine='xlsxwriter')
#     df.to_excel(writer, sheet_name='Sheet1')

#     # Close the Pandas Excel writer and output the Excel file.
#     writer.save()

def store_data(posts_info):
    for post in posts_info:
        print("*********************************************")
        print("group_id     : ", post.get_group_id())
        print("post_id      : ", post.get_post_id())
        print("post_owner_id: ", post.get_post_owner_id())
        print("post_content : ", post.get_post_content())
        print("date_crawl   : ", post.get_date_crawl())
        print("date_post    : ", post.get_date_post())
        print("no. comments : ", post.get_post_comment_num())
        print("no. reactions: ", post.get_post_reaction_num())
        print("no. shares   : ", post.get_post_share_num())
        print("score        : ", post.get_score())
        print("date_post    : ", post.get_date_post())
        print("date_post    : ", post.get_date_post())
        print("post_comments: ")
        for comment in post.get_post_comments():
            print("    ------------")
            print("    comment_owner_id: ", comment['comment_owner_id'])
            print("    comment_content : ", comment['comment_content'])
            print("    comment_tags    : ", comment['comment_tags'])
            print("    comment_replies : ")
            for reply in comment['comment_replies']:
                print("      reply_user   :", reply['reply_user'])
                print("      reply_comment:", reply['reply_comment'])
                print("      reply_tag    :", reply['reply_tag'])
            
