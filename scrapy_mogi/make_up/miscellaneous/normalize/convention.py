# **************************************** price *************************************

NUMBER_CARDINALITY = {
    "nghin" : {
        "order" : 3,
        "value" : 1000,
        "aliases" : ["ngan", "nghin", "k"],
    },
    "trieu" : {
        "order" : 2,
        "value" : 1000000,
        "aliases" : ["trieu", "tr"],
    },
    "ty" : {
        "order" : 1,
        "value" : 1000000000,
        "aliases" : ["ti", "ty", "tt", "t", "tyy", "tyr"],
    },
    
}

NUMBER = {
    '1' : 'mot',
    '2' : 'hai',
    '3' : 'ba',
    '4' : 'bon',
    '5' : 'nam',
    '6' : 'sau',
    '7' : 'bay',
    '8' : 'tam',
    '9' : 'chin',
}

FOREIGN_CURRENCY = {
    "usd": ["usd", "dollar", "dola", '\$']
}

MAIN_DIVIDER = '-'
DIVIDERS     = ['toi', 'va', '~', 'hoac', "=>", "->", "-->", "den"]

dollar_vnd_exchange_rate = 23137.75

# if the price if greater than this BOUNDARY, the price is price of real estate, not price per metter square
UP_BOUNDARY = 200000000

LOW_BOUNDARY = 500






# ************************************* transaction type ******************************
TRANSACTION_TYPE = {
    "mua": {
        "aliases"       : [r"mua"],
        "finding_name"  : "bán"
    },
    "thuê": {
        "aliases"       : [r"thue"],
        "finding_name"  : "thuê"
    },
    "nhượng": {
        "aliases"       : [r"nhuong", r'sang'],
        "finding_name"  : "nhượng"
    },
    "bán": {
        "aliases"       : [r"ban"],
        "finding_name"  : "mua"
    },
}

# ************************************* real estate type ******************************
REALESTATE_TYPE = {
    'nhà' : {
        "aliases" : [r'nha(?!\sxuong|\sbo|\shang|\stro|\syen)', r'penthouse', r'biet thu', r'dinh thu', ]
    },
    'mặt bằng' : {
        'aliases' : [r'office', r'mat bang', r'shop', r'xuong', r'quan', r'kiot', r'kiosk', r'cua hang', r'nha hang', r'kho']
    },
    'đất' : {
        "aliases" : [r'dat', r'vuon', r'nen', r'mb', r'kdt']
    }, 
    'phòng' : {
        "aliases" : [r'phong', r'tro', r'nha tro', r'day tro', r'vp', r'nha tro']
    },
    'căn hộ' : {
        "aliases" : [r'can ho', r'can', r'building', r'buillding', r'chung cu', r'ch(?! san)', r'villa', r'vila', r'homestay']
    },
    'khách sạn' : {
        "aliases" : [r'khach san', r'hostel', r'hotel', r'nha nghi']
    }
}


# ****************************************** city ************************************
CITIES = {
    "Hồ Chí Minh" : {
        "alias"         : [r"ho chi minh", r"hcm", r"saigon", r"sai gon"]
    },
    "Đồng Nai" : {
        "alias"         : [r"dong nai", r'\. nai', r'dnai']
    }
}



# //////////////////////////// WARNING /////////////////////////////////////
# THIS SECTION IS AVAILABLE FOR DEMO THE PRODUCT ONLY, AFTER DEMO IS COMPLETED,
# THIS SECTION MUST BE REMOVED AND REPLACED BY MORE STABLE VERSION
# //////////////////////////////////////////////////////////////////////////

