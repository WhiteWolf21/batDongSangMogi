import requests

from make_up.miscellaneous.get_addr import add_street_num_to_addr

url = "http://35.240.240.251/api/v1/real-estate-extraction"

# data = 'Chính chủ 02 lô đất Củ Chi , liền kề nhau.  Dt: 1.000m2 giá 770 triệu/ 1.000m2 , ' \
#        'sổ còn thơm mùi giấy chưa qua kinh doanh , ' \
#        'không dính quy hoạch gi cả . Liên Hệ : 0948881115 để đặt cọc nhanh lẹ.'


def get_from_api(post_content):
    request = requests.Session()
    data_list = [post_content]
    headers = {}

    response = request.post(url=url, headers=headers, json=data_list)

    data_attrs = {
        "attr_addr_number"                  : "",
        "attr_addr_street"                  : "",
        "attr_addr_district"                : "",
        "attr_addr_ward"                    : "",
        "attr_addr_city"                    : "",
        "attr_position"                     : "",
        "attr_surrounding"                  : "",
        "attr_surrounding_name"             : "",
        "attr_surrounding_characteristics"  : "",
        "attr_transaction_type"             : "",
        "attr_realestate_type"              : "",
        "attr_potential"                    : "",
        "attr_area"                         : "",
        "attr_price"                        : "",
        "attr_price_m2"                     : "",
        "attr_interior_floor"               : "",
        "attr_interior_room"                : "",
        "attr_orientation"                  : "",
        "attr_project"                      : "",
        "attr_legal"                        : "",
    }
    json_response = response.json()

    #global normal_tag_flag         # notify that the previous tag is "normal"
    normal_tag_flag = False
    normal_tag_content = None

    for content in json_response[0]["tags"]:
        if content["type"] == "normal":
            normal_tag_content = content['content']
            normal_tag_flag = True

        elif content["type"] == "addr_street":
            if normal_tag_flag is True:
                normal_tag_flag = False
                data_attrs["attr_addr_number"] = add_street_num_to_addr(normal_tag_content)

            data_attrs["attr_addr_street"] = content["content"]

        elif content["type"] == "addr_ward":
            data_attrs["attr_addr_ward"] = content["content"]

        elif content["type"] == "addr_district":
            data_attrs["attr_addr_district"] = content["content"]

        elif content["type"] == "addr_city":
            data_attrs["attr_addr_city"] = content["content"]
        
        elif content["type"] == "position":
            data_attrs["attr_position"] = content["content"]        

        elif content["type"] == "surrounding":
            data_attrs["attr_surrounding"] = content["content"]

        elif content["type"] == "surrounding_name":
            data_attrs["attr_surrounding_name"] = content["content"]

        elif content["type"] == "surrounding_characteristics":
            data_attrs["attr_surrounding_characteristics"] = content["content"]

        elif content["type"] == "transaction_type":
            data_attrs["attr_transaction_type"] = content["content"]

        elif content["type"] == "realestate_type":
            data_attrs["attr_realestate_type"] = content["content"]

        elif content["type"] == "potential":
            data_attrs["attr_potential"] = content["content"]        

        elif content["type"] == "area":
            data_attrs["attr_area"] = content["content"]

        elif content["type"] == "price":
            data_attrs["attr_price"] = content["content"]

        elif content["type"] == "attr_price_m2":
            data_attrs["attr_price_m2"] = content["content"]
        
        elif content["type"] == "interior_floor":
            data_attrs["attr_interior_floor"] = content["content"]

        elif content["type"] == "interior_room":
            data_attrs["attr_interior_room"] = content["content"]

        elif content["type"] == "attr_orientation":
            data_attrs["attr_attr_orientation"] = content["content"]

        elif content["type"] == "project":
            data_attrs["attr_project"] = content["content"]

        elif content["type"] == "legal":
            data_attrs["attr_legal"] = content["content"]

    return data_attrs

    # ------------- FOR DEBUGGING PURPOSE -----------------
    # print("\n\n")
    # print("*********************************")
    # print('RESPONSE_DATA:\n %s' % json.dumps(response.json(), ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))

