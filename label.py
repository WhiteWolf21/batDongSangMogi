import pandas as pd
import xlrd
import xlwt 
from xlutils.copy import copy

# xls = pd.ExcelFile(r'C:\Users\Khang\Desktop\login\nopA.xls')
# wb = xlrd.open_workbook(xls)
# sheet = wb.sheet_by_name('Comment')

#Open file
xls = pd.ExcelFile(r'C:\Users\Khang\Desktop\login\result.xlsx')
wb = xlrd.open_workbook(xls)
sheet = wb.sheet_by_name('Sheet1')

book = xlwt.Workbook(encoding="utf-8")
w_sheet = book.add_sheet('2')
sheet.cell_value(0,0)

#Put all comments to a list
list_1 = []
for i in range(1, sheet.nrows):
    list_1.append(sheet.cell_value(i, 2))

#List of word, if the comment contains one of them, it will be labeled
intent = []
a = ['cho hỏi giá','cho mình hỏi giá' ,'cho giá' ,'giá?' ,'giá bao nhiêu', 'giá bao nhiu', 'giá bn', 'giá bnhiu', 'giá bnhju' ,
'giá b nhiêu', 'giá bnhiu', 'giá b nhiu', 'giá thế nào', 'giá như thế nào' ,'giá tn', 'giá ntn', 'giá tnào', 'giá tnao', 'giá nhiu', 
'giá nhiêu', 'giá sao', 'giá sao', 'giá s', 'xin giá', 'xin gia', 'cho giá', 'cho gia',
'bao nhiêu 1m', 'bao nhiêu 1 m', 'bao nhiêu m2', 'bao nhiêu 1 mét', 'bao nhiu 1m',
'bao nhiu 1 m', 'bao nhiu m2', 'bao nhiu 1 mét', 'bnhiu 1m', 'bnhiu m2'
'bnhiu 1 mét', 'bnhiêu 1m', 'bnhiêu 1 m', 'bnhiêu m2', 'bnhiêu 1 mét', 'bn 1m', 'bn 1 m',
'bn m2', 'bn 1 mét', 'bao tiền 1m', 'bao tiền 1 m', 'bao tiền m2', 'bao tiền 1 mét', 'giá cả', 'giá tiền', 'giá bán', 'gia a oi', 'gia c oi', 'gia ban oi', 'giá a ơi'
,'giá anh ơi', 'giá bạn ơi','giá c ơi', 'giá chị ơi', 'ib giá', 'inbox giá', 'ibox giá', 'ib gia', 'inbox gia', 'ibox gia']

b = []
hoigia = []
i = 0
while i < len(a):
        b.append(a[i].capitalize())
        i += 1

hoigia = a + b

c = ['cho thông tin', 'xin thông tin', 'ib thông tin', 'inbox thông tin', 'ibox thông tin', 'cho thông tin chính xác',
'cho thông tin cụ thể', 'cho thông tin lô đất', 'cho thông tin căn nhà', 'cho thông tin căn hộ', 'ib thêm thông tin', 'inbox thêm thông tin',
'ibox thêm thông tin', 'inb thêm thông tin', 'đất gì vậy', 'hẻm bê tông ko', 'hẻm bê tông không', 'hẻm bê tông k', 'hẻm bê tông kg', 'hẻm bê tông hông',
'cho biết thông tin', 'ib giúp', 'inbox giúp', 'ibox giúp', 'inb giúp', 'ib giup', 'inbox giup', 'ibox giup', 'inb giup',
'có quy hoạch ko', 'có quy hoạch không', 'có quy hoạch k', 'có quy hoạch kg', 'có quy hoạch hông', 'xin thông tin', 'xin thong tin', 'ttin', 'xin ttin', 'inbox ttin', 'ibox ttin', 'ib ttin']

d = []
hoithongtin = []
i = 0
while i < len(c):
        d.append(c[i].capitalize())
        i += 1

hoithongtin = c + d


e = ['sở hữu bao lâu', 'sở hữu mấy năm', 'sở hữu bao nhiêu năm', 'sở hữu bao nhiu năm', 'sở hữu bnhiu', 'sử dụng bao nhiêu lâu', 'sử dụng bao nhiêu năm',
'sử dụng bao nhiu lâu', 'sử dụng bao nhiu năm', 'sử dụng bnhiu lâu', 'sử dụng bnhiu năm', 'sử dụng bnhieu lâu', 'sử dụng bnhieu năm', 'sử dụng bn lâu',
'sử dụng bn năm', 'bán bao nhiêu lâu', 'bán bao nhiêu năm',
'bán bao nhiu lâu', 'bán bao nhiu năm', 'bán bnhiu lâu', 'bán bnhiu năm', 'bán bnhieu lâu', 'bán bnhieu năm', 'bán bn lâu',
'bán bn năm',  'vĩnh viễn hay có thời hạn']

f = []
thoigiansohuu = []
i = 0
while i < len(e):
        f.append(e[i].capitalize())
        i += 1

thoigiansohuu = e + f

#Label comments
for i in range(len(list_1)):
        if any(x in list_1[i] for x in hoigia):
                intent.append('Hỏi giá')
        elif any(x in list_1[i] for x in hoithongtin):
                intent.append('Hỏi thông tin chung chung')
        elif any(x in list_1[i] for x in thoigiansohuu):
                intent.append('Thời gian sở hữu (căn hộ)')
        else:
                intent.append('')

print(intent)

#writing to another excel file
for i in range(len(intent)):
        w_sheet.write(i, 4, intent[i])
book.save(r'C:\Users\Khang\Desktop\login\label2.xls')
