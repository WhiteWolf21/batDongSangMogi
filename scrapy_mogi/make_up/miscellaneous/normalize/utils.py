import re

import make_up.miscellaneous.normalize.convention as convention
from make_up.miscellaneous.normalize.Price import Price

s1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
s0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"

def remove_accents(input_str):
    s = ""
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s.lower()

re_addr = r"(\d*.*\d*[^\sa-z])"
def normalize_address(str_addr):
    if str_addr is None or str_addr == "":
        return None

    str_addr = remove_accents(str_addr)
    
    return re.findall(re_addr, str_addr)[0]




re_district = r"quận |huyện "
def normalize_district(str_district):
    if str_district is None or str_district == "":
        return None
    if re.search(r'\d+', str_district) is None:
        return re.sub(re_district, "", str_district)
    else:
        return str_district




re_ward = r"phường "
def normalize_ward(str_ward):
    if str_ward is None or str_ward == "":
        return None

    return re.sub(re_ward, "", str_ward)




re_position_mat_tien = "mat|mt|tien"
re_position_hem      = "hem|hxh|ngo"
def normalize_position(str_position):
    if str_position is None or str_position == "":
        return None

    str_position = remove_accents(str_position)
    if re.search(re_position_mat_tien, str_position):
        return "mặt tiền"
    elif re.search(re_position_hem, str_position):
        return "hẻm"
    else:
        return "khác"




re_area = r"\d+[\.]{0,1}\d*"
def normalize_area(str_area):
    if str_area is None or str_area == "":
        return None

    str_area = re.sub(r",", ".", str_area)
    return float(re.findall(re_area, str_area)[0])




def normalize_price(str_price):
    '''Extract price_min, price_max
       May detect that price is of price per meter square or price of the whole real estate
       May detect area 
    
    :Args:
    str_price - string of price extracted by NLP API

    :Returns:
    a 5-element tuple of: (price_min, price_max, price_min_m2, price_min_m2, area), None value may be one of 5 elements in tuple
    '''
    # basic processing

    str_price = re.sub('Mười','10', str_price)
    str_price = re.sub('mười','10', str_price)
    str_price = re.sub('tỏi', 'ty', str_price)

    str_price = remove_accents(str_price)
    
    for number, spelling in convention.NUMBER.items():
        str_price = re.sub(r"\b{}\b".format(spelling), number, str_price)

    # subtitute unconventional spelling name to conventional one
    for conventional, value in convention.NUMBER_CARDINALITY.items():
        for alias in value['aliases']:

            # this command for the case: 33t / m2
            if (alias == 't'or alias == 'tt') and re.search(r"m|m2", str_price):
                str_price = re.sub(r"\b({})\b".format(alias), "trieu", str_price)
            else:
                str_price = re.sub(r"\b({})\b".format(alias), conventional, str_price)

    # remove space
    str_price = re.sub(r'\s','', str_price)
    
   
    # recognize usd
    # we have to check the following condition because in some case the price is "570 tr / 1100 m 2"
    # this price is for the whole 1100-meter-square land, not per meter square
    is_usd = False
    is_price_m2 = False
    for alias in convention.FOREIGN_CURRENCY['usd']:
        if re.search(alias, str_price):
            is_usd = True
            break
    
    
    
    
    
    # split str_price into 2 parts
    for divider in convention.DIVIDERS:
        str_price = re.sub(r"{}".format(divider), convention.MAIN_DIVIDER, str_price)

    str_price_parts = []
    for part in str_price.split(convention.MAIN_DIVIDER):
        if part != '':
            str_price_parts.append(Price(part, is_price_m2, is_usd))

    # each part recognizes itself
    for i in range(len(str_price_parts)):        
        str_price_parts[i].recognize()


    # if one of part are price_m2 or dollar or has biggest cardinality available, set it to the rest
    if len(str_price_parts) > 1:
        # there are 2 parts of price

        # for cardinality, it is a little bit different
        #  if 2 parts have their own biggest cardinality, ignore this case
        #  if part 2 has while part 1 doesn't, 2 parts share the same cardinality
        if str_price_parts[0].get_biggest_cardinality() is None:
            str_price_parts[0].set_biggest_cardinality(str_price_parts[1].get_biggest_cardinality())

    
    # calculate price and print out
    for i in range(len(str_price_parts)):
        str_price_parts[i].calculate_price()
        # str_price_parts[i].debug()
        
        
    
    
    # return results
    if len(str_price_parts) == 0:
        return None, None, None, None, None

    
    price_min    = str_price_parts[0].get_price()

    return price_min



re_orientation = r"([^\s]{3,4})\s?(.{3,4})?"
def normalize_orientation(str_orientation):
    if str_orientation == "Không xác định" or str_orientation is None or str_orientation == "":
        return None

    
    str_orientation = str_orientation.lower()
    tmp = re.search(re_orientation, str_orientation).groups()
    return ' - '.join(tmp) if tmp[1] != None else tmp[0].replace(" ", "")



re_legal_so_hong = "so hong"
re_legal_so_do   = "so do"
def normalize_legal(str_legal):
    if str_legal is None or str_legal == "":
        return None
    
    str_legal = remove_accents(str_legal)
    if re.search(re_legal_so_hong, str_legal):
        return "sổ hồng"
    elif re.search(re_legal_so_do, str_legal):
        return "sổ đỏ"
    return "khác"