PRESENT_GEOLOCATION = {
    "Hồ Chí Minh" : {
        "aliases"         : ["tp . hồ chí minh", "tp . hcm", "hcm", "sài gòn", "tphcm", "tp hồ chí minh"
                           "hồ chí minh", "thành phố hồ chí minh", "tp hcm", "Hồ Chí Minh", "tp . hcmchủ", "sài thành"]
    },
    "Đồng Nai" : {
        "aliases"         : [". nai", "đồng nai", "Đồng Nai"]
    }

}
PRESENT_REALESTATE_TYPE = {
    'nhà' : {
        "aliases" : ['biêt thự', 'biệt thư', 'biệt thự', 'dinh thự', 'nha', 'nhà', 'thự']
    },
    'mặt bằng' : {
        'aliases' : ['căn shop', 'cửa hàng', 'kho','kiot', 'mb', 'mbkd', 'mặt băng', 'mặt bằng', 
                     'mặt sàn', 'nhà hàng', 'nhà phố', 'nhà xưởng', 'nhà yến', 'officetel', 'office', 'quán', 'quán bar', 'quán bar'
                     'shop', 'shophouse', 'toà nhà', 'tòa nhà', 'vp', 'văn phòng', 'xưởng']
    },
    'đất' : {
        "aliases" : ['dât', 'dãy trọ', 'dạy trọ', 'kđt', 'nền', 'nền biệt thự', 'vườn bưởi', 'vườn bằng', 'đát', 'đât', 'đât nền', 'đẤT', 'đất',
                     'đất nông nghiệp', 'đất nền', 'đất nền biệt thự', 'đất thuốc']
    }, 
    'phòng' : {
        "aliases" : ['homestay', 'nhà trọ', 'p . trọ', 'phòng', 'phòng trọ', 'trọ', 'đày trọ']
    },
    'căn hộ' : {
        "aliases" : ['Căn hộ', 'building', 'buillding', 'cao ốc', 'chcc cc', 'chdv', 'chung', 'chung cư', 'căn hộ', 'căn hộ mini'
                     'căn mới', 'penthouse', 'villa']
    },
    'khách sạn' : {
        "aliases" : ['hostel', 'khách sạn']
    }
}

PRESENT_TRANSACTION_TYPE = {
    "bán": {
        "aliases"       : ['mua'],
    },
    "thuê": {
        "aliases"       : ['cho thuê', 'thuê', 'cần thuê', 'chi thuê', 'ho thuê'],
    },
    "nhượng": {
        "aliases"       : ['chuyển nhượng', 'nhượng', 'sang'],
    },
    "mua": {
        "aliases"       : ['bán', 'Bán', 'bấn', 'ban'],
    },
}

PRESENT_DISTRICT = {
    "quận 1"           : r'[q|Q]?[^1]*1\b',
    "quận 2"           : r'[q|Q]?[^1]*2\b',
    "quận 3"           : r'[q|Q]?.*3',
    "quận 4"           : r'[q|Q]?.*4',
    "quận 5"           : r'[q|Q]?.*5',
    "quận 6"           : r'[q|Q]?.*6',
    "quận 7"           : r'[q|Q]?.*7',
    "quận 8"           : r'[q|Q]?.*8',
    "quận 9"           : r'[q|Q]?.*9',
    "quận 10"          : r'[q|Q]?.*10',
    "quận 11"          : r'[q|Q]?.*11',
    "quận 12"          : r'[q|Q]?.*12',
    "quận Bình Tân"    : r'[q|Q]?.*[B|b].nh\s[T|t].n',
    "quận Bình Thạnh"  : r'[q|Q]?.*[B|b].nh\s[T|t]h.nh',
    "quận Gò Vấp"      : r'[q|Q]?gv|[q|Q]?.*[B|b].nh\s[T|t]h.nh',
    "quận Tân Phú"     : r'[q|Q]?tp|[q|Q]?.*[T|t].n\s[P|p]h.',
    "quận Phú Nhuận"   : r'[q|Q]?pn|[q|Q]?.*[P|p]h.\s[N|n]hu.n',
    "quận Tân Bình"    : r'[q|Q]?tb|[q|Q]?.*[T|t].n\s[B|b].nh',
    "quận Thủ Đức"     : r'[q|Q]?.*[T|t]h.\s..c',
    "huyện Bình Chánh" : r'[B|b].nh\s[C|c]h.nh',
    "huyện Củ Chi"     : r'[C|c].\s[C|c]h.',
    "huyện Nhà Bè"     : r'[N|n]h.\s[B|b].',

    "huyện Nhơn Trạch" : r'[N|n]h.n\s[T|t]r.ch',
    "huyện Long Khánh" : r'[L|l]ong\s[K|h]h.nh',
    "huyện Long Thành" : r'[L|l]ong\s[T|t]h.nh',
    "huyện Trảng Bom"  : r'[T|t]r.ng\s[B|b]om',
    "huyện Thống Nhất" : r'[T|t]h.ng\s[N|n]h.t',
    "Biên Hòa"         : r'[B|b]i.n\s[H|h]..',
    "huyện Cẩm Mỹ"     : r'[C|c].m\s[M|m].',
    "huyện Định Quán"  : r'..nh\s[Q|q]u.n',
    "huyện Vĩnh Cửu"   : r'[V|v].nh\s[C|c]..',
    "huyện Tân Phú"    : r'[T|t].n\s[P|p]h.',
    "huyện Xuân Lộc"   : r'[X|x]u.n\s[L|l].c'
}
