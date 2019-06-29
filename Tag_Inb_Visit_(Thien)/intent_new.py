import xlrd
from xlwt import Workbook

path = ("intent.xlsx")

wb = xlrd.open_workbook(path)
sheet = wb.sheet_by_index(0)

posi = []
strc = []
status = []

for i in range (sheet.nrows):
    if sheet.cell_value(i,0) != "":
        posi.append(sheet.cell_value(i,0))
    if sheet.cell_value(i,1) != "":
        strc.append(sheet.cell_value(i,1))
    if sheet.cell_value(i,2) != "":
        status.append(sheet.cell_value(i,2))

path = ("result.xls")

wb = xlrd.open_workbook(path)
sheet = wb.sheet_by_index(1)

wb = Workbook('test_new1.xlsx')
sheet1 = wb.add_sheet('Comment')

com = 1
for i in range (sheet.nrows):
    poScore = 0
    strScore = 0
    staScore = 0

    for element in posi:
        if (element + " ") in sheet.cell_value(i, com):
            poScore = poScore + 1

    # Tương tự ở trên cho nhắn tin riêng
    for element in strc:
        if (element + " ") in sheet.cell_value(i, com):
            strScore = strScore + 1

    # Tương tự ở trên cho điểm tham quan, xem mẫu.
    for element in status:
        if (element + " ") in sheet.cell_value(i, com):
            staScore = staScore + 1

    sheet1.write(i, 0, sheet.cell_value(i, 0))
    sheet1.write(i, 1, sheet.cell_value(i, 1))
    sheet1.write(i, 2, sheet.cell_value(i, 2))
    sheet1.write(i, 3, sheet.cell_value(i, 3))

    if poScore > strScore:
        if poScore > staScore:
            sheet1.write(i, 4, "Vị trí, hướng")
            sheet1.write(i, 5, "Minh Huy")
            #sheet1.write(i, 5, "Tag bạn bè")
            #sheet1.write(i, 6, "Huỳnh Ngọc Thiện")
    elif strScore > staScore:
        sheet1.write(i, 4, "Cơ sở hạ tầng")
        sheet1.write(i, 5, "Minh Huy")
        #sheet1.write(i, 5, "Nhắn tin riêng")
        #sheet1.write(i, 6, "Huỳnh Ngọc Thiện")
    elif staScore != 0:
        sheet1.write(i, 4, "Tiến độ")
        sheet1.write(i, 5, "Minh Huy")
        #sheet1.write(i, 5, "Tham quan, xem mẫu")
        #sheet1.write(i, 6, "Huỳnh Ngọc Thiện")
    else:
        sheet1.write(i, 4, sheet.cell_value(i, 4))
        sheet1.write(i, 5, sheet.cell_value(i, 5))



wb.save('test_final3.xls')
