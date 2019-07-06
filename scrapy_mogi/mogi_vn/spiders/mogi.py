import scrapy
import re
import time
import os
from datetime import datetime
from pymongo import MongoClient
import urllib
from scrapy.utils.project import get_project_settings

from make_up.miscellaneous.regex_operation import get_latlng
from make_up.miscellaneous.PostInfo import PostInfo


re_address = r"\<div class\=\"address nowrap\"\>[^\<]*\<\/div\>"

re_postid = r"id(\d{4,})"

re_title = r"(.*) - Mogi.*"


BASE_URLS = {
    # 1: {
    #     'link'            : '/mua-nha?cp=',
    #     'realestate_type' : 'nhà',
    #     'transaction_type': 'bán'
    # },
    # 2: {
    #     'link'            : '/mua-can-ho?cp=',  
    #     'realestate_type' : 'căn hộ',
    #     'transaction_type': 'bán'
    # },
    3: {
        'link'            : '/mua-dat?cp=',
        'realestate_type' : 'đất',
        'transaction_type': 'bán'
    },
    4: {
        'link'            : '/mua-dat-nen-du-an?cp=',
        'realestate_type' : 'đất nền',
        'transaction_type': 'bán'
    },
    # 5: {
    #     'link'            : '/thue-nha?cp=',
    #     'realestate_type' : 'nhà',
    #     'transaction_type': 'thuê'
    # },
    # 6: {
    #     'link'            : '/thue-nha-xuong?cp=',
    #     'realestate_type' : 'xưởng',
    #     'transaction_type': 'thuê'
    # },
    # 7: {
    #     'link'            : '/thue-dat-trong?cp=',
    #     'realestate_type' : 'đất',
    #     'transaction_type': 'thuê'
    # },
    # 8: {
    #     'link'            : '/thue-nha-kho?cp=',
    #     'realestate_type' : 'kho',
    #     'transaction_type': 'thuê'
    # }

}

PROVINCES = {
    1:  ["an-giang",        "An Giang"],
    2:  ["bac-can",         "Bắc Kạn"],
    3:  ["bac-giang",       "Bắc Giang"],
    4:  ["bac-lieu",        "Bạc Liêu"],
    5:  ["bac-ninh",        "Bắc Ninh"],
    6:  ["ba-ria-vung-tau", "bà rịa - vũng tàu"],
    7:  ["ben-tre",         "Bến Tre"],
    8:  ["binh-dinh",       "Bình Định"],
    9:  ["binh-duong",      "bình dương"],
    10: ["binh-phuoc",      "Bình Phước"],
    11: ["binh-thuan",      "Bình Thuận"],
    12: ["ca-mau",          "Cà Mau"],
    13: ["can-tho",         "Cần Thơ"],
    14: ["cao-bang",        "Cao Bằng"],
    15: ["dak-lak",         "Đắk Lắk"],
    16: ["dak-nong"         "Đắk Nông"],
    17: ["da-nang",         "Đà Nẵng"],
    18: ["dien-bien"        "Điện Biên"],
    19: ["dong-nai",        "đồng nai"],
    20: ["dong-thap",       "Đồng Tháp"],
    21: ["gia-lai",         "Gia Lai"],
    22: ["ha-giang",        "Hà Giang"],
    23: ["hai-duong",       "Hải Dương"],
    24: ["hai-phong",       "Hải Phòng"],
    25: ["ha-nam",          "Hà Nam"],
    26: ["ha-noi",          "hà nội"],
    27: ["ha-tinh",         "Hà Tĩnh"],
    28: ["hau-giang"        "Hậu Giang"],
    29: ["hoa-binh",        "Hoà Bình"],
    30: ["ho-chi-minh",     "hồ chí minh"],
    31: ["hung-yen",        "Hưng Yên"],
    32: ["khanh-hoa",       "Khánh Hoà"],
    33: ["kien-giang",      "Kiên Giang"],
    34: ["kon-tum",         "Kon Tum"],
    35: ["lai-chau",        "Lai Châu"],
    36: ["lam-dong",        "Lâm Đồng"],
    37: ["lang-son",        "Lạng Sơn"],
    38: ["lao-cai",         "Lào Cai"],
    39: ["long-an",         "Long An"],
    40: ["nam-dinh",        "Nam Định"],
    41: ["nghe-an",         "Nghệ An"],
    42: ["ninh-binh",       "Ninh Bình"],
    43: ["ninh-thuan",      "Ninh Thuận"],
    44: ["phu-tho",         "Phú Thọ"],
    45: ["phu-yen",         "Phú Yên"],
    46: ["quang-binh",      "Quảng Bình"],
    47: ["quang-nam",       "Quảng Nam"],
    48: ["quang-ngai",      "Quảng Ngãi"],
    49: ["quang-ninh",      "Quảng Ninh"],
    50: ["quang-tri",       "Quảng Trị"],
    51: ["soc-trang",       "Sóc Trăng"],
    52: ["son-la",          "Sơn La"],
    53: ["tay-ninh",        "Tây Ninh"],
    54: ["thai-binh",       "Thái Bình"],
    55: ["thai-nguyen",     "Thái Nguyên"],
    56: ["thanh-hoa",       "Thanh Hoá"],
    57: ["thua-thien-hue",  "huế"],
    58: ["tien-giang",      "Tiền Giang"],
    59: ["tra-vinh",        "Trà Vinh"],
    60: ["tuyen-quang",     "Tuyên Quang"],
    61: ["vinh-long",       "Vĩnh Long"],
    62: ["vinh-phuc",       "Vĩnh Phúc"],
    63: ["yen-bai",         "Yên Bái"]
}

settings = get_project_settings()


## get old post list from database for checking matching with the newly crawled post

# def check_old_ID(id):
#     """Check if the id is already in database

