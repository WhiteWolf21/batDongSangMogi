# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from make_up.post_extraction import posts_extract
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class PostExtractPipeline(object):
    def process_item(self, item, spider):
        if item['data'] is None:
            return None
        
        post_data = item['data']
        posts_extract(post_data)

        return item


class MongoPipeline(object):
    def process_item(self, item, spider):
        if item is None:
            return None
        
        mongo_client = MongoClient(settings.get('MONGO_LINK'))
        collection = mongo_client[settings.get('MONGO_DB')][settings.get('MONGO_DATA')]

        tmp = item['data'].get_info_all()
        # print(tmp)
        tmp['location'] = {
            "type" : "Point",
            "coordinates" : [tmp['location_lng'], tmp['location_lat']]
        }
        
        for x in ['address', 'city', 'bedroom', 'bathroom']:
            del tmp[x]

        collection.insert_one(tmp)

        mongo_client.close()
        return None
