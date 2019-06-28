from re import findall

from modules.make_up.api.api_NLP_communicate import get_from_api
from modules.make_up.api.api_GGMap_communicate import get_from_ggmap
from modules.make_up.miscellaneous.normalize.utils import *
from modules.make_up.miscellaneous.regex_operation import *


filling_attrs = [
    "attr_addr_number",
    "attr_addr_street",
    "attr_addr_district",
    "attr_addr_ward",
    "attr_addr_city",
    "attr_position",
    "attr_surrounding",
    "attr_surrounding_name",
    "attr_surrounding_characteristics",
    "attr_transaction_type",
    "attr_realestate_type",
    "attr_potential",
    "attr_price",
    "attr_price_min",
    "attr_price_max",
    "attr_price_m2",
    "attr_interior_floor",
    "attr_interior_room",
    "attr_orientation",
    "attr_project",
    "attr_legal",
    'location_lng',
    'location_lat',
]


def make_up(post_info):
    """
        try to fill in the keys in PostInfo
    :return:
    """
    print("====================== MAKE UP DATA =========================")

    # get attributes of post from NLP API and Google Geo API
    attributes = get_attributes(post_info)
    lat_lng    = get_lat_lon(post_info, attributes)
    # lat_lng = (None, None)
    price_min, price_max, price_m2, area_tmp, price_str = get_price(post_info, attributes)
    area       = get_area(post_info, attributes)

    # update area or price_m2
    if area == 0 and area_tmp != 0:
        area = float(area_tmp)

    if price_m2 == 0 and price_min != 0 and area != 0:
        price_m2 = price_min / area

    print("price: ", price_str)
    print("price_min: ", price_min)
    print("price_max: ", price_max)
    print("price_m2: ", price_m2)
    print("area: ", area)

    for attribute in filling_attrs:
        if post_info.get_info(attribute) is None:
            if attribute == "attr_price_min":
                post_info.set_info(attribute, price_min)
            elif attribute == "attr_price_max":
                post_info.set_info(attribute, price_max)
            elif attribute == "attr_price_m2":
                post_info.set_info(attribute, price_m2)
            elif attribute == "attr_area":
                post_info.set_info(attribute, area)
            elif attribute == "attr_price":
                post_info.set_info(attribute, price_str)

            elif attribute == "location_lat":
                post_info.set_info(attribute, lat_lng[0])
            elif attribute == "location_lng":
                post_info.set_info(attribute, lat_lng[1])

            else:
                if attributes[attribute] == "":
                    post_info.set_info(attribute, None)
                else:
                    post_info.set_info(attribute, attributes[attribute])

    # standardize attributes
    post_info.set_info("attr_addr_number",      normalize_address(post_info.get_info("attr_addr_number")))
    post_info.set_info("attr_addr_street",      normalize_street(post_info.get_info("attr_addr_street")))
    post_info.set_info("attr_addr_district",    normalize_district(post_info.get_info("attr_addr_district")))
    post_info.set_info("attr_addr_ward",        normalize_ward(post_info.get_info("attr_addr_ward")))
    post_info.set_info("attr_addr_city",        normalize_city(post_info.get_info("attr_addr_city")))
    post_info.set_info("attr_position",         normalize_position(post_info.get_info("attr_position")))
    post_info.set_info("attr_transaction_type", normalize_transaction_type(post_info.get_info("attr_transaction_type")))
    post_info.set_info("attr_realestate_type",  normalize_realestate_type(post_info.get_info("attr_realestate_type")))
    post_info.set_info("attr_legal",            normalize_legal(post_info.get_info("attr_legal")))