#     :Args:
#     id - an ID of post 
       
#     :Return:
#     True - there is no post having given ID
#     False - otherwise
#     """
#     client = MongoClient(settings.get('MONGO_LINK'))
#     records = list(client[settings.get('MONGO_DB')][settings.get('MONGO_DATA')].find({"post_id" : id}))
#     client.close()

#     if len(records) == 0:
#         # no post has that ID
#         return True
#     else:
#         return False


class Mogi(scrapy.Spider):
    name              = "mogi"

    PREFIX            = 'https://mogi.vn/'

    province_id       = None
    province_name     = None
    realestate_type   = None
    transaction_type  = None

    def start_requests(self):        
        # read setting from MongoDB
        
        
        self.MAX_SCROLL       = settings.get('MAX_SCROLL')

        for province in settings.get('PROVINCES'):

            # start crawling

            self.province_id   = PROVINCES[province][0]
            self.province_name = PROVINCES[province][1]

            for _, item in BASE_URLS.items():
                self.realestate_type  = item['realestate_type']
                self.transaction_type = item['transaction_type']

                for page in range(self.MAX_SCROLL):
                    url = self.PREFIX + self.province_id + item['link'] + str(page)
                    yield scrapy.Request(url=url, callback=self.parse_max_index)


    def parse_max_index(self, response):
        # links in top section
        links = response.css('div[class="property-top-title"]').css('a::attr(\'href\')').getall()
        for link in links:
            url = self.PREFIX + link
            yield scrapy.Request(url=url, callback=self.parse_article)

        # links in main section
        links = response.css('div[class="prop-info"]').css('a::attr(\'href\')').getall()
        for link in links:
            url = self.PREFIX + link
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        # verify newly crawled post's id with the ones stored in database
        post_id = re.findall(pattern=re_postid, string=response.url)[0]

        # if the newly crawled post has an ID matching with one stored in database
        # if check_old_ID(post_id) is False:
        #     return {'data': None}


        # backup images in post
        print("Start storing image")
        img_links = []
        img_links = img_links + response.xpath("//div[@class='media-item']/img/@src").extract()
        img_links = img_links + response.xpath("//div[@class='media-item']/img/@data-src").extract()

        for img_link, i in zip(img_links, range(len(img_links))):
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers = {'User-Agent':user_agent,}
            request = urllib.request.Request(img_link,None,headers) #The assembled request
            image = urllib.request.urlopen(request)

            img_folder = "images/" + post_id
            try:
                os.mkdir(img_folder)

                f = open( img_folder + '/' + str(i) + ".jpg", 'wb' )
                f.write( image.read() )
                f.close()
            except FileExistsError:
                continue

        print("Stop storing image")



        # retrieve post information


        post_data = PostInfo()

        # fill basic info
        post_data.set_info('page',                  self.PREFIX)
        post_data.set_info('link',                  response.url)
        post_data.set_info('score',                 0)
        post_data.set_info('post_id',               post_id)
        post_data.set_info('message',               ''.join(response.xpath("//div[@class='prop-info-content']/text()").extract()))
        post_data.set_info('title',                 re.findall(pattern=re_title, string=response.xpath('//title/text()').extract()[0])[0])
        post_data.set_info('address',               re.findall(re_address, str(response.text))[0].replace("<div class=\"address nowrap\">", "").replace("</div>", "").strip())

        # fill post day and crawl date
        publish_date = response.xpath('//*[@id="prop-info"]/ul[1]/li[4]/text()').extract()[0].strip()[2:]
        post_data.set_info('post_date',             datetime.strptime(publish_date, "%d/%m/%Y").isoformat())
        post_data.set_info('crawled_date',          datetime.now().isoformat())

        # fill basic attributes from page
        post_data.set_info('city',                  self.province_name)
        post_data.set_info('attr_transaction_type', self.transaction_type)
        post_data.set_info('attr_realestate_type',  self.realestate_type)
        post_data.set_info('attr_price',            response.xpath('//*[@id="prop-info"]/ul[1]/li[1]/text()').extract()[0].strip()[2:])

        attr_area = response.xpath('//*[@id="prop-info"]/ul[1]/li[2]/text()').extract()[0].strip()[2:]   # usable area
        tmp = response.xpath('//*[@id="prop-info"]/ul[1]/li[3]/text()').extract()[0].strip()[2:]         # area
        if tmp != "":
            attr_area = tmp
        post_data.set_info('attr_area',             attr_area)

        post_data.set_info('attr_legal',            response.xpath('//*[@id="prop-info"]/ul[2]/li[3]/text()').extract()[0].strip()[2:])
        post_data.set_info('attr_orientation',      response.xpath('//*[@id="prop-info"]/ul[2]/li[4]/text()').extract()[0].strip()[2:])

        # fill bathroom and bedroom
        bedroom  = response.xpath('//*[@id="prop-info"]/ul[2]/li[1]/text()').extract()[0].strip()[2:]
        bathroom = response.xpath('//*[@id="prop-info"]/ul[2]/li[2]/text()').extract()[0].strip()[2:]
        if len(bedroom) != 0:
            post_data.set_info('bedroom',           int(bedroom))
        if len(bathroom) != 0:
            post_data.set_info('bathroom',          int(bathroom))


        # fill lat lon
        try:
            lat_lng = get_latlng(response.css('div[class="map-display"]').css('iframe::attr(src)').getall()[0])
        except IndexError:
            lat_lng = (None, None)

        if lat_lng[0]:
            post_data.set_info('location_lat',      float(lat_lng[0]))
            post_data.set_info('location_lng',      float(lat_lng[1]))
        else:
            post_data.set_info('location_lat',      None)
            post_data.set_info('location_lng',      None)
        


        return {
            'data': post_data
        }

