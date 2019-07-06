# -*- coding: utf-8 -*-
import re
import requests

main_divider = '-'
dividers = ['toi', 'va', '~', 'hoac']
currency_unit = ['ti', 'ty', 'trieu', 'tr', 'nghin', 'ngan', 'k', 't']
maping_num = {'mot':'1', 'hai':'2', 'ba':'3', 'bon':'4', 'nam':'5', 'sau':'6', 'bay':'7', 'tam':'8', 'chin':'9'}


def getExchangeRate():
    response = requests.get(
        'http://www.apilayer.net/api/live?access_key=a993873254303ba0dbc1e07e6a04aede&format=1'
    )
    json = str(response.json())
    reg = '\'USDVND\': ([+-]?([0-9]*[.])?[0-9]+)'
    return re.findall(reg, json)[0][0]


reg_usd = '([+-]?([0-9]*[.])?[0-9]+)(|[ ]+)usd'

def analyzeText(text):
    text = text.lower()
    rate = re.findall(reg_usd, text, re.IGNORECASE)
    txt = ''
    exchangeRate = 23325
    if(len(rate) == 2):
        text = repr(round(float(rate[0][0]) * exchangeRate)) + '-' + repr(round(float(rate[1][0]) * exchangeRate))
    if(len(rate) == 1):
        txt = repr(round(float(rate[0][0]) * exchangeRate))
        text = text.replace(rate[0][0], txt)
        text = text.replace("usd", '')
        text = text.replace("USD", '')
    return text


def normalize_price(text):
    text = compound2unicode(text)
    text = re.sub('Mười','10', text)
    text = re.sub('mười','10', text)
    text = remove_vietnamese_accent(text)
    for key, value in maping_num.items():
        text = re.sub(r"\b{}\b".format(key), "{}".format(value), text)
    text = text.replace('ti', 'ty')
    text = text.replace('tram', '#00')
    text = text.replace('trieu', 'tr')
    text = text.replace('muoi', '#0') #Mươi :)))
    text = text.replace(' #', '')
    text = text.replace('ruoi', '5') # rưỡi
    text = text.replace('mot', '1') #Mốt nhé
    text = text.replace('k', 'kk')
    text = text.replace('nghin', 'kk')
    text = text.replace('ngan', 'kk')
    text = text.replace('dong', 'vnd')
    text = text.replace('t', 'ty')
    text = text.replace('tyy', 'ty')
    text = text.replace('tyr', 'tr')

    position_comma = text.find(',')
    position_point = text.find('.')

    if position_comma != -1 and position_point != -1:
        text = text.replace(',', '')
        text = text.replace('.', '')
    else:
        text = text.replace(',', '.')

    text = text.replace(' ', '')

    text = analyzeText(text)
    for div in dividers:
        text = re.sub(div, main_divider, text)
    price_list = list()
    arr = text.split(main_divider)
    biggest_unit = None
    for element in reversed(arr):
        prices = split_price(element)
        for price in reversed(prices):
            value, unit = normalize_price_unit(price, biggest_unit)
            if value == 0:
                continue
            price_list.append(value)
            biggest_unit = unit

    if len(price_list) == 0:
        low, high = None, None
    elif len(price_list) == 1:
        low, high = price_list[0], None
    else:
        low, high = min(price_list), max(price_list)
    return low, high


re_num = '\d+(\s\.\s\d+)?'
re_vnd = re.compile('(\d+(\s\.\s\d+)?\svnd)')
re_hud = re.compile('(\d+(\s\.\s\d+)?\skk)')
re_mil = re.compile('(\d+(\s\.\s\d+)?\str)')
re_bil = re.compile('(\d+(\s\.\s\d+)?\sty)')


