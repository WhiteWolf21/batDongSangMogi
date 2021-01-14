import pandas as pd
import settings
from modules.data_backup.api_NLP_communicate import get_from_api

def store_data(posts_info):

    df_dict = {
            "Link_post": [],
            "Post_owner_id": [],
        }

    for post in posts_info:
        df_dict["Link_post"].append(post.get_post_id())
        df_dict["Post_owner_id"].append(settings.URL + post.get_post_owner_id())


    df = pd.DataFrame(df_dict)
    writer = pd.ExcelWriter('result5.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


