import re
from make_up.miscellaneous.normalize.utils import *

s = [
        "Không xác định",
    "Đông",
    "Nam",
    "Tây",
    "Bắc",
    "Tây Nam",
    "Đông Nam",
    "Tây Bắc",
    "Đông Bắc"
]

for i in s:
    print(i, " - ", normalize_orientation(i))