def split_price(text):
    text = text.strip()
    idx_bil = [0] + [i.start() for i in re.finditer(re_bil, text)] + [len(text)]
    idx_mil = [0] + [i.start() for i in re.finditer(re_mil, text)] + [len(text)]
    idx_hud = [0] + [i.start() for i in re.finditer(re_hud, text)] + [len(text)]
    idx_vnd = [0] + [i.start() for i in re.finditer(re_vnd, text)] + [len(text)]
    price_list = list()
    if len(idx_bil) > 2:
        for i in range(0, len(idx_bil) - 1):
            price = text[idx_bil[i]:idx_bil[i+1]]
            if price != '':
                price_list.append(price)
    elif len(idx_mil) > 2:
        for i in range(0, len(idx_mil) - 1):
            price = text[idx_mil[i]:idx_mil[i+1]]
            if price != '':
                price_list.append(price)
    elif len(idx_hud) > 2:
        for i in range(0, len(idx_hud) - 1):
            price = text[idx_hud[i]:idx_hud[i+1]]
            if price != '':
                price_list.append(price)
    elif len(idx_vnd) >2:
        for i in range(0, len(idx_vnd) - 1):
            price = text[idx_vnd[i]:idx_vnd[i+1]]
            if price != '':
                price_list.append(price)
    elif text != '':
        price_list.append(text)
    return price_list

maping_unit = {'ty': 1000000000, 'tr': 1000000, 'kk':1000, 'vnd':1}
def normalize_price_unit(text, pre_unit):
    if text == '':
        return None, None
    final_value = 0
    arr = text.split(' ')
    if pre_unit is None:
        pre_unit = 'vnd'
    current_unit = pre_unit
    num_list = [float(re.sub(' ','', i.group())) for i in re.finditer('\d+(\s.\s\d+)?', text)]
    unit_list = [i.group() for i in re.finditer('[a-z]+', text)]
    if len(unit_list) == 0:

        final_value = num_list[-1] * maping_unit[pre_unit]
        return final_value, pre_unit

    odd_unit = 'vnd'
    for i in range(min(len(num_list), len(unit_list))):
        num = num_list[i]
        unit = unit_list[i]
        if unit in maping_unit.keys():
            final_value += maping_unit[unit]*num
            odd_unit = unit
    if len(num_list) > len(unit_list):
        odd = num_list[len(unit_list)]
        if odd < 10:
            final_value += maping_unit[odd_unit]*odd/10
        else:
            final_value += maping_unit[odd_unit]*odd/1000
    return final_value, odd_unit
def remove_vietnamese_accent(s):
#     s = s.decode('utf-8')
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[ìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u'[Đ]', 'D', s)
    s = re.sub(u'[đ]', 'd', s)
#     return s.encode('utf-8')
    s = s.lower()
    return s