def get_attributes(post_info):
    tmp = get_from_api(post_info.get_info('message'))

    if post_info.get_info('address'):
        tmp1 = get_from_api(post_info.get_info('address'))
        tmp['attr_addr_number']   = tmp1['attr_addr_number']
        tmp['attr_addr_street']   = tmp1['attr_addr_street']
        tmp['attr_addr_district'] = tmp1['attr_addr_district']
        tmp['attr_addr_ward']     = tmp1['attr_addr_ward']

    if post_info.get_info('city'):
        tmp['attr_addr_city'] = post_info.get_info('city')

    if post_info.get_info('attr_transaction_type'):
        tmp['attr_transaction_type'] = post_info.get_info('attr_transaction_type')

    if post_info.get_info('attr_realestate_type'):
        tmp['attr_realestate_type'] = post_info.get_info('attr_realestate_type')

    if post_info.get_info('attr_area'):
        tmp['attr_area'] = post_info.get_info('attr_area')

    if post_info.get_info('attr_legal'):
        tmp['attr_legal'] = post_info.get_info('attr_legal')

    if post_info.get_info('attr_orientation'):
        tmp['attr_orientation'] = post_info.get_info('attr_orientation')

    if post_info.get_info('bedroom'):
        tmp['attr_interior_room'] = int(post_info.get_info('bedroom'))

    if post_info.get_info('bathroom'):
        tmp['attr_interior_room'] += int(post_info.get_info('bathroom'))

    return tmp


def get_lat_lon(post_info, attributes):
    print("Link in lat_lon: ", post_info.get_info("link"))
    if post_info.get_info('location_lat') is not None:
        return post_info.get_info('location_lat'), post_info.get_info('location_lng')

    full_addr = ""
    for tag in ['attr_addr_number', 'attr_addr_street', 'attr_addr_ward', 'attr_addr_district'] :                
        clean_tag = attributes[tag].replace("\n", '')
        if len(tag) <= 1:
            continue

        if tag == 'attr_addr_number':
            tmp = clean_addr(clean_tag)
            if len(tmp) != 0:
                full_addr = full_addr + tmp + ' '
        elif tag == 'attr_addr_ward':
            tmp = clean_addr(clean_tag)
            if len(tmp) != 0:
                full_addr = full_addr + tmp + ' '
        elif tag == 'attr_addr_district':
            tmp = clean_district(clean_tag)
            if len(tmp) != 0:
                full_addr = full_addr + tmp + ' '
        else:
            full_addr = full_addr + clean_tag + ' '

    res = clean_full_address(full_addr)
    if len(res) > 1:
        # print('addr: \'', ' '.join(found.groups()), '\'')
        result = get_from_ggmap(' '.join(res))
        if result:
            return result['lat'], result['lng']
    
    return None, None

    


def get_price(post_info, attributes):
    if post_info.get_info('attr_price') is not None:
        return normalize_price(post_info.get_info('attr_price'))
    else:
        price_min = 0
        price_max = 0
        price_m2  = 0
        area_tmp  = 0
        price_str = ""

        for tmp in attributes['attr_price']:
            price = normalize_price(tmp)
            if price_min == 0 and price[0]:
                price_str = tmp
                price_min = price[0]
            if price_max == 0 and price[1]:
                price_max = price[1]
            if price_m2 == 0 and price[2]:
                price_m2 = price[2]
            if area_tmp == 0 and price[4]:
                area_tmp = price[4]

        # if reach here that means not any one extracted by NLP API is valueable
        return price_min, price_max, price_m2, area_tmp, price_str

# regex for area
re_area = r"(\d+\.\d+|\d+)"

def extract_area(str_area):
    str_area = str_area.replace(" ", "").replace(",", ".").replace("m2", "").replace("m", "").replace("ha", "0000")
    #print(str_area)
    if search(pattern=r"(x|\*)", string=str_area) is None:
        return max(findall(re_area, str_area))
    else:
        tmp = 1
        for number in findall(pattern=re_area, string=str_area):
            tmp = tmp * float(number)
        
        return tmp

    
def get_area(post_info, attributes):
    if post_info.get_info('attr_area') is not None:
        return float(extract_area(post_info.get_info('attr_area')))
    else:
        for area in attributes['attr_area']:
            t = extract_area(area)
            if t:
                post_info.set_info("attr_area", t)
                return float(t)

        # if reaches here, no any string of area extracted by NLP API found
        return 0

    
    