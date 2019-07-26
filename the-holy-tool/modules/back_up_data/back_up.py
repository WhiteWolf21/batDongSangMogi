from pymongo import MongoClient
import pandas as pd 
import json

import settings
from modules.make_up.make_up import make_up
from bson import json_util



# Save data to mongodb
def save_data_to_db(data, client, db, dbconnection):
    # Picking the data
    # data = json.dumps(data)

    # saving data to mongodb
    # creating connect
    try:
        myClient = MongoClient(client,serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        print("Access Successfully")
    except:
        print("Access Failed")

    # creating database in mongodb
    mydb = myClient[db]

    # creating collection
    myconn = mydb[dbconnection]
    info = myconn.insert_one(data)
    print(info.inserted_id,'saved with this id successfully')

    # details = {
    #     'inserted_id':info.inserted_id,
    #     'data_name': data_name,
    #     'created_time': time.time()
    # }
    # return details

# Load model from mongodb - DO NOT TOUCHED IN THIS MOMENT
def load_from_db(client, db, dbconnection):
    json_data = {}

    # saving model to mongodb
    # creating connection
    try:
        myClient = MongoClient(client,serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        print("Access Successfully")
    except:
        print("Access Failed")

    # creating database in mongodb
    mydb = myClient[db]

    # creating collection
    myconn = mydb[dbconnection]
    data = myconn.find({
            # 'name':model_name
        })
    print("\n === Load data from db === \n")
    for i in data:
        print(i,"\n\n")
        # json_data = i

    # # fetching model to mongodb
    # pickled_model = json_data[model_name]

    # return pickle.loads(pickled_model)

def back_up(posts_info):
    for post_info in posts_info:
        dict_extract_post = {   
                            # "post_"+str(i):{}                            
                            # for i in range(len(posts_info) )
                            # if i <= 5
                            }   
        dict_attrs = {
            "attr_addr_number":post_info.get_info("attr_addr_number"),
            "attr_addr_street":post_info.get_info("attr_addr_street"),
            "attr_addr_district":post_info.get_info("attr_addr_district"),
            "attr_addr_ward":post_info.get_info("attr_addr_ward"),
            "attr_addr_city":post_info.get_info("attr_addr_city"),
            "attr_position":post_info.get_info("attr_position"),
            "attr_area":post_info.get_info("attr_area"),
            "attr_surrounding":post_info.get_info("attr_surrounding"),
            "attr_surrounding_name":post_info.get_info("attr_surrounding_name"),
            "attr_surrounding_characteristics":post_info.get_info("attr_surrounding_characteristics"),
            "attr_transaction_type":post_info.get_info("attr_transaction_type"),
            "attr_realestate_type":post_info.get_info("attr_realestate_type"),
            "attr_potential":post_info.get_info("attr_potential"),
            "attr_price":post_info.get_info("attr_price"),
            "attr_price_min":post_info.get_info("attr_price_min"),
            "attr_price_max":post_info.get_info("attr_price_max"),
            "attr_price_m2":post_info.get_info("attr_price_m2"),
            "attr_interior_floor":post_info.get_info("attr_interior_floor"),
            "attr_interior_room":post_info.get_info("attr_interior_room"),
            "attr_orientation":post_info.get_info("attr_orientation"),
            "attr_project":post_info.get_info("attr_project"),
            "attr_legal":post_info.get_info("attr_legal"),
            "location_lng":post_info.get_info("location_lng"),
            "location_lat":post_info.get_info("location_lat"),
        }
        dict_cmt, dict_replies = [], []
        dict_extract_post["message"] = [post_info.get_info("message")]
        
        dict_extract_post["attributes"] = dict_attrs

        dict_extract_post["group_id"] = \
                            [post.get_info("group") for post in posts_info]

        dict_extract_post["post_id"] = \
                            [post.get_info("post_id") for post in posts_info]
        
        for cmt in post_info.get_info("post_comments"):            
            for rep in cmt["comment_replies"]:
                dict_replies.append({
                        "reply_user":rep["reply_user"],
                        "reply_comment":rep["reply_comment"],
                        "reply_tag":rep["reply_tag"],
                    })
            dict_cmt.append({
                "comment_owner_id": cmt["comment_owner_id"],
                "comment_content" : cmt["comment_content"],
                "comment_tags"    : cmt["comment_tags"],
                "comment_replies" : dict_replies,
                })

        dict_extract_post["comments"] = dict_cmt
        print('\n\n\n\n dict_extract_post\n',json.dumps(dict_extract_post))

        # saving to mongodb
        print("=== Saving to mongodb ===")
        save_data_to_db(   dict_extract_post,
                                # client='mongodb://localhost:27017/cool_db',
                                # db='cool_db',
                                # dbconnection='posts'
                                client=settings.MONGO_LINK,
                                db=settings.MONGO_DB,
                                dbconnection=settings.MONGO_DATA
                                )    

        # fetch from mongodb
        print("=== Fetch from mongodb ===")
        load_from_db(
                        # model_name='xgb_model', 
                        # client='mongodb://localhost:27017/cool_db', 
                        # db='cool_db',
                        # dbconnection='posts'
                        client=settings.MONGO_LINK,
                        db=settings.MONGO_DB,
                        dbconnection=settings.MONGO_DATA
                        )