def compound2unicode(text):
    text = text.replace("\u0065\u0309", "\u1EBB")    # ẻ
    text = text.replace("\u0065\u0301", "\u00E9")    # é
    text = text.replace("\u0065\u0300", "\u00E8")    # è
    text = text.replace("\u0065\u0323", "\u1EB9")    # ẹ
    text = text.replace("\u0065\u0303", "\u1EBD")    # ẽ
    text = text.replace("\u00EA\u0309", "\u1EC3")    # ể
    text = text.replace("\u00EA\u0301", "\u1EBF")    # ế
    text = text.replace("\u00EA\u0300", "\u1EC1")    # ề
    text = text.replace("\u00EA\u0323", "\u1EC7")    # ệ
    text = text.replace("\u00EA\u0303", "\u1EC5")    # ễ
    text = text.replace("\u0079\u0309", "\u1EF7")    # ỷ
    text = text.replace("\u0079\u0301", "\u00FD")    # ý
    text = text.replace("\u0079\u0300", "\u1EF3")    # ỳ
    text = text.replace("\u0079\u0323", "\u1EF5")    # ỵ
    text = text.replace("\u0079\u0303", "\u1EF9")    # ỹ
    text = text.replace("\u0075\u0309", "\u1EE7")    # ủ
    text = text.replace("\u0075\u0301", "\u00FA")    # ú
    text = text.replace("\u0075\u0300", "\u00F9")    # ù
    text = text.replace("\u0075\u0323", "\u1EE5")    # ụ
    text = text.replace("\u0075\u0303", "\u0169")    # ũ
    text = text.replace("\u01B0\u0309", "\u1EED")    # ử
    text = text.replace("\u01B0\u0301", "\u1EE9")    # ứ
    text = text.replace("\u01B0\u0300", "\u1EEB")    # ừ
    text = text.replace("\u01B0\u0323", "\u1EF1")    # ự
    text = text.replace("\u01B0\u0303", "\u1EEF")    # ữ
    text = text.replace("\u0069\u0309", "\u1EC9")    # ỉ
    text = text.replace("\u0069\u0301", "\u00ED")    # í
    text = text.replace("\u0069\u0300", "\u00EC")    # ì
    text = text.replace("\u0069\u0323", "\u1ECB")    # ị
    text = text.replace("\u0069\u0303", "\u0129")    # ĩ
    text = text.replace("\u006F\u0309", "\u1ECF")    # ỏ
    text = text.replace("\u006F\u0301", "\u00F3")    # ó
    text = text.replace("\u006F\u0300", "\u00F2")    # ò
    text = text.replace("\u006F\u0323", "\u1ECD")    # ọ
    text = text.replace("\u006F\u0303", "\u00F5")    # õ
    text = text.replace("\u01A1\u0309", "\u1EDF")    # ở
    text = text.replace("\u01A1\u0301", "\u1EDB")    # ớ
    text = text.replace("\u01A1\u0300", "\u1EDD")    # ờ
    text = text.replace("\u01A1\u0323", "\u1EE3")    # ợ
    text = text.replace("\u01A1\u0303", "\u1EE1")    # ỡ
    text = text.replace("\u00F4\u0309", "\u1ED5")    # ổ
    text = text.replace("\u00F4\u0301", "\u1ED1")    # ố
    text = text.replace("\u00F4\u0300", "\u1ED3")    # ồ
    text = text.replace("\u00F4\u0323", "\u1ED9")    # ộ
    text = text.replace("\u00F4\u0303", "\u1ED7")    # ỗ
    text = text.replace("\u0061\u0309", "\u1EA3")    # ả
    text = text.replace("\u0061\u0301", "\u00E1")    # á
    text = text.replace("\u0061\u0300", "\u00E0")    # à
    text = text.replace("\u0061\u0323", "\u1EA1")    # ạ
    text = text.replace("\u0061\u0303", "\u00E3")    # ã
    text = text.replace("\u0103\u0309", "\u1EB3")    # ẳ
    text = text.replace("\u0103\u0301", "\u1EAF")    # ắ
    text = text.replace("\u0103\u0300", "\u1EB1")    # ằ
    text = text.replace("\u0103\u0323", "\u1EB7")    # ặ
    text = text.replace("\u0103\u0303", "\u1EB5")    # ẵ
    text = text.replace("\u00E2\u0309", "\u1EA9")    # ẩ
    text = text.replace("\u00E2\u0301", "\u1EA5")    # ấ
    text = text.replace("\u00E2\u0300", "\u1EA7")    # ầ
    text = text.replace("\u00E2\u0323", "\u1EAD")    # ậ
    text = text.replace("\u00E2\u0303", "\u1EAB")    # ẫ
    text = text.replace("\u0045\u0309", "\u1EBA")    # Ẻ
    text = text.replace("\u0045\u0301", "\u00C9")    # É
    text = text.replace("\u0045\u0300", "\u00C8")    # È
    text = text.replace("\u0045\u0323", "\u1EB8")    # Ẹ
    text = text.replace("\u0045\u0303", "\u1EBC")    # Ẽ
    text = text.replace("\u00CA\u0309", "\u1EC2")    # Ể
    text = text.replace("\u00CA\u0301", "\u1EBE")    # Ế
    text = text.replace("\u00CA\u0300", "\u1EC0")    # Ề
    text = text.replace("\u00CA\u0323", "\u1EC6")    # Ệ
    text = text.replace("\u00CA\u0303", "\u1EC4")    # Ễ
    text = text.replace("\u0059\u0309", "\u1EF6")    # Ỷ
    text = text.replace("\u0059\u0301", "\u00DD")    # Ý
    text = text.replace("\u0059\u0300", "\u1EF2")    # Ỳ
    text = text.replace("\u0059\u0323", "\u1EF4")    # Ỵ
    text = text.replace("\u0059\u0303", "\u1EF8")    # Ỹ
    text = text.replace("\u0055\u0309", "\u1EE6")    # Ủ
    text = text.replace("\u0055\u0301", "\u00DA")    # Ú
    text = text.replace("\u0055\u0300", "\u00D9")    # Ù
    text = text.replace("\u0055\u0323", "\u1EE4")    # Ụ
    text = text.replace("\u0055\u0303", "\u0168")    # Ũ
    text = text.replace("\u01AF\u0309", "\u1EEC")    # Ử
    text = text.replace("\u01AF\u0301", "\u1EE8")    # Ứ
    text = text.replace("\u01AF\u0300", "\u1EEA")    # Ừ
    text = text.replace("\u01AF\u0323", "\u1EF0")    # Ự
    text = text.replace("\u01AF\u0303", "\u1EEE")    # Ữ
    text = text.replace("\u0049\u0309", "\u1EC8")    # Ỉ
    text = text.replace("\u0049\u0301", "\u00CD")    # Í
    text = text.replace("\u0049\u0300", "\u00CC")    # Ì
    text = text.replace("\u0049\u0323", "\u1ECA")    # Ị
    text = text.replace("\u0049\u0303", "\u0128")    # Ĩ
    text = text.replace("\u004F\u0309", "\u1ECE")    # Ỏ
    text = text.replace("\u004F\u0301", "\u00D3")    # Ó
    text = text.replace("\u004F\u0300", "\u00D2")    # Ò
    text = text.replace("\u004F\u0323", "\u1ECC")    # Ọ
    text = text.replace("\u004F\u0303", "\u00D5")    # Õ
    text = text.replace("\u01A0\u0309", "\u1EDE")    # Ở
    text = text.replace("\u01A0\u0301", "\u1EDA")    # Ớ
    text = text.replace("\u01A0\u0300", "\u1EDC")    # Ờ
    text = text.replace("\u01A0\u0323", "\u1EE2")    # Ợ
    text = text.replace("\u01A0\u0303", "\u1EE0")    # Ỡ
    text = text.replace("\u00D4\u0309", "\u1ED4")    # Ổ
    text = text.replace("\u00D4\u0301", "\u1ED0")    # Ố
    text = text.replace("\u00D4\u0300", "\u1ED2")    # Ồ
    text = text.replace("\u00D4\u0323", "\u1ED8")    # Ộ
    text = text.replace("\u00D4\u0303", "\u1ED6")    # Ỗ
    text = text.replace("\u0041\u0309", "\u1EA2")    # Ả
    text = text.replace("\u0041\u0301", "\u00C1")    # Á
    text = text.replace("\u0041\u0300", "\u00C0")    # À
    text = text.replace("\u0041\u0323", "\u1EA0")    # Ạ
    text = text.replace("\u0041\u0303", "\u00C3")    # Ã
    text = text.replace("\u0102\u0309", "\u1EB2")    # Ẳ
    text = text.replace("\u0102\u0301", "\u1EAE")    # Ắ
    text = text.replace("\u0102\u0300", "\u1EB0")    # Ằ
    text = text.replace("\u0102\u0323", "\u1EB6")    # Ặ
    text = text.replace("\u0102\u0303", "\u1EB4")    # Ẵ
    text = text.replace("\u00C2\u0309", "\u1EA8")    # Ẩ
    text = text.replace("\u00C2\u0301", "\u1EA4")    # Ấ
    text = text.replace("\u00C2\u0300", "\u1EA6")    # Ầ
    text = text.replace("\u00C2\u0323", "\u1EAC")    # Ậ
    text = text.replace("\u00C2\u0303", "\u1EAA")    # Ẫ
    return text
