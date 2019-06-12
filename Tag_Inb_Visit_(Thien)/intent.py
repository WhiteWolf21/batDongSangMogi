# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 22:30:37 2019

@author: WhiteWolf21
"""
# Đây là thư viện dùng để đọc giá trị từ file excel theo cột và dòng
import xlrd 

# Đây là thư viện tạo và ghi giá trị cho file excel
from xlwt import Workbook

# Đường dẫn đến các giá trị đã được dán nhãn
path = ("regularExpression.xlsx") 

# Mở file và truy xuất dữ liệu theo sheet cụ thể  
wb = xlrd.open_workbook(path) 
sheet = wb.sheet_by_index(0) # Ở đây 0 là sheet đầu tiên theo thứ tự tăng dần

# Tạo hai mảng rỗng để chứa dữ liệu truy xuất tư bảng dán nhãn
tag = [] # Dán nhãn nhắn tin riêng - inbox
inb = [] # Dán nhãn nhắn tin riêng - inbox
visit = [] # Dán nhãn tham quan, xem mẫu - visit

# Truy xuất dự liệu theo từng dòng 1.
for i in range(sheet.nrows):
    if sheet.cell_value(i, 0) != "":
        tag.append(sheet.cell_value(i, 0))
    if sheet.cell_value(i, 1) != "": # Nếu giá trị các ô trong cột nhắn tin riêng không rỗng thì mới thêm vào mảng. Tương tự ở dưới cho tham quan, xem mẫu
        inb.append(sheet.cell_value(i, 1))
    if sheet.cell_value(i, 2) != "":
        visit.append(sheet.cell_value(i, 2))

# Đường dẫn đến các giá trị cần được dán nhãn
path = ("result.xls") 

wb = xlrd.open_workbook(path) 
sheet = wb.sheet_by_index(1) # Sheet thứ 2 - Comment

# Tạo file excel mới chuẩn bị truy xuất dữ liệu intent của comment
wb = Workbook('test2.xlsx') 
sheet1 = wb.add_sheet('Comment') # Tạo sheet tên comment

# Comment column
com = 1 # File anh Tuan Anh
# com = 2 File của Mai

# Kiểm tra dữ liệu theo từng dòng
# for i in range(69, 70): 
for i in range(sheet.nrows): 
    # Biến lưu điểm của từng intent, intent nào có điểm cao nhất thì comment sẽ được gán cho intent đó.
    tagScore = 0
    inbScore = 0
    visitScore = 0
    
    # Nếu comment chỉ là số điện thoại thì đó ngay lập tức là nhắn tin riêng.
    if sheet.cell_value(i, com).isdigit():
        inbScore = inbScore + 1
        
    # Kiểm tra xem những từ đã được dán dãn có trong comment không. Mỗi từ có sẽ cộng thêm 1 điểm cho điểm cho tag bạn bè.
    for element in tag:        
        if (element + " ") in sheet.cell_value(i, com):
            tagScore = tagScore + 1
        
    # Tương tự ở trên cho nhắn tin riêng
    for element in inb:      
        if (element + " ") in sheet.cell_value(i, com):
            inbScore = inbScore + 1
    
    # Tương tự ở trên cho điểm tham quan, xem mẫu.
    for element in visit:        
        if (element + " ") in sheet.cell_value(i, com):
            visitScore = visitScore + 1
    
    # Viết lại những giá trị không đổi trong bảng cần được dán nhãn như ID comment, STT dòng, ... Phần này tùy theo file result mà tinh chỉnh
    sheet1.write(i, 0, sheet.cell_value(i, 0)) 
    sheet1.write(i, 1, sheet.cell_value(i, 1)) 
    sheet1.write(i, 2, sheet.cell_value(i, 2)) 
    sheet1.write(i, 3, sheet.cell_value(i, 3))
    #sheet1.write(i, 4, sheet.cell_value(i, 4))
    
    # Kiểm tra điểm nào cao nhất để dán nhãn điểm đó, nếu không có điểm nào thì coi như không thuộc 3 thuột tính của tool này.
    # Phần sheet1 trong comment là dành cho file result dạng của Mai
    if tagScore > inbScore:
        if tagScore > visitScore:
            sheet1.write(i, 4, "Tag bạn bè") 
            sheet1.write(i, 5, "Huỳnh Ngọc Thiện")
            #sheet1.write(i, 5, "Tag bạn bè") 
            #sheet1.write(i, 6, "Huỳnh Ngọc Thiện") 
    elif inbScore > visitScore:
        sheet1.write(i, 4, "Nhắn tin riêng") 
        sheet1.write(i, 5, "Huỳnh Ngọc Thiện")
        #sheet1.write(i, 5, "Nhắn tin riêng") 
        #sheet1.write(i, 6, "Huỳnh Ngọc Thiện") 
    elif visitScore != 0:
        sheet1.write(i, 4, "Tham quan, xem mẫu") 
        sheet1.write(i, 5, "Huỳnh Ngọc Thiện")
        #sheet1.write(i, 5, "Tham quan, xem mẫu") 
        #sheet1.write(i, 6, "Huỳnh Ngọc Thiện")
    else:
        sheet1.write(i, 4, sheet.cell_value(i, 4)) 
        sheet1.write(i, 5, sheet.cell_value(i, 5))
        #sheet1.write(i, 5, sheet.cell_value(i, 5)) 
        #sheet1.write(i, 6, sheet.cell_value(i, 6))

# Lưu lại file mới tên là test.
wb.save('test.xls')  
    