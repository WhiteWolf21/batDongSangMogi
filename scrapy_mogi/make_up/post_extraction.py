# import pandas as pd
# from openpyxl import load_workbook

from make_up.api.api_NLP_communicate import get_from_api
from make_up.api.api_GGMap_communicate import get_from_ggmap
from make_up.miscellaneous.normalize_price import normalize_price
from make_up.miscellaneous.regex_operation import *
from make_up.miscellaneous.normalize.utils import *

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
    "attr_area",
    "attr_interior_floor",
    "attr_interior_room",
    "attr_orientation",
    "attr_project",
    "attr_legal",
    'location_lng',
    'location_lat',
]


def posts_extract(post_data):
    """
        try to fill in the keys in PostInfo
    :return:
    """

    # get attributes of post from NLP API and Google Geo API
    attributes = get_attributes(post_data)
    lat_lng    = get_lat_lon(post_data, attributes)

    for attribute in filling_attrs:
        if post_data.get_info(attribute) is None:
            if attribute == "location_lat":
                post_data.set_info(attribute, lat_lng[0])
            elif attribute == "location_lng":
                post_data.set_info(attribute, lat_lng[1])
            else:
                post_data.set_info(attribute, attributes[attribute])

    # standardize attributes
    post_data.set_info("attr_addr_number",   normalize_address(post_data.get_info("attr_addr_number")))
    post_data.set_info("attr_addr_district", normalize_district(post_data.get_info("attr_addr_district")))
    post_data.set_info("attr_addr_ward",     normalize_ward(post_data.get_info("attr_addr_ward")))
    post_data.set_info("attr_position",      normalize_position(post_data.get_info("attr_position")))
    post_data.set_info("attr_area",          normalize_area(post_data.get_info("attr_area")))
    post_data.set_info("attr_price_min",     normalize_price(post_data.get_info("attr_price")))
    post_data.set_info("attr_orientation",   normalize_orientation(post_data.get_info("attr_orientation")))
    post_data.set_info("attr_legal",         normalize_legal(post_data.get_info("attr_legal")))



    post_data.set_info("attr_price_m2",      post_data.get_info("attr_price_min") / post_data.get_info("attr_area"))



def get_attributes(post_data):
    tmp = get_from_api(post_data.get_info('message'))

    if post_data.get_info('address'):
        tmp1 = get_from_api(post_data.get_info('address'))
        tmp['attr_addr_number']   = tmp1['attr_addr_number']
        tmp['attr_addr_street']   = tmp1['attr_addr_street']
        tmp['attr_addr_district'] = tmp1['attr_addr_district']
        tmp['attr_addr_ward']     = tmp1['attr_addr_ward']

    if post_data.get_info('city'):
        tmp['attr_addr_city'] = post_data.get_info('city')

    if post_data.get_info('attr_transaction_type'):
        tmp['attr_transaction_type'] = post_data.get_info('attr_transaction_type')

    if post_data.get_info('attr_realestate_type'):
        tmp['attr_realestate_type'] = post_data.get_info('attr_realestate_type')

    if post_data.get_info('attr_area'):
        tmp['attr_area'] = post_data.get_info('attr_area')

    if post_data.get_info('attr_legal'):
        tmp['attr_legal'] = post_data.get_info('attr_legal')

    if post_data.get_info('attr_orientation'):
        tmp['attr_orientation'] = post_data.get_info('attr_orientation')

    if post_data.get_info('bedroom'):
        tmp['attr_interior_room'] = int(post_data.get_info('bedroom'))

    if post_data.get_info('bathroom'):
        tmp['attr_interior_room'] += int(post_data.get_info('bathroom'))

    return tmp


def get_lat_lon(post_data, attributes):
    if post_data.get_info('location_lat') is not None:
        return post_data.get_info('location_lat'), post_data.get_info('location_lng')

    full_addr = ""
    for tag in ['attr_addr_number', 'attr_addr_street', 'attr_addr_ward', 'attr_addr_district',
                'attr_surrounding_name']:
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
